# Test CV in Keysight E4990 instrument

import os.path
import sys
import numpy as np

from config.default.instruments import Keysight_E4990A, Keithley_2470
from config.default.tests.common import save_results_to_file, build_results_folder, get_plot_parameters
from config.functions import *
import toml

global test_status, measurement_status
global dieActual, moduleActual

global CV_parameters
global base_dir, tests_dir, results_dir, username, cartographic_measurement


def load_CV_parameters():
    global CV_parameters

    import json
    # default values
    CV_parameters =  {
        "START_VOLTAGE": 0,
        "STOP_VOLTAGE": 0,
        "NUM_POINTS": 101,
        "FREQ": 1000,
        "OSC": 500,
        "APERTURE": "5",
        "POINT_AVERAGE": False,
        "AVERAGE_POINTS": 8,
        "SWEEP_AVERAGE": False,
        "AVERAGE_SWEEPS": 8,
        "HYSTERESIS": False,
        "HYSTERESIS_TIME": 0,
        "WAIT_TIME": 0.0,
        "LIGHT": False,
        "LIGHT_TIME": 1,
        "GRAPH1": "CP",
        "GRAPH2": "G",
        "PADS_POSITION": "RF_ON",
        "SMU_VOLTAGE": 40,
        "ACTIVE_POINTS": 10,
        "INACTIVE_POINTS": 6,
        "TIME_TOTAL": 20
    }
    # load from external toml file in tests_dir (if exists, if not default values)
    filename_config = os.getcwd() + base_dir + tests_dir + '/Keysight_E4990A/CV_RF_nanusens.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        CV_parameters = toml_info["parameters"]
        if "output" in toml_info:
            CV_parameters["output"] = toml_info["output"]
        if "plot" in toml_info:
            CV_parameters["plot"] = toml_info["plot"]


try:
    # init CV_parameters
    load_CV_parameters()
    print("CV_parameters:", CV_parameters)
    # init variables
    voltage = []
    capacitance = []
    conductance = []

    E4990A = Keysight_E4990A(instruments["Keysight_E4990A"])
    # use K2470 as SMU to apply voltage
    k2470 = Keithley_2470(instruments["Keithley_2470"])

    # -----------------------
    # Construir secuencia ACTIVE/INACTIVE (idéntica lógica MATLAB)
    # -----------------------

    activePoints = 10
    inactivePoints = 6

    time_total = CV_parameters["TIME_TOTAL"]  # total time in seconds (as MATLAB)

    # Duraciones: en MATLAB usan numPoints/20 -> total measurement time 20 s
    # activeDuration = activePoints/(numPoints/20)
    # So timePerPoint scaling will be aplicado después; aquí replicamos la misma lógica
    numPoints = int(CV_parameters["NUM_POINTS"])
    precisionAvg = int(CV_parameters["APERTURE"])
    pointAvg = CV_parameters["POINT_AVERAGE"]
    sweepAverage = CV_parameters["SWEEP_AVERAGE"]
    averageSweeps = CV_parameters["AVERAGE_SWEEPS"]
    activeDuration = activePoints / (numPoints / time_total)
    inactiveDuration = inactivePoints / (numPoints / time_total)

    cyclePoints = inactivePoints + activePoints # +2 lo he quitado y al final de la medida acaba bien a inactive
    numCycles = int(np.floor((numPoints - inactivePoints) / cyclePoints))

    print(f"numCycles: {numCycles}, cyclePoints: {cyclePoints}, numPoints: {numPoints}")

    dur = []
    points = []
    stat = []
    for i in range(numCycles):
        dur.extend([inactiveDuration, activeDuration])
        points.extend([inactivePoints, activePoints])
        stat.extend(['INACTIVE', 'ACTIVE'])

    remainingPoints = numPoints - (numCycles * cyclePoints)
    if remainingPoints > 0:
        extraDuration = remainingPoints / (numPoints / time_total)
        dur.append(extraDuration)
        points.append(remainingPoints)
        stat.append('INACTIVE')

    # Estimación tiempo por punto (tabla como MATLAB)
    apertureTimeTable = [0.002, 0.01, 0.02, 0.1, 0.2]
    # precisionAvg analogous to aperture index 1..5 in MATLAB; clamp
    idx = min(max(int(precisionAvg), 1), 5) - 1
    timePerPoint = apertureTimeTable[idx]

    if pointAvg > 0:
        totalDuration = numPoints * timePerPoint * pointAvg
    elif sweepAverage > 0:
        totalDuration = numPoints * timePerPoint * averageSweeps
    else:
        totalDuration = numPoints * timePerPoint

    print(f"Estimated totalDuration (s): {totalDuration:.2f}")
    # ajust timePerPoint to fit total time. Estimated totalDuration 20.20, real 18.30
    print(f"Initial timePerPoint (s): {timePerPoint:.4f}")

    # single measure
    # Configurar E4990A
    if not E4990A.config_CV_RF(CV_parameters):
        raise RuntimeError("Config failed for E4990A")


    # Configure SMU
    k2470.set_route_term("FRONT")
    k2470.set_voltage(CV_parameters["SMU_VOLTAGE"])
    k2470.output("OFF")  # ensure output is off

    # -----------------------
    # Perform Measurement (Switching)
    # -----------------------
    # create alias
    ia = E4990A.instrument
    smu = k2470.instrument
    # Trigger source BUS, continuous ON (E4990A), then single trigger to start continuous sweeps
    ia.write(':TRIG:SOUR BUS')
    ia.write(':INIT1:CONT ON')
    ia.write(':TRIG:SING')

    start_time = time.time()

    # Build cumulative sum of points to switch segments (como MATLAB: sum(points(1:index)) )
    points_arr = np.array(points, dtype=int) if len(points) > 0 else np.array([], dtype=int)
    cum_points = np.cumsum(points_arr)
    index = 0
    points_done = 0

    # autoscale visual (igual que MATLAB)
    ia.write(':DISP:WIND1:TRAC1:Y:SCAL:AUTO')
    ia.write(':DISP:WIND1:TRAC2:Y:SCAL:AUTO')

    # Repetimos por cada punto medido en el sweep definido (numPoints)
    for value in range(1, numPoints + 1):
        # actualizar estado segun index
        if len(points_arr) > 0 and value > (cum_points[index] if index < len(cum_points) else np.inf):
            index += 1
            if index >= len(stat):
                break

        currentState = stat[index] if index < len(stat) else 'INACTIVE'

        # # autoscale visual (igual que MATLAB)
        # ia.write(':DISP:WIND1:TRAC1:Y:SCAL:AUTO')
        # ia.write(':DISP:WIND1:TRAC2:Y:SCAL:AUTO')

        # switch SMU output ON/OFF según estado
        if currentState == 'ACTIVE':
            smu.write('OUTP ON')  # output on
        else:
            smu.write('OUTP OFF')  # output off

        # Pause aproximada según timePerPoint para que E4990A registre punto
        time.sleep(timePerPoint)

    # Ensure SMU OFF at end
    smu.write('OUTP OFF')
    smu.write(':SOUR:VOLT 0')  # volver a 0V por seguridad

    print(f"Measurement completed in {time.time() - start_time:.2f} seconds.")

    time.sleep(0.5)

    # small autoscale calls
    ia.write(':DISP:WIND1:TRAC1:Y:SCAL:AUTO')
    ia.write(':DISP:WIND1:TRAC2:Y:SCAL:AUTO')

    # -----------------------
    # Read Results (igual que MATLAB)
    # -----------------------

    # Parameter 1 (C)
    ia.write(':CALC1:PAR1:SEL')
    ia.write(':FORM:DATA ASC')
    ia.write(':FORM:REAL:ASC:LENG 12')
    r1 = ia.query(':CALC1:DATA:FDAT?')
    # r1 es string CSV -> convertir a float array
    ra1 = np.fromstring(r1, sep=',')
    # Parameter 2 (G)
    ia.write(':CALC1:PAR2:SEL')
    ia.write(':FORM:DATA ASC')
    ia.write(':FORM:REAL:ASC:LENG 12')
    r2 = ia.query(':CALC1:DATA:FDAT?')
    ra2 = np.fromstring(r2, sep=',')
    # X-axis
    rx = ia.query(':CALC1:DATA:XAX?')
    rax = np.fromstring(rx, sep=',')

    # Construir arrays finales (tomamos solo la parte real de cada par)
    C = ra1[0::2][:numPoints]  # cada 2 valores, empezando en 0
    G = ra2[0::2][:numPoints]
    V = rax[:numPoints]

    # # Construir arrays C, G, V conforme MATLAB: C(u) = ra1(1+2*(u-1))
    # C = np.zeros(numPoints)
    # G = np.zeros(numPoints)
    # V = np.zeros(numPoints)
    # print(f"Constructing C, G, V arrays for {numPoints} points.")
    # for u in range(1, numPoints + 1):
    #     idx1 = 1 + 2 * (u - 1)  # MATLAB 1-based indexing
    #     # en Python: idx1-1
    #     i = idx1 - 1
    #     # validar índices
    #     if i < len(ra1):
    #         C[u - 1] = ra1[i]
    #     else:
    #         C[u - 1] = np.nan
    #     if i < len(ra2):
    #         G[u - 1] = ra2[i]
    #     else:
    #         G[u - 1] = np.nan
    #     if (u - 1) < len(rax):
    #         V[u - 1] = rax[u - 1]
    #     else:
    #         V[u - 1] = np.nan

        # -----------------------
        # Close devices
        # -----------------------
    ia.write(':SOUR1:BIAS:STAT OFF')
    ia.clear()
    smu.write('OUTP OFF')
    # cerrar recursos
    ia.close()
    smu.close()

    voltage = V
    capacitance = C
    conductance = G
    # print(f"Voltage: {voltage}")
    # print(f"Capacitance: {capacitance}")
    # print(f"Conductance: {conductance}")


    # print(f"Voltage points: {voltage}")
    # print(f"Capacitance points: {capacitance}")
    # print(f"Conductance points: {conductance}")
    # Plot parameters
    plot_config = CV_parameters.get("plot", {}).copy()
    plot_config["TITLE"] = f"CV {CV_parameters['PADS_POSITION']} Measurement"

    results_data_dict = {"V": voltage, "C": capacitance * 1e15, "G": conductance * 1e9}
    plot_parameters = get_plot_parameters(results_data_dict, ["V", "C", "G"], plot_config)

    if plot_config.get("SHOW_PLOT", True):
        emit_plot(plot_parameters)
    
    results_data = list(zip(voltage, capacitance, conductance))
    variables_list = ["V", "C", "G"]
    output_params = CV_parameters.get("output", {"separator": "comma", "prefix": "CV_RF", "suffix": ""})
    
    save_results_to_file(
        results_data=results_data,
        variables_list=variables_list,
        test_parameters=output_params,
        die=1,
        module=1,
        folder_func=lambda: build_results_folder(
            username=username,
            process=main.ui.txtProcess.text(),
            lot=main.ui.txtLot.text(),
            wafer=main.ui.txtWafer.text()
        )
    )


except:
    message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<", "").replace(">", "") + " occurred. " + str(
        sys.exc_info()[1])
    main.updateTextDescription(message, "ERROR")
    retval = messageBox(main, "ERROR", message, "critical")

    # print("ERROR: " + "Oops! " + str(sys.exc_info()[0]) + " occurred. " + str(sys.exc_info()[1]))

