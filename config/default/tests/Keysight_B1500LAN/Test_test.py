# SOLARMEM test
import os
import sys
import statistics
from datetime import datetime
import time

global test_status, measurement_status
global dieActual, moduleActual
global posx, posy

global TEST_parameters


def test_B1500(B1500):
    status = "meas_success"
    message = ""
    results = ""
    try:
        # single measurement
        B1500.single()
        # wait for dataready
        opc = B1500.dataready()
        # get data
        data = B1500.get_data()
        variables = B1500.get_vars(data)
        results = B1500.get_data_numpy(data, variables)

    except Exception as ex:
        status = "meas_error"
        message = "Problem in test (exception): " + str(ex)

    return [status, message, results]

def load_TEST_parameters():
    global TEST_parameters

    import json
    # default values
    TEST_parameters = {
        "WORKSPACE_NAME" : "SIAM",
        "GROUP" : "SOLARMEMS",
        "TEST_PRESET_GROUP_NAME" : "Solarmems"
    }
    # load from external toml file in tests_dir (if exists, if not default values)
    filename_config = os.getcwd() + base_dir + tests_dir + '/Keysight_B1500LAN/Test.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        TEST_parameters = toml_info["parameters"]

load_TEST_parameters()

workspace_name = TEST_parameters["WORKSPACE_NAME"]
group = TEST_parameters["GROUP"]
test_preset_group_name = TEST_parameters["TEST_PRESET_GROUP_NAME"]

B1500 = Keysight_B1500LAN(instruments["Keysight_B1500LAN"])
B1500.instrument.timeout = 200000 # bigger than test time

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

B1500.open_preset_group(group)  # open group
time.sleep(1)
B1500.open_test_preset_group(test_preset_group_name)
time.sleep(1)

# configure format for B1500 data
B1500.configure_format()

# make the test measurement
test_result = test_B1500(B1500)

# show information
print("Test status: ", test_result[0])
print("Test message: ", test_result[1])
print("Test results: ", test_result[2])

