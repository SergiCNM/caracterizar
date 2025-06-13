import sys
import os
import time
import pandas as pd

global contact_test, contact_errors, test_status, actual_height
global dieActual, moduleActual
global connDeep

""" 
    Agregar el path donde estara el script de DeepDetection
    En este caso = c:/user\ssanchez\Desktop\DeepDetection_script
"""
deep_detection_script_path = os.path.join(os.path.expanduser('~'), "Desktop", "DeepDetection_script")
sys.path.append(deep_detection_script_path)
"""
    main_JD_JM para realizar el chip test 
    connection para hacer la conexion con la camara 
"""
from main_JD_JM import chip_test
from check_programming import chip_test_programming
from only_one_acquisition import chip_test_adquisition
from photonai_probe_board.DD_Lib.MainAccesslib.comm_accesspoint import Connection
from programming_acq import chip_test_acp_program

if self.IsCartographyMeasurement():
    column_row = self.waferwindow.wafer_parameters["wafer_positions"]
    column = column_row[int(dieActual)-1].split()[0]
    row = column_row[int(dieActual)-1].split()[1]
    wafer_pos = self.ui.txtProcess.text()

    if str(dieActual) == "1" and str(moduleActual) == "1":
        connDeep = Connection()
else:

    row = 1
    column = 5
    wafer_pos = self.ui.txtProcess.text()
    dieActual = 1

    #connDeep = Connection()

with Connection() as connDeep:
    """
    error = chip_test(row=row, column=column,
                             wafer_pos=wafer_pos,
                             data_folder_path="", bridge=connDeep)
    """
    #error = chip_test_programming(data_folder_path="", bridge=connDeep)

    #error = chip_test_adquisition( bridge=connDeep)
    """"""
    error = chip_test_acp_program(row=row, column=column,
                             wafer_pos=wafer_pos,
                             data_folder_path="", bridge=connDeep)
    error_txt = str(error)
    message = ""
    meas_status = "meas_success"

    if error_txt == "2":
        message = "Impossible to program chip register and pixel register"
        meas_status = "meas_warning"
    elif error_txt == "4":
        message = "DAC test fail."
        meas_status = "meas_warning"
    elif error_txt == "7":
        message = "DISC-IFEED test fail."
        meas_status = "meas_warning"

    else:
        print("\nChip " + str(dieActual) + " test correct!")

    if self.IsCartographyMeasurement():
        self.waferwindow.meas_result[int(dieActual)-1][int(moduleActual)-1] = {
            "status" : meas_status,
            "message" : message,
            "contact_height" : str(actual_height),
            "variables" : {
                "params" : [{"name" : "status", "value" : meas_status},{"name" : "message", "value" : message}],
                "data" : []
            },
            #"variables" : [{"name" : "cmax(pF)", "value" : 420.056},{"name" : "cmin(pF)", "value" : 210.057}],
            "plot_parameters" : ""

        }


