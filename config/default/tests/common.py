"""
Common functions for test files
"""
import os


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
    separator = get_output_separator(test_parameters.get("separator", "comma"))
    prefix = test_parameters.get("prefix", "")
    suffix = test_parameters.get("suffix", "")
    variables = test_parameters.get("variables", "")

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