# CUSTOM functions

import math
import time

from PySide6.QtWidgets import QApplication


def print_pretty_header(text):
	length = len(text)
	symbol_horizontal = "-"
	symbol_vertical = "|"
	print(print_simbol(length,symbol_horizontal))
	print(symbol_vertical + " " + text + " " + symbol_vertical)
	print(print_simbol(length,symbol_horizontal))

def print_simbol(length,symbol):
	return symbol*(length+4)

# -----------------------------------------------------
# SaveWafer function (wafers.py)
# -----------------------------------------------------
def get_btnName(x,y):
	# x, y (positive)
    btn_x = int(x) *-1
    btn_y = int(y) *-1
    
    btnName = "btn_" + str(btn_x) + "_" + str(btn_y)
    return btnName

def change_coord_to_origin(x,y,origin):
	# x, y (negative)
    origin_x, origin_y = origin.split()
    x_to_origin = int(x) - int(origin_x)
    y_to_origin = int(y) - int(origin_y)
    return str(x_to_origin) + " " + str(y_to_origin)

def calc_wafer_size(wafer_size_inch):
	# default 4"
	wafer_size_inch = int(wafer_size_inch)
	wafer_size_mm = 100
	thickness = 525
	if wafer_size_inch==1:
	    wafer_size_mm = 25
	    thickness = 1
	if wafer_size_inch==2:
	    wafer_size_mm = 51
	    thickness = 275
	if wafer_size_inch==3:
	    wafer_size_mm = 76
	    thickness = 375
	if wafer_size_inch==4:
	    wafer_size_mm = 100
	    thickness = 525
	if wafer_size_inch==5: # 4.9 inch
	    wafer_size_mm = 125
	    thickness = 625
	if wafer_size_inch==6: # 5.9 inch
	    wafer_size_mm = 150
	    thickness = 675
	if wafer_size_inch==8: # 7.9 inch
	    wafer_size_mm = 200
	    thickness = 725
	if wafer_size_inch==12: # 11.8 inch
	    wafer_size_mm = 300 
	    thickness = 775
	return [wafer_size_mm, thickness]
# -----------------------------------------------------

def get_cmin(cap_list):
	i=0
	cmin = 99999
	for cap in cap_list:
		if float(cap)<float(cmin):
			cmin = float(cap)

	return cmin


def calcular_cv(parameters):
	voltage = parameters["voltage"] # list
	capacitance = parameters["capacitance"] # list
	conductance  = parameters["conductance"] # list
	temperature = parameters["TEMPERATURE"] # value ºC
	area = parameters["AREA"] # area in um2
	fims = parameters["FIMS"] # fiMs value
	frequency = parameters["FREQ"]
	PN = parameters["PN"]
	hysteresis = parameters["hysteresis_marker"] # True/False
	serial_res = parameters["SERIAL_RES"] # True/Fase
	permittivity = parameters["PERMITTIVITY"] # Ex: 3.9 for SiO2

	# Parameters returned (error values)
	vcmax = -9E99
	vcmin = -9E99
	vdox = -9E99
	vna = -9E99
	vvfb = -9E99
	vnss = -9E99
	vrs = -9E99

	if not parameters["CALCULATE_PARAMS"]:
		return {"cmax(pf)": vcmax, "cmin(pF)": vcmin, "dox(A)": vdox, "Na(cm¯³)": vna, "Vfb(V)": vvfb, "Nss(cm¯²)": vnss, "Rs(ohms)": vrs}
	
	if len(voltage) != len(capacitance) or len(capacitance) != len(conductance):
		# error
		if hysteresis:
			return {"cmax_h(pf)": vcmax, "cmin_h(pF)": vcmin, "dox_h(A)": vdox, "Na_h(cm¯³)": vna, "Vfb_h(V)": vvfb, "Nss_h(cm¯²)": vnss, "Rs_H(ohms)": vrs}
		else:
			return {"cmax(pf)": vcmax, "cmin(pF)": vcmin, "dox(A)": vdox, "Na(cm¯³)": vna, "Vfb(V)": vvfb, "Nss(cm¯²)": vnss, "Rs(ohms)": vrs}

	nmuestras = len(capacitance)

	# Constantes utilizadas
	# ---------------------
	# Electron charge (cul)
	Q = 1.60218E-19
	# Boltzmann constant (J/K)
	K = 1.38066E-23
	# Vacuum dielectric constant (F/m)
	E0 = 8.85418E-12
	# Si permittivity constant
	Esi = 11.8
	# Dielectric constant (SiO2, Nitruro,...)
	Eox = permittivity
	# Temperature
	T0 = 273
	# Si gap energy (eV)
	Eg = 1.12
	# -----------------------
	# -----------------------
	T = T0 + temperature
	S = area * 1E-12
	B = Q/(K*T)
	
	Ni = 6.99E21*pow(T,1.5)*math.exp((-1*B*Eg)/2)
	
	# check RS
	i = nmuestras-1
	CmaTOT = 0
	GmaTOT = 0
	while i!= nmuestras-6:
		CmaTOT = CmaTOT + capacitance[i]
		GmaTOT = GmaTOT + conductance[i]
		i = i-1

		Cma = CmaTOT/5
		Gma = GmaTOT/5
		# Miramos ahora la frecuencia de medida
		frec = float(frequency*1000)
		# calculo de w
		PI = 2*math.asin(1.0)
		w = frec*2*PI
		# calculo de RS
		Rs = Gma/((Gma*Gma)+(w*w*Cma*Cma))
		vrs = "{:e}".format(Rs)
	if serial_res:
		# change vectors and extract Rs value
		# Obtenemos valor de Rs en acumulación: Rs=Gma/(Gma²+w²Cma²)
	    # Como hacemos siempre medida CV de INV-->ACU entonces
	    # tenemos la Cma y Gma de las últimas (hacemos media de los
	    # últimos 5 valores).
	    
	    
	    # Aplicar formulas de Nicollian para Cc y Gc (pág 224)
	    i = 0
	    w2 = w*w
	    capacitanceC = []
	    conductanceC = []
	    while i<nmuestras:
	        Gm = conductance[i]
	        Cm = capacitance[i]
	        Gm2 = Gm*Gm
	        Cm2 = Cm*Cm
	        # a=Gm-(Gm²+w²Cm²)*Rs
	        a = Gm-(Gm2+(w2*Cm2))*Rs
	        a2 = a*a
	        # Cc=(Gm²+w²*Cm²)*Cm / a²+Cm²*w²
	        Cc = ((Gm2+w2*Cm2)*Cm)/(a2+Cm2*w2)
	        # Gc=(Gm²+w²*Cm²)*a / a²+Cm²*w²
	        Gc = ((Gm2+w2*Cm2)*a)/(a2+Cm2*w2)
	        capacitanceC.append(Cc)
	        conductanceC.append(Gc)
	        i = i + 1
	    
	    capacitance = capacitanceC
	    conductance = conductanceC
	
	# --------
	# GET CMAX
	# --------
	if capacitance[nmuestras-3] > capacitance[3]:
	  cmax = (capacitance[nmuestras-3]+capacitance[nmuestras-4]+capacitance[nmuestras-5])/3
	  sentido = 1
	else:
	  cmax = (capacitance[3]+capacitance[4]+capacitance[5])/3
	  sentido = 2

	# --------
	# GET CMIN
	# --------
	try:
		cmin = get_cmin(capacitance)
	except:
		print("Oops!", sys.exc_info()[0], "occurred.")


	# check errors
	if cmax<=cmin or cmax<=0 or cmin<=0:
		# error
		if hysteresis:
			return {"cmax_h(pf)": vcmax, "cmin_h(pF)": vcmin, "dox_h(A)": vdox, "Na_h(cm¯³)": vna, "Vfb_h(V)": vvfb, "Nss_h(cm¯²)": vnss, "Rs_H(ohms)": vrs}
		else:
			return {"cmax(pf)": vcmax, "cmin(pF)": vcmin, "dox(A)": vdox, "Na(cm¯³)": vna, "Vfb(V)": vvfb, "Nss(cm¯²)": vnss, "Rs(ohms)": vrs}
	
	# dox extraction
	cox = cmax
	cdmin = (cox*cmin)/(cox-cmin)
	dox = (Eox*E0*S)/cox
	# Na extraction
	Wmax = (Esi*E0*S)/cdmin
	A1 = (Q*Q*Ni*Wmax*Wmax)/(4*Esi*E0*K*T)
	C2 = 6/A1
	C1 = C2
	C2 = C1*(1-math.log(C1))/(1-A1*C1)
	while abs((C2-C1)/C1)>=1E-5:
		C1 = C2
		C2 = C1*(1-math.log(C1))/(1-A1*C1)
	Na = Ni*C2
	# Cfb extraction
	Pp0 = Na
	Ld = math.sqrt((2*Esi*E0*K*T)/(Q*Q*Pp0))
	Cdfb = S*Esi*E0*math.sqrt(2)/Ld
	Cfb = Cdfb*cox/(Cdfb+cox)
	if cmax<=Cfb or cmin>=Cfb:
		# error
		if hysteresis:
			return {"cmax_h(pf)": vcmax, "cmin_h(pF)": vcmin, "dox_h(A)": vdox, "Na_h(cm¯³)": vna, "Vfb_h(V)": vvfb, "Nss_h(cm¯²)": vnss, "Rs_H(ohms)": vrs}
		else:
			return {"cmax(pf)": vcmax, "cmin(pF)": vcmin, "dox(A)": vdox, "Na(cm¯³)": vna, "Vfb(V)": vvfb, "Nss(cm¯²)": vnss, "Rs(ohms)": vrs}

	# nss extraction
	i = 0
	j = 1
	final = 0
	while final==0:
		if sentido==1:
			if capacitance[i]<=Cfb and capacitance[j]>Cfb:
				final = 1
			else:
				i = i + 1
				j = i + 1
		else:
			if capacitance[i]>Cfb and capacitance[j]<=Cfb:
				final = 1
			else:
				i = i + 1
				j = i + 1

	vfb = voltage[i]+((Cfb-capacitance[i])*(voltage[j]-voltage[i])/(capacitance[j]-capacitance[i]))
	fims = fims-4.71-PN*K*T*math.log(Na/Ni)/Q
	nss = (fims-vfb)*cox/(Q*S)

	# set format to values
	vcmax = "{:e}".format(cmax*1E12) # in pF
	vcmin = "{:e}".format(cmin*1E12) # in pF
	vdox = "{:e}".format(dox*1E10) # in A
	vna = "{:e}".format(Na*1E-6) # in cm¯³
	vvfb = vfb
	vnss = "{:e}".format(nss*1E-4) # in cm¯²
	#set vnss [format {%e} $vnss]
	# Ok values
	if hysteresis:
		return {"cmax_h(pf)": vcmax, "cmin_h(pF)": vcmin, "dox_h(A)": vdox, "Na_h(cm¯³)": vna, "Vfb_h(V)": vvfb, "Nss_h(cm¯²)": vnss, "Rs_H(ohms)": vrs}
	else:
		return {"cmax(pf)": vcmax, "cmin(pF)": vcmin, "dox(A)": vdox, "Na(cm¯³)": vna, "Vfb(V)": vvfb, "Nss(cm¯²)": vnss, "Rs(ohms)": vrs}


def measure_CV(hp4192A,CV_parameters,voltage,capacitance,conductance):
	i = 0
	# Calc samples
	num_samples = abs((float(CV_parameters["START"])-float(CV_parameters["STOP"]))/float(CV_parameters["STEP"])) + 1
	# Calc PN
	PN = 1
	if CV_parameters["START"] < CV_parameters["STOP"]:
		PN = -1
	# lectura Capacitance 4192a ex: NCM+000.008E-12,NGM+000.03E-6,V+01.00

	for i in range(0,int(num_samples)):
		hp4192A.single()
		try:
			lectura = hp4192A.read()
			lectura_array = lectura.split(",")
			capacitance_value = lectura_array[0][4:]
			conductance_value = lectura_array[1][4:]
			voltage_value = lectura_array[2][1:]
			capacitance.append(float(capacitance_value))
			conductance.append(float(conductance_value))
			voltage.append(float(voltage_value))
		except Exception as e:
			# with error in read stop the loop
			print(f"Error: {e}")
			break

		#time.sleep(1)
		hp4192A.srq()
		
	return voltage,capacitance,conductance


def measure_CW(hp4192A,CW_parameters,frequency,capacitance,conductance):
	i = 0
	# Calc samples
	num_samples = abs((float(CW_parameters["START"])-float(CW_parameters["STOP"]))/float(CW_parameters["STEP"])) + 1
	# lectura 4192a ex: NCPN+0.7910E-06,NGFN+14.940E+00,K+01000.000
	frequency_value = 0
	while float(frequency_value)<float(CW_parameters["STOP"]):
		hp4192A.single()
		lectura = hp4192A.read()
		lectura_array = lectura.split(",")
		capacitance_value = lectura_array[0][4:]
		conductance_value = lectura_array[1][4:]
		frequency_value = lectura_array[2][1:]
		capacitance.append(float(capacitance_value))
		conductance.append(float(conductance_value))
		frequency.append(float(frequency_value))
		hp4192A.srq()
		
	return frequency,capacitance,conductance


def message_user(main, title, message, type_buttons="yes_cancel"):
	"""
	Ask user for input in a message box. This function is used to ask the user to load the MES file manually.
	:type main: MainWindow
	:param title: title of the message box
	:param message: message to be displayed in the message box
	:param type_buttons: type of buttons to be displayed in the message box. Default is "yes_cancel". Other options are "ok_cancel" and "ok".
	:return:  result of the message box (yes, no, ok, cancel)
	"""
	main.script_thread.message_box_result = None  # reset the result
	main.script_thread.request_message_box.emit(
		title,
		message,
        type_buttons,
	)
	while main.script_thread.message_box_result is None:
		QApplication.processEvents()
		time.sleep(0.1)  # Wait for the message box to be closed

	return main.script_thread.message_box_result