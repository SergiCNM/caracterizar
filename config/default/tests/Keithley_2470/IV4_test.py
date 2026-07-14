# Test IV in Keithley 2470 instrument
import os.path
import sys
from config.default.instruments import Keithley_2470
from config.default.devices import *
from config.default.tests.common import save_results_to_file, build_results_folder, get_plot_parameters
from config.functions import *
from PySide6.QtWidgets import QMessageBox
import toml, time

global test_status, measurement_status
global dieActual, moduleActual
global IV_parameters
global base_dir, tests_dir, results_dir, username, cartographic_measurement


def load_IV_parameters():
    """
    Load parameters from toml file or default
    :return: None
    """
    global IV_parameters

    import json
    # default values
    IV_parameters = {
        "START": 1,
        "STOP": -1,
        "STEP": 0.1,
        "COMPLIANCE": 0.1,
        "HYSTERESIS": False,
        "WAIT_TIME": 0,
        "LIGHT": False,
        "LIGHT_TIME": 1,
        "RANGE": "AUTO",
        "ROUTE_TERM": "REAR",
        "MEAS_SOURCE": "VOLT",
        "MEAS_SENSE": "CURR",
        "SOURCE_DELAY": 1.0,
        "COUNTS": 3,
        "RES_MIN": 100.0,
        "RES_MAX": 120.0
    }
    # load from external toml file in tests_dir (if exists, if not default values)
    filename_config = os.getcwd() + base_dir + tests_dir + '/Keithley_2470/IV4.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        IV_parameters = toml_info["parameters"]
        if "output" in toml_info:
            IV_parameters["output"] = toml_info["output"]
        if "plot" in toml_info:
            IV_parameters["plot"] = toml_info["plot"]

def save_file(main, voltage, current, resistance, namefile):
    """
    Save file using common.save_results_to_file
    """
    global dieActual, moduleActual
    
    results_data = list(zip(voltage, current, resistance))
    variables_list = ["V", "I", "R"]
    output_params = IV_parameters.get("output", {"separator": "comma", "prefix": "IV4", "suffix": ""})
    
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

def measure_IV(IV_parameters, k2470):
    # create empty list if not exists
    voltage, current, resistance = [], [], []
    if IV_parameters["WAIT_TIME"] > 0:
        # put start voltage in keithley 2470
        k2470.set_voltage(IV_parameters["START"])
        # output voltage ON
        k2470.output("ON")
        time.sleep(IV_parameters["WAIT_TIME"])
    if IV_parameters["LIGHT"]:
        # prober is not initialized when you select single measurement
        main.init_prober()
        if main.prober != "":
            main.prober.light("1")
            time.sleep(IV_parameters["LIGHT_TIME"])
            main.prober.light("0")

    # measure
    if k2470.config_IV4(IV_parameters):
        voltage, current = k2470.measure_normal_IV(IV_parameters)
    # convert current to float
    current_float = list(map(float, current))
    # get resistance
    for i in range(0, len(current_float)):
        if current_float[i] != 0:
            resistance.append(float(voltage[i]) / current_float[i])
        else:
            resistance.append(0)
    return [voltage, current_float, resistance]


# Removed local get_plot_parameters


if __name__ == "__main__":
    try:
        # init IV_parameters
        load_IV_parameters()
        k2470 = Keithley_2470(instruments["Keithley_2470"])
        if cartographic_measurement:
            if str(dieActual)=="1" and str(moduleActual) == "1":
                retval = message_user(main, "Init instrument for IV 4 wire!",
                                      "Please, configure instrument for initialization",
                                      "yes_cancel")
                if retval == QMessageBox.Yes:
                    test_status.status = "STARTED"
                else:
                    test_status.status = "ABORTED"

            if test_status.status == "STARTED":
                # measure IV
                time.sleep(1)
                voltage, current, resistance = measure_IV(IV_parameters, k2470)

                # error in measurement if error counts >0
                meas_status = "meas_error"
                message = "Some error in measurement!"
                voltage_end = float(voltage[len(voltage) - 1])
                current_end = float(current[len(current)-1])
                if float(IV_parameters["STOP"]) == voltage_end:
                    meas_status = "meas_success" # if reach the stop voltage
                    message = f"Current at {voltage_end} V : {current_end} A"
                else:
                    if k2470.get_error_count() == 0:
                        meas_status = "meas_warning"  # if not reach the stop voltage
                        message = f"Current at {voltage_end} V : {current_end} A"
                # get average of resistance, strip first and last 2 points
                if len(resistance) > 4:
                    resistance_avg = sum(resistance[2:-2]) / (len(resistance) - 4)
                else:
                    resistance_avg = sum(resistance) / len(resistance)

                if meas_status == "meas_success":
                    if resistance_avg < IV_parameters["RES_MIN"] or resistance_avg > IV_parameters["RES_MAX"]:
                        meas_status = "meas_warning"
                        message = f"R_avg ({resistance_avg:.4e} Ohms) out of limits)"
                # show results resistance average in description
                main.updateTextDescription(f"R_avg: {resistance_avg:.4e} Ohm", "RESULT")
                # get plot parameters
                results_data_dict = {"V": voltage, "I": current, "R": resistance}
                plot_parameters = get_plot_parameters(results_data_dict, ["V", "I", "R"], IV_parameters.get("plot", {}))
                # save results
                main.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1] = {
                    "status": meas_status,
                    "message": message,
                    "contact_height": "",
                    "variables": [{
                        "params": [{"name": "pass", "value": str(meas_status)},
                                   {"name": "R_avg", "value": str(resistance_avg)}],
                        "data": [{"name": "V", "values": voltage, "units": "V"},
                                 {"name": "I", "values": current, "units": "A"},
                                 {"name": "R", "values": resistance, "units": "Ohm"}
                                 ]
                    }],
                    "plot_parameters": plot_parameters

                }

                namefile = f"IV4_{main.ui.txtLot.text()}_W" + f"{int(main.ui.txtWafer.text()):02d}_{str(dieActual)}_{str(moduleActual)}"
                save_file(main, voltage, current, resistance, namefile)
        else:
            # single measure
            if k2470.config_IV(IV_parameters):
                voltage, current, resistance = measure_IV(IV_parameters, k2470)
                # get average of resistance, strip first and last 2 points
                if len(resistance) > 4:
                    resistance_avg = sum(resistance[2:-2]) / (len(resistance) - 4)
                else:
                    resistance_avg = sum(resistance) / len(resistance)

                # show results resistance average in description
                main.updateTextDescription(f"R_avg: {resistance_avg:.4e} Ohm", "RESULT")
                # self.updateTextDescription(txt_result)
                results_data_dict = {"V": voltage, "I": current, "R": resistance}
                plot_parameters = get_plot_parameters(results_data_dict, ["V", "I", "R"], IV_parameters.get("plot", {}))
                # Single measurement, view plot
                if IV_parameters.get("plot", {}).get("SHOW_PLOT", True):
                    emit_plot(plot_parameters)
                # Save file in results
                namefile = f"IV4_{main.ui.txtLot.text()}_W{int(main.ui.txtWafer.text()):02d}_single"
                save_file(main, voltage, current, resistance, namefile)

        # stop process, put instrument in local mode
        k2470.stop()
        k2470.close()

    except:
        message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<", "").replace(">", "") + " occurred. " + str(
            sys.exc_info()[1])
        main.updateTextDescription(message, "ERROR")
        message_user(main, "ERROR", message, "ok_error")

