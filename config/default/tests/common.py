"""
Common functions for test files
"""
import os
import numpy as np

def build_results_folder(username, process, lot, wafer):
    """
    Build standard results folder path
    
    Args:
        username: username string
        process: process name from main.ui.txtProcess.text()
        lot: lot name from main.ui.txtLot.text()
        wafer: wafer number from main.ui.txtWafer.text()
    
    Returns:
        folder path string
    """
    return os.getcwd() + "/results/" + username + "/" + process + "/" + lot + "_W" + f"{int(wafer):02d}" + "/"


def get_output_separator(separator_str):
    """
    Convert separator string to character
    :param separator_str: "space", "tab", or "comma" (default)
    :return: separator character
    """
    if separator_str == "space":
        return " "
    elif separator_str == "tab":
        return "\t"
    else:
        return ","


def save_results_to_file(results_data, variables_list, test_parameters, die, module, folder_func):
    """
    Save measurement results to a columnated text file
    
    :param results_data: list of data rows (list of lists) or single list
    :param variables_list: list of variable names for header
    :param test_parameters: dict with keys: separator, prefix, suffix
    :param die: die number
    :param module: module number
    :param folder_func: function that returns folder path string
    :return: filepath of saved file
    """
    separator = get_output_separator(test_parameters.get("SEPARATOR", test_parameters.get("separator", "comma")))
    prefix = test_parameters.get("PREFIX", test_parameters.get("prefix", ""))
    suffix = test_parameters.get("SUFFIX", test_parameters.get("suffix", ""))
    variables = test_parameters.get("VARIABLES", test_parameters.get("variables", ""))

    die = int(die)
    module = int(module)
    
    folder = folder_func()
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
        if variables_list:
            header_line = separator.join(variables_list)
            f.write(header_line + "\n")
        
        if results_data and hasattr(results_data, '__len__') and len(results_data) > 0:
            if hasattr(results_data[0], '__len__'):
                for row in results_data:
                    row_str = separator.join([str(v) for v in row])
                    f.write(row_str + "\n")
            else:
                row_str = separator.join([str(v) for v in results_data])
                f.write(row_str + "\n")
    
    return filepath


def get_plot_parameters(results_data, variables_list, plot_config):
    """
    Get dict for plot parameters
    :param results_data: numpy array or dictionary of lists with measurement data
    :param variables_list: list of variable names
    :param plot_config: dictionary with plot configuration from TOML
    :return: plot_parameters dict
    """
    plot_data = {}
    for var_name in variables_list:
        if hasattr(results_data, 'dtype') and var_name in results_data.dtype.names:
            plot_data[var_name] = list(results_data[var_name])
        elif isinstance(results_data, dict) and var_name in results_data:
            plot_data[var_name] = list(results_data[var_name])
        elif hasattr(results_data, '__getitem__') and len(results_data) > 0:
            idx = variables_list.index(var_name) if var_name in variables_list else 0
            if idx < len(results_data):
                # Try to handle it if it's a list of rows
                if isinstance(results_data[0], (list, tuple)):
                    plot_data[var_name] = [row[idx] for row in results_data]
                else:
                    plot_data[var_name] = [float(x) for x in results_data]

    x_var = plot_config.get("X_VARIABLE", variables_list[0] if len(variables_list) > 0 else None)
    y1_var = plot_config.get("Y1_VARIABLE", variables_list[1] if len(variables_list) > 1 else None)
    y2_var = plot_config.get("Y2_VARIABLE", variables_list[2] if len(variables_list) > 2 else None)

    x_data = plot_data.get(x_var, []) if x_var else []
    y1_data = plot_data.get(y1_var, []) if y1_var else []
    y2_data = plot_data.get(y2_var, []) if y2_var else []

    plot_parameters = {
        "name": plot_config.get("NAME", "Measurement"),
        "x": x_data,
        "y1": y1_data,
        "y2": y2_data,
        "contact_height": "",
        "variables": [{
            "params": [],
            "data": [{"name": var, "values": plot_data.get(var, []), "units": ""} for var in variables_list]
        }],
        "titles": {
            "title": plot_config.get("TITLE", "Measurement"),
            "left": plot_config.get("LEFT_LABEL", "Y1"),
            "bottom": plot_config.get("BOTTOM_LABEL", "X"),
            "right": plot_config.get("RIGHT_LABEL", "Y2")
        },
        "units": {
            "left": plot_config.get("LEFT_UNITS", ""),
            "bottom": plot_config.get("BOTTOM_UNITS", ""),
            "right": plot_config.get("RIGHT_UNITS", "")
        },
        "showgrid": {"x": plot_config.get("SHOW_GRID", False), "y": plot_config.get("SHOW_GRID", False), "y1": plot_config.get("SHOW_GRID", False)},
        "legend": plot_config.get("LEGEND", True)
    }

    step_var = plot_config.get("STEP_VARIABLE")
    sweep_var = plot_config.get("X_VARIABLE")
    measure_var = plot_config.get("Y1_VARIABLE")

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
                    "label": f"{plot_config.get('STEP_LABEL', step_var)} = {val:.4g}{plot_config.get('STEP_UNITS', '')}"
                })
            plot_parameters["series"] = series

    return plot_parameters