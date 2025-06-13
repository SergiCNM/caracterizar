# Test IV in Keithley 2470 instrument
import os.path
import sys
from config.default.instruments import Keithley_2470
from config.default.devices import *
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
        "HYSTERESIS_TIME": 0,
        "WAIT_TIME": 0,
        "LIGHT": False,
        "LIGHT_TIME": 1,
        "RANGE": "AUTO",
        "ROUTE_TERM": "REAR"
    }
    # load from external toml file in tests_dir (if exists, if not default values)
    filename_config = os.getcwd() + base_dir + tests_dir + '/Keithley_2470/IV.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        IV_parameters = toml_info["parameters"]

def save_file(main, voltage, current, namefile):
    """
    Save file
    :param main: main program
    :param voltage: voltage list
    :param current:
    :param namefile:
    :return: None
    """
    global dieActual, moduleActual
    separation_char = ","
    lines = ["V" + separation_char + "I"]
    for i in range(0,len(voltage)):
        lines.append(str(voltage[i]) + separation_char + str(current[i]))
    # create folder
    folder = os.path.join(os.getcwd(), results_dir, username, main.ui.txtProcess.text())
    namefile = os.path.join(folder, namefile + ".txt").replace("\\", "/")
    f = open(namefile, "w+")
    s1 = '\n'.join(lines)
    f.write(s1)
    f.close()

def measure_IV(IV_parameters, k2470):
    # create empty list if not exists
    voltage = []
    current = []
    if IV_parameters["WAIT_TIME"] > 0:
        time.sleep(IV_parameters["WAIT_TIME"])
    if IV_parameters["LIGHT"]:
        # prober is not initialized when you select single measurement
        main.init_prober()
        if main.prober != "":
            main.prober.light("1")
            time.sleep(IV_parameters["LIGHT_TIME"])
            main.prober.light("0")

    # measure
    if k2470.config_IV(IV_parameters):
        print("keithley configured")
        voltage, current = k2470.measure_list_IV(IV_parameters)
    # hysteresis?
    if IV_parameters["HYSTERESIS"]:
        voltage_h = []
        current_h = []
        # wait time between hysteresis
        if IV_parameters["HYSTERESIS_TIME"] > 0:
            time.sleep(IV_parameters["HYSTERESIS_TIME"])
        # swap variables
        IV_parameters["START"], IV_parameters["STOP"] = IV_parameters["STOP"], IV_parameters["START"]
        if k2470.config_IV(IV_parameters):
            voltage_h, current_h = k2470.measure_list_IV(IV_parameters)
        # union lists
        voltage = voltage + voltage_h
        current = current + current_h

    current_float = list(map(float, current))
    return [voltage, current_float]


def get_plot_parameters(voltage, current):
    """
    Get dict for plot parameters
    :param voltage: voltage list
    :param current: current list
    :return: plot_parameters dict
    """
    plot_parameters = {
        "name": "Plot IV",
        "x": voltage,
        "y1": current,
        "contact_height": "",
        "variables": [{
            "params": [],
            "data": [{"name": "V", "values": voltage, "units": "V"},
                     {"name": "I", "values": current, "units": "A"}]
        }],
        "titles": {
            "title": "I-V Measurement",
            "left": "Current",
            "bottom": "Voltage"
        },
        "units": {
            "left": "A",
            "bottom": "V"
        },
        "showgrid": {"x": False, "y": False},
        "legend": False
        # "foreground" : "#CCCCCC"

    }
    return plot_parameters


if __name__ == "__main__":
    try:
        k2470 = Keithley_2470(instruments["Keithley_2470"])
        if cartographic_measurement:
            if str(dieActual)=="1" and str(moduleActual) == "1":
                # init IV_parameters
                load_IV_parameters()
                retval = QMessageBox.question(
                    main,
                    "Init instrument for IV!",
                    "Please, configure instrument for initialization",
                    buttons=QMessageBox.Yes | QMessageBox.Cancel ,
                    defaultButton=QMessageBox.Yes,
                )
                if retval == QMessageBox.Yes:
                    if k2470.config_IV(IV_parameters):
                        test_status.status = "STARTED"
                    else:
                        test_status.status = "ABORTED"

                else:
                    test_status.status = "ABORTED"

            if test_status.status == "STARTED":
                # measure IV
                time.sleep(1)
                if k2470.config_IV(IV_parameters):
                    time.sleep(2)
                    voltage, current = measure_IV(IV_parameters, k2470)

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

                plot_parameters = get_plot_parameters(voltage, current)
                # save results
                main.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1] = {
                    "status": meas_status,
                    "message": message,
                    "contact_height": "",
                    "variables": [{
                        "params": [{"name" : "pass", "value" : str(meas_status)}],
                        "data": [{"name": "V", "values": voltage, "units": "V"},
                                 {"name": "I", "values": current, "units": "A"}
                                 ]
                    }],
                    "plot_parameters": plot_parameters

                }

                namefile = f"{main.ui.txtLot.text()}_W" + f"{int(main.ui.txtWafer.text()):02d}_{str(dieActual)}_{str(moduleActual)}"
                save_file(main, voltage, current, namefile)
        else:
            # init IV_parameters
            load_IV_parameters()
            # single measure
            if k2470.config_IV(IV_parameters):
                time.sleep(2)
                voltage, current = measure_IV(IV_parameters, k2470)
                # main.updateTextDescription(txt_result)
                plot_parameters = get_plot_parameters(voltage, current)
                # Single measurement, view plot
                # self.show_graph(plot_parameters)
                emit_plot(plot_parameters)
                # Save file in results
                namefile = f"{main.ui.txtLot.text()}_W{int(main.ui.txtWafer.text()):02d}_0_1"
                save_file(main, voltage,current, namefile)

        # stop process, put instrument in local mode
        # k2470.stop()
        # k2470.local()



    except:
        message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<","").replace(">","") + " occurred. " + str(sys.exc_info()[1])
        main.updateTextDescription(message,"ERROR")
        # retval = messageBox(main,"ERROR",message,"critical")
        message_user(main, "ERROR", message, "ok_error")
        #print("ERROR: " + "Oops! " + str(sys.exc_info()[0]) + " occurred. " + str(sys.exc_info()[1]))


