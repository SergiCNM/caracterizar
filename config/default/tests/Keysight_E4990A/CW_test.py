# Test CV in Keysight E4990 instrument

import os.path
import sys
import numpy as np
from config.functions import *
import toml

global test_status, measurement_status
global dieActual, moduleActual

global CW_parameters


def load_CW_parameters():
    global CW_parameters

    import json
    # default values
    CW_parameters = {
        "START": 0,
        "STOP": 40,
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
    }
    # load from external toml file in tests_dir (if exists, if not default values)
    filename_config = os.getcwd() + base_dir + tests_dir + '/Keysight_E4990A/CW.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        CW_parameters = toml_info["parameters"]


try:

    keysightE4990A = Keysight_E4990A(instruments["Keysight_E4990A"])
    # measure CV
    # send CW_parameters to CONFIG HP4192A
    # default parameters

    if cartographic_measurement:
        if str(dieActual) == "1" and str(moduleActual) == "1":
            retval = QMessageBox.question(
                self,
                "Init instrument for CW!",
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
            # init CW_parameters
            load_CW_parameters()
            freq = []
            capacitance = []
            conductance = []
            freq_h = []
            capacitance_h = []
            conductance_h = []
            if keysightE4990A.config_CW(CW_parameters):
                if CW_parameters["WAIT_TIME"] > 0:
                    time.sleep(CW_parameters["WAIT_TIME"])

                if CW_parameters["LIGHT"] and CW_parameters["LIGHT_TIME"] > 0:
                    self.prober.light("1")
                    time.sleep(CW_parameters["LIGHT_TIME"])
                    self.prober.light("0")

                CW_parameters["hysteresis_mode"] = False
                freq, capacitance, conductance = keysightE4990A.measure(CW_parameters)
                CW_parameters["freq"] = freq
                CW_parameters["capacitance"] = capacitance
                CW_parameters["conductance"] = conductance
                CW_parameters["hysteresis"] = False

                # hysteresis?
                if CW_parameters["HYSTERESIS"]:
                    # wait time between hysteresis
                    if CW_parameters["HYSTERESIS_TIME"] > 0:
                        time.sleep(CW_parameters["HYSTERESIS_TIME"])
                    # swap variables
                    CW_parameters["START"], CW_parameters["STOP"] = CW_parameters["STOP"], CW_parameters["START"]
                    if keysightE4990A.config_CV(CW_parameters):
                        CW_parameters["hysteresis_mode"] = True
                        freq_h, capacitance_h, conductance_h = keysightE4990A.measure(CW_parameters)
                        CW_parameters["freq"] = freq_h
                        CW_parameters["capacitance"] = capacitance_h
                        CW_parameters["conductance"] = conductance_h
                        CW_parameters["hysteresis"] = True
                    # concatenate lists
                    freq = np.concatenate((freq, freq_h))
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
                    "data": [{"name": "W", "values": freq, "units": "Hz"},
                             {"name": "C", "values": capacitance * 1e12, "units": "pF"},
                             {"name": "G", "values": conductance * 1E6, "units": "uS"}]
                },
                "plot_parameters": {
                    "name": "Plot CW Die " + str(dieActual) + " Module " + str(moduleActual),
                    "x": freq,
                    "y1": capacitance * 1e12,
                    "y2": conductance * 1e6,

                    "titles": {
                        "title": "C-W Measurement" + str(dieActual) + " Module " + str(moduleActual),
                        "left": "Capacitance",
                        "bottom": "Frequency",
                        "right": "Conductance"
                    },
                    "units": {
                        "left": "pF",
                        "bottom": "Hz",
                        "right": "uS"
                    },
                    "showgrid": {"x": True, "y": True},

                    "legend": False

                }

            }
            plot_parameters = self.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1]["plot_parameters"]
            self.show_graph(plot_parameters)
            namefile = self.getDirs("results") + "/CW_" + self.ui.txtProcess.text() + "_" + str(dieActual) + "_" + str(
                moduleActual) + ".txt"
            self.save_lists_to_txt(namefile=namefile, var_list=[freq, capacitance, conductance],
                                   headers=["F", "C", "G"], separation=",")
    else:
        # init CW_parameters
        load_CW_parameters()
        freq = []
        capacitance = []
        conductance = []
        freq_h = []
        capacitance_h = []
        conductance_h = []
        # single measure
        if keysightE4990A.config_CW(CW_parameters):
            if CW_parameters["WAIT_TIME"] > 0:
                time.sleep(CW_parameters["WAIT_TIME"])
            if CW_parameters["LIGHT"]:
                # prober is not initialized when you select single measurement
                self.init_prober()
                if self.prober != "":
                    self.prober.light("1")
                    time.sleep(CW_parameters["LIGHT_TIME"])
                    self.prober.light("0")

            # measure
            CW_parameters["hysteresis_mode"] = False
            freq, capacitance, conductance = keysightE4990A.measure(CW_parameters)
            CW_parameters["freq"] = freq
            CW_parameters["capacitance"] = capacitance
            CW_parameters["conductance"] = conductance
            CW_parameters["hysteresis"] = False
            # hysteresis?
            if CW_parameters["HYSTERESIS"]:
                # wait time between hysteresis
                if CW_parameters["HYSTERESIS_TIME"] > 0:
                    time.sleep(CW_parameters["HYSTERESIS_TIME"])
                # swap variables
                CW_parameters["START"], CW_parameters["STOP"] = CW_parameters["STOP"], CW_parameters["START"]
                if keysightE4990A.config_CV(CW_parameters):
                    CW_parameters["hysteresis_mode"] = True
                    freq_h, capacitance_h, conductance_h = keysightE4990A.measure(CW_parameters)
                    CW_parameters["freq"] = freq_h
                    CW_parameters["capacitance"] = capacitance_h
                    CW_parameters["conductance"] = conductance_h
                    CW_parameters["hysteresis"] = True
                # concatenate lists
                freq = np.concatenate((freq, freq_h))
                capacitance = np.concatenate((capacitance, capacitance_h))
                conductance = np.concatenate((conductance, conductance_h))
            # Turn off bias
            keysightE4990A.turn_off_bias()
            # Plot parameters
            plot_parameters = {
                "name": "Plot CW",
                "x": freq,
                "y1": capacitance * 1e12,
                "y2": conductance * 1e6,

                "titles": {
                    "title": "C-W Measurement",
                    "left": "Capacitance",
                    "bottom": "Frequency",
                    "right": "Conductance"
                },
                "units": {
                    "left": "pF",
                    "bottom": "Hz",
                    "right": "uS"
                },
                "showgrid": {"x": True, "y": True},
                "legend": True
                # "foreground" : "#CCCCCC"

            }

            self.show_graph(plot_parameters)
            namefile = self.getDirs("results") + "/CW_" + self.ui.txtProcess.text() + "_1_1.txt"
            self.save_lists_to_txt(namefile=namefile, var_list=[freq, capacitance, conductance],
                                   headers=["F", "C", "G"], separation=",")

    # stop process
    # keysightE4990A.stop()

    # keysightE4990A.local()




except:
    message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<", "").replace(">", "") + " occurred. " + str(
        sys.exc_info()[1])
    self.updateTextDescription(message, "ERROR")
    retval = messageBox(self, "ERROR", message, "critical")

    # print("ERROR: " + "Oops! " + str(sys.exc_info()[0]) + " occurred. " + str(sys.exc_info()[1]))

