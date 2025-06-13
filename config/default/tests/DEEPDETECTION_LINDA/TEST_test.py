# LINDA TEST
#global kbridge, commbridge
global contact_test, contact_errors, test_status, actual_height
global dieActual, moduleActual

import os

from PBaccesslib.main import chip_test
from PBaccesslib.keithley_bridge import KBridge
from PBaccesslib.comm_bridge import CommBridge

#DATA_FOLDER_PATH = "/Users/User/Desktop/data"
# LIBPATH = "/Users/User/Desktop/linda-lib.dll"
DATA_FOLDER_PATH = "/2home/rsiam/github/caracterizar/results/16bitsW123"
LIBPATH = "/2home/rsiam/github/IFAEControl/deepdetection_comm_lib/build/lib/liblinda-lib.so"

""" Start bridge and instrument"""
#IP_commbridge = "192.168.0.101"
#IP_kbridge = "192.168.0.170"
IP_commbridge = "172.16.17.103"
IP_kbridge = "172.16.17.105"

SYNC = 32000
ASYNC = 32001
KEITHLEY_ADRESS = "TCPIP0::"+IP_kbridge+"::inst0::INSTR"

kbridge = KBridge(KEITHLEY_ADRESS)
commbridge = CommBridge(IP_commbridge, SYNC, ASYNC, LIBPATH)


if str(dieActual)=="1" and str(moduleActual)=="1":

    kbridge.clear_inst()
    kbridge.set_values(100e-3, 100e-3, 20, 2.5) # a_l, b_l, rnge, level
    contact_errors = 0
    kbridge.set_2v5_on()


column_row = self.waferwindow.wafer_parameters["wafer_positions"]


column = column_row[int(dieActual)-1].split()[0]
row = column_row[int(dieActual)-1].split()[1]
wafer_pos = self.ui.txtProcess.text()

error = chip_test(row,column,wafer_pos,DATA_FOLDER_PATH,commbridge.return_bridge(),kbridge.return_instrument())
error_txt = str(error)
message = ""

if error_txt == "1":
    message = "Can´t download chip_reg/pixel reg files. Check path."
    meas_status = "meas_error"
elif error_txt == "2":
    message = "Wafer test fail. Touchdown or tension/current fail."
    meas_status = "meas_warning"
elif error_txt == "3":
    message = "Impossible to program chip register and pixel register."
    meas_status = "meas_warning"
elif error_txt == "4":
    message = "Dac test fail."
    meas_status = "meas_warning"
elif error_txt == "5":
    message = "DISC test fail."
    meas_status = "meas_warning"
elif error_txt == "6":
    message = "IFEED test fail."
    meas_status = "meas_warning"
else:
    print("Chip " + str(dieActual) + " test correct!")


kbridge.set_2v5_off()
kbridge.close_connection()
commbridge.kill_hearbeat()
commbridge.close_connection()

if contact_test==1:
    meas_status = "meas_warning"
    message = "Only one needle in contact"

if contact_test==2:
    if message=="":
       meas_status = "meas_success"
    else:
       #meas_status = "meas_error"
       message = "Contact OK! " + message

if contact_test==3:
    meas_status = "meas_error"
    message = "Not in contact! Abort measurement!"


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

