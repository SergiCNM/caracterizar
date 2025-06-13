# Test CW in HP 4192A instrument

import os.path
import sys
from PySide6.QtWidgets import QMessageBox
from config.functions import *
global test_status, measurement_status
global dieActual, moduleActual
global CW_parameters
global base_dir, tests_dir, cartographic_measurement
    

def load_CW_parameters():
    global CW_parameters
    
    import json
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
    filename_config = os.getcwd() + base_dir + tests_dir + '/HP_4192A/CW.json'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        with open(filename_config) as json_file:
            CW_parameters = json.load(json_file)


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
                    "data" : [{"name" : "V", "values" : frequency, "units" : "V"},{"name": "C", "values" : capacitance, "units": "F"},{"name": "G", "values" : conductance, "units": "S"}]
                },
                #"variables" : [{"name" : "cmax(pF)", "value" : 420.056},{"name" : "cmin(pF)", "value" : 210.057}],
                "plot_parameters" : {
                    "name" : "Plot CV",
                    "x" : frequency,
                    "y1" : capacitance,
                    "y2" : conductance,

                    "titles" : {
                        "title" : "C-V Measurement",
                        "left" : "Capacitance",
                        "bottom" : "Voltage",
                        "right" : "Conductance"
                    },
                    "units" : {
                        "left" : "F",
                        "bottom" : "V",
                        "right" : "S"
                    },
                    "showgrid" : {"x" : False, "y" : False},
                    "legend" : False

                }

            }
            plot_parameters = main.waferwindow.meas_result[int(dieActual)-1][int(moduleActual)-1]["plot_parameters"]
            # self.show_plotwindow(plot_parameters, posx, posy)
            emit_plot(plot_parameters)
            namefile = main.getDirs("results") + "/CV_" + main.ui.txtProcess.text() + "_" + str(dieActual) + "_" + str(
                moduleActual) + ".txt"
            main.save_lists_to_txt(namefile=namefile, var_list=[frequency, capacitance, conductance],
                                   headers=["F", "C", "G"], separation=",")
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
                "name" : "Plot CW",
                "x" : frequency,
                "y1" : capacitance,
                "y2" : conductance,

                "titles" : {
                    "title" : "CW Measurement",
                    "left" : "Capacitance",
                    "bottom" : "Frequency",
                    "right" : "Conductance"
                },
                "units" : {
                    "left" : "F",
                    "bottom" : "Hz",
                    "right" : "s"
                },
                "showgrid" : {"x" : False, "y" : False},
                "legend" : False
                #"foreground" : "#CCCCCC"

            }

            posx = 0
            posy = 0
            #self.show_plotwindow(plot_parameters, posx, posy)
            emit_plot(plot_parameters)
            namefile = main.getDirs("results") + "/CW_" + main.ui.txtProcess.text() + "_1_1.txt"
            main.save_lists_to_txt(namefile=namefile, var_list=[frequency, capacitance, conductance],
                                   headers=["F", "C", "G"], separation=",")
    # stop process
    hp4192A.stop()
    hp4192A.local()

    


except:
    message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<","").replace(">","") + " occurred. " + str(sys.exc_info()[1])
    main.updateTextDescription(message,"ERROR")
    # retval = messageBox(main,"ERROR",message,"critical")
    message_user(main, "ERROR", message, "ok_error")
    #print("ERROR: " + "Oops! " + str(sys.exc_info()[0]) + " occurred. " + str(sys.exc_info()[1]))




