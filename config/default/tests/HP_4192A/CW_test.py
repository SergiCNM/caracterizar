# Test CW in HP 4192A instrument

import os.path
import sys
from PySide6.QtWidgets import QMessageBox

from config.default.instruments import HP_4192A
from config.functions import *
import toml
global test_status, measurement_status
global dieActual, moduleActual
global CW_parameters
global base_dir, tests_dir, cartographic_measurement
    
def measure_CW(hp4192A,CW_parameters,frequency,capacitance,conductance):
    i = 0
    # Calc samples
    num_samples = abs((float(CW_parameters["START"])-float(CW_parameters["STOP"]))/float(CW_parameters["STEP"])) + 1
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


def load_CW_parameters():
    global CW_parameters
    
    # default values
    CW_parameters = {
    "START" : 1,
    "STOP" : 1000,
    "STEP" : 1,
    "VOLTAGE" : -5,
    "SPOT" : 30,
    "CIRCUIT_MODE" : "Parallel",
    "AVERAGE" : False # True is slow measure
    }
    # load from external json file in tests_dir (if exists, if not default values)
    # filename_config = os.getcwd() + base_dir + tests_dir + '/HP_4192A/CW.json'
    # file_exists = os.path.exists(filename_config)
    # if file_exists:
    #     with open(filename_config) as json_file:
    #         CW_parameters = json.load(json_file)
    filename_config = os.getcwd() + base_dir + tests_dir + '/HP_4192A/CW.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        CW_parameters = toml_info["parameters"]
    else:
        print(f"File toml {filename_config} doesn't exists!")


try:

    hp4192A = HP_4192A(instruments["HP_4192A"])
    # measure CV
    # send CV_parameters to CONFIG HP4192A
    # default parameters
    

    if cartographic_measurement:
        # init CW_parameters
        load_CW_parameters()
        if str(dieActual)=="1" and str(moduleActual)=="1":
            # retval = QMessageBox.question(
            #     main,
            #     "Init instrument for CW!",
            #     "Please, configure instrument for initialization",
            #     buttons=QMessageBox.Yes | QMessageBox.Cancel ,
            #     defaultButton=QMessageBox.Yes,
            # )
            retval = message_user(main, "Init instrument for CW!", "Please, configure instrument for initialization",
                                  "yes_cancel")
            if retval == QMessageBox.Yes:
                # reset instrument
                hp4192A.reset()
                # Zero open & Zero shorth
                #hp4192A.zero_open("ON")
                #hp4192A.zero_short("OFF")
                test_status.status = "STARTED"
            else:
                test_status.status = "ABORTED"

        if test_status.status=="STARTED":
            frequency = []
            capacitance = []
            conductance = []
            if hp4192A.config_CW(CW_parameters):

                frequency, capacitance, conductance = measure_CW(hp4192A,CW_parameters,frequency,capacitance,conductance)
                CW_parameters["frequency"] = frequency # list
                CW_parameters["capacitance"] = capacitance # list
                CW_parameters["conductance"] = conductance # list

            meas_status = "meas_success"
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
                    "name" : f"Plot CW Die {dieActual} Module {moduleActual}",
                    "x" : frequency,
                    "y1" : capacitance,
                    "y2" : conductance,

                    "titles" : {
                        "title" : f"Plot CW Die {dieActual} Module {moduleActual}",
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
                    "legend" : False

                }

            }
            plot_parameters = main.waferwindow.meas_result[int(dieActual)-1][int(moduleActual)-1]["plot_parameters"]

    else:
        # init CW_parameters
        load_CW_parameters()
        # single measure
        if hp4192A.config_CW(CW_parameters):
            frequency = []
            capacitance = []
            conductance = []

            frequency, capacitance, conductance = measure_CW(hp4192A,CW_parameters,frequency,capacitance,conductance)
            CW_parameters["frequency"] = frequency # list
            CW_parameters["capacitance"] = capacitance # list
            CW_parameters["conductance"] = conductance # list
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

            posx = 0
            posy = 0
            dieActual = 1
            moduleActual = 1

    emit_plot(plot_parameters)
    namefile = main.getDirs("results") + "/CV_" + main.ui.txtProcess.text() + "_" + str(dieActual) + "_" + str(
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




