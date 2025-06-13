# Test CV in HP 4192A instrument

import os.path
import sys
from PySide6.QtWidgets import QMessageBox
from config.functions import *
import toml
global test_status, measurement_status
global dieActual, moduleActual
global CV_parameters
global base_dir, tests_dir, cartographic_measurement


def load_CV_parameters():
    global CV_parameters
    
    import json
    # default values
    CV_parameters = {
    "START" : 1,
    "STOP" : -1,
    "STEP" : 0.1,
    "FREQ" : 100,
    "OSC" : 30,
    "PN" : 1, # Tipo P = 1, Tipo N = -1
    "CIRCUIT_MODE" : "Parallel",
    "NOT_CHANGE" : False,
    "AVERAGE" : False, # True is slow measure
    "HYSTERESIS" : False,
    "HYSTERESIS_TIME" : 0,
    "WAIT_TIME" : 1,
    "LIGHT": False,
    "LIGHT_TIME" : 1,
    # parameters to calc
    "TEMPERATURE" : 21.0,
    "AREA" : 9120000, # in um2
    "FIMS" : 4.1, # Al: 4.1, P++: 5.24, N++ 4.15
    "PERMITTIVITY" : 3.9, # SiO2: 3.9, Nitruro: 7.5
    "SERIAL_RES" : False,
    "CALCULATE_PARAMS" : True
    }
    # load from external toml file in tests_dir (if exists, if not default values)
    filename_config = os.getcwd() + base_dir + tests_dir + '/HP_4192A/CV.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        CV_parameters = toml_info["parameters"]
    else:
        print(f"File toml {filename_config} doesn't exists!")

try:

    hp4192A = HP_4192A(instruments["HP_4192A"])
    # measure CV
    # send CV_parameters to CONFIG HP4192A
    # default parameters
    

    if cartographic_measurement:
        # init CV_parameters
        load_CV_parameters()
        if str(dieActual)=="1" and str(moduleActual)=="1":


            # retval = QMessageBox.question(
            #     self,
            #     "Init instrument for CV!",
            #     "Please, configure instrument for initialization",
            #     buttons=QMessageBox.Yes | QMessageBox.Cancel ,
            #     defaultButton=QMessageBox.Yes,
            # )
            retval = message_user(main, "Init instrument for CV!", "Please, configure instrument for initialization", "yes_cancel")
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
            voltage = []
            capacitance = []
            conductance = []
            results = {}
            if hp4192A.config_CV(CV_parameters):
                if CV_parameters["WAIT_TIME"]>0:
                    time.sleep(CV_parameters["WAIT_TIME"])

                if CV_parameters["LIGHT"] and CV_parameters["LIGHT_TIME"]>0:
                    main.prober.light("1")
                    time.sleep(CV_parameters["LIGHT_TIME"])
                    main.prober.light("0")

                voltage, capacitance, conductance = measure_CV(hp4192A,CV_parameters,voltage,capacitance,conductance)
                CV_parameters["voltage"] = voltage # list
                CV_parameters["capacitance"] = capacitance # list
                CV_parameters["conductance"] = conductance # list
                CV_parameters["hysteresis_marker"] = False
                print(f"Capacitance {dieActual}: {capacitance}")
                print("Calculating CV")
                if CV_parameters["CALCULATE_PARAMS"]:
                    results = calcular_cv(CV_parameters)
                # hysteresis?
                if CV_parameters["HYSTERESIS"]:
                    voltage_h = []
                    capacitance_h = []
                    conductance_h = []
                    # wait time between measures
                    if CV_parameters["HYSTERESIS_TIME"]>0:
                        time.sleep(CV_parameters["HYSTERESIS_TIME"])
                    # swap variables
                    CV_parameters["START"], CV_parameters["STOP"] = CV_parameters["STOP"], CV_parameters["START"]
                    voltage_h, capacitance_h, conductance_h = measure_CV(hp4192A,CV_parameters,voltage_h,capacitance_h,conductance_h)
                    CV_parameters["voltage"] = voltage_h
                    CV_parameters["capacitance"] = capacitance_h
                    CV_parameters["conductance"] = conductance_h
                    CV_parameters["hysteresis_marker"] = True
                    if CV_parameters["CALCULATE_PARAMS"]:
                        results_h = calcular_cv(CV_parameters)
                        # add to results
                        for clave in results_h:
                            results[clave] = results_h[clave]
                    # union lists
                    voltage = voltage + voltage_h
                    capacitance = capacitance + capacitance_h
                    conductance = conductance + conductance_h

            params = []
            data = []
            if CV_parameters["CALCULATE_PARAMS"]:
                txt_result = "<br /><strong>Results: </strong><br />"
                for clave in results:
                    txt_result = txt_result + " <strong>- " + clave + "</strong> = " + str(results[clave]) + "<br />"
                    params.append({"name" : clave, "value" : str(results[clave])})
                main.updateTextDescription(txt_result)
            meas_status = "meas_success"
            # save results
            main.waferwindow.meas_result[int(dieActual)-1][int(moduleActual)-1] = {
                "status" : meas_status,
                "message" : "",
                "contact_height" : "", 
                "variables" : {
                    "params" : params,
                    "data" : [{"name" : "V", "values" : voltage, "units" : "V"},{"name": "C", "values" : capacitance, "units": "F"},{"name": "G", "values" : conductance, "units": "S"}]
                },
                "plot_parameters" : {
                    "name" : "Plot CV",
                    "x" : voltage,
                    "y1" : capacitance,
                    "y2" : conductance,

                    "titles" : {
                        "title" : "C-V Measurement Die " + str(dieActual) + " Module " + str(moduleActual),
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
            # self.show_graph(plot_parameters)
            emit_plot(plot_parameters)
            namefile = main.getDirs("results") + "/CV_" + main.ui.txtProcess.text() + "_" + str(dieActual) + "_" + str(moduleActual) + ".txt"
            main.save_lists_to_txt(namefile=namefile, var_list=[voltage, capacitance, conductance],
                                   headers=["V", "C", "G"], separation=",")
    else:
        # init CV_parameters
        load_CV_parameters()
        # single measure
        if hp4192A.config_CV(CV_parameters):
            # create empty list if not exists
            voltage = []
            capacitance = []
            conductance = []
            results = {}
            if CV_parameters["WAIT_TIME"]>0:
                time.sleep(CV_parameters["WAIT_TIME"])
            if CV_parameters["LIGHT"]:
                # prober is not initialized when you select single measurement
                main.init_prober()
                if main.prober!="":
                    main.prober.light("1")
                    time.sleep(CV_parameters["LIGHT_TIME"])
                    main.prober.light("0")

            # measure
            voltage, capacitance, conductance = measure_CV(hp4192A,CV_parameters,voltage,capacitance,conductance)
            CV_parameters["voltage"] = voltage
            CV_parameters["capacitance"] = capacitance
            CV_parameters["conductance"] = conductance
            CV_parameters["hysteresis_marker"] = False
            if CV_parameters["CALCULATE_PARAMS"]:
                results = calcular_cv(CV_parameters)
            # hysteresis?
            if CV_parameters["HYSTERESIS"]:
                voltage_h = []
                capacitance_h = []
                conductance_h = []
                # wait time between hysteresis
                if CV_parameters["HYSTERESIS_TIME"]>0:
                    time.sleep(CV_parameters["HYSTERESIS_TIME"])
                # swap variables
                CV_parameters["START"], CV_parameters["STOP"] = CV_parameters["STOP"], CV_parameters["START"]
                if hp4192A.config_CV(CV_parameters):
                    voltage_h, capacitance_h, conductance_h = measure_CV(hp4192A,CV_parameters,voltage_h,capacitance_h, conductance_h)
                    CV_parameters["voltage"] = voltage_h
                    CV_parameters["capacitance"] = capacitance_h
                    CV_parameters["conductance"] = conductance_h
                    CV_parameters["hysteresis_marker"] = True
                    if CV_parameters["CALCULATE_PARAMS"]:
                        # calculate parameters
                        results_h = calcular_cv(CV_parameters)
                        # add to results
                        for clave in results_h:
                            results[clave] = results_h[clave]
                # union lists
                voltage = voltage + voltage_h
                capacitance = capacitance + capacitance_h
                conductance = conductance + conductance_h
            params = []
            data = []
            if CV_parameters["CALCULATE_PARAMS"]:
                txt_result = "<br /><strong>Results: </strong><br />"
                for clave in results:
                    txt_result = txt_result + " <strong>- " + clave + "</strong> = " + str(results[clave]) + "<br />"
                    params.append({"name" : clave, "value" : str(results[clave])})
                main.updateTextDescription(txt_result)

            plot_parameters = {
                "name" : "Plot CV",
                "x" : voltage,
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
                    "right" : "s"
                },
                "showgrid" : {"x" : False, "y" : False},
                "legend" : False
                #"foreground" : "#CCCCCC"

            }

            # self.show_graph(plot_parameters)
            emit_plot(plot_parameters)
            namefile = main.getDirs("results") + "/CV_" + main.ui.txtProcess.text() + "_1_1.txt"
            main.save_lists_to_txt(namefile=namefile, var_list=[voltage, capacitance, conductance], headers=["V", "C", "G"], separation=",")
    # stop process
    hp4192A.stop()
    hp4192A.local()


except:
    message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<","").replace(">","") + " occurred. " + str(sys.exc_info()[1])
    main.updateTextDescription(message,"ERROR")
    # retval = messageBox(main,"ERROR",message,"critical")
    message_user(main, "ERROR",message,"ok_error")
    #print("ERROR: " + "Oops! " + str(sys.exc_info()[0]) + " occurred. " + str(sys.exc_info()[1]))




