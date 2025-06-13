# LeCroy W62XS instrument driver
import pyvisa
import time


class LeCroy_W62XS:
	def __init__(self,parameters):
		rm = pyvisa.ResourceManager()
		inst = rm.open_resource(parameters["address"])
		self.instrument = inst
		self.address = parameters["address"]
		self.read_termination(parameters["read_termination"])
		self.write_termination(parameters["write_termination"])
		if "timeout" in parameters:
			self.timeout(int(parameters["timeout"]))


	def reset(self):
		self.instrument.write('*RST')

	def read_termination(self,read_termination):
		self.instrument.read_termination = read_termination

	def write_termination(self,write_termination):
		self.instrument.write_termination = write_termination

	def timeout(self,timeout):
		self.instrument.timeout = timeout

	def idn(self):
		return self.instrument.query('*IDN?')

	def measure_osc_peak_freq(self, channel, channel2): # Measure freq and peak to peak
		self.instrument.write("ASET") # Automatic setup.
		self.instrument.write("PACU 1,PKPK,C"+str(channel)) # Measure parameter peak to peak in measure 1
		self.instrument.write("PACU 2,FREQ,C"+str(channel)) # Measure parameter frequency in measure 2
		self.instrument.write("PACU 3,PKPK,C"+str(channel2)) # Measure parameter peak to peak in measure 3
		peak_val_1 = self.instrument.query("PAVA? CUST1") # Get peak value of measure 1
		meas_freq = self.instrument.query("PAVA? CUST2") # Get freq value of measure 2
		peak_val_2 = self.instrument.query("PAVA? CUST3") # Get peak value of measure 3
		peak_val_1 = peak_val_1[10:len(peak_val_1)] # Format data
		peak_val_1 = float(peak_val_1[0:peak_val_1.index(" V,")]) # Format data
		meas_freq = meas_freq[10:len(meas_freq)] # Format data
		meas_freq = float(meas_freq[0:meas_freq.index(" HZ,")]) # Format data
		peak_val_2 = peak_val_2[10:len(peak_val_2)] # Format data
		peak_val_2 = float(peak_val_2[0:peak_val_2.index(" V,")]) # Format data

		return peak_val_1, peak_val_2, meas_freq

	def screenshot_osc(self): # Take a screenshot, return the PNG binary file content

		self.instrument.write("HCSU DEV, PNG, FORMAT,PORTRAIT, BCKG, WHITE, DEST, REMOTE, PORT, NET, AREA,GRIDAREAONLY")
		self.instrument.write("SCDP")

		return self.instrument.read_raw()