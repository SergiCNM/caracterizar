# -------------------------------------------------------
# Test CV_IV_external in Keysight E4990A and Keithley 2470 instruments
# -------------------------------------------------------
# This test is used to measure CV curves using external voltage source
# - Keithley 2470 applies voltage steps
# - Keysight E4990A measures capacitance at each voltage step
# It can be used in cartographic mode or single measurement mode
# In cartographic mode, the test is performed in each die and module of the wafer
# In single measurement mode, the test is performed in a single device
# The test can be configured to:
#   - make OPEN and SHORT compensation before the measurement
#   - make hysteresis measurement
#   - use light during the measurement
#   - use different frequencies for the measurement
# The results are saved in a text file and plotted in the main window
# The results are also saved in the meas_result variable of the waferwindow object
# The configuration is saved in a toml file
# -------------------------------------------------------

import os.path
import numpy as np
import time
from PySide6.QtWidgets import QMessageBox

from config.default.instruments import Keysight_E4990A
from config.default.instruments import Keithley_2470
from config.default.devices import *
from config.functions import *
import toml

global test_status, measurement_status
global dieActual, moduleActual
global CV_IV_external_parameters
global base_dir, tests_dir, cartographic_measurement


def load_CV_IV_external_parameters():
    """
    Load parameters from toml file or default
    :return: None
    """
    global CV_IV_external_parameters

    # default values
    CV_IV_external_parameters = {
        "START": 0.0,
        "STOP": 40.0,
        "STEP": 1.0,
        "FREQ": "100",
        "OSC": 500,
        "APERTURE": "5",
        "POINT_AVERAGE": False,
        "AVERAGE_POINTS": 8,
        "SWEEP_AVERAGE": False,
        "AVERAGE_SWEEPS": 8,
        "HYSTERESIS": False,
        "HYSTERESIS_TIME": 0,
        "WAIT_TIME": 0.5,
        "SETTLE_TIME": 0.1,
        "LIGHT": False,
        "LIGHT_TIME": 1,
        "COMPLIANCE": 0.01,
        "RANGE": "AUTO",
        "ROUTE_TERM": "REAR",
        "COMPENSATION_OPEN": False,
        "COMPENSATION_SHORT": False,
        "COMPENSATION_DONE": False,
        "GRAPH1": "CP",
        "GRAPH2": "G",
    }
    # load from external toml file in tests_dir (if exists, if not default values)
    filename_config = os.getcwd() + base_dir + tests_dir + '/Keysight_E4990A/CV_IV_external.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        CV_IV_external_parameters = toml_info["parameters"]


def config_E4990A_for_spot_measurement(keysightE4990A, CV_IV_external_parameters):
    """
    Configure E4990A for spot capacitance measurement at fixed frequency
    Without applying DC bias (external voltage source will be used)
    Configure in continuous mode to read single points
    :param keysightE4990A: E4990A instrument instance
    :param CV_IV_external_parameters: parameters dictionary
    :return: True if successful
    """
    try:
        # Configure display and parameters
        if CV_IV_external_parameters["GRAPH2"] != "NONE":
            keysightE4990A.instrument.write(':DISP:WIND1:SPL D1_2')
            keysightE4990A.instrument.write(f':CALC1:PAR2:DEF {CV_IV_external_parameters["GRAPH2"]}')
        else:
            keysightE4990A.instrument.write(':DISP:WIND1:SPL D1')
        keysightE4990A.instrument.write(f':CALC1:PAR1:DEF {CV_IV_external_parameters["GRAPH1"]}')

        # Configure AC signal
        keysightE4990A.instrument.write(f':SOUR1:VOLT:LEV {CV_IV_external_parameters["OSC"] * 1e-3}')

        # Set frequency to fixed value (convert kHz to Hz) - CW mode
        freq_hz = float(CV_IV_external_parameters["FREQ"]) * 1e3
        keysightE4990A.instrument.write(f':SENS1:FREQ:CW {freq_hz}')

        # Set sweep type to point (single measurement at fixed frequency)
        # Configure for point measurement at fixed frequency
        keysightE4990A.instrument.write(':SENS1:SWE:POIN 1')  # Single point
        keysightE4990A.instrument.write(':INIT1:CONT OFF')  # Single shot mode

        # Configure measurement settings
        keysightE4990A.instrument.write(f':SENS1:APER {CV_IV_external_parameters["APERTURE"]}')
        keysightE4990A.instrument.write(f':SENS1:AVER:COUN {CV_IV_external_parameters["AVERAGE_POINTS"]}')
        keysightE4990A.instrument.write(f':SENS1:AVER:STAT {1 if CV_IV_external_parameters["POINT_AVERAGE"] else 0}')
        keysightE4990A.instrument.write(f':CALC1:AVER:COUN {CV_IV_external_parameters["AVERAGE_SWEEPS"]}')
        keysightE4990A.instrument.write(f':CALC1:AVER:STAT {1 if CV_IV_external_parameters["SWEEP_AVERAGE"] else 0}')

        # Set bias to 0V and keep it off (external source will control DC voltage)
        keysightE4990A.instrument.write(':SOUR:BIAS:VOLT 0')
        keysightE4990A.instrument.write(':SOUR:BIAS:STAT OFF')

        # Trigger y modo de adquisición
        keysightE4990A.instrument.write(':TRIG:SOUR BUS')
        keysightE4990A.instrument.write(':INIT:CONT ON')

        return True
    except Exception as ex:
        print(f"Error configuring E4990A: {ex}")
        return False


def measure_single_capacitance_old(keysightE4990A, CV_IV_external_parameters):
    """
    Measure single capacitance value at current voltage (set by external source)
    Read the last measured point from continuous measurement
    :param keysightE4990A: E4990A instrument instance
    :param CV_IV_external_parameters: parameters dictionary
    :return: capacitance, conductance
    """
    try:
        start_time = time.time()
        # Trigger single measurement

        keysightE4990A.instrument.write(':TRIG:SING')

        # Wait for measurement to complete
        # opc = keysightE4990A.instrument.query('*OPC?')
        keysightE4990A.instrument.write('*WAI')

        # Check for errors
        error = keysightE4990A.error()
        if error != '+0,"No error"':
            print(f"ERROR: {error}")
            keysightE4990A.clear()
            return None, None

        # Read capacitance (PAR1) - read last point
        keysightE4990A.instrument.write(':CALC1:PAR1:SEL')
        keysightE4990A.instrument.write(':FORM:DATA ASC')
        keysightE4990A.instrument.write(':FORM:REAL:ASC:LENG 12')
        r1 = keysightE4990A.instrument.query(':CALC1:SEL:DATA:FDAT?')
        ra1 = np.fromstring(r1, sep=',')

        # Read conductance (PAR2) - read last point
        if CV_IV_external_parameters["GRAPH2"] != "NONE":
            keysightE4990A.instrument.write(':CALC1:PAR2:SEL')
            keysightE4990A.instrument.write(':FORM:DATA ASC')
            keysightE4990A.instrument.write(':FORM:REAL:ASC:LENG 12')
            r2 = keysightE4990A.instrument.query(':CALC1:SEL:DATA:FDAT?')
            ra2 = np.fromstring(r2, sep=',')
            # Data format: real, imag for each point - get first point real part
            conductance = ra2[0] if len(ra2) > 0 else 0.0
        else:
            conductance = 0.0

        # Data format: real, imag - get real part of capacitance
        capacitance = ra1[0] if len(ra1) > 0 else None

        elapsed = time.time() - start_time

        return capacitance, conductance, elapsed

    except Exception as ex:
        print(f"Error measuring capacitance: {ex}")
        return None, None, None

def measure_single_capacitance(keysightE4990A, CV_IV_external_parameters):
    try:
        t0 = time.time()

        # Disparo de una única medida
        keysightE4990A.instrument.write(':TRIG:SING')
        keysightE4990A.instrument.write('*WAI')

        # Read capacitance (PAR1) - read last point
        keysightE4990A.instrument.write(':CALC1:PAR1:SEL')
        keysightE4990A.instrument.write(':FORM:DATA ASC')
        keysightE4990A.instrument.write(':FORM:REAL:ASC:LENG 12')
        r1 = keysightE4990A.instrument.query(':CALC1:SEL:DATA:FDAT?')
        ra1 = np.fromstring(r1, sep=',')

        # Read conductance (PAR2) - read last point
        if CV_IV_external_parameters["GRAPH2"] != "NONE":
            keysightE4990A.instrument.write(':CALC1:PAR2:SEL')
            keysightE4990A.instrument.write(':FORM:DATA ASC')
            keysightE4990A.instrument.write(':FORM:REAL:ASC:LENG 12')
            r2 = keysightE4990A.instrument.query(':CALC1:SEL:DATA:FDAT?')
            ra2 = np.fromstring(r2, sep=',')
            # Data format: real, imag for each point - get first point real part
            conductance = ra2[0] if len(ra2) > 0 else 0.0
        else:
            conductance = 0.0

        # Data format: real, imag - get real part of capacitance
        capacitance = ra1[0] if len(ra1) > 0 else None


        elapsed = time.time() - t0
        return capacitance, conductance, elapsed


    except Exception as ex:
        print("Error measuring:", ex)
        return None, None, None


def measure_CV_IV_external(main, k2470, keysightE4990A, CV_IV_external_parameters):
    """
    Measure CV curve using external voltage source (Keithley 2470)
    :param main: main program instance
    :param k2470: Keithley 2470 instrument instance
    :param keysightE4990A: Keysight E4990A instrument instance
    :param CV_IV_external_parameters: parameters dictionary
    :return: voltage, capacitance, conductance lists
    """
    voltage_list = []
    capacitance_list = []
    conductance_list = []
    print("measuring CV_IV_external...")
    # Generate voltage steps
    start = CV_IV_external_parameters["START"]
    stop = CV_IV_external_parameters["STOP"]
    step = CV_IV_external_parameters["STEP"]

    if start > stop:
        step = -abs(step)
    else:
        step = abs(step)

    num_points = int(abs((stop - start) / step)) + 1
    voltage_steps = np.linspace(start, stop, num_points)

    # Configure Keithley 2470 for voltage source mode
    compliance = float(CV_IV_external_parameters["COMPLIANCE"] * 1E-3)
    print("set compliance:", str(compliance))
    k2470.instrument.write(f":SENS:CURR:RANGE {str(compliance)}")

    if k2470.config_IV(CV_IV_external_parameters):
        k2470.set_voltage(start)
        k2470.output("ON")
    else:
        print("Error configuring Keithley 2470")
        return [], [], []

    # Light control
    if CV_IV_external_parameters["LIGHT"]:
        main.init_prober()
        if main.prober != "":
            main.prober.light("1")
            time.sleep(CV_IV_external_parameters["LIGHT_TIME"])
            main.prober.light("0")

    # Wait time before starting
    if CV_IV_external_parameters["WAIT_TIME"] > 0:
        time.sleep(CV_IV_external_parameters["WAIT_TIME"])

    # Measure at each voltage step
    for voltage in voltage_steps:
        try:
            # Set voltage on Keithley 2470
            print("Setting voltage to:", voltage)
            k2470.set_voltage(voltage)

            # Wait for voltage to settle
            if CV_IV_external_parameters["SETTLE_TIME"] > 0:
                time.sleep(CV_IV_external_parameters["SETTLE_TIME"])

            print("Measure single capacitance...")
            # Measure capacitance with E4990A
            capacitance, conductance, t_meas = measure_single_capacitance(keysightE4990A, CV_IV_external_parameters)
            print("measured capacitance: ", capacitance)
            print(f"tmeas: {t_meas * 1000:.1f} ms")
            if capacitance is not None:
                voltage_list.append(voltage)
                capacitance_list.append(capacitance)
                conductance_list.append(conductance)
            else:
                print(f"Error measuring at voltage {voltage}V")

        except Exception as ex:
            print(f"Error at voltage {voltage}V: {ex}")

    # Turn off Keithley output
    k2470.output("OFF")

    # Hysteresis measurement (reverse direction)
    if CV_IV_external_parameters["HYSTERESIS"]:
        if CV_IV_external_parameters["HYSTERESIS_TIME"] > 0:
            time.sleep(CV_IV_external_parameters["HYSTERESIS_TIME"])

        # Reverse voltage steps
        voltage_steps_reverse = voltage_steps[::-1]

        k2470.output("ON")
        for voltage in voltage_steps_reverse:
            try:
                k2470.set_voltage(voltage)
                if CV_IV_external_parameters["SETTLE_TIME"] > 0:
                    time.sleep(CV_IV_external_parameters["SETTLE_TIME"])

                capacitance, conductance = measure_single_capacitance(keysightE4990A, CV_IV_external_parameters)

                if capacitance is not None:
                    voltage_list.append(voltage)
                    capacitance_list.append(capacitance)
                    conductance_list.append(conductance)

            except Exception as ex:
                print(f"Error at voltage {voltage}V (hysteresis): {ex}")

        k2470.output("OFF")

    return voltage_list, capacitance_list, conductance_list


def make_compensation(main, keysightE4990A, CV_IV_external_parameters):
    """
    Make OPEN and SHORT compensation
    :param main: main program instance
    :param keysightE4990A: E4990A instrument instance
    :param CV_IV_external_parameters: parameters dictionary
    :return: True if successful
    """
    retval = message_user(main, "Compensation",
                          "Please, make OPEN compensation: remove the device from the fixture and press OK",
                          "ok_cancel")
    if retval != QMessageBox.Ok:
        return False
    main.updateTextDescription("Making OPEN compensation...<br />")
    if CV_IV_external_parameters["COMPENSATION_OPEN"]:
        keysightE4990A.zero_open("ON")
    else:
        keysightE4990A.zero_open("OFF")
    time.sleep(1)
    retval = message_user(main, "Compensation", "Please, make SHORT compensation: short the fixture and press OK",
                          "ok_cancel")
    if retval != QMessageBox.Ok:
        return False
    main.updateTextDescription("Making SHORT compensation...<br />")
    if CV_IV_external_parameters["COMPENSATION_SHORT"]:
        keysightE4990A.zero_short("ON")
    else:
        keysightE4990A.zero_short("OFF")
    time.sleep(1)
    return True


def make_full_compensation(main, keysightE4990A, CV_IV_external_parameters):
    """
    Make full compensation if not already done
    :param main: main program instance
    :param keysightE4990A: E4990A instrument instance
    :param CV_IV_external_parameters: parameters dictionary
    :return: None
    """
    if not CV_IV_external_parameters["COMPENSATION_DONE"]:
        main.updateTextDescription("<br />Making compensation...<br />")
        if not make_compensation(main, keysightE4990A, CV_IV_external_parameters):
            main.updateTextDescription("Compensation failed! Aborting test...<br />", "ERROR")
            test_status.status = "ABORTED"
        else:
            # Modify toml file to indicate that compensation is done
            CV_IV_external_parameters["COMPENSATION_DONE"] = True
            filename_config = os.getcwd() + base_dir + tests_dir + '/Keysight_E4990A/CV_IV_external.toml'
            file_exists = os.path.exists(filename_config)
            if file_exists:
                toml_info = toml.load(filename_config)
                toml_info["parameters"] = CV_IV_external_parameters
                with open(filename_config, 'w', encoding='utf-8') as tomlfile:
                    toml.dump(toml_info, tomlfile)
            main.updateTextDescription("Compensation done!<br />")
            retval = message_user(main, "Compensation done!",
                                  "Please, configure instruments for measurement, make CONTACT and press YES to continue",
                                  "yes_cancel")


try:
    # Initialize instruments
    k2470 = Keithley_2470(instruments["Keithley_2470"])
    keysightE4990A = Keysight_E4990A(instruments["Keysight_E4990A"])

    # Load parameters
    load_CV_IV_external_parameters()

    # Extract frequencies (comma-separated list)
    freqs = CV_IV_external_parameters["FREQ"].replace(" ", "").split(",")
    freqs = [float(f) for f in freqs if f]

    if cartographic_measurement:
        if str(dieActual) == "1" and str(moduleActual) == "1":
            retval = message_user(main, "Init instruments for CV_IV_external!",
                                  "Please, configure instruments for initialization", "yes_cancel")
            if retval == QMessageBox.Yes:
                test_status.status = "STARTED"
                # Make compensation
                make_full_compensation(main, keysightE4990A, CV_IV_external_parameters)
            else:
                test_status.status = "ABORTED"

        if test_status.status == "STARTED":
            # Measure for each frequency
            for freq in freqs:
                load_CV_IV_external_parameters()  # Reload parameters
                CV_IV_external_parameters["FREQ"] = str(freq)

                # Configure E4990A for spot measurement
                if config_E4990A_for_spot_measurement(keysightE4990A, CV_IV_external_parameters):
                    # Measure CV curve
                    voltage, capacitance, conductance = measure_CV_IV_external(
                        main, k2470, keysightE4990A, CV_IV_external_parameters)

                    if len(voltage) > 0:
                        meas_status = "meas_success"
                        meas_message = f"Measured {len(voltage)} points"
                    else:
                        meas_status = "meas_error"
                        meas_message = "No measurements obtained"

                    # Convert to numpy arrays for easier manipulation
                    voltage = np.array(voltage)
                    capacitance = np.array(capacitance)
                    conductance = np.array(conductance)

                    # Save results
                    main.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1] = {
                        "status": meas_status,
                        "message": meas_message,
                        "contact_height": "",
                        "variables": {
                            "params": [],
                            "data": [
                                {"name": "V", "values": voltage.tolist(), "units": "V"},
                                {"name": "C", "values": (capacitance * 1e12).tolist(), "units": "pF"},
                                {"name": "G", "values": (conductance * 1e9).tolist(), "units": "nS"}
                            ]
                        },
                        "plot_parameters": {
                            "name": f"Plot CV_IV_external {freq}kHz (Die {dieActual} Module {moduleActual})",
                            "x": voltage.tolist(),
                            "y1": (capacitance * 1e12).tolist(),
                            "y2": (conductance * 1e9).tolist(),
                            "titles": {
                                "title": f"CV_IV_external {freq}kHz (Die {dieActual} Module {moduleActual})",
                                "left": "Capacitance",
                                "bottom": "Voltage",
                                "right": "Conductance"
                            },
                            "units": {
                                "left": "pF",
                                "bottom": "V",
                                "right": "nS"
                            },
                            "showgrid": {"x": True, "y": True},
                            "legend": False
                        }
                    }

                    plot_parameters = main.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1][
                        "plot_parameters"]
                    emit_plot(plot_parameters)

                    # Save to file
                    namefile = main.getDirs(
                        "results") + f"/CV_IV_external{freq}kHz_{main.ui.txtProcess.text()}_{dieActual}_{moduleActual}.txt"
                    main.save_lists_to_txt(namefile=namefile, var_list=[voltage, capacitance, conductance],
                                           headers=["V", "C", "G"], separation=",")
                else:
                    meas_status = "meas_error"
                    meas_message = "Error configuring E4990A"

    else:
        # Single measurement mode
        # Make compensation
        make_full_compensation(main, keysightE4990A, CV_IV_external_parameters)

        # Measure for each frequency
        for freq in freqs:
            load_CV_IV_external_parameters()
            CV_IV_external_parameters["FREQ"] = str(freq)

            if config_E4990A_for_spot_measurement(keysightE4990A, CV_IV_external_parameters):
                voltage, capacitance, conductance = measure_CV_IV_external(
                    main, k2470, keysightE4990A, CV_IV_external_parameters)

                if len(voltage) > 0:
                    voltage = np.array(voltage)
                    capacitance = np.array(capacitance)
                    conductance = np.array(conductance)

                    plot_parameters = {
                        "name": f"Plot CV_IV_external {freq}kHz",
                        "x": voltage.tolist(),
                        "y1": (capacitance * 1e12).tolist(),
                        "y2": (conductance * 1e9).tolist(),
                        "titles": {
                            "title": f"CV_IV_external Measurement at {freq}kHz",
                            "left": "Capacitance",
                            "bottom": "Voltage",
                            "right": "Conductance"
                        },
                        "units": {
                            "left": "pF",
                            "bottom": "V",
                            "right": "nS"
                        },
                        "showgrid": {"x": True, "y": True},
                        "legend": True
                    }

                    emit_plot(plot_parameters)

                    # Save to file
                    dieActual = 1
                    moduleActual = 1
                    namefile = main.getDirs(
                        "results") + f"/CV_IV_external{freq}kHz_{main.ui.txtProcess.text()}_single.txt"
                    main.save_lists_to_txt(namefile=namefile, var_list=[voltage, capacitance, conductance],
                                           headers=["V", "C", "G"], separation=",")

    # Stop and close instruments
    k2470.stop()
    k2470.close()
    keysightE4990A.stop()

except:
    import sys

    message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<", "").replace(">", "") + " occurred. " + str(
        sys.exc_info()[1])
    main.updateTextDescription(message, "ERROR")
    message_user(main, "ERROR", message, "ok_error")

