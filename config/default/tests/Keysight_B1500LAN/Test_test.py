# SOLARMEM test
import os
import sys
import statistics
from datetime import datetime
import time
import toml
import numpy as np
from config.default.instruments import Keysight_B1500LAN
from PySide6.QtWidgets import QMessageBox

global test_status, measurement_status
global dieActual, moduleActual
global base_dir, tests_dir, results_dir, username, cartographic_measurement


global TEST_parameters

B1500 = None


def configure_test(B1500, workspace_name, group, test_preset_group_name):
    """
    Configure B1500 instrument: open workspace, load preset, configure format
    :param B1500: Keysight B1500 instrument instance
    :param workspace_name: workspace name to open
    :param group: group name to open
    :param test_preset_group_name: test preset group name to open
    :return: configured B1500 instrument
    """

    status = B1500.status_workspace()
    if status == "CLOS":
        B1500.open_workspace(workspace_name)
    else:
        if B1500.get_name_workspace().replace('"', '') != workspace_name:
            B1500.close_workspace()
            status = B1500.status_workspace()
            while status != "CLOS":
                status = B1500.status_workspace()
                time.sleep(1)
            B1500.open_workspace(workspace_name)

    status = B1500.status_workspace()

    while status != "OPEN":
        status = B1500.status_workspace()
        time.sleep(1)

    B1500.open_preset_group(group)
    time.sleep(1)
    B1500.open_test_preset_group(test_preset_group_name)
    time.sleep(1)

    B1500.configure_format()

    return B1500


def get_output_separator(separator_str):
    if separator_str == "space":
        return " "
    elif separator_str == "tab":
        return "\t"
    else:
        return ","


def check_existing_files():
    folder = os.getcwd() + "/" + results_dir + "/" + username + "/" + main.ui.txtProcess.text() + "/" + main.ui.txtLot.text() + "_W" + f"{int(main.ui.txtWafer.text()):02d}" + "/"

    if cartographic_measurement:
        if os.path.exists(folder):
            files = os.listdir(folder)
            if files:
                return True, folder
    else:
        die = int(dieActual)
        module = int(moduleActual)
        prefix = TEST_parameters.get("prefix", "")
        suffix = TEST_parameters.get("suffix", "")

        if prefix and suffix:
            filename = f"{prefix}_{die}_{module}_{suffix}.txt"
        elif prefix:
            filename = f"{prefix}_{die}_{module}.txt"
        elif suffix:
            filename = f"{die}_{module}_{suffix}.txt"
        else:
            filename = f"{die}_{module}.txt"

        filepath = os.path.join(folder, filename)
        if os.path.exists(filepath):
            return True, folder

    return False, folder


def save_results_to_file(results_data, variables_list):
    separator = get_output_separator(TEST_parameters.get("separator", "comma"))
    prefix = TEST_parameters.get("prefix", "")
    suffix = TEST_parameters.get("suffix", "")
    die = int(dieActual)
    module = int(moduleActual)

    folder = os.getcwd() + "/" + results_dir + "/" + username + "/" + main.ui.txtProcess.text() + "/" + main.ui.txtLot.text() + "_W" + f"{int(main.ui.txtWafer.text()):02d}" + "/"

    os.makedirs(folder, exist_ok=True)

    if prefix and suffix:
        filename = f"{prefix}_{die}_{module}_{suffix}.txt"
    elif prefix:
        filename = f"{prefix}_{die}_{module}.txt"
    elif suffix:
        filename = f"{die}_{module}_{suffix}.txt"
    else:
        filename = f"{die}_{module}.txt"

    filepath = os.path.join(folder, filename)

    with open(filepath, 'w') as f:
        header_line = separator.join(variables_list)
        f.write(header_line + "\n")

        if hasattr(results_data, '__len__') and len(results_data) > 0:
            if hasattr(results_data[0], '__len__'):
                for row in results_data:
                    row_str = separator.join([str(v) for v in row])
                    f.write(row_str + "\n")
            else:
                row_str = separator.join([str(v) for v in results_data])
                f.write(row_str + "\n")


def get_plot_parameters(results_data, variables_list):
    """
    Get dict for plot parameters
    :param results_data: numpy array with measurement data
    :param variables_list: list of variable names
    :return: plot_parameters dict
    """
    plot_config = TEST_parameters.get("plot", {})

    plot_data = {}
    for var_name in variables_list:
        if hasattr(results_data, 'dtype') and var_name in results_data.dtype.names:
            plot_data[var_name] = list(results_data[var_name])
        elif hasattr(results_data, '__getitem__') and len(results_data) > 0:
            idx = variables_list.index(var_name) if var_name in variables_list else 0
            if idx < len(results_data):
                plot_data[var_name] = [float(x) for x in results_data]

    x_var = plot_config.get("x_variable", variables_list[0] if len(variables_list) > 0 else None)
    y1_var = plot_config.get("y1_variable", variables_list[1] if len(variables_list) > 1 else None)
    y2_var = plot_config.get("y2_variable", variables_list[2] if len(variables_list) > 2 else None)

    x_data = plot_data.get(x_var, []) if x_var else []
    y1_data = plot_data.get(y1_var, []) if y1_var else []
    y2_data = plot_data.get(y2_var, []) if y2_var else []

    plot_parameters = {
        "name": plot_config.get("name", "Measurement"),
        "x": x_data,
        "y1": y1_data,
        "y2": y2_data,
        "contact_height": "",
        "variables": [{
            "params": [],
            "data": [{"name": var, "values": plot_data.get(var, []), "units": ""} for var in variables_list]
        }],
        "titles": {
            "title": plot_config.get("title", "Measurement"),
            "left": plot_config.get("left_label", "Y1"),
            "bottom": plot_config.get("bottom_label", "X"),
            "right": plot_config.get("right_label", "Y2")
        },
        "units": {
            "left": plot_config.get("left_units", ""),
            "bottom": plot_config.get("bottom_units", ""),
            "right": plot_config.get("right_units", "")
        },
        "showgrid": {"x": plot_config.get("show_grid", False), "y": plot_config.get("show_grid", False)},
        "legend": plot_config.get("legend", True)
    }

    step_var = plot_config.get("step_variable")
    sweep_var = plot_config.get("x_variable")
    measure_var = plot_config.get("y1_variable")

    if step_var and sweep_var and measure_var and hasattr(results_data, 'dtype'):
        if step_var in results_data.dtype.names and sweep_var in results_data.dtype.names and measure_var in results_data.dtype.names:
            step_values = results_data[step_var]
            unique_steps = np.unique(step_values)
            series = []
            for val in unique_steps:
                mask = step_values == val
                series.append({
                    "x": list(results_data[sweep_var][mask]),
                    "y": list(results_data[measure_var][mask]),
                    "label": f"{plot_config.get('step_label', step_var)} = {val:.4g}{plot_config.get('step_units', '')}"
                })
            plot_parameters["series"] = series

    return plot_parameters


def test_B1500(B1500):
    status = "meas_success"
    message = ""
    results = ""
    try:
        print("single measure...")
        B1500.single()
        print("measuring & wait opc..")
        opc = B1500.dataready()
        print("data ready, getting data...")
        data = B1500.get_data()
        print("data: ", data)
        variables = B1500.get_vars(data)
        print("variables: ", variables)
        results = B1500.get_data_numpy(data, variables)
        print("results: ", results)

    except Exception as ex:
        status = "meas_error"
        message = "Problem in test (exception): " + str(ex)

    return [status, message, results]


def load_TEST_parameters():
    global TEST_parameters

    TEST_parameters = {
        "WORKSPACE_NAME": "SIAM",
        "GROUP": "SOLARMEMS",
        "TEST_PRESET_GROUP_NAME": "Solarmems",
        "variables": "V1,I1,V2,I2",
        "separator": "comma",
        "prefix": "IV",
        "suffix": "",
        "plot": {
            "name": "IV Measurement",
            "title": "I-V Measurement",
            "x_variable": "V1",
            "y1_variable": "I1",
            "y2_variable": "I2",
            "left_label": "Current",
            "right_label": "Current",
            "bottom_label": "Voltage",
            "left_units": "A",
            "right_units": "A",
            "bottom_units": "V",
            "show_grid": False,
            "legend": True
        }
    }

    filename_config = os.getcwd() + base_dir + tests_dir + '/Keysight_B1500LAN/Test.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        if "parameters" in toml_info:
            TEST_parameters.update(toml_info["parameters"])
        if "output" in toml_info:
            TEST_parameters.update(toml_info["output"])
        if "plot" in toml_info:
            TEST_parameters["plot"] = toml_info["plot"]

print("loading test parameters...")
load_TEST_parameters()
print(TEST_parameters)

B1500 = Keysight_B1500LAN(instruments["Keysight_B1500LAN"])
B1500.instrument.timeout = 20000 # bigger than test

try:
    workspace_name = TEST_parameters["WORKSPACE_NAME"]
    group = TEST_parameters["GROUP"]
    test_preset_group_name = TEST_parameters["TEST_PRESET_GROUP_NAME"]
    variables_config = TEST_parameters.get("variables", "V1,I1,V2,I2").split(",")

    exists, folder = check_existing_files()

    print("Exists: ", exists)

    print(folder)

    if exists:
        if cartographic_measurement:
            init_chip = main.waferwindow.wafer_parameters.get("init_chip", 1)
            is_first = str(dieActual) == str(init_chip) and str(moduleActual) == "1"
        else:
            is_first = True

        if is_first:
            retval = message_user(main, "Warning: Existing Data", "Data already exists in results folder.\nFolder: " + folder + "\nDo you want to continue and overwrite the data?", "yes_cancel")
            if retval == QMessageBox.No or retval == QMessageBox.Cancel:
                status = "meas_cancelled"
                message = "Test cancelled by user - existing data"
                main.updateTextDescription("Test cancelled: " + message)
                sys.exit()

    if cartographic_measurement:
        init_chip = main.waferwindow.wafer_parameters.get("init_chip", 1)

        if str(dieActual) == str(init_chip) and str(moduleActual) == "1":
            retval = message_user(main, "Init Keysight B1500 for measurement!", "Please, configure instrument for initialization", "yes_cancel")
            print("retval", retval)
            if retval == QMessageBox.Yes:
                configure_test(B1500, workspace_name, group, test_preset_group_name)
                test_status.status = "STARTED"
            else:
                test_status.status = "ABORTED"

        if test_status.status == "STARTED":
            test_result = test_B1500(B1500)
            status = test_result[0]
            message = test_result[1]
            results_data = test_result[2]

            plot_parameters = {}
            if status == "meas_success" and results_data is not None:
                save_results_to_file(results_data, variables_config)
                plot_parameters = get_plot_parameters(results_data, variables_config)

            main.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1] = {
                "status": status,
                "message": message,
                "contact_height": "",
                "variables": plot_parameters.get("variables", []),
                "plot_parameters": plot_parameters
            }

            if status == "meas_success":
                main.updateTextDescription("Test completed successfully")
            elif status == "meas_error":
                main.updateTextDescription("Test error: " + message)
            else:
                main.updateTextDescription("Test status: " + status + " - " + message)
        else:
            main.updateTextDescription("Test aborted or cancelled")
    else:
        dieActual = "1"
        moduleActual = "1"
        print("Configure test...")
        configure_test(B1500, workspace_name, group, test_preset_group_name)
        print("Test configured...")

        test_result = test_B1500(B1500)
        print("Result: ", test_result)
        status = test_result[0]
        message = test_result[1]
        results_data = test_result[2]

        plot_parameters = {}
        if status == "meas_success" and results_data is not None:
            save_results_to_file(results_data, variables_config)
            plot_parameters = get_plot_parameters(results_data, variables_config)

        
        if status == "meas_success":
            main.updateTextDescription("Test completed successfully")
            emit_plot(plot_parameters)
        elif status == "meas_error":
            main.updateTextDescription("Test error: " + message)
        else:
            main.updateTextDescription("Test status: " + status + " - " + message)

except:
    error_message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<", "").replace(">", "") + " occurred. " + str(sys.exc_info()[1])
    main.updateTextDescription(error_message, "ERROR")
    # retval = message_user(main, "ERROR", error_message, "ok")