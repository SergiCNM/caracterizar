# Keysight E4990A instrument driver
import pyvisa
import time
import numpy as np
from PySide6.QtWidgets import QMessageBox


class Keysight_E4990A:
	def __init__(self,parameters):
		rm = pyvisa.ResourceManager()
		inst = rm.open_resource(parameters["address"])
		self.instrument = inst
		self.address = parameters["address"]
		self.read_termination(parameters["read_termination"])
		self.write_termination(parameters["write_termination"])
		self.timeout(int(parameters["timeout"]))
		print(self.idn())
		print(self.error())
		# self.stop()
		self.clear()
		#self.reset()
		# self.instrument.buffer_read = 2048


	def reset(self):
		self.instrument.write('*RST')

	def clear(self):
		self.instrument.write('*CLS')

	def clear_buffer(self):
		self.instrument.write(':MEM:CLE DBUF')

	def read_termination(self,read_termination):
		self.instrument.read_termination = read_termination

	def write_termination(self,write_termination):
		self.instrument.write_termination = write_termination

	def timeout(self, timeout):
		"""
        Set timeout
        :param timeout: time in ms
        :return: None
        """
		self.instrument.timeout = timeout

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

	def autoscale(self, traces=2):
		for i in range(1, traces+1):
			self.instrument.write(f':DISP:WIND1:TRAC{str(i)}:Y:AUTO')
			time.sleep(1)
		#self.instrument.write(':DISP:WIND1:TRAC2:Y:AUTO')

	def opc(self):
		return self.instrument.query('*OPC?')

	def error(self):
		return self.instrument.query(':SYST:ERR?')

	def config_CV(self, CV_parameters):
		# CV_parameters dictionary with:
		# "START" (V) (from -35 to 35), "STOP"(V), "NUM_POINTS" (V) (from 2 to 1601), "OSC" (mV from 5 to 1000), "FREQ" (kHz from 0.02 to 20000),

		# FIRST CHECK PARAMETERS
		if "START" in CV_parameters and "STOP" in CV_parameters and "NUM_POINTS" in CV_parameters and "OSC" in CV_parameters and "FREQ" in CV_parameters:
			# parameters passed
			if -40 <= CV_parameters["START"] <= 40:
				if -40 <= CV_parameters["STOP"] <= 40:
					if 2 <= CV_parameters["NUM_POINTS"] <= 1601:
						if 5 <= CV_parameters["OSC"] <= 1000:
							if not 0.02 <= CV_parameters["FREQ"] <= 20000:
								print("FREQUENCY not in range (0.02kHz, 20000kHz): " + str(CV_parameters["FREQ"]))
								return False		
						else:
							print("OSCILLATION LEVEL not in range (5mV, 1000mv): " + str(CV_parameters["OSC"]))
							return False		
					else:
						print("NUM POINTS not in range (2, 1601): " + str(CV_parameters["NUM_POINTS"]))
						return False
						
				else:
					print("STOP BIAS not in range (-40V, 40V): " + str(CV_parameters["STOP"]))
					return False
			else:
				print("START BIAS not in range (-40V, 40V): " + str(CV_parameters["START"]))
				return False
		else:
			print("Parameters config CV not passed!")
			return False

		if CV_parameters["WAIT_TIME"]>=0.0 and CV_parameters["WAIT_TIME"]<=30:
			self.instrument.write(f':SENS1:SWE:DEL {CV_parameters["WAIT_TIME"]}')
		else:
			print("Wait time not in range (0 - 30 s")
		PN = -1
		if CV_parameters["START"] > CV_parameters["STOP"]:
			PN = 1
		CV_parameters["PN"] = PN
		# -----------------
		# CONFIGURATION CV
		# -----------------
		if (CV_parameters["GRAPH2"]!="NONE"):
			self.instrument.write(':DISP:WIND1:SPL D1_2')  # Split Display
			self.instrument.write(f':CALC1:PAR2:DEF {CV_parameters["GRAPH2"]}')  # Calculate G
		else:
			self.instrument.write(':DISP:WIND1:SPL D1')
		self.instrument.write(f':CALC1:PAR1:DEF {CV_parameters["GRAPH1"]}')  # Calculate Cp
		# self.instrument.write(':CALC1:PAR2:DEF G')  # Calculate G
		self.instrument.write(f':SOUR1:VOLT:LEV {CV_parameters["OSC"]*1e-3}')  # Set Oscillation Level
		self.instrument.write(f':SENS1:FREQ {CV_parameters["FREQ"]*1e3}')  # Set Oscillation Frequency
		self.instrument.write(':SENS1:SWE:TYPE BIAS')  # Set Sweep Type to Bias
		start = CV_parameters["START"]
		stop = CV_parameters["STOP"]
		if CV_parameters["START"]>CV_parameters["STOP"]:
			self.instrument.write(f':SENS1:SWE:DIR DOWN')
			start, stop = stop, start
		else:
			self.instrument.write(f':SENS1:SWE:DIR UP')

		self.instrument.write(f':SENS1:SWE:POIN {CV_parameters["NUM_POINTS"]}')  # Set Number of Points per Sweep
		self.instrument.write(f':SOUR1:BIAS:VOLT:STAR {start}')  # Set Start Voltage
		self.instrument.write(f':SOUR1:BIAS:VOLT:STOP {stop}')  # Set Stop Voltage
		self.instrument.write(f':SENS1:APER {CV_parameters["APERTURE"]}')  # Set measurement speed
		self.instrument.write(f':SENS1:AVER:COUN {CV_parameters["AVERAGE_POINTS"]}')  # Set Point Averaging Count
		self.instrument.write(f':SENS1:AVER:STAT {1 if CV_parameters["POINT_AVERAGE"] else 0}')  # Enable/Disable Point Averaging
		self.instrument.write(f':CALC1:AVER:COUN {CV_parameters["AVERAGE_SWEEPS"]}')  # Set Sweep Averaging Count
		self.instrument.write(f':CALC1:AVER:STAT {1 if CV_parameters["SWEEP_AVERAGE"] else 0}')  # Enable/Disable Sweep Averaging


		return True

	def measure(self, parameters):
		try:
			#self.instrument.write(':SENS1:DC:MEAS:CLE')
			# self.instrument.write(':CALC1:AVER:CLE')
			self.instrument.write(':SOUR:BIAS:STAT ON')  # Turn on Bias
			self.instrument.write(':TRIG:SOUR BUS')
			self.instrument.write(':INIT1:CONT OFF')
			self.instrument.write(':INIT:IMM')
			self.instrument.write(':TRIG:SING')
			numQueries = 0
			numQueriesAutoscale = 10  # 0 for never autoscaling
			# while True:
			# 	time.sleep(1)
			# 	print("check opc...")
			# 	opc = self.opc()
			# 	print(f'opc = {opc}')
			# 	if opc == '+1':
			# 		break
			# 	if numQueriesAutoscale > 0:
			# 		numQueries += 1
			# 		if numQueries >= numQueriesAutoscale:
			# 			print("autoscale...")
			# 			self.autoscale()
			# 			numQueries = 0
			opc = self.instrument.query('*OPC?') # increase timeout to wait measure finiah
			self.autoscale()
			error = self.error()
			if error != '+0,"No error"':
				print(f"ERROR: {error}")
				self.clear()
			# Read Results
			self.instrument.write(':CALC1:PAR1:SEL')
			self.instrument.write(':FORM:DATA ASC')
			self.instrument.write(':FORM:REAL:ASC:LENG 12')
			r1 = self.instrument.query(':CALC1:SEL:DATA:FDAT?')
			# print(f'r1 = {r1}')
			ra1 = np.fromstring(r1, sep=',')
			self.instrument.write(':CALC1:PAR2:SEL')
			self.instrument.write(':FORM:DATA ASC')
			self.instrument.write(':FORM:REAL:ASC:LENG 12')
			r2 = self.instrument.query(':CALC1:SEL:DATA:FDAT?')
			ra2 = np.fromstring(r2, sep=',')
			rx = self.instrument.query(':CALC1:SEL:DATA:XAX?')
			rax = np.fromstring(rx, sep=',')

			if not parameters["HYSTERESIS"]:
				self.turn_off_bias()

			data = np.zeros((parameters["NUM_POINTS"], 3))
			for u in range(parameters["NUM_POINTS"]):
				data[u, 0] = rax[u]
				data[u, 1] = ra1[2 * u]
				data[u, 2] = ra2[2 * u]

			X = data[:, 0]
			Y1 = data[:, 1]
			Y2 = data[:, 2]

			if parameters["START"] > parameters["STOP"]:
				# invert X, Y1 and Y2
				X = np.flip(X)
				Y1 = np.flip(Y1)
				Y2 = np.flip(Y2)


		except Exception as ex:
			print(f"error ocurred: {ex} ")
			self.stop()

			return [], [], []

		return X, Y1, Y2

	def config_CW(self, CW_parameters):
		# CW_parameters dictionary with:
		# "START" (kHz) (0.02 to 20000), "STOP"(kHz) (0.02 to 20000), "NUM_POINTS" (V) (from 2 to 1601), "OSC" (mV from 5 to 1000), "VOLTAGE" (V) (-40 to 40),

		# FIRST CHECK PARAMETERS
		if "START" in CW_parameters and "STOP" in CW_parameters and "NUM_POINTS" in CW_parameters and "OSC" in CW_parameters and "VOLTAGE" in CW_parameters:
			# parameters passed
			if 0.02 <= CW_parameters["START"] <= 20000:
				if 0.02 <= CW_parameters["STOP"] <= 20000:
					if CW_parameters["STOP"] > CW_parameters["START"]:
						if 2 <= CW_parameters["NUM_POINTS"] <= 1601:
							if -40 <= CW_parameters["VOLTAGE"] <= 40:
								if 1000 < CW_parameters["OSC"] < 5:
									print("OSCILLATION LEVEL not in range (5mV, 1000mv): " + str(CW_parameters["OSC"]))
									return False
							else:
								print("VOLTAGE not in range (-40V, 40V): " + str(CW_parameters["VOLTAGE"]))
								return False
						else:
							print("NUM POINTS not in range (2, 1601): " + str(CW_parameters["NUM_POINTS"]))
							return False
					else:
						print("FREQUENCY STOP is less than FREQUENCY START")
						return False

				else:
					print("FREQUENCY STOP not in range (0.02kHz, 20000kHz): " + str(CW_parameters["STOP"]))
					return False
			else:
				print("FREQUENCY START not in range (0.02kHz, 20000kHz): " + str(CW_parameters["START"]))
				return False
		else:
			print("Parameters config CW not passed!")
			return False

		if CW_parameters["WAIT_TIME"] >= 0.0 and CW_parameters["WAIT_TIME"] <= 30:
			self.instrument.write(f':SENS1:SWE:DEL {CW_parameters["WAIT_TIME"]}')
		else:
			print("Wait time not in range (0 - 30 s")

		# -----------------
		# CONFIGURATION CW
		# -----------------
		if (CW_parameters["GRAPH2"] != "NONE"):
			self.instrument.write(':DISP:WIND1:SPL D1_2')  # Split Display
			self.instrument.write(f':CALC1:PAR2:DEF {CW_parameters["GRAPH2"]}')  # Calculate G
		else:
			self.instrument.write(':DISP:WIND1:SPL D1')
		self.instrument.write(f':CALC1:PAR1:DEF {CW_parameters["GRAPH1"]}')  # Calculate Cp
		# self.instrument.write(':CALC1:PAR2:DEF G')  # Calculate G
		self.instrument.write(f':SOUR1:VOLT:LEV {CW_parameters["OSC"] * 1e-3}')  # Set Oscillation Level
		# self.instrument.write(f':SENS1:FREQ {CW_parameters["FREQ"] * 1e3}')  # Set Oscillation Frequency
		if CW_parameters["LOGFREQ"]:
			self.instrument.write(':SENS1:SWE:TYPE LOG')  # Set Sweep Type to Logarithmic
		else:
			self.instrument.write(':SENS1:SWE:TYPE LIN')  # Set Sweep Type to Linear
		# always UP
		self.instrument.write(f':SENS1:SWE:DIR UP')

		self.instrument.write(f':SENS1:SWE:POIN {CW_parameters["NUM_POINTS"]}')  # Set Number of Points per Sweep
		self.instrument.write(f':SENS1:FREQ:STAR {CW_parameters["START"] * 1e3}')  # Set Start FREQ (kHz)
		self.instrument.write(f':SENS1:FREQ:STOP {CW_parameters["STOP"] * 1e3}')  # Set Stop FREQ (kHz)
		self.instrument.write(f':SENS1:APER {CW_parameters["APERTURE"]}')  # Set measurement speed
		self.instrument.write(f':SENS1:AVER:COUN {CW_parameters["AVERAGE_POINTS"]}')  # Set Point Averaging Count
		self.instrument.write(
			f':SENS1:AVER:STAT {1 if CW_parameters["POINT_AVERAGE"] else 0}')  # Enable/Disable Point Averaging
		self.instrument.write(f':CALC1:AVER:COUN {CW_parameters["AVERAGE_SWEEPS"]}')  # Set Sweep Averaging Count
		self.instrument.write(
			f':CALC1:AVER:STAT {1 if CW_parameters["SWEEP_AVERAGE"] else 0}')  # Enable/Disable Sweep Averaging

		# set VOLTAGE
		self.instrument.write(f':SOUR:BIAS:VOLT {CW_parameters["VOLTAGE"]}')

		return True

	def read(self):
		return self.instrument.read()
		
	def stop(self):
		cmd = ":SOUR:BIAS:STAT OFF" #  DC BIAS OFF
		self.instrument.write(cmd)

	def turn_off_bias(self):
		cmd = ':SOUR:BIAS:STAT OFF' # Turn off Bias
		self.instrument.write(cmd)

	def calibration_type(self, cal_type):
		cal_type = cal_type.upper()
		if cal_type == "OPEN":
			cmd = ":SENS1:CORR1:COLL:TYPE OPEN"
		elif cal_type=="SHORT":
			QMessageBox.warning(
				self,
				"Short Calibration",
				"Please, connect the SHORT calibration standard to the instrument",
				buttons=QMessageBox.Ok,
				defaultButton=QMessageBox.Ok,
			)
			cmd = ":SENS1:CORR1:COLL:TYPE SHOR"
		elif cal_type=="LOAD":
			QMessageBox.warning(
				self,
				"Load Calibration",
				"Please, connect the LOAD calibration standard to the instrument",
				buttons=QMessageBox.Ok,
				defaultButton=QMessageBox.Ok,
			)
			cmd = ":SENS1:CORR1:COLL:TYPE LOAD"
		self.instrument.write(cmd)
		opc = self.opc()
		if opc == '+1':
			return True

		return False

	def calibration(self, cal_type=["OPEN"]):
		cal_ok = True
		# Set compensation point to fix
		cmd = ":SENS1:CORR1:COLL:FPO FIX"
		self.instrument.write(cmd)
		cal_types = ["OPEN", "SHORT", "LOAD"]
		for calibration in cal_type:
			calibration = calibration.upper()
			if calibration in cal_types:
				if self.calibration_type(calibration):
					print(f"Calibration type ('{calibration}') set")
				else:
					cal_ok = False
					print(f"Calibration type ('{calibration}') not set")
			else:
				cal_ok = False
				print(f"Calibration type ('{calibration}') not valid")
		# save calibration
		cmd = ":SENS1:CORR1:COLL:SAVE"
		self.instrument.write(cmd)

		return cal_ok
