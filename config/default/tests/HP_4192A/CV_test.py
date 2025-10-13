# Test CV in HP 4192A instrument

import os.path
import sys
from PySide6.QtWidgets import QMessageBox

from config.default.instruments import HP_4192A
from config.functions import *
import toml
global test_status, measurement_status
global dieActual, moduleActual
global CV_parameters
global base_dir, tests_dir, cartographic_measurement


def measure_CV(hp4192A,CV_parameters):
    # create empty list
    voltage, capacitance, conductance = [], [], []
    # Calc samples
    num_samples = abs((float(CV_parameters["START"])-float(CV_parameters["STOP"]))/float(CV_parameters["STEP"])) + 1
    PN = 1
    if CV_parameters["START"] > CV_parameters["STOP"]:
        PN = -1
    for i in range(0,int(num_samples)):
        try:
            hp4192A.single()  # lanza la medida
            lectura = hp4192A.read()  # lee la medida
            lectura_array = lectura.split(",")
            capacitance_value = lectura_array[0][4:]
            conductance_value = lectura_array[1][4:]
            voltage_value = lectura_array[2][1:]
            capacitance.append(float(capacitance_value))
            conductance.append(float(conductance_value))
            voltage.append(float(voltage_value))
            hp4192A.srq()  # habilita SRQ

        except Exception as e:
            # with error in read stop the loop
            print(f"Error: {e}")
            break

    return voltage,capacitance,conductance


def measure_CV_full(hp4192A, main, CV_parameters):
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
    voltage, capacitance, conductance = measure_CV(hp4192A, CV_parameters)
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
        if hp4192A.config_CV(CV_parameters):
            voltage_h, capacitance_h, conductance_h = measure_CV(hp4192A, CV_parameters)
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
        voltage = voltage + voltage_h
        capacitance = capacitance + capacitance_h
        conductance = conductance + conductance_h

    return voltage, capacitance, conductance, results


def make_compensation(main, hp4192A, CV_parameters):
    # make OPEN and SHORT compensation
    retval = message_user(main, "Compensation", "Please, make OPEN compensation: remove the device from the fixture and press OK", "ok_cancel")
    if retval != QMessageBox.Ok:
        return False
    main.updateTextDescription("Making OPEN compensation...<br />")
    if CV_parameters["COMPENSATION_OPEN"]:
        hp4192A.zero_open("ON")
    else:
        hp4192A.zero_open("OFF")
    time.sleep(1)
    retval = message_user(main, "Compensation", "Please, make SHORT compensation: short the fixture and press OK", "ok_cancel")
    if retval != QMessageBox.Ok:
        return False
    main.updateTextDescription("Making SHORT compensation...<br />")
    if CV_parameters["COMPENSATION_SHORT"]:
        hp4192A.zero_short("ON")
    else:
        hp4192A.zero_short("OFF")
    time.sleep(1)

    return True

# Make compensation
def make_full_compensation(main, hp4192A, CV_parameters):
    if not CV_parameters["COMPENSATION_DONE"]:
        main.updateTextDescription("<br />Making compensation...<br />")
        if not make_compensation(main, hp4192A, CV_parameters):
            main.updateTextDescription("Compensation failed! Aborting test...<br />", "ERROR")
            test_status.status = "ABORTED"
        else:
            # modify toml file to indicate that compensation is done
            CV_parameters["COMPENSATION_DONE"] = True
            filename_config = os.getcwd() + base_dir + tests_dir + '/HP_4192A/CV.toml'
            file_exists = os.path.exists(filename_config)
            if file_exists:
                toml_info = toml.load(filename_config)
                toml_info["parameters"] = CV_parameters
                # save file in UTF-8
                with open(filename_config, 'w', encoding='utf-8') as tomlfile:
                    toml.dump(toml_info, tomlfile)
            main.updateTextDescription("Compensation done!<br />")
            retval = message_user(main, "Compensation done!", "Please, configure instrument for measurement, make CONTACT and press YES to continue", "yes_cancel")


def load_CV_parameters():
    global CV_parameters
    
    # default values
    CV_parameters = {
    "START" : 1,
    "STOP" : -1,
    "STEP" : 0.1,
    "FREQ" : "100",
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
    # load CV parameters from toml
    load_CV_parameters()
    # extract frequencies
    freqs = CV_parameters["FREQ"].replace(" ", "").split(",")
    # convert to float
    freqs = [float(frequency) for frequency in freqs if frequency.isnumeric()]
    if cartographic_measurement:
        if str(dieActual)=="1" and str(moduleActual)=="1":
            retval = message_user(main, "Init instrument for CV!", "Please, configure instrument for initialization", "yes_cancel")
            if retval == QMessageBox.Yes:
                # reset instrument
                hp4192A.reset()
                test_status.status = "STARTED"
                # make compensation
                make_full_compensation(main, hp4192A, CV_parameters)
            else:
                test_status.status = "ABORTED"

        if test_status.status=="STARTED":
            # single measure
            for freq in freqs:
                CV_parameters["FREQ"] = freq
                if hp4192A.config_CV(CV_parameters):
                    voltage, capacitance, conductance, results = measure_CV_full(hp4192A, main, CV_parameters)
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
                else:
                    voltage, capacitance, conductance = [], [], []
                    meas_status = "meas_error"
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
                        "name" : f"Plot CV Die {dieActual} Module {moduleActual}",
                        "x" : voltage,
                        "y1" : capacitance,
                        "y2" : conductance,

                        "titles" : {
                            "title" : "Plot CV " + str(CV_parameters["FREQ"]) + "kHz (Die " + str(dieActual) + " Module " + str(moduleActual) + ")",
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
                        "legend" : True

                    }

                }
                plot_parameters = main.waferwindow.meas_result[int(dieActual)-1][int(moduleActual)-1]["plot_parameters"]

                emit_plot(plot_parameters)
                namefile = main.getDirs("results") + "/CV" + str(CV_parameters["FREQ"]) + "kHz_" + main.ui.txtProcess.text() + "_" + str(
                    dieActual) + "_" + str(
                    moduleActual) + ".txt"
                main.save_lists_to_txt(namefile=namefile, var_list=[voltage, capacitance, conductance],
                                       headers=["V", "C", "G"], separation=",")

    else:
        # reset instrument
        hp4192A.reset()
        # make compensation
        make_full_compensation(main, hp4192A, CV_parameters)
        # single measure
        for freq in freqs:
            CV_parameters["FREQ"] = freq
            if hp4192A.config_CV(CV_parameters):
                voltage, capacitance, conductance, results = measure_CV_full(hp4192A, main, CV_parameters)
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
                        "title" : "CV Measurement at " + str(CV_parameters["FREQ"]) + "kHz",
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
                    "legend" : True
                    #"foreground" : "#CCCCCC"

                }

                dieActual = 1
                moduleActual = 1
                # stop process
                hp4192A.stop()
                emit_plot(plot_parameters)
                namefile = main.getDirs("results") + "/CV" + str(CV_parameters["FREQ"]) + "kHz_" + main.ui.txtProcess.text() + "_" + str(dieActual) + "_" + str(
                    moduleActual) + ".txt"
                main.save_lists_to_txt(namefile=namefile, var_list=[voltage, capacitance, conductance],
                                       headers=["V", "C", "G"], separation=",")


    hp4192A.local()
    hp4192A.close()


except:
    message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<","").replace(">","") + " occurred. " + str(sys.exc_info()[1])
    main.updateTextDescription(message,"ERROR")
    # retval = messageBox(main,"ERROR",message,"critical")
    message_user(main, "ERROR",message,"ok_error")
    #print("ERROR: " + "Oops! " + str(sys.exc_info()[0]) + " occurred. " + str(sys.exc_info()[1]))




