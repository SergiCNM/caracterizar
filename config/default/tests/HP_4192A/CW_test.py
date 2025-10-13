# -------------------------------------------------------
# Test CW in HP 4192A instrument
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

from config.default.instruments import HP_4192A
from config.functions import *
import toml
global test_status, measurement_status
global dieActual, moduleActual
global CW_parameters
global base_dir, tests_dir, cartographic_measurement


def measure_CW(hp4192A, CW_parameters):
    """ Measure CW from START to STOP with STEP"""
    frequency, capacitance, conductance = [],[],[]
    # lectura 4192a ex: NCPN+0.7910E-06,NGFN+14.940E+00,K+01000.000
    frequency_value = 0
    while float(frequency_value)<float(CW_parameters["STOP"]):
        hp4192A.single()
        lectura = hp4192A.read()
        lectura_array = lectura.split(",")
        capacitance_value = lectura_array[0][4:]
        conductance_value = lectura_array[1][4:]
        frequency_value = lectura_array[2][1:]
        capacitance.append(float(capacitance_value))
        conductance.append(float(conductance_value))
        frequency.append(float(frequency_value))
        hp4192A.srq()

    return frequency,capacitance,conductance

def make_compensation(main, hp4192A, CW_parameters):
    # make OPEN and SHORT compensation
    retval = message_user(main, "Compensation", "Please, make OPEN compensation: remove the device from the fixture and press OK", "ok_cancel")
    if retval != QMessageBox.Ok:
        return False
    main.updateTextDescription("Making OPEN compensation...<br />")
    if CW_parameters["COMPENSATION_OPEN"]:
        hp4192A.zero_open("ON")
    else:
        hp4192A.zero_open("OFF")
    time.sleep(1)
    retval = message_user(main, "Compensation", "Please, make SHORT compensation: short the fixture and press OK", "ok_cancel")
    if retval != QMessageBox.Ok:
        return False
    main.updateTextDescription("Making SHORT compensation...<br />")
    if CW_parameters["COMPENSATION_SHORT"]:
        hp4192A.zero_short("ON")
    else:
        hp4192A.zero_short("OFF")
    time.sleep(1)

    return True

# Make compensation
def make_full_compensation(main, hp4192A, CW_parameters):
    if not CW_parameters["COMPENSATION_DONE"]:
        main.updateTextDescription("<br />Making compensation...<br />")
        if not make_compensation(main, hp4192A, CW_parameters):
            main.updateTextDescription("Compensation failed! Aborting test...<br />", "ERROR")
            test_status.status = "ABORTED"
        else:
            # modify toml file to indicate that compensation is done
            CW_parameters["COMPENSATION_DONE"] = True
            filename_config = os.getcwd() + base_dir + tests_dir + '/HP_4192A/CW.toml'
            file_exists = os.path.exists(filename_config)
            if file_exists:
                toml_info = toml.load(filename_config)
                toml_info["parameters"] = CW_parameters
                # save file in UTF-8
                with open(filename_config, 'w', encoding='utf-8') as tomlfile:
                    toml.dump(toml_info, tomlfile)
            main.updateTextDescription("Compensation done!<br />")
            retval = message_user(main, "Compensation done!", "Please, configure instrument for measurement, make CONTACT and press YES to continue", "yes_cancel")



def load_CW_parameters():
    global CW_parameters
    
    # default values
    CW_parameters = {
    "START" : 1,
    "STOP" : 1000,
    "STEP" : 1,
    "SPOT" : "-5",
    "OSC": 30,
    "CIRCUIT_MODE" : "Parallel",
    "AVERAGE" : True, # True is slow measure
    "COMPENSATION_OPEN" : True,
    "COMPENSATION_SHORT" : True,
    "COMPENSATION_DONE" : False
    }
    filename_config = os.getcwd() + base_dir + tests_dir + '/HP_4192A/CW.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        CW_parameters = toml_info["parameters"]
    else:
        print(f"File toml {filename_config} doesn't exists!")


try:

    hp4192A = HP_4192A(instruments["HP_4192A"])
    # init CW_parameters
    load_CW_parameters()
    frequency, capacitance, conductance = [],[],[]
    # extract spots
    spots = CW_parameters["SPOT"].replace(" ", "").split(",")
    # convert to float
    spots = [float(i) for i in spots
             if (i.isnumeric() or
                 (i[0]=="-" and i[1:].isnumeric()) or
                 (i[0]=="+" and i[1:].isnumeric()))]

    if cartographic_measurement:
        if str(dieActual)=="1" and str(moduleActual)=="1":
            retval = message_user(main, "Init instrument for CW!", "Please, configure instrument for initialization",
                                  "yes_cancel")
            if retval == QMessageBox.Yes:
                # reset instrument
                hp4192A.reset()
                test_status.status = "STARTED"
                # make compensation
                make_full_compensation(main, hp4192A, CW_parameters)
            else:
                test_status.status = "ABORTED"

        if test_status.status=="STARTED":
            for spot in spots:
                CW_parameters["SPOT"] = spot
                if hp4192A.config_CW(CW_parameters):
                    frequency, capacitance, conductance = measure_CW(hp4192A, CW_parameters)
                    CW_parameters["frequency"] = frequency
                    CW_parameters["capacitance"] = capacitance
                    CW_parameters["conductance"] = conductance

                    meas_status = "meas_success"
                else:
                    frequency, capacitance, conductance = [],[],[]
                    meas_status = "meas_error"
                # save results
                main.waferwindow.meas_result[int(dieActual)-1][int(moduleActual)-1] = {
                    "status" : meas_status,
                    "message" : "",
                    "contact_height" : "",
                    "variables" : {
                        "params" : [],
                        "data" : [{"name" : "V", "values" : frequency, "units" : "V"},{"name": "C", "values" : capacitance, "units": "pF"},{"name": "G", "values" : conductance, "units": "nS"}]
                    },
                    #"variables" : [{"name" : "cmax(pF)", "value" : 420.056},{"name" : "cmin(pF)", "value" : 210.057}],
                    "plot_parameters" : {
                        "name" : "Plot CW " + str(CW_parameters["SPOT"]) + "V (Die " + str(dieActual) + " Module " + str(moduleActual) + ")",
                        "x" : frequency,
                        "y1" : capacitance,
                        "y2" : conductance,

                        "titles" : {
                            "title" : "Plot CW " + str(CW_parameters["SPOT"]) + "V (Die " + str(dieActual) + " Module " + str(moduleActual) + ")",
                            "left" : "Capacitance",
                            "bottom" : "Frequency",
                            "right" : "Conductance"
                        },
                        "units" : {
                            "left" : "F",
                            "bottom" : "kHz",
                            "right" : "S"
                        },
                        "showgrid" : {"x" : False, "y" : False},
                        "legend" : True,
                        "logarithmic": {"x": True, "y": False},

                    }

                }
                plot_parameters = main.waferwindow.meas_result[int(dieActual)-1][int(moduleActual)-1]["plot_parameters"]

                emit_plot(plot_parameters)
                namefile = main.getDirs("results") + "/CW"+ str(CW_parameters["SPOT"]) + "V" + main.ui.txtProcess.text() + "_" + str(
                    dieActual) + "_" + str(
                    moduleActual) + ".txt"
                main.save_lists_to_txt(namefile=namefile, var_list=[frequency, capacitance, conductance],
                                       headers=["F", "C", "G"], separation=",")

    else:
        # reset instrument
        hp4192A.reset()
        # make compensation
        make_full_compensation(main, hp4192A, CW_parameters)
        # single measure
        for spot in spots:
            CW_parameters["SPOT"] = spot
            if hp4192A.config_CW(CW_parameters):
                frequency, capacitance, conductance = measure_CW(hp4192A, CW_parameters)
                CW_parameters["frequency"] = frequency
                CW_parameters["capacitance"] = capacitance
                CW_parameters["conductance"] = conductance
                plot_parameters = {
                    "name" : f"Plot CW Single Measure",
                    "x" : frequency,
                    "y1" : capacitance,
                    "y2" : conductance,

                    "titles" : {
                        "title" : "Plot CW Single Measure",
                        "left" : "Capacitance",
                        "bottom" : "Frequency",
                        "right" : "Conductance"
                    },
                    "units" : {
                        "left" : "F",
                        "bottom" : "kHz",
                        "right" : "s"
                    },
                    "showgrid" : {"x" : False, "y" : False},
                    "legend" : True,
                    "logarithmic" : {"x" : True, "y" : False},
                    #"foreground" : "#CCCCCC"

                }

                dieActual = 1
                moduleActual = 1

                emit_plot(plot_parameters)
                namefile = main.getDirs("results") + "/CW" + str(
                    CW_parameters["SPOT"]) + "V" + main.ui.txtProcess.text() + "_" + str(
                    dieActual) + "_" + str(
                    moduleActual) + ".txt"
                main.save_lists_to_txt(namefile=namefile, var_list=[frequency, capacitance, conductance],
                                       headers=["F", "C", "G"], separation=",")

    # stop process
    hp4192A.stop()
    hp4192A.local()

    hp4192A.close()


except:
    message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<","").replace(">","") + " occurred. " + str(sys.exc_info()[1])
    main.updateTextDescription(message,"ERROR")
    # retval = messageBox(main,"ERROR",message,"critical")
    message_user(main, "ERROR", message, "ok_error")
    #print("ERROR: " + "Oops! " + str(sys.exc_info()[0]) + " occurred. " + str(sys.exc_info()[1]))




