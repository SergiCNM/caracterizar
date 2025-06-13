# SOLARMEM test

import os.path
import sys
import statistics

global test_status, measurement_status
global dieActual, moduleActual

global Voltage, bad_devices, good_devices

path_images = '//fitxers2/fitxers/0_LAB SIAM/'
path_images = 'c:/photos_carto/'  


def solarmems_statistics(leakage_currents,photo_currents):
	import statistics
	
	promedio = statistics.mean(photo_currents)
	desvest = statistics.stdev(photo_currents)
	coefvar = desvest/promedio
	stability = "V"
	if coefvar>0.05:
		stability = "X"

	return [promedio,desvest,coefvar,stability]

def save_file_solarmems(self,V,I1,I2,I3,I4,mode="dark"):
	lines = []
	# list with coord of all wafer positions
	all_wafer_positions = ['0 0', '-1 0', '-2 0', '-3 0', '-4 0', '2 -1', '1 -1', '0 -1', '-1 -1', '-2 -1', '-3 -1', '-4 -1', '-5 -1', '-6 -1', '3 -2', '2 -2', '1 -2', '0 -2', '-1 -2', '-2 -2', '-3 -2', '-4 -2', '-5 -2', '-6 -2', '-7 -2', '4 -3', '3 -3', '2 -3', '1 -3', '0 -3', '-1 -3', '-2 -3', '-3 -3', '-4 -3', '-5 -3', '-6 -3', '-7 -3', '-8 -3', '4 -4', '3 -4', '2 -4', '1 -4', '0 -4', '-1 -4', '-2 -4', '-3 -4', '-4 -4', '-5 -4', '-6 -4', '-7 -4', '-8 -4', '5 -5', '4 -5', '3 -5', '2 -5', '1 -5', '0 -5', '-1 -5', '-2 -5', '-3 -5', '-4 -5', '-5 -5', '-6 -5', '-7 -5', '-8 -5', '-9 -5', '5 -6', '4 -6', '3 -6', '2 -6', '1 -6', '0 -6', '-1 -6', '-2 -6', '-3 -6', '-4 -6', '-5 -6', '-6 -6', '-7 -6', '-8 -6', '-9 -6', '5 -7', '3 -7', '2 -7', '1 -7', '0 -7', '-1 -7', '-2 -7', '-3 -7', '-4 -7', '-5 -7', '-6 -7', '-7 -7', '-9 -7', '5 -8', '4 -8', '3 -8', '2 -8', '1 -8', '0 -8', '-1 -8', '-2 -8', '-3 -8', '-4 -8', '-5 -8', '-6 -8', '-7 -8', '-8 -8', '-9 -8', '5 -9', '4 -9', '3 -9', '2 -9', '1 -9', '0 -9', '-1 -9', '-2 -9', '-3 -9', '-4 -9', '-5 -9', '-6 -9', '-7 -9', '-8 -9', '-9 -9', '4 -10', '3 -10', '2 -10', '1 -10', '0 -10', '-1 -10', '-2 -10', '-3 -10', '-4 -10', '-5 -10', '-6 -10', '-7 -10', '-8 -10', '4 -11', '3 -11', '2 -11', '1 -11', '0 -11', '-1 -11', '-2 -11', '-3 -11', '-4 -11', '-5 -11', '-6 -11', '-7 -11', '-8 -11', '3 -12', '2 -12', '1 -12', '0 -12', '-1 -12', '-2 -12', '-3 -12', '-4 -12', '-5 -12', '-6 -12', '-7 -12', '2 -13', '1 -13', '0 -13', '-1 -13', '-2 -13', '-3 -13', '-4 -13', '-5 -13', '-6 -13', '0 -14', '-1 -14', '-2 -14', '-3 -14', '-4 -14']
	all_wafer_real_origin_chip = "-6 -1"
	separation_char = ","
	# construct header file
	if cartographic_measurement:
		column_row = self.waferwindow.wafer_parameters["wafer_positions"]
		die = int(dieActual)-1
		if len(column_row) != len(all_wafer_positions):
			# corrections in case diferents positions (Refs chips/All chips)
			real_origin_chip = self.waferwindow.wafer_parameters["real_origin_chip"]
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
	lines.append("Info: " + self.ui.txtProcess.text() + " " + self.ui.txtLot.text() + "_" + self.ui.txtWafer.text() + " " + self.ui.txtMask.text() + " / Device ID: " + name_sensor + " / Location: " + coord + " / Type: Standard Cell")
	lines.append("V [V]; I01 [A]; I02 [A]; I03 [A]; I04 [A]")
	# create other lines
	for i in range(0,len(V)):
		texto = str(V[i]) + separation_char + str(I1[i]) + separation_char + str(I2[i]) + separation_char + str(I3[i]) + separation_char + str(I4[i])
		lines.append(texto)

	# create folder
	folder = os.getcwd() + "/" + results_dir + "/" + username + "/" + self.ui.txtProcess.text() + "/" + self.ui.txtLot.text() + "_W" + f"{int(self.ui.txtWafer.text()):02d}" + "/" + mode + "/" 
	if not os.path.exists(folder):
		os.makedirs(folder)
	namefile = folder + name_sensor + ".txt"
	f = open(namefile, "w")
	s1 = '\n'.join(lines)
	f.write(s1)
	f.close()

	return name_sensor

def configure_meas_solarmems(B1500):

	global Voltage
	# reset
	B1500.reset()
	# read all errors
	error = B1500.error(0)
	# configure channels
	code = "MM 16,2,3,4,5" # smus 1-4 (slots 2-5) to Multi channel sweep (mode 16)
	B1500.instrument.write(code)
	# set data output format to 5 mode
	B1500.set_data_output_format(1,0)
	# set voltage sweep channel 2, Linear sweep (1), range auto (0), start(-30), stop(0), step(100), Icomp(50mA)

	type_sweep = 1 # 1 = lineal
	type_range = 0 # 0 = auto
	start_voltage = 0
	stop_voltage = -30
	step = 100 # number of points
	# create Voltage list
	step_voltage = abs(start_voltage-stop_voltage)/step
	Voltage = []
	volts = float(start_voltage)
	for i in range(0,step+1):
		Voltage.append(f"{float(volts):02f}")
		if start_voltage>stop_voltage:
			volts = volts - step_voltage
		else:
			volts = volts + step_voltage
	compliance = 0.05
	# configure channels 2 to 5 slot (SMU1, SMU2, SMU3, SMU4)
	for channel in range(2,6): 
		B1500.instrument.write("WV " + str(channel) + "," + str(type_sweep) + "," + str(type_range) + "," + str(start_voltage) + "," + str(stop_voltage) + "," + str(step+1) + "," + str(compliance))

	return Voltage


def test_solarmems(B1500):
	status = "meas_success"
	message = ""
	try: 
		# enable channels
		B1500.enable_channels()
		# execute measurement
		B1500.single()
		# wait for dataready
		B1500.dataready()
		# check error
		error = B1500.error(1)
		if int(error)==0:
			# no error, read value
			read_mes = B1500.instrument.read()
			# parse values
			I1 = []
			I2 = []
			I3 = []
			I4 = []
			read_mes_array = read_mes.replace("\r","").split(",")
			i =0
			while i<len(read_mes_array):
				I1.append(read_mes_array[i].replace('NBI',''))
				i += 1
				I2.append(read_mes_array[i].replace('NCI',''))
				i += 1
				I3.append(read_mes_array[i].replace('NDI',''))
				i += 1
				I4.append(read_mes_array[i].replace('NEI',''))
				i += 1
			
		else:
			print("Error: " + str(error))
			status = "meas_warning"
			message = str(error)
		B1500.force_0V()
		B1500.disable_channels()
	except:
		status = "meas_error"
		message = "Problem in test (exception)"

	return [status,message, I1, I2, I3, I4]



def get_params(leakage_currents,photo_currents):
	import statistics

	leakage_limit = 10E-9
	photo_limit = 0.35E-3
	# convert list of currents to float
	leakage_currents = list(map(float,leakage_currents))
	photo_currents = list(map(float,photo_currents))
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
	if coefvar>0.05:
		stability = 0
	#promedio,desvest,coefvar,stability = solarmems_statistics(leakage_currents,photo_currents)
	params.append({"name": "Mean", "value": str(promedio)})
	params.append({"name": "DesvEst", "value": str(desvest)})
	params.append({"name": "CoefVar", "value": str(coefvar)})
	params.append({"name": "Stability Cv", "value": str(stability)})
	pass_leakage_current = 1
	for current in leakage_currents:
		if current>=leakage_limit:
			pass_leakage_current = 0
			break
	pass_photo_current = 1
	for current in photo_currents:
		if current<=photo_limit:
			pass_photo_current = 0
			break

	params.append({"name": "Pass leakage current", "value": str(pass_leakage_current)})
	params.append({"name": "Pass photo current", "value": str(pass_photo_current)})

	return params



try:

	B1500 = Keysight_B1500(instruments["Keysight_B1500"])
	

	if cartographic_measurement:
		nchips = self.waferwindow.wafer_parameters["nchips"]
		if str(dieActual)=="1" and str(moduleActual)=="1":

			retval = QMessageBox.question(
				self,
				"Init Keysight B1500 for measurement!",
				"Please, configure instrument for initialization",
                buttons=QMessageBox.Yes | QMessageBox.Cancel,
                defaultButton=QMessageBox.Yes,
            )
			if retval == QMessageBox.Yes:
				# init B1500 for measurement
				Voltage = []
				bad_devices = 0
				good_devices = 0
				Voltage = configure_meas_solarmems(B1500)
				test_status.status = "STARTED"
			else:
				test_status.status = "ABORTED"


		if test_status.status =="STARTED":
			# 1) DARK MEAS
			self.prober.light("0")
			meas_status_dark, message_dark, I1_dark, I2_dark, I3_dark, I4_dark = test_solarmems(B1500)
			# save file .txt for sensor
			save_file_solarmems(self,Voltage,I1_dark,I2_dark,I3_dark,I4_dark,"dark")
			# get current in -3.3V (12 position in list)
			leakage_currents = [I1_dark[11], I2_dark[11], I3_dark[11], I4_dark[11]]
			# 2) LIGHT MEAS
			self.prober.light("1")
			meas_status_light, message_light, I1_light, I2_light, I3_light, I4_light = test_solarmems(B1500)
			# save file .txt for sensor
			name_sensor = save_file_solarmems(self,Voltage,I1_light,I2_light,I3_light,I4_light,"light")
			# get current in -3.3V (12 position in list)
			photo_currents = [I1_light[11], I2_light[11], I3_light[11], I4_light[11]]
			# 3) GET PARAMS
			params = get_params(leakage_currents,photo_currents)
			# 4) MAKE PHOTO
			self.prober.image(path_images + name_sensor + ".jpg",1)
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
				good_devices +=1
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
				bad_devices +=1
				meas_status = "meas_warning"
				message = "Some Pass test failed!"
			
			# save results
			self.waferwindow.meas_result[int(dieActual)-1][int(moduleActual)-1] = {
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
			posx = [0,0]
			posy = [0,0]
			num_graphs = 2
			plot_parameters = self.waferwindow.meas_result[int(dieActual)-1][int(moduleActual)-1]["plot_parameters"]
			for i in range(0,num_graphs):
				#self.plotwindow[i] = ""
				self.show_plotwindow(plot_parameters[i], posx[i], posy[i],i)
			# print final result
			if dieActual == str(nchips):
				self.prober.light("0")
				yield_value = good_devices /(good_devices+bad_devices) 
				percentage_yield = str(round(yield_value*100)) + "%"

				self.updateTextDescription("- Defective Devices: " + str(bad_devices) + "<br />" + "- Good Devices: " + str(good_devices) + "<br />" + "- Yield : " + percentage_yield)

	
	else:
		print("set Voltage")
		Voltage = configure_meas_solarmems(B1500)
		print(Voltage)
		if self.prober=="":
			self.prober_init()
		# 1) DARK MEAS
		self.prober.light("0")
		meas_status_dark, message_dark, I1_dark, I2_dark, I3_dark, I4_dark = test_solarmems(B1500)
		# save file .txt for sensor
		save_file_solarmems(self,Voltage,I1_dark,I2_dark,I3_dark,I4_dark,"dark")
		# get current in -3.3V (12 position in list)
		leakage_currents = [I1_dark[11], I2_dark[11], I3_dark[11], I4_dark[11]]
		# 2) LIGHT MEAS
		self.prober.light("1")
		meas_status_light, message_light, I1_light, I2_light, I3_light, I4_light = test_solarmems(B1500)
		# save file .txt for sensor
		name_sensor = save_file_solarmems(self,Voltage,I1_light,I2_light,I3_light,I4_light,"light")
		# get current in -3.3V (12 position in list)
		photo_currents = [I1_light[11], I2_light[11], I3_light[11], I4_light[11]]
		# 3) GET PARAMS
		params = get_params(leakage_currents,photo_currents)
		# 4) MAKE PHOTO
		self.prober.image(path_images + name_sensor + ".jpg",1)
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
		self.updateTextDescription(text_update)	
		# show 2 graphs
		posx = [0,0]
		posy = [0,0]


except:
    message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<","").replace(">","") + " occurred. " + str(sys.exc_info()[1])
    self.updateTextDescription(message,"ERROR")
    retval = messageBox(self,"ERROR",message,"critical")

