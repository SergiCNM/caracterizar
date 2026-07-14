# -------------------------------------------------------
# Test CV in Keysight E4990A instrument
# -------------------------------------------------------
# This test is used to measure CV curves in a semiconductor device
# It can be used in cartographic mode or single measurement mode
# In cartographic mode, the test is performed in each die and module of the wafer
# In single measurement mode, the test is performed in a single device
# The test can be configured to:
#   - make OPEN and SHORT compensation before the measurement
#   - make hysteresis measurement
#   - calculate parameters from the CV curve
#   - use light during the measurement
#   - use different frequencies for the measurement
# The results are saved in a text file and plotted in the main window
# The results are also saved in the meas_result variable of the waferwindow object
# The configuration is saved in a toml file
# -------------------------------------------------------

import os.path
import numpy as np
from PySide6.QtWidgets import QMessageBox

from config.default.instruments import Keysight_E4990A
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
    CV_parameters = {
        "START": 0,
        "STOP": 40,
        "NUM_POINTS": 101,
        "FREQ": "1000",
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
        "SERIAL_RES": False,
        "CALCULATE_PARAMS": False,
        "COMPENSATION_OPEN": False,
        "COMPENSATION_SHORT": False,
        "COMPENSATION_DONE": False,
        "GRAPH1": "CP",
        "GRAPH2": "G",
    }
    # load from external toml file in tests_dir (if exists, if not default values)
    filename_config = os.getcwd() + base_dir + tests_dir + '/Keysight_E4990A/CV.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        CV_parameters = toml_info["parameters"]
        if "output" in toml_info:
            CV_parameters["output"] = toml_info["output"]
        if "plot" in toml_info:
            CV_parameters["plot"] = toml_info["plot"]


def measure_CV(keysightE4990A, CV_parameters):
    try:
        #self.instrument.write(':SENS1:DC:MEAS:CLE')
        # self.instrument.write(':CALC1:AVER:CLE')
        keysightE4990A.instrument.write(':SOUR:BIAS:STAT ON')  # Turn on Bias
        keysightE4990A.instrument.write(':TRIG:SOUR BUS')
        keysightE4990A.instrument.write(':INIT1:CONT OFF')
        keysightE4990A.instrument.write(':INIT:IMM')
        keysightE4990A.instrument.write(':TRIG:SING')

        opc = keysightE4990A.instrument.query('*OPC?') # increase timeout to wait measure finish
        keysightE4990A.autoscale()
        error = keysightE4990A.error()
        if error != '+0,"No error"':
            print(f"ERROR: {error}")
            keysightE4990A.clear()

        # Read Results
        keysightE4990A.instrument.write(':CALC1:PAR1:SEL')
        keysightE4990A.instrument.write(':FORM:DATA ASC')
        keysightE4990A.instrument.write(':FORM:REAL:ASC:LENG 12')
        r1 = keysightE4990A.instrument.query(':CALC1:SEL:DATA:FDAT?')
        # print(f'r1 = {r1}')
        ra1 = np.fromstring(r1, sep=',')
        keysightE4990A.instrument.write(':CALC1:PAR2:SEL')
        keysightE4990A.instrument.write(':FORM:DATA ASC')
        keysightE4990A.instrument.write(':FORM:REAL:ASC:LENG 12')
        r2 = keysightE4990A.instrument.query(':CALC1:SEL:DATA:FDAT?')
        ra2 = np.fromstring(r2, sep=',')
        rx = keysightE4990A.instrument.query(':CALC1:SEL:DATA:XAX?')
        rax = np.fromstring(rx, sep=',')
        if not CV_parameters["HYSTERESIS"]:
            keysightE4990A.turn_off_bias()

        data = np.zeros((CV_parameters["NUM_POINTS"], 3))
        for u in range(CV_parameters["NUM_POINTS"]):
            data[u, 0] = rax[u]
            data[u, 1] = ra1[2 * u]
            data[u, 2] = ra2[2 * u]

        X = data[:, 0]
        Y1 = data[:, 1]
        Y2 = data[:, 2]

        if CV_parameters["START"] > CV_parameters["STOP"]:
            # invert X, Y1 and Y2
            X = np.flip(X)
            Y1 = np.flip(Y1)
            Y2 = np.flip(Y2)


    except Exception as ex:
        print(f"error ocurred: {ex} ")
        keysightE4990A.stop()

        return [], [], []

    return X, Y1, Y2

def measure_CV_full(main, keysightE4990A, CV_parameters):
    results = {}
    if CV_parameters["WAIT_TIME"] > 0:
        time.sleep(CV_parameters["WAIT_TIME"])
    if CV_parameters["LIGHT"]:
        # prober is not initialized when you select single measurement
        main.init_prober()
        if main.prober != "":
            main.prober.light("1")
            time.sleep(CV_parameters["LIGHT_TIME"])
            main.prober.light("0")

    # measure
    voltage, capacitance, conductance = measure_CV(keysightE4990A, CV_parameters)
    CV_parameters["voltage"] = voltage
    CV_parameters["capacitance"] = capacitance
    CV_parameters["conductance"] = conductance
    CV_parameters["hysteresis_marker"] = False
    if CV_parameters["CALCULATE_PARAMS"]:
        voltage, capacitance, conductance, results = calcular_cv(CV_parameters)
    # hysteresis?
    if CV_parameters["HYSTERESIS"]:
        # wait time between hysteresis
        if CV_parameters["HYSTERESIS_TIME"] > 0:
            time.sleep(CV_parameters["HYSTERESIS_TIME"])
        # swap variables
        CV_parameters["START"], CV_parameters["STOP"] = CV_parameters["STOP"], CV_parameters["START"]
        if keysightE4990A.config_CV(CV_parameters):
            voltage_h, capacitance_h, conductance_h = measure_CV(keysightE4990A, CV_parameters)
            CV_parameters["voltage"] = voltage_h
            CV_parameters["capacitance"] = capacitance_h
            CV_parameters["conductance"] = conductance_h
            CV_parameters["hysteresis_marker"] = True
            if CV_parameters["CALCULATE_PARAMS"]:
                # calculate parameters
                voltage_h, capacitance_h, conductance_h, results_h = calcular_cv(CV_parameters)
                # add to results
                for clave in results_h:
                    results[clave] = results_h[clave]
        # union lists
        voltage = np.concatenate((voltage, voltage_h))
        capacitance = np.concatenate((capacitance, capacitance_h))
        conductance = np.concatenate((conductance, conductance_h))

    return voltage, capacitance, conductance, results


def make_compensation(main, keysightE4990A, CV_parameters):
    # make OPEN and SHORT compensation
    retval = message_user(main, "Compensation", "Please, make OPEN compensation: remove the device from the fixture and press OK", "ok_cancel")
    if retval != QMessageBox.Ok:
        return False
    main.updateTextDescription("Making OPEN compensation...<br />")
    if CV_parameters["COMPENSATION_OPEN"]:
        keysightE4990A.zero_open("ON")
    else:
        keysightE4990A.zero_open("OFF")
    time.sleep(1)
    retval = message_user(main, "Compensation", "Please, make SHORT compensation: short the fixture and press OK", "ok_cancel")
    if retval != QMessageBox.Ok:
        return False
    main.updateTextDescription("Making SHORT compensation...<br />")
    if CV_parameters["COMPENSATION_SHORT"]:
        keysightE4990A.zero_short("ON")
    else:
        keysightE4990A.zero_short("OFF")
    time.sleep(1)

    return True

# Make compensation
def make_full_compensation(main, keysightE4990A, CV_parameters):
    if not CV_parameters["COMPENSATION_DONE"]:
        main.updateTextDescription("<br />Making compensation...<br />")
        if not make_compensation(main, keysightE4990A, CV_parameters):
            main.updateTextDescription("Compensation failed! Aborting test...<br />", "ERROR")
            test_status.status = "ABORTED"
        else:
            # modify toml file to indicate that compensation is done
            CV_parameters["COMPENSATION_DONE"] = True
            filename_config = os.getcwd() + base_dir + tests_dir + '/Keysight_E4990A/CV.toml'
            file_exists = os.path.exists(filename_config)
            if file_exists:
                toml_info = toml.load(filename_config)
                toml_info["parameters"] = CV_parameters
                # save file in UTF-8
                with open(filename_config, 'w', encoding='utf-8') as tomlfile:
                    toml.dump(toml_info, tomlfile)
            main.updateTextDescription("Compensation done!<br />")
            retval = message_user(main, "Compensation done!", "Please, configure instrument for measurement, make CONTACT and press YES to continue", "yes_cancel")



try:

    keysightE4990A = Keysight_E4990A(instruments["Keysight_E4990A"])
    # init CV_parameters
    load_CV_parameters()
    # extract frequencies
    freqs = CV_parameters["FREQ"].replace(" ", "").split(",")
    # convert to float
    freqs = [float(frequency) for frequency in freqs if frequency.isnumeric()]

    if cartographic_measurement:
        if str(dieActual) == "1" and str(moduleActual) == "1":
            retval = message_user(main, "Init instrument for CV!", "Please, configure instrument for initialization",
                                  "yes_cancel")
            if retval == QMessageBox.Yes:
                test_status.status = "STARTED"
                # make compensation
                make_full_compensation(main, keysightE4990A, CV_parameters)
            else:
                test_status.status = "ABORTED"

        if test_status.status == "STARTED":
            # single measure
            for freq in freqs:
                CV_parameters["FREQ"] = freq
                if keysightE4990A.config_CV(CV_parameters):
                    voltage, capacitance, conductance, results = measure_CV_full(main, keysightE4990A, CV_parameters)
                    params = []
                    data = []
                    if CV_parameters["CALCULATE_PARAMS"]:
                        txt_result = "<br /><strong>Results: </strong><br />"
                        for clave in results:
                            txt_result = txt_result + " <strong>- " + clave + "</strong> = " + str(
                                results[clave]) + "<br />"
                            params.append({"name": clave, "value": str(results[clave])})
                        main.updateTextDescription(txt_result)


                    meas_status = "meas_success"
                    meas_message = ""
                else:
                    meas_status = "meas_error"
                    meas_message = "Error configuring instrument"
                # save results
                    plot_config = CV_parameters.get("plot", {}).copy()
                    plot_config["NAME"] = f"Plot CV Die {dieActual} Module {moduleActual}"
                    plot_config["TITLE"] = f"Plot CV {CV_parameters['FREQ']}kHz (Die {dieActual} Module {moduleActual})"
                    
                    results_data_dict = {"V": voltage, "C": capacitance * 1e12, "G": conductance * 1e9}
                    plot_parameters = get_plot_parameters(results_data_dict, ["V", "C", "G"], plot_config)
                    
                    main.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1] = {
                        "status": meas_status,
                        "message": meas_message,
                        "contact_height": "",
                        "variables": {
                            "params": [],
                            "data": [{"name": "V", "values": voltage, "units": "V"},
                                     {"name": "C", "values": capacitance * 1e12, "units": "pF"},
                                     {"name": "G", "values": conductance * 1E9, "units": "nS"}]
                        },
                        "plot_parameters": plot_parameters
                    }

                    if plot_config.get("SHOW_PLOT", True):
                        emit_plot(plot_parameters)
                
                results_data = list(zip(voltage, capacitance, conductance))
                variables_list = ["V", "C", "G"]
                output_params = CV_parameters.get("output", {"separator": "comma", "prefix": f"CV{CV_parameters['FREQ']}kHz", "suffix": ""})
                
                save_results_to_file(
                    results_data=results_data,
                    variables_list=variables_list,
                    test_parameters=output_params,
                    die=dieActual,
                    module=moduleActual,
                    folder_func=lambda: build_results_folder(
                        username=username,
                        process=main.ui.txtProcess.text(),
                        lot=main.ui.txtLot.text(),
                        wafer=main.ui.txtWafer.text()
                    )
                )
    else:

        # make compensation
        make_full_compensation(main, keysightE4990A, CV_parameters)
        # single measure
        for freq in freqs:
            CV_parameters["FREQ"] = freq
            if keysightE4990A.config_CV(CV_parameters):
                voltage, capacitance, conductance, results = measure_CV_full(main, keysightE4990A, CV_parameters)
                params = []
                data = []
                if CV_parameters["CALCULATE_PARAMS"]:
                    txt_result = "<br /><strong>Results: </strong><br />"
                    for clave in results:
                        txt_result = txt_result + " <strong>- " + clave + "</strong> = " + str(
                            results[clave]) + "<br />"
                        params.append({"name": clave, "value": str(results[clave])})
                    main.updateTextDescription(txt_result)
                plot_config = CV_parameters.get("plot", {}).copy()
                plot_config["TITLE"] = f"CV Measurement at {CV_parameters['FREQ']}kHz"
                
                results_data_dict = {"V": voltage, "C": capacitance * 1e12, "G": conductance * 1e9}
                plot_parameters = get_plot_parameters(results_data_dict, ["V", "C", "G"], plot_config)

                dieActual = 1
                moduleActual = 1
                # stop process
                keysightE4990A.stop()

                if plot_config.get("SHOW_PLOT", True):
                    emit_plot(plot_parameters)
                
                results_data = list(zip(voltage, capacitance, conductance))
                variables_list = ["V", "C", "G"]
                output_params = CV_parameters.get("output", {"separator": "comma", "prefix": f"CV{CV_parameters['FREQ']}kHz", "suffix": "single"})
                
                save_results_to_file(
                    results_data=results_data,
                    variables_list=variables_list,
                    test_parameters=output_params,
                    die=dieActual,
                    module=moduleActual,
                    folder_func=lambda: build_results_folder(
                        username=username,
                        process=main.ui.txtProcess.text(),
                        lot=main.ui.txtLot.text(),
                        wafer=main.ui.txtWafer.text()
                    )
                )

    # Close instrument
    # keysightE4990A.close()


except:
    message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<", "").replace(">", "") + " occurred. " + str(
        sys.exc_info()[1])
    main.updateTextDescription(message, "ERROR")
    message_user(main, "ERROR",message,"ok_error")

    # print("ERROR: " + "Oops! " + str(sys.exc_info()[0]) + " occurred. " + str(sys.exc_info()[1]))




