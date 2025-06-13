# Test CV in Keysight E4990A instrument

import os.path
import sys
import numpy as np
from config.functions import *
import toml

global test_status, measurement_status
global dieActual, moduleActual

global CV_parameters


def load_CV_MultiFreq_parameters():
    global CV_parameters

    import json
    # default values
    CV_parameters = {
        "START": 0,
        "STOP": 40,
        "NUM_POINTS": 101,
        "MULTIFREQ": "100,1000",
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
    }
    # load from external toml file in tests_dir (if exists, if not default values)
    filename_config = os.getcwd() + base_dir + tests_dir + '/Keysight_E4990A/CV_MultiFreq.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        CV_parameters = toml_info["parameters"]


try:

    keysightE4990A = Keysight_E4990A(instruments["Keysight_E4990A"])
    # measure CV
    # send CV_parameters to CONFIG HP4192A
    # default parameters

    if cartographic_measurement:
        if str(dieActual) == "1" and str(moduleActual) == "1":
            retval = QMessageBox.question(
                self,
                "Init instrument for CV!",
                "Please, configure instrument for initialization",
                buttons=QMessageBox.Yes | QMessageBox.Cancel,
                defaultButton=QMessageBox.Yes,
            )
            if retval == QMessageBox.Yes:
                # reset instrument
                # keysightE4990A.reset()
                # # Calibration open, short, load
                # self.prober.move_separation()
                # if keysightE4990A.calibration(["OPEN"]):
                #     test_status.status = "STARTED"
                #     self.prober.move_contact()
                # else:
                #     test_status.status = "ABORTED"
                test_status.status = "STARTED"
            else:
                test_status.status = "ABORTED"

        if test_status.status == "STARTED":
            # init CV_parameters
            multiFreq = CV_parameters["MULTIFREQ"].split(",")
            # set multi frequency
            for i in range(len(multiFreq)):
                # set frequency to int value
                CV_parameters["FREQ"] = int(multiFreq[i].strip())
                voltage = []
                capacitance = []
                conductance = []
                voltage_h = []
                capacitance_h = []
                conductance_h = []
                if keysightE4990A.config_CV(CV_parameters):
                    if CV_parameters["WAIT_TIME"] > 0:
                        time.sleep(CV_parameters["WAIT_TIME"])

                    if CV_parameters["LIGHT"] and CV_parameters["LIGHT_TIME"] > 0:
                        self.prober.light("1")
                        time.sleep(CV_parameters["LIGHT_TIME"])
                        self.prober.light("0")

                    CV_parameters["hysteresis_mode"] = False
                    voltage, capacitance, conductance = keysightE4990A.measure(CV_parameters)
                    CV_parameters["voltage"] = voltage  # list
                    CV_parameters["capacitance"] = capacitance  # list
                    CV_parameters["conductance"] = conductance  # list
                    CV_parameters["hysteresis"] = False

                    # hysteresis?
                    if CV_parameters["HYSTERESIS"]:
                        # wait time between measures
                        if CV_parameters["HYSTERESIS_TIME"] > 0:
                            time.sleep(CV_parameters["HYSTERESIS_TIME"])
                        # swap variables
                        CV_parameters["START"], CV_parameters["STOP"] = CV_parameters["STOP"], CV_parameters["START"]
                        if keysightE4990A.config_CV(CV_parameters):
                            CV_parameters["hysteresis_mode"] = True
                            voltage_h, capacitance_h, conductance_h = keysightE4990A.measure(CV_parameters)
                            CV_parameters["voltage"] = voltage_h
                            CV_parameters["capacitance"] = capacitance_h
                            CV_parameters["conductance"] = conductance_h
                            CV_parameters["hysteresis"] = True
                        # concatenate lists
                        voltage = np.concatenate((voltage, voltage_h))
                        capacitance = np.concatenate((capacitance, capacitance_h))
                        conductance = np.concatenate((conductance, conductance_h))
                        # Turn off bias
                        keysightE4990A.turn_off_bias()

                params = []
                data = []

                meas_status = "meas_success"
                # save results
                self.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1] = {
                    "status": meas_status,
                    "message": "",
                    "contact_height": "",
                    "variables": {
                        "params": params,
                        "data": [{"name": "V", "values": voltage, "units": "V"},
                                 {"name": "C", "values": capacitance * 1e15, "units": "fF"},
                                 {"name": "G", "values": conductance * 1E9, "units": "nS"}]
                    },
                    "plot_parameters": {
                        "name": "Plot CV Die " + str(dieActual) + " Module " + str(moduleActual),
                        "x": voltage,
                        "y1": capacitance * 1e15,
                        "y2": conductance * 1e9,

                        "titles": {
                            "title": "C-V Measurement" + str(dieActual) + " Module " + str(moduleActual),
                            "left": "Capacitance",
                            "bottom": "Voltage",
                            "right": "Conductance"
                        },
                        "units": {
                            "left": "fF",
                            "bottom": "V",
                            "right": "nS"
                        },
                        "showgrid": {"x": True, "y": True},
                        "legend": False

                    }

                }
                QApplication.processEvents()
                plot_parameters = self.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1]["plot_parameters"]
                self.show_graph(plot_parameters)
                namefile = (self.getDirs("results") + "/CV_" + self.ui.txtProcess.text() + "_" + str(CV_parameters["FREQ"]) +
                            "kHz_" + str(dieActual) + "_" + str(moduleActual) + ".txt")
                self.save_lists_to_txt(namefile=namefile, var_list=[voltage, capacitance, conductance],
                                       headers=["V", "C", "G"], separation=",")
                QApplication.processEvents()
    else:
        # init CV_parameters
        load_CV_MultiFreq_parameters()
        multiFreq = CV_parameters["MULTIFREQ"].split(",")
        # set multi frequency
        for i in range(len(multiFreq)):
            # set frequency to int value
            CV_parameters["FREQ"] = int(multiFreq[i].strip())
            message = "CV at " + str(CV_parameters["FREQ"]) + " kHz"
            self.updateTextDescription(message, "INFO")
            voltage = []
            capacitance = []
            conductance = []
            voltage_h = []
            capacitance_h = []
            conductance_h = []
            # single measure
            if keysightE4990A.config_CV(CV_parameters):
                if CV_parameters["WAIT_TIME"] > 0:
                    time.sleep(CV_parameters["WAIT_TIME"])
                if CV_parameters["LIGHT"]:
                    # prober is not initialized when you select single measurement
                    self.init_prober()
                    if self.prober != "":
                        self.prober.light("1")
                        time.sleep(CV_parameters["LIGHT_TIME"])
                        self.prober.light("0")

                # measure
                CV_parameters["hysteresis_mode"] = False
                voltage, capacitance, conductance = keysightE4990A.measure(CV_parameters)
                CV_parameters["voltage"] = voltage
                CV_parameters["capacitance"] = capacitance
                CV_parameters["conductance"] = conductance
                CV_parameters["hysteresis"] = False
                # hysteresis?
                if CV_parameters["HYSTERESIS"]:
                    # wait time between hysteresis
                    if CV_parameters["HYSTERESIS_TIME"] > 0:
                        time.sleep(CV_parameters["HYSTERESIS_TIME"])
                    # swap variables
                    CV_parameters["START"], CV_parameters["STOP"] = CV_parameters["STOP"], CV_parameters["START"]
                    if keysightE4990A.config_CV(CV_parameters):
                        CV_parameters["hysteresis_mode"] = True
                        voltage_h, capacitance_h, conductance_h = keysightE4990A.measure(CV_parameters)
                        CV_parameters["voltage"] = voltage_h
                        CV_parameters["capacitance"] = capacitance_h
                        CV_parameters["conductance"] = conductance_h
                        CV_parameters["hysteresis"] = True
                    # concatenate lists
                    voltage = np.concatenate((voltage, voltage_h))
                    capacitance = np.concatenate((capacitance, capacitance_h))
                    conductance = np.concatenate((conductance, conductance_h))
                # Turn off bias
                keysightE4990A.turn_off_bias()
                # Plot parameters
                plot_parameters = {
                    "name": "Plot CV",
                    "x": voltage,
                    "y1": capacitance * 1e15,
                    "y2": conductance * 1e9,

                    "titles": {
                        "title": "C-V Measurement at " + str(CV_parameters["FREQ"]) + " kHz" ,
                        "left": "Capacitance",
                        "bottom": "Voltage",
                        "right": "Conductance"
                    },
                    "units": {
                        "left": "fF",
                        "bottom": "V",
                        "right": "nS"
                    },
                    "showgrid": {"x": True, "y": True},
                    "legend": True
                    # "foreground" : "#CCCCCC"

                }
                QApplication.processEvents()
                self.show_graph(plot_parameters)
                namefile = self.getDirs("results") + "/CV_" + self.ui.txtProcess.text() + "_" + str(CV_parameters["FREQ"]) + "kHz_1_1.txt"
                self.save_lists_to_txt(namefile=namefile, var_list=[voltage, capacitance, conductance],
                                       headers=["V", "C", "G"], separation=",")
                QApplication.processEvents()


except:
    message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<", "").replace(">", "") + " occurred. " + str(
        sys.exc_info()[1])
    self.updateTextDescription(message, "ERROR")
    retval = messageBox(self, "ERROR", message, "critical")

    # print("ERROR: " + "Oops! " + str(sys.exc_info()[0]) + " occurred. " + str(sys.exc_info()[1]))




