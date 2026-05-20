# -------------------------------------------------------
# Test CW in Keysight E4990A instrument
# -------------------------------------------------------
# This test is used to measure CW curves in a semiconductor device
# It can be used in cartographic mode or single measurement mode
# In cartographic mode, the test is performed in each die and module of the wafer
# In single measurement mode, the test is performed in a single device
# The test can be configured to:
#   - perform OPEN and SHORT compensation
#   - set START, STOP and STEP frequencies
#   - set SPOT voltages (can be multiple, separated by commas)
#   - set OSC level
#   - set CIRCUIT_MODE (Parallel or Series)
#   - set AVERAGE (True or False)
# The results are saved in a text file and plotted in the main window
# The results are also saved in the meas_result variable of the waferwindow object
# The configuration is saved in a toml file
# -------------------------------------------------------

import os.path
from PySide6.QtWidgets import QMessageBox

import numpy as np

from config.default.instruments import Keysight_E4990A
from config.default.tests.common import save_results_to_file, build_results_folder
from config.functions import *
import toml

global test_status, measurement_status
global dieActual, moduleActual
global CW_parameters
global base_dir, tests_dir, results_dir, username, cartographic_measurement

def load_CW_parameters():
    global CW_parameters

    import json
    # default values
    CW_parameters = {
        "START": 1.0,
        "STOP": 1000,
        "NUM_POINTS": 101,
        "LOGSTEP": True,
        "SPOT": -5,
        "OSC": 30,
        "APERTURE": "5",
        "POINT_AVERAGE": False,
        "AVERAGE_POINTS": 8,
        "SWEEP_AVERAGE": False,
        "AVERAGE_SWEEPS": 8,
        "GRAPH1": "CP",
        "GRAPH2": "G",
        "COMPENSATION_OPEN": True,
        "COMPENSATION_SHORT": True,
        "COMPENSATION_DONE": False
    }
    # load from external toml file in tests_dir (if exists, if not default values)
    filename_config = os.getcwd() + base_dir + tests_dir + '/Keysight_E4990A/CW.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        CW_parameters = toml_info["parameters"]
        if "output" in toml_info:
            CW_parameters["output"] = toml_info["output"]
    else:
        print(f"File toml {filename_config} doesn't exists!")


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


def measure_CW(keysightE4990A, CW_parameters):
    try:
        #self.instrument.write(':SENS1:DC:MEAS:CLE')
        # self.instrument.write(':CALC1:AVER:CLE')
        opc = keysightE4990A.instrument.query('*OPC?')  # increase timeout to wait measure finish
        keysightE4990A.instrument.write(':SOUR:BIAS:STAT ON')  # Turn on Bias
        opc = keysightE4990A.instrument.query('*OPC?')  # increase timeout to wait measure finish
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
        # Turn off bias
        keysightE4990A.turn_off_bias()

        data = np.zeros((CW_parameters["NUM_POINTS"], 3))
        for u in range(CW_parameters["NUM_POINTS"]):
            data[u, 0] = rax[u]
            data[u, 1] = ra1[2 * u]
            data[u, 2] = ra2[2 * u]

        X = data[:, 0]
        Y1 = data[:, 1]
        Y2 = data[:, 2]

        if CW_parameters["START"] > CW_parameters["STOP"]:
            # invert X, Y1 and Y2
            X = np.flip(X)
            Y1 = np.flip(Y1)
            Y2 = np.flip(Y2)


    except Exception as ex:
        print(f"error ocurred: {ex} ")
        keysightE4990A.stop()

        return [], [], []

    return X, Y1, Y2

try:

    keysightE4990A = Keysight_E4990A(instruments["Keysight_E4990A"])
    # init CW_parameters
    load_CW_parameters()
    frequency, capacitance, conductance = [], [], []
    # extract spots
    spots = CW_parameters["SPOT"].replace(" ", "").split(",")
    # convert to float
    spots = [float(i) for i in spots
             if (i.isnumeric() or
                 (i[0] == "-" and i[1:].isnumeric()) or
                 (i[0] == "+" and i[1:].isnumeric()))]

    if cartographic_measurement:
        if str(dieActual) == "1" and str(moduleActual) == "1":
            retval = message_user(main, "Init instrument for CW!", "Please, configure instrument for initialization",
                                  "yes_cancel")
            if retval == QMessageBox.Yes:
                # reset instrument (delete previous configuration)
                keysightE4990A.reset()
                test_status.status = "STARTED"
                # make compensation
                make_full_compensation(main, keysightE4990A, CW_parameters)
            else:
                test_status.status = "ABORTED"

        if test_status.status == "STARTED":
            # init CW_parameters
            load_CW_parameters()
            frequency, capacitance, conductance = [], [], []
            for spot in spots:
                CW_parameters["SPOT"] = spot
                # single measure
                if keysightE4990A.config_CW(CW_parameters):
                    if CW_parameters["WAIT_TIME"] > 0:
                        time.sleep(CW_parameters["WAIT_TIME"])
                    frequency, capacitance, conductance = measure_CW(keysightE4990A, CW_parameters)

                    # Turn off bias
                    keysightE4990A.turn_off_bias()
                    meas_status = "meas_success"
                else:
                    frequency, capacitance, conductance = [],[],[]
                    meas_status = "meas_error"
                params = []
                data = []

                # save results
                main.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1] = {
                    "status": meas_status,
                    "message": "",
                    "contact_height": "",
                    "variables": {
                        "params": params,
                        "data": [{"name": "W", "values": frequency, "units": "Hz"},
                                 {"name": "C", "values": capacitance * 1e12, "units": "pF"},
                                 {"name": "G", "values": conductance * 1E6, "units": "uS"}]
                    },
                    "plot_parameters": {
                        "name": "Plot CW " + str(CW_parameters["SPOT"]) + "V (Die " + str(dieActual) + " Module " + str(moduleActual) + ")",
                        "x": frequency/1e3,
                        "y1": capacitance * 1e12,
                        "y2": conductance * 1e6,

                        "titles": {
                            "title": "Plot CW " + str(CW_parameters["SPOT"]) + "V (Die " + str(dieActual) + " Module " + str(moduleActual) + ")",
                            "left": "Capacitance",
                            "bottom": "Frequency",
                            "right": "Conductance"
                        },
                        "units": {
                            "left": "pF",
                            "bottom": "kHz",
                            "right": "uS"
                        },
                        "showgrid": {"x": True, "y": True},

                        "legend": True,
                        "logarithmic" : {"x" : True, "y" : False} if CW_parameters["LOGFREQ"] else {"x" : False, "y" : False},

                    }

                }
                plot_parameters = main.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1]["plot_parameters"]

                emit_plot(plot_parameters)
                
                results_data = list(zip(frequency, capacitance, conductance))
                variables_list = ["F", "C", "G"]
                output_params = CW_parameters.get("output", {"separator": "comma", "prefix": f"CW{CW_parameters['SPOT']}V", "suffix": ""})
                
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
        make_full_compensation(main, keysightE4990A, CW_parameters)
        # init CW_parameters
        load_CW_parameters()
        frequency, capacitance, conductance = [], [], []
        # single measure
        for spot in spots:
            CW_parameters["SPOT"] = spot
            if keysightE4990A.config_CW(CW_parameters):
                if CW_parameters["WAIT_TIME"] > 0:
                    time.sleep(CW_parameters["WAIT_TIME"])

                frequency, capacitance, conductance = measure_CW(keysightE4990A, CW_parameters)

                # Turn off bias
                keysightE4990A.turn_off_bias()
                # Plot parameters
                plot_parameters = {
                    "name": "Plot CW",
                    "x": frequency/1e3,
                    "y1": capacitance * 1e12,
                    "y2": conductance * 1e6,

                    "titles": {
                        "title": f"Plot CW at {str(spot)} V",
                        "left": "Capacitance",
                        "bottom": "Frequency",
                        "right": "Conductance"
                    },
                    "units": {
                        "left": "pF",
                        "bottom": "kHz",
                        "right": "uS"
                    },
                    "showgrid": {"x": True, "y": True},
                    "legend": True,
                    "logarithmic" : {"x" : True, "y" : False} if CW_parameters["LOGFREQ"] else {"x" : False, "y" : False},

                }
                dieActual = 1
                moduleActual = 1

                emit_plot(plot_parameters)
                
                results_data = list(zip(frequency, capacitance, conductance))
                variables_list = ["F", "C", "G"]
                output_params = CW_parameters.get("output", {"separator": "comma", "prefix": f"CW{CW_parameters['SPOT']}V", "suffix": "single"})
                
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
    main.updateTextDescription(message,"ERROR")
    message_user(main, "ERROR", message, "ok_error")
