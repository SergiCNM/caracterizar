# SOLARMEM test
import os
import sys

from config.default.instruments import Keysight_B1500LAN
from config.functions import *
import toml
from datetime import datetime
import time


global test_status, measurement_status
global dieActual, moduleActual
global posx, posy
global username, instruments
global base_dir, tests_dir, results_dir, cartographic_measurement

global Voltage, bad_devices, good_devices, defective_devices, bad_coefvar_devices

global TEST_parameters



brightness_light = 100 # brightness microscope light for light measurements
brightness_light_photo = 4  # brightness microscope light for photos

# new levels 
global leakage_level, photo_level, coefvar_level
leakage_level = 10E-9 # @3.3V
photo_level = 5E-6 # 3.3V por cuadrante
coefvar_level = 0.05 # 5% entre los cuadrantes del mismo chip

def get_folder_photos(main):
	global TEST_parameters
	folder = TEST_parameters["FOLDER_IMAGES"]

	return folder


def get_folder_namefile(main):
	folder = os.getcwd() + "/" + results_dir + "/" + username + "/" + main.ui.txtProcess.text() + "/" + main.ui.txtLot.text() + "_W" + f"{int(main.ui.txtWafer.text()):02d}" + "/" 
	namefile = main.ui.txtLot.text() + "_W" + f"{int(main.ui.txtWafer.text()):02d}" + ".txt"
	return folder, namefile

def save_results_file_solarmems(main, name_sensor,leakage_currents,leakage_currents2,photo_currents,photo_currents2,params):
	
	# create unique result file for dark & light
	eof = '\n'
	folder = os.getcwd() + "/" + results_dir + "/" + username + "/" + main.ui.txtProcess.text() + "/" + main.ui.txtLot.text() + "_W" + f"{int(main.ui.txtWafer.text()):02d}" + "/" 
	namefile = main.ui.txtLot.text() + "_W" + f"{int(main.ui.txtWafer.text()):02d}" + ".txt"
	# open file to append information
	f = open(folder + namefile, 'a')

	s1 = name_sensor + ";"
	s1 += str(leakage_currents[0]) + ";" + str(leakage_currents[1]) + ";" + str(leakage_currents[2]) + ";" + str(leakage_currents[3]) + ";"
	s1 += str(leakage_currents2[0]) + ";" + str(leakage_currents2[1]) + ";" + str(leakage_currents2[2]) + ";" + str(leakage_currents2[3]) + ";"
	s1 += str(photo_currents[0]) + ";" + str(photo_currents[1]) + ";" + str(photo_currents[2]) + ";" + str(photo_currents[3]) + ";"
	s1 += str(photo_currents2[0]) + ";" + str(photo_currents2[1]) + ";" + str(photo_currents2[2]) + ";" + str(photo_currents2[3]) + ";"

	for param in params:
		if param["name"]=="Mean":
			mean = param["value"]
		if param["name"]=="DesvEst":
			desvest = param["value"]
		if param["name"]=="CoefVar":
			coefvar = param["value"]
		if param["name"]=="Stability Cv":
			stability = param["value"]

	s1 += str(mean) + ";" + str(desvest) + ";" + str(coefvar) + ";" + str(stability) + eof
	f.write(s1)
	f.close()
	

def save_measurement_file_solarmems(main, V,I1,I2,I3,I4,mode="dark"):
	# saving measurements files in folders
	lines = []
	# list with coord of all wafer positions
	all_wafer_positions = ['0 0', '-1 0', '-2 0', '-3 0', '-4 0', '2 -1', '1 -1', '0 -1', '-1 -1', '-2 -1', '-3 -1', '-4 -1', '-5 -1', '-6 -1', '3 -2', '2 -2', '1 -2', '0 -2', '-1 -2', '-2 -2', '-3 -2', '-4 -2', '-5 -2', '-6 -2', '-7 -2', '4 -3', '3 -3', '2 -3', '1 -3', '0 -3', '-1 -3', '-2 -3', '-3 -3', '-4 -3', '-5 -3', '-6 -3', '-7 -3', '-8 -3', '4 -4', '3 -4', '2 -4', '1 -4', '0 -4', '-1 -4', '-2 -4', '-3 -4', '-4 -4', '-5 -4', '-6 -4', '-7 -4', '-8 -4', '5 -5', '4 -5', '3 -5', '2 -5', '1 -5', '0 -5', '-1 -5', '-2 -5', '-3 -5', '-4 -5', '-5 -5', '-6 -5', '-7 -5', '-8 -5', '-9 -5', '5 -6', '4 -6', '3 -6', '2 -6', '1 -6', '0 -6', '-1 -6', '-2 -6', '-3 -6', '-4 -6', '-5 -6', '-6 -6', '-7 -6', '-8 -6', '-9 -6', '5 -7', '3 -7', '2 -7', '1 -7', '0 -7', '-1 -7', '-2 -7', '-3 -7', '-4 -7', '-5 -7', '-6 -7', '-7 -7', '-9 -7', '5 -8', '4 -8', '3 -8', '2 -8', '1 -8', '0 -8', '-1 -8', '-2 -8', '-3 -8', '-4 -8', '-5 -8', '-6 -8', '-7 -8', '-8 -8', '-9 -8', '5 -9', '4 -9', '3 -9', '2 -9', '1 -9', '0 -9', '-1 -9', '-2 -9', '-3 -9', '-4 -9', '-5 -9', '-6 -9', '-7 -9', '-8 -9', '-9 -9', '4 -10', '3 -10', '2 -10', '1 -10', '0 -10', '-1 -10', '-2 -10', '-3 -10', '-4 -10', '-5 -10', '-6 -10', '-7 -10', '-8 -10', '4 -11', '3 -11', '2 -11', '1 -11', '0 -11', '-1 -11', '-2 -11', '-3 -11', '-4 -11', '-5 -11', '-6 -11', '-7 -11', '-8 -11', '3 -12', '2 -12', '1 -12', '0 -12', '-1 -12', '-2 -12', '-3 -12', '-4 -12', '-5 -12', '-6 -12', '-7 -12', '2 -13', '1 -13', '0 -13', '-1 -13', '-2 -13', '-3 -13', '-4 -13', '-5 -13', '-6 -13', '0 -14', '-1 -14', '-2 -14', '-3 -14', '-4 -14']
	all_wafer_real_origin_chip = "-6 -1"
	separation_char = ","
	# construct header file
	if cartographic_measurement:
		column_row = main.waferwindow.wafer_parameters["wafer_positions"]
		die = int(dieActual)-1
		if len(column_row) != len(all_wafer_positions):
			# corrections in case diferents positions (Refs chips/All chips)
			real_origin_chip = main.waferwindow.wafer_parameters["real_origin_chip"]
			correction_x = int(real_origin_chip.split()[0])-int(all_wafer_real_origin_chip.split()[0])
			correction_y = int(real_origin_chip.split()[1])-int(all_wafer_real_origin_chip.split()[1])
			column_row_mod = []
			for col_row in column_row:
				x_pos = int(col_row.split()[0])+correction_x
				y_pos = int(col_row.split()[1])+correction_y
				column_row_mod.append(str(x_pos) + " " + str(y_pos))
			
			num_sensor = all_wafer_positions.index(column_row_mod[die])
		else:
			# 175 sensors, not necessary to do corrections
			num_sensor = die

	else:
		column_row = ["0 0"]
		die = 0
		num_sensor = 0
	
	coord = column_row[die]
	name_sensor = "S" + f"{num_sensor:03d}"
	lines.append("Info: " + main.ui.txtProcess.text() + " " + main.ui.txtLot.text() + "_" + main.ui.txtWafer.text() + " " + main.ui.txtMask.text() + " / Device ID: " + name_sensor + " / Location: " + coord + " / Type: Standard Cell")
	lines.append("V [V]; I01 [A]; I02 [A]; I03 [A]; I04 [A]")
	# create other lines
	for i in range(0,len(V)):
		texto = str(V[i]) + separation_char + str(I1[i]) + separation_char + str(I2[i]) + separation_char + str(I3[i]) + separation_char + str(I4[i])
		lines.append(texto)

	# create folder
	folder = os.getcwd() + "/" + results_dir + "/" + username + "/" + main.ui.txtProcess.text() + "/" + main.ui.txtLot.text() + "_W" + f"{int(main.ui.txtWafer.text()):02d}" + "/" + mode + "/" 
	if not os.path.exists(folder):
		os.makedirs(folder)
	namefile = folder + name_sensor + ".txt"
	f = open(namefile, "w")
	s1 = '\n'.join(lines)
	f.write(s1)
	f.close()

	return name_sensor

def configure_meas_solarmems(B1500):
	global TEST_parameters
	workspace_name = TEST_parameters["WORKSPACE_NAME"]
	group = TEST_parameters["GROUP"]
	test_preset_group_name = TEST_parameters["TEST_PRESET_GROUP_NAME"]

	status = B1500.status_workspace()
	if status=="CLOS":
		B1500.open_workspace(workspace_name)
	else:
		if B1500.get_name_workspace().replace('"','')!=workspace_name:
			B1500.close_workspace()
			status = B1500.status_workspace()
			while status!="CLOS":
				status = B1500.status_workspace()
				time.sleep(1)
			B1500.open_workspace(workspace_name)
		
	status = B1500.status_workspace()

	while status!="OPEN":
		status = B1500.status_workspace()
		time.sleep(1)

	B1500.open_preset_group(group) # open SOLARMEMS group
	time.sleep(1)
	B1500.open_test_preset_group(test_preset_group_name)
	time.sleep(1)

	# configure format for B1500 data
	B1500.configure_format()



def test_solarmems(B1500):
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
		results = B1500.get_data_numpy(data,variables)
		
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
    filename_config = os.getcwd() + base_dir + tests_dir + '/Keysight_B1500LAN/SOLARMEMS.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        TEST_parameters = toml_info["parameters"]

def get_params(leakage_currents,photo_currents):
	import statistics  # no debería hacer falta
	global leakage_level, photo_level, coefvar_level

	leakage_limit = leakage_level
	photo_limit = photo_level
	# convert list of currents to float & abs values to calcl statistics
	leakage_currents = list((map(float,leakage_currents)))
	# leakage_currents = list((map(abs,leakage_currents)))
	photo_currents = list((map(float,photo_currents)))
	# photo_currents = list((map(abs,photo_currents)))
	params = []
	params.append({"name" : "Leakage current I1 @ 3.3V [A]", "value" : str(leakage_currents[0])})
	params.append({"name" : "Leakage current I2 @ 3.3V [A]", "value" : str(leakage_currents[1])})
	params.append({"name" : "Leakage current I3 @ 3.3V [A]", "value" : str(leakage_currents[2])})
	params.append({"name" : "Leakage current I4 @ 3.3V [A]", "value" : str(leakage_currents[3])})
	params.append({"name" : "Photo current I1 @ 3.3V [A]", "value" : str(photo_currents[0])})
	params.append({"name" : "Photo current I2 @ 3.3V [A]", "value" : str(photo_currents[1])})
	params.append({"name" : "Photo current I3 @ 3.3V [A]", "value" : str(photo_currents[2])})
	params.append({"name" : "Photo current I4 @ 3.3V [A]", "value" : str(photo_currents[3])})
	# calc statistics photo currents
	promedio = statistics.mean(photo_currents)
	desvest = statistics.stdev(photo_currents)
	coefvar = float(desvest)/float(promedio)
	stability = 1
	if abs(coefvar)>coefvar_level:
		stability = 0

	params.append({"name": "Mean", "value": str(promedio)})
	params.append({"name": "DesvEst", "value": str(desvest)})
	params.append({"name": "CoefVar", "value": str(coefvar)})
	params.append({"name": "Stability Cv", "value": str(stability)})
	pass_leakage_current = 1
	for current in leakage_currents:
		if abs(current)>=leakage_limit:
			pass_leakage_current = 0
			break
	pass_photo_current = 1
	for current in photo_currents:
		if abs(current)<photo_limit:
			pass_photo_current = 0
			break

	params.append({"name": "Pass leakage current", "value": str(pass_leakage_current)})
	params.append({"name": "Pass photo current", "value": str(pass_photo_current)})

	return params


def create_file_results(main, folder, namefile):
	# create file result
	create_file = True
	if os.path.exists(folder + namefile):
		# retval = QMessageBox.information(
		#     main,
		#     "Process canceled!",
		#     "Please, move existing information to another folder!",
		#     buttons=QMessageBox.Ok ,
		#     defaultButton=QMessageBox.Ok,
		# )
		retval = message_user(main, "Process canceled!", "Please, move existing information to another folder!",
							  "ok")

		create_file = False
		test_status.status = "ABORTED"
		
		
	if create_file:
		# create folder
		if not os.path.exists(folder):
			os.makedirs(folder)
		f = open(folder + namefile, "w+")
		# -------------------
		# Create header
		# -------------------
		eof = '\n'
		today = datetime.now()
		# dd/mm/YY
		d1 = today.strftime("%d/%m/%Y")
		nchips = 1
		if cartographic_measurement:
			nchips = main.waferwindow.wafer_parameters["nchips"]
		header = 'iSSOC: Silicon Sensors Photodiodes Delivery' + eof
		header += 'Delivery#: ' + eof
		header += 'Caract. date: ' + str(d1) + eof
		header += 'Run: ' + main.ui.txtLot.text() + eof
		header += 'Wafer: ' + f"{int(main.ui.txtWafer.text()):02d}" + eof
		header += 'Devices#: ' + str(nchips) + eof
		header += 'Temperature: ' + main.ui.txtTemperature.text() + " ºC" + eof
		header += 'Humidity: ' + main.ui.txtHumidity.text() + " % RH" + eof + eof
		header += "Device ID;"
		header += "I1 [A] Leakage current @ 3.3V;I2 [A] Leakage current @ 3.3V;I3 [A] Leakage current @ 3.3V;I4 [A] Leakage current @ 3.3V;"
		header += "I1 [A] Leakage current @ 9.9V;I2 [A] Leakage current @ 9.9V;I3 [A] Leakage current @ 9.9V;I4 [A] Leakage current @ 9.9V;"
		header += "I1 [A] Photo current @ 3.3V;I2 [A] Photo current @ 3.3V;I3 [A] Photo current @ 3.3V;I4 [A] Photo current @ 3.3V;"
		header += "I1 [A] Photo current @ 9.9V;I2 [A] Photo current @ 9.9V;I3 [A] Photo current @ 9.9V;I4 [A] Photo current @ 9.9V;"
		header += "Mean Photo current @ 3.3V;DesvEst Photo current @ 3.3V;CoefVar Photo current @ 3.3V;Stability CoefVar Photo current @ 3.3V" + eof
		# -------------------
		f.write(header)
		f.close()

	return create_file


try:
	load_TEST_parameters()
	path_images = get_folder_photos(main)
	if not TEST_parameters["ONLY_PHOTOS"]:
		# connect to B1500
		B1500 = Keysight_B1500LAN(instruments["Keysight_B1500LAN"])
		B1500.instrument.timeout = 200000 # bigger than test

	if cartographic_measurement:
		nchips = main.waferwindow.wafer_parameters["nchips"]
		if str(dieActual)=="1" and str(moduleActual)=="1":


			# retval = QMessageBox.question(
			# 	main,
			# 	"Init Keysight B1500 for measurement!",
			# 	"Please, configure instrument for initialization",
            #     buttons=QMessageBox.Yes | QMessageBox.Cancel,
            #     defaultButton=QMessageBox.Yes,
            # )
			if not TEST_parameters["ONLY_PHOTOS"]:
				retval = message_user(main, "Init Keysight B1500 for measurement!", "Please, configure instrument for initialization", "yes_cancel")
				if retval == QMessageBox.Yes:
					# init B1500 for measurement
					Voltage = []
					bad_devices = 0
					bad_coefvar_devices = 0
					defective_devices = 0
					good_devices = 0
					configure_meas_solarmems(B1500)
					test_status.status = "STARTED"
					folder, namefile = get_folder_namefile(main)
					if not create_file_results(main, folder, namefile):
						test_status.status = "ABORTED"

				else:
					test_status.status = "ABORTED"
			else:
				test_status.status = "STARTED"


		if test_status.status =="STARTED":
			if not TEST_parameters["ONLY_PHOTOS"]:
				# 1) DARK MEAS
				main.prober.light("0")
				meas_status_dark, message_dark, results = test_solarmems(B1500)
				Voltage, I1_dark, I2_dark, I3_dark, I4_dark = results['V1'], results['I1'], results['I2'], results['I3'], results['I4']
				# save file .txt for sensor
				save_measurement_file_solarmems(main,Voltage,I1_dark,I2_dark,I3_dark,I4_dark,"dark")
				# get current in -3.3V (12 position in list)
				leakage_currents = [I1_dark[11], I2_dark[11], I3_dark[11], I4_dark[11]]
				# get current in -9.9V (34 position in list)
				leakage_currents2 = [I1_dark[33], I2_dark[33], I3_dark[33], I4_dark[33]]

				# 2) LIGHT MEAS
				main.prober.light_property("light", brightness_light)
				main.prober.light("1")
				# wait time to adjust light & make measurement with correct light
				time.sleep(1)
				meas_status_light, message_light, results = test_solarmems(B1500)
				Voltage, I1_light, I2_light, I3_light, I4_light = results['V1'], results['I1'], results['I2'], results['I3'], results['I4']
				# save file .txt for sensor
				name_sensor = save_measurement_file_solarmems(main,Voltage,I1_light,I2_light,I3_light,I4_light,"light")
				# get current in -3.3V (12 position in list)
				photo_currents = [I1_light[11], I2_light[11], I3_light[11], I4_light[11]]
				# get current in -9.9V (34 position in list)
				photo_currents2 = [I1_light[33], I2_light[33], I3_light[33], I4_light[33]]

				# 3) GET PARAMS & SAVE (line) TO RESULTS FILE
				params = get_params(leakage_currents,photo_currents)
				save_results_file_solarmems(main, name_sensor,leakage_currents,leakage_currents2,photo_currents,photo_currents2,params)
			else:
				column_row = main.waferwindow.wafer_parameters["wafer_positions"]
				die = int(dieActual)-1
				num_sensor = die
				name_sensor = "S" + f"{num_sensor:03d}"

			# 4) MAKE PHOTO
			main.prober.light_property("light", brightness_light_photo)
			# wait time to adjust light & make photo with correct light
			time.sleep(1)
			main.prober.image(path_images + name_sensor + ".jpg",1)

			if not TEST_parameters["ONLY_PHOTOS"]:
				# 5) GET yield
				pass_leakage_current = 0
				pass_photo_current = 0
				pass_stability = 0
				for param in params:
					if param["name"]=="Pass leakage current":
						pass_leakage_current = param["value"]
					if param["name"]=="Pass photo current":
						pass_photo_current = param["value"]
					if param["name"]=="Stability Cv":
						pass_stability = param["value"]

				if pass_leakage_current and pass_photo_current and pass_stability:
					#good_devices +=1
					meas_status = "meas_success"
					message = ""
					if not meas_status_dark:
						meas_status = "meas_error"
						message = message_dark
					else:
						if not meas_status_light:
							meas_status = "meas_error"
							message = message_light
				else:
					if pass_leakage_current and pass_photo_current and not pass_stability:
						#bad_coefvar_devices +=1
						meas_status = "meas_warning"
						message = "Bad CoefV!"
					else:
						#defective_devices +=1
						meas_status = "meas_error"
						message = "Unstable device!"

				# save results
				main.waferwindow.meas_result[int(dieActual)-1][int(moduleActual)-1] = {
					"status" : meas_status,
					"message" : message,
					"contact_height" : "",
					"variables" : [{
						"params" : [],
						"data" : [{"name" : "V", "values" : Voltage, "units" : "V"},{"name": "I01", "values" : I1_dark, "units": "A"},{"name": "I02", "values" : I2_dark, "units": "A"},{"name": "I03", "values" : I3_dark, "units": "A"},{"name": "I04", "values" : I4_dark, "units": "A"}]
					},{
						"params" : params,
						"data" : [{"name" : "V", "values" : Voltage, "units" : "V"},{"name": "I01", "values" : I1_light, "units": "A"},{"name": "I02", "values" : I2_light, "units": "A"},{"name": "I03", "values" : I3_light, "units": "A"},{"name": "I04", "values" : I4_light, "units": "A"}]
					}],
					"plot_parameters" : [{
						"name" : "Plot IV dark",
						"x" : Voltage,
						"y1" : I1_dark,
						"y2" : I2_dark,
						"y3" : I3_dark,
						"y4" : I4_dark,
						"titles" : {
							"title" : "I-V Measurement dark",
							"left" : "Sensor current",
							"bottom" : "Voltage"
						},
						"units" : {
							"left" : "A",
							"bottom" : "V",
							"right" : "A"
						},
						"showgrid" : {"x" : False, "y" : False},
						"legend" : False,
						"multiaxis" : False

					},{
						"name" : "Plot IV light",
						"x" : Voltage,
						"y1" : I1_light,
						"y2" : I2_light,
						"y3" : I3_light,
						"y4" : I4_light,
						"titles" : {
							"title" : "I-V Measurement light",
							"left" : "Sensor current",
							"bottom" : "Voltage"
						},
						"units" : {
							"left" : "A",
							"bottom" : "V",
							"right" : "A"
						},
						"showgrid" : {"x" : False, "y" : False},
						"legend" : False,
						"multiaxis" : False

					}]

				}
				# show 2 graphs
				posx_array = [0,0]
				posy_array = [0,0]
				num_graphs = 2
				plot_parameters = main.waferwindow.meas_result[int(dieActual)-1][int(moduleActual)-1]["plot_parameters"]
				# print(plot_parameters)
				for i in range(0,num_graphs):
					#main.plotwindow[i] = ""
					posx = posx_array[i]
					posy = posy_array[i]
					# emit_plot(plot_parameters[i])
					# main.show_plotwindow(plot_parameters[i],i)
			else:

				# only photos, no measurements
				meas_status = "meas_success"
				message = "Only photos taken!"
				main.waferwindow.meas_result[int(dieActual)-1][int(moduleActual)-1] = {
					"status" : meas_status,
					"message" : message,
					"contact_height" : "",
					"variables" : [],
					"plot_parameters" : []
				}
			# print final result
			if dieActual == str(nchips):
				main.prober.light("0")
				#bad_devices = defective_devices + bad_coefvar_devices
				#yield_value = good_devices /(good_devices+bad_devices)
				#percentage_yield = str(round(yield_value*100)) + "%"

				#main.updateTextDescription("- Defective Devices: " + str(defective_devices) + "<br />" + "- Good Devices: " + str(good_devices) + "<br />" + "- Bad CoefVar Devices: " + str(bad_coefvar_devices) + "<br />"  + "- Yield : " + percentage_yield)

	
	else:

		folder, namefile = get_folder_namefile(main)
		if create_file_results(main, folder, namefile):
			# ------------------
			# SINGLE MEASUREMENT
			# ------------------
			configure_meas_solarmems(B1500)
			if main.prober=="":
				main.init_prober()
			# 1) DARK MEAS
			main.prober.light("0")
			meas_status_dark, message_dark, results = test_solarmems(B1500)
			Voltage, I1_dark, I2_dark, I3_dark, I4_dark = results['V1'], results['I1'], results['I2'], results['I3'], results['I4']
			# save file .txt for sensor
			save_measurement_file_solarmems(main,Voltage,I1_dark,I2_dark,I3_dark,I4_dark,"dark")
			# get current in -3.3V (12 position in list)
			leakage_currents = [I1_dark[11], I2_dark[11], I3_dark[11], I4_dark[11]]
			# get current in -9.9V (34 position in list)
			leakage_currents2 = [I1_dark[33], I2_dark[33], I3_dark[33], I4_dark[33]]
			# 2) LIGHT MEAS
			main.prober.light_property("light", brightness_light)
			main.prober.light("1")
			# wait time to adjust light & make measurement with correct light
			time.sleep(1)
			meas_status_light, message_light, results = test_solarmems(B1500)
			Voltage, I1_light, I2_light, I3_light, I4_light = results['V1'], results['I1'], results['I2'], results['I3'], results['I4']
			# save file .txt for sensor
			name_sensor = save_measurement_file_solarmems(main,Voltage,I1_light,I2_light,I3_light,I4_light,"light")
			# get current in -3.3V (12 position in list)
			photo_currents = [I1_light[11], I2_light[11], I3_light[11], I4_light[11]]
			# get current in -9.9V (34 position in list)
			photo_currents2 = [I1_light[33], I2_light[33], I3_light[33], I4_light[33]]
			# 3) GET PARAMS & SAVE (line) TO RESULTS FILE
			params = get_params(leakage_currents,photo_currents)
			save_results_file_solarmems(main, name_sensor,leakage_currents,leakage_currents2,photo_currents,photo_currents2,params)
			# 4) MAKE PHOTO
			main.prober.light_property("light", brightness_light_photo)
			# wait time to adjust light & make photo with correct light
			time.sleep(1)
			main.prober.image(path_images + name_sensor + ".jpg",1)
			# 5) GET yield
			pass_leakage_current = 0
			pass_photo_current = 0
			pass_stability = 0
			text_update =""
			for param in params:
				text_update += param["name"] + ":" + str(param["value"]) + "<br />"
				if param["name"]=="Pass leakage current":
					pass_leakage_current = param["value"]
				if param["name"]=="Pass photo current":
					pass_photo_current = param["value"]
				if param["name"]=="Stability Cv":
					pass_stability = param["value"]
			
			text_update += "<br />- Leakage current test: " + "OK" if pass_leakage_current else "NOT OK"
			text_update += "<br />- Photo current test: " + "OK" if pass_photo_current else "NOT OK"
			text_update += "<br />- Stability test: " + "OK" if pass_stability else "NOT OK"
			main.updateTextDescription(text_update)	
			# show 2 graphs
			posx = [0,0]
			posy = [0,0]
			# light in for individual measurements
			main.prober.light("1")
		else:
			message = 'Problem creating file results!'
			main.updateTextDescription(message,"ERROR")
			retval = message_user(main, "ERROR", message,
								  "ok_error")
			# retval = messageBox(main,"ERROR",message,"critical")


except:
	message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<","").replace(">","") + " occurred. " + str(sys.exc_info()[1])
	main.updateTextDescription(message,"ERROR")
    # retval = messageBox(main,"ERROR",message,"critical")
	retval = message_user(main, "ERROR", message, "ok_error")