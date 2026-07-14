# Test CW in Keithley 4200 instrument

import os.path
import sys
from PySide6.QtWidgets import QMessageBox

from config.default.instruments import Keithley_4200
from config.default.tests.common import save_results_to_file, build_results_folder, get_plot_parameters
from config.functions import *
import toml
global test_status, measurement_status
global dieActual, moduleActual
global CW_parameters
global base_dir, tests_dir, results_dir, username, cartographic_measurement


def load_CW_parameters():
    global CW_parameters

    # default values
    CW_parameters = {
        "START_FREQ": 1e3,
        "STOP_FREQ": 1e6,
        "POINTS": 50,
        "VOLTAGE": 0.5,
        "OSC": 30,
        "CIRCUIT_MODE": "Parallel",
        "WAIT_TIME": 1,
        "LIGHT": False,
        "LIGHT_TIME": 1
    }

    filename_config = os.getcwd() + base_dir + tests_dir + '/Keithley_4200/CW.toml'
    if os.path.exists(filename_config):
        toml_info = toml.load(filename_config)
        CW_parameters = toml_info["parameters"]
        if "output" in toml_info:
            CW_parameters["output"] = toml_info["output"]
        if "plot" in toml_info:
            CW_parameters["plot"] = toml_info["plot"]
    else:
        print(f"File toml {filename_config} doesn't exist!")

try:

    k4200 = Keithley_4200(instruments["Keithley_4200"])
    timeout = int(instruments["Keithley_4200"].get("timeout", 20000))  # 20 seconds default

    # init CV_parameters
    load_CW_parameters()
    # Parallel mode: Cp = C, Gp = G
    x_text = "Frequency"
    y_text_left = "Capacitance (Cp)" if CW_parameters["CIRCUIT_MODE"].lower() == "parallel" else "Capacitance (Cs)"
    y_text_right = "Conductance (Gp)" if CW_parameters["CIRCUIT_MODE"].lower() == "parallel" else "Resistance (Rs)"

    if cartographic_measurement:
        if str(dieActual) == "1" and str(moduleActual) == "1":
            retval = message_user(main, "Init instrument for CW!", "Please, configure instrument for initialization", "yes_cancel")
            if retval == QMessageBox.Yes:
                k4200.reset()
                test_status.status = "STARTED"
            else:
                test_status.status = "ABORTED"

        if test_status.status == "STARTED":
            if k4200.config_CW(CW_parameters):
                if CW_parameters["WAIT_TIME"] > 0:
                    time.sleep(CW_parameters["WAIT_TIME"])
                if CW_parameters["LIGHT"] and CW_parameters["LIGHT_TIME"] > 0:
                    main.prober.light("1")
                    time.sleep(CW_parameters["LIGHT_TIME"])
                    main.prober.light("0")

                freq, capacitance, conductance = k4200.measure_CW(CW_parameters, timeout)

                # Save and plot
                meas_status = "meas_success"
                    plot_config = CW_parameters.get("plot", {})
                    plot_config["LEFT_LABEL"] = y_text_left
                    plot_config["RIGHT_LABEL"] = y_text_right
                    plot_config["RIGHT_UNITS"] = "S" if CW_parameters.get("CIRCUIT_MODE", "").lower() == "parallel" else "Ohm"
                    
                    results_data_dict = {"f": freq, "C": capacitance, "G": conductance}
                    plot_parameters = get_plot_parameters(results_data_dict, ["f", "C", "G"], plot_config)
                    
                    main.waferwindow.meas_result[int(dieActual)-1][int(moduleActual)-1] = {
                        "status": meas_status,
                        "message": "",
                        "contact_height": "",
                        "variables": {
                            "params": [],
                            "data": [
                                {"name": "f", "values": freq, "units": "Hz"},
                                {"name": "C", "values": capacitance, "units": "F"},
                                {"name": "G", "values": conductance, "units": "S"}
                            ]
                        },
                        "plot_parameters": plot_parameters
                    }

                    if plot_config.get("SHOW_PLOT", True):
                        emit_plot(plot_parameters)
                
                results_data = list(zip(freq, capacitance, conductance))
                variables_list = ["f", "C", "G"]
                output_params = CW_parameters.get("output", {"separator": "comma", "prefix": "CW", "suffix": ""})
                
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
        if k4200.config_CW(CW_parameters):
            if CW_parameters["WAIT_TIME"] > 0:
                time.sleep(CW_parameters["WAIT_TIME"])
            if CW_parameters["LIGHT"]:
                main.init_prober()
                if main.prober != "":
                    main.prober.light("1")
                    time.sleep(CW_parameters["LIGHT_TIME"])
                    main.prober.light("0")

            freq, capacitance, conductance = k4200.measure_CW(CW_parameters, timeout)

            plot_config = CW_parameters.get("plot", {})
            plot_config["LEFT_LABEL"] = y_text_left
            plot_config["RIGHT_LABEL"] = y_text_right
            plot_config["RIGHT_UNITS"] = "S" if CW_parameters.get("CIRCUIT_MODE", "").lower() == "parallel" else "Ohm"
            
            results_data_dict = {"f": freq, "C": capacitance, "G": conductance}
            plot_parameters = get_plot_parameters(results_data_dict, ["f", "C", "G"], plot_config)

            if plot_config.get("SHOW_PLOT", True):
                emit_plot(plot_parameters)

            results_data = list(zip(freq, capacitance, conductance))
            variables_list = ["f", "C", "G"]
            output_params = CW_parameters.get("output", {"separator": "comma", "prefix": "CW", "suffix": "single"})
            
            save_results_to_file(
                results_data=results_data,
                variables_list=variables_list,
                test_parameters=output_params,
                die=1,
                module=1,
                folder_func=lambda: build_results_folder(
                    username=username,
                    process=main.ui.txtProcess.text(),
                    lot=main.ui.txtLot.text(),
                    wafer=main.ui.txtWafer.text()
                )
            )

except:
    message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<", "").replace(">", "") + " occurred. " + str(sys.exc_info()[1])
    main.updateTextDescription(message, "ERROR")
    message_user(main, "ERROR", message, "ok_error")