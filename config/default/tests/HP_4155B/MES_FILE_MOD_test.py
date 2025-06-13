# Test MES FILE in HP 4155B instrument
import os.path
import sys

from config.default.instruments import HP_4155B
from config.functions import *
import toml

global test_status, measurement_status
global dieActual, moduleActual
global MES_parameters


def load_MES_parameters():
	global MES_parameters

	import json
	# default values
	MES_parameters = {
		"INTEGRATION": "SHOR",
		"NET": "NET1",
		"NET_UPDATE": "NET2",
		"UPDATE_COUNT": 50,
		"TEST_NAMES": ""
	}
	# load from external toml file in tests_dir (if exists, if not default values)
	filename_config = os.getcwd() + base_dir + tests_dir + '/HP_4155B/MES_FILE_MOD.toml'
	file_exists = os.path.exists(filename_config)
	if file_exists:
		toml_info = toml.load(filename_config)
		MES_parameters = toml_info["parameters"]

def measure_single(hp4155):
	# single measurement
	measurement_status.status = "START"
	hp4155.single()
	hp4155.dataReady()
	measurement_status.status = "FINISH"


load_MES_parameters()
if MES_parameters["TEST_NAMES"] == "":
	# exit with error
	meas_result = {"meas_status" : "meas_error", "meas_message" : "No test names defined in MES_FILE_MOD.toml"}
	txt_result = "Error: No test names defined in MES_FILE_MOD.toml"
	self.updateTextDescription(txt_result)
else:
	hp4155 = HP_4155B(instruments["HP_4155B"])
	count = 0
	if cartographic_measurement:
		if str(dieActual)=="1" and str(moduleActual)=="1":
			retval = QMessageBox.question(
				self,
				"Cartographic process starting!",
				"Please, when you are ready press button Yes!",
				buttons=QMessageBox.Yes | QMessageBox.Cancel ,
				defaultButton=QMessageBox.Yes,
			)
			if retval == QMessageBox.Yes:
				# configure int time and view graph
				hp4155.integration_time(MES_parameters["INTEGRATION"])
				hp4155.view_graph()
				test_names = MES_parameters["TEST_NAMES"].split(",")
				# init test
				test_status.status = "STARTED"
			else:
				test_status.status = "ABORTED"

		if test_status.status=="STARTED":
			for test_name in test_names:
				# set test name
				hp4155.load_mes(destination=MES_parameters["NET"], namefile=test_name)
				# measure single
				measure_single(hp4155)
				# save DAT file in cartographic process
				hp4155.save_result(MES_parameters["NET"], f"{test_name}_" + str(dieActual) + "_" + str(moduleActual))

				meas_result = {"meas_status": "meas_success", "meas_message": ""}
				txt_result = f"Measurement {test_name} done, die: " + str(dieActual) + " module: " + str(moduleActual)
				self.updateTextDescription(txt_result)

			count += 1
			# not variables in cartographic process
			self.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1] = {
				"status": meas_result["meas_status"],
				"message": meas_result["meas_message"],
				"contact_height": "",
				"variables": [],
				"plot_parameters": {
					"name": "Plot IV",
					"x": [],
					"y1": [],
					"y2": [],

					"titles": {
						"title": "I-V Measurement",
						"left": "Current I1",
						"bottom": "Voltage",
						"right": "Current I2"
					},
					"units": {
						"left": "A",
						"bottom": "V",
						"right": "A"
					},
					"showgrid": {"x": False, "y": False},
					"legend": False

				}

			}

			if count == MES_parameters["UPDATE_COUNT"]:
				hp4155.refresh_net(MES_parameters)
				count = 0

	else:
		dieActual = 1
		moduleActual = 1
		# reset instrument
		# hp4155.reset()
		# configure int time to default (SHOR) and view graph
		hp4155.integration_time(MES_parameters["INTEGRATION"])
		hp4155.view_graph()
		test_names = MES_parameters["TEST_NAMES"].split(",")
		for test_name in test_names:
			# set test name
			hp4155.load_mes(destination=MES_parameters["NET"], namefile=test_name)
			# measure single
			measure_single(hp4155)
			meas_result = {"meas_status" : "meas_success", "meas_message" : ""}
			txt_result = f"Measurement {test_name} done, die: " + str(dieActual) + " module: " + str(moduleActual)
			self.updateTextDescription(txt_result)
	


