# HP4192A instrument driver
import pyvisa
import time


class HP_4192A:
	def __init__(self,parameters):
		rm = pyvisa.ResourceManager()
		inst = rm.open_resource(parameters["address"])
		self.instrument = inst
		self.address = parameters["address"]
		self.read_termination(parameters["read_termination"])
		self.write_termination(parameters["write_termination"])
		self.stop()
		self.local()
		# self.instrument.clear()
		# self.instrument.buffer_read = 2048
		if "timeout" in parameters:
			self.timeout(int(parameters["timeout"]))

	def reset(self):
		self.instrument.write('*RST')

	def timeout(self,timeout):
		self.instrument.timeout = timeout

	def read_termination(self,read_termination):
		self.instrument.read_termination = read_termination

	def write_termination(self,write_termination):
		self.instrument.write_termination = write_termination

	def idn(self):
		return self.instrument.query('*IDN?')

	def srq(self):
		self.instrument.write('SR1')

	def wait(self):
		self.instrument.write('*WAI')

	def local(self):
		self.instrument.write('RL1')
		time.sleep(1)
		self.instrument.write('T1')



	def config_CV(self,CV_parameters):
		# CV_parameters dictionary with:
		# "START" (V) (from -35 to 35), "STOP"(V), "STEP" (V) (from 0.01 to 5V), "OSC" (mV from 5 to 1100), "FREQ" (kHz from 0.005 to 13000), 
		# Optional: "CIRCUIT_MODE" (Series/Paralell), "AVERAGE" (True/False)

		# FIRST CHECK PARAMETERS
		if "START" in CV_parameters and "STOP" in CV_parameters and "STEP" in CV_parameters and "OSC" in CV_parameters and "FREQ" in CV_parameters:
			# parameters passed
			if -35 <= CV_parameters["START"] <= 35:
				if -35 <= CV_parameters["STOP"] <= 35:
					if 0.001 <= CV_parameters["STEP"] <= 5 or -5<=CV_parameters["STEP"]<=-0.001:
						if 5 <= CV_parameters["OSC"] <= 1100:
							if not 0.005 <= CV_parameters["FREQ"] <= 13000:
								print("FREQUENCY not in range (0.005kHz, 13000kHz): " + str(CV_parameters["FREQ"]))
								return False		
						else:
							print("OSCILLATION LEVEL not in range (5mV, 1100mv): " + str(CV_parameters["OSC"]))
							return False		
					else:
						print("STEP VOLTAGE not in range (0.001V, 5V): " + str(CV_parameters["STEP"]))
						return False
						
				else:
					print("STOP BIAS not in range (-35V, 35V): " + str(CV_parameters["STOP"]))
					return False
			else:
				print("START BIAS not in range (-35V, 35V): " + str(CV_parameters["START"]))
				return False
		else:
			print("Parameters config CV not passed!")
			return False
		PN = -1
		if CV_parameters["START"] > CV_parameters["STOP"]:
			PN = 1
		# ------------
		# CIRCUIT MODE
		# ------------
		circuit_mode = "C1"
		if "CIRCUIT_MODE" in CV_parameters:
			if CV_parameters["CIRCUIT_MODE"]=="Parallel":
				circuit_mode = "C3"
			if CV_parameters["CIRCUIT_MODE"] == "Series":
				circuit_mode = "C2"
		# --------
		# DISPLAY
		# --------
		cmd = "A4 B3 " + circuit_mode + " F1" # A4: Display A = C, B3: Display B = R/G, F1: Display A/B/C
		self.instrument.write(cmd)
		# -----------------
		# OSCILLATION LEVEL
		# -----------------
		oscillation_level = float(CV_parameters["OSC"]*1000)
		cmd = "OL" + str(oscillation_level).replace(",",".") + "EN"
		self.instrument.write(cmd)
		# ---------
		# FREQUENCY
		# ---------
		freq = CV_parameters["FREQ"]
		cmd = "FR" + str(freq).replace(",",".") + "EN"
		self.instrument.write(cmd)

		# ---------
		# AVERAGE (normally off - V0)
		# ---------
		if "AVERAGE" in CV_parameters:
			if CV_parameters["AVERAGE"]:
				self.average("ON") 
			else:
				self.average("OFF")
		else:
			self.average("OFF") # default OFF
		# ---------
		# STEP BIAS
		# ---------
		step_bias = abs(CV_parameters["STEP"])  # always positive
		cmd = "SB" + str(step_bias).replace(",", ".") + "EN"
		self.instrument.write(cmd)
		# -----------------
		# START & STOP BIAS
		# -----------------
		start_bias = CV_parameters["START"]
		stop_bias = CV_parameters["STOP"]
		if stop_bias < start_bias:
			cmd = "TB" + str(stop_bias).replace(",", ".") + "EN"
			self.instrument.write(cmd)
			cmd = "PB" + str(start_bias).replace(",", ".") + "EN"
			self.instrument.write(cmd)
			AUTO_SWEEP = "W4"
		else:
			cmd = "TB" + str(start_bias).replace(",", ".") + "EN"
			self.instrument.write(cmd)
			cmd = "PB" + str(stop_bias).replace(",", ".") + "EN"
			self.instrument.write(cmd)
			AUTO_SWEEP = "W2"
		# not_change = False
		# if "NOT_CHANGE" in CV_parameters:
		# 	not_change = CV_parameters["NOT_CHANGE"]
		# if not_change:
		# 	if PN==1:
		# 		cmd = "TB" + str(abs(stop_bias)*-1).replace(",",".") + "EN"
		# 		self.instrument.write(cmd)
		# 		cmd = "PB" + str(abs(start_bias)).replace(",",".") + "EN"
		# 		self.instrument.write(cmd)
		# 	else:
		# 		cmd = "TB" + str(abs(start_bias)*-1).replace(",",".") + "EN"
		# 		self.instrument.write(cmd)
		# 		cmd = "PB" + str(abs(stop_bias)).replace(",",".") + "EN"
		# 		self.instrument.write(cmd)
		# else:
		# 	cmd = "TB" + str(start_bias).replace(",",".") + "EN"
		# 	self.instrument.write(cmd)
		# 	cmd = "PB" + str(stop_bias).replace(",",".") + "EN"
		# 	self.instrument.write(cmd)


		
		
		cmd = "AB W1 T3" # AB: sweep abort, W1: sweep auto, T3: TRIGGER HOLD/MANUAL
		self.instrument.write(cmd)
		cmd = AUTO_SWEEP
		self.instrument.write(cmd)
		# cmd = "W2" # W2: AUTO SWEEP START UP , or W4?
		# if PN==1:
		# 	cmd = "W4" # PN=1
		# self.instrument.write(cmd)

		return True


	def config_CW(self,CW_parameters):
		# CW_parameters dictionary with:
		# "START" (kHz) (from 0.005 to 13000), "STOP"(kHz), "STEP" (kHz) (from 0.000001 to 13000), "OSC" (mV from 5 to 1100), "SPOT" (-35 to 35 V), 
		# Optional: "CIRCUIT_MODE" (Series/Paralell), "AVERAGE" (True/False), "LOG" (True/False)
		
		# FIRST CHECK PARAMETERS
		if "START" in CW_parameters and "STOP" in CW_parameters and "STEP" in CW_parameters and "OSC" in CW_parameters and "SPOT" in CW_parameters:
			# parameters passed
			if 0.005 <= CW_parameters["START"] <= 13000:
				if 0.005 <= CW_parameters["STOP"] <= 13000:
					if 0.000001 <= CW_parameters["STEP"] <= 13000:
						if 5 <= CW_parameters["OSC"] <= 1100:
							if not -35 <= CW_parameters["SPOT"] <= 35:
								print("SPOT not in range (-35V, 35V): " + str(CW_parameters["SPOT"]))
								return False		
						else:
							print("OSCILLATION LEVEL not in range (5mV, 1100mv): " + str(CW_parameters["OSC"]))
							return False		
					else:
						print("STEP FREQ not in range (0.000001kHz, 13000kHz): " + str(CW_parameters["STEP"]))
						return False
						
				else:
					print("STOP FREQ not in range (0.005kHz, 13000kHz): " + str(CW_parameters["STOP"]))
					return False
			else:
				print("START FREQ not in range (0.005kHz, 13000kHz): " + str(CW_parameters["START"]))
				return False
		else:
			print("Parameters config CV not passed!")
			return False
		# ------------
		# CIRCUIT MODE
		# ------------
		circuit_mode = "C1" # Auto 
		if "CIRCUIT_MODE" in CW_parameters:
			if CW_parameters["CIRCUIT_MODE"]=="Parallel":
				circuit_mode = "C3"
			if CW_parameters["CIRCUIT_MODE"] == "Series":
				circuit_mode = "C2"

        # --------
		# DISPLAY
		# --------
		cmd = "A4 B3 " + circuit_mode + " F1" # A4: Display A = C, B3: Display B = R/G, F1: Display A/B/C
		self.instrument.write(cmd)

		# -----------------
		# OSCILLATION LEVEL
		# -----------------
		oscillation_level = float(CW_parameters["OSC"]*1000)
		cmd = "OL" + str(oscillation_level) + "EN"
		self.instrument.write(cmd)
		# ---------
		# AVERAGE (normally off - V0)
		# ---------
		if "AVERAGE" in CW_parameters:
			if CW_parameters["AVERAGE"]:
				self.average("ON") 
			else:
				self.average("OFF")
		else:
			self.average("ON") # default ON in CW measurements
		# -------------
		# SPOT VOLTAGE
		# ------------
		spot = CW_parameters["SPOT"]
		cmd = "BI" + str(spot) + "EN"
		self.instrument.write(cmd)
		
		
		# -----------------
		# START & STOP FREQ
		# -----------------
		start_freq = CW_parameters["START"]
		stop_freq = CW_parameters["STOP"]
		cmd = "TF" + str(start_freq) + "EN"
		self.instrument.write(cmd)
		cmd = "PF" + str(stop_freq) + "EN"
		self.instrument.write(cmd)
		# ---------
		# STEP FREQ
		# ---------
		step_freq = abs(CW_parameters["STEP"]) # always positive
		cmd = "SF" + str(step_freq) + "EN"
		self.instrument.write(cmd)
		
		
		# ---------
		# LOG (normally on in CW - G1)
		# ---------
		if "LOG" in CW_parameters:
			if CW_parameters["LOG"]:
				self.log("ON") 
			else:
				self.log("OFF")
		else:
			self.log("ON") # default ON

		cmd = "AB W1 T3" # AB: sweep abort, W1: sweep auto, T3: TRIGGER HOLD/MANUAL
		self.instrument.write(cmd)
		cmd = "W2" # W2: AUTO SWEEP START UP (always up in FREQ?)
		self.instrument.write(cmd)

		return True

	def zero_open(self,control):
		# doesn't function in A5, A6, A7 in display A
		cmd="ZO"
		if control=="ON" or control=="1":
			cmd = cmd + "1"
		if control=="OFF" or control=="0":
			cmd = cmd + "0"
		if len(cmd)==3:
			self.instrument.write(cmd)

	def zero_short(self,control):
		# doesn't function in A5, A6, A7 in display A
		cmd="ZS"
		if control=="ON" or control=="1":
			cmd = cmd + "1"
		if control=="OFF" or control=="0":
			cmd = cmd + "0"
		if len(cmd)==3:
			self.instrument.write(cmd)

	def average(self,control):
		# average ON/OFF
		cmd="V"
		if control=="ON" or control=="1":
			cmd = cmd + "1"
		if control=="OFF" or control=="0":
			cmd = cmd + "0"
		if len(cmd)==2:
			self.instrument.write(cmd)

	def log(self,control):
		# log ON/OFF
		cmd="G"
		if control=="ON" or control=="1":
			cmd = cmd + "1"
		if control=="OFF" or control=="0":
			cmd = cmd + "0"
		if len(cmd)==2:
			self.instrument.write(cmd)

	def high_speed(self,control):
		# default code H0 (OFF)
		cmd="H"
		if control=="ON" or control=="1":
			cmd = cmd + "1"
		if control=="OFF" or control=="0":
			cmd = cmd + "0"
		if len(cmd)==2:
			self.instrument.write(cmd)

	def self_test(self):
		# get PASS in DISPLAY A
		cmd="S1"
		self.instrument.write(cmd)		

		
	def log_sweep(self,control):
		# default code G0 (OFF)
		cmd="G"
		if control=="ON" or control=="1":
			cmd = cmd + "1"
		if control=="OFF" or control=="0":
			cmd = cmd + "0"
		if len(cmd)==2:
			self.instrument.write(cmd)
	
	def circuit_mode(self,control):
		# default code AUTO (series) C1, C2 Series, C3 Parallel
		cmd="C"
		if control=="AUTO" or control=="1":
			cmd = cmd + "1"
		if control=="Series" or control=="2":
			cmd = cmd + "2"
		if control=="Parallel" or control=="3":
			cmd = cmd + "3"
		if len(cmd)==2:
			self.instrument.write(cmd)	
		else:
			self.instrument.write("C1")	 # default auto

	def gain_mode(self,control):
		# dBm or dBV, these codes cannot be used when DISPLAY A is set to A1, A2, A3 or A4
		cmd="N"
		if control=="dBm" or control=="1":
			cmd = cmd + "1"
		if control=="dBV" or control=="2":
			cmd = cmd + "2"
		if len(cmd)==2:
			self.instrument.write(cmd)				

	def single(self):
		cmd = "EX" # execute
		self.instrument.write(cmd)

	def read(self):
		return self.instrument.read()
		

	def stop(self):
		cmd = "AB I0" # sweep abort and DC BIAS OFF
		self.instrument.write(cmd)




