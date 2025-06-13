# Keysight B1500 instrument driver
import pyvisa
import time


class Keysight_B1500:
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

	def sqr(self):
		self.instrument.write('*STB?')

	def wait(self):
		self.instrument.write('*WAI')

	def self_calibration(self):
		calibration = self.instrument.query('*CAL?')
		if calibration!=0:
			return False
		return True
	
	def self_test(self):
		code = self.instrument.query('*TST?')
		if code!=0:
			return False
		return True

	def dataready(self):
		cmd = "*OPC?"
		res = self.instrument.query(cmd)
		while res.replace("\r","")!='1':
			#qApp.processEvents()
			res = self.instrument.query(cmd)
			time.sleep(0.5)	

	def error(self,mode=0):
		# get error: 0 reads error in queue, 1 reads one error code from the head of the error
		cmd = "ERR? "
		if int(mode)==0 or int(mode)==1:
			cmd = cmd + str(mode)
			return self.instrument.query(cmd)

	def filter(self,mode):
		if int(mode)==0 or int(mode)==1:
			self.instrument.write("FL " + str(mode))

	def enable_channels(self,channel="all"):
		cmd = "CN"
		if channel!="all":
			if int(channel)>=1 and int(channel)<=4:
				cmd = cmd + " " + strt(channel)
		self.instrument.write(cmd)

	def disable_channels(self,channel="all"):
		cmd = "CL"
		if channel!="all":
			if int(channel)>=1 and int(channel)<=4:
				cmd = cmd + " " + str(channel)
		self.instrument.write(cmd)	

	def force_0V(self,channel="all"):
		cmd = "DZ"
		if channel!="all":
			if int(channel)>=1 and int(channel)<=4:
				cmd = cmd + " " + strt(channel)
		self.instrument.write(cmd)	

	def set_data_output_format(self,format,mode=0):
		formats =[1,2,3,4,5,11,12,13,14,15,21,22,25]
		cmd = "FMT "
		if format in formats:
			cmd = cmd + str(format)
			if mode>=00 and mode<=10:
				cmd = cmd + "," + str(mode)
			self.instrument.write(cmd)

	def auto_calibration(self,mode):
		# set autocalibration on/off
		if int(mode)==0 or int(mode)==1:
			cmd = "CM " + str(mode)
			self.instrument.write(cmd)

	def single(self):
		cmd = "XE"
		self.instrument.write(cmd)

	def abort(self):
		# abort command execution
		cmd = "AB"
		self.instrument.write(cmd)	

	def information_modules(self):
		# return information of all modules
		return self.instrument.query("UNT?")


	def solarmems_meas(self):
		# disable auto_calibration
		self.auto_calibration(0)
		# enable all channels
		self.enable_channels()
		# filter off
		self.filter(0)
		# configure channels
		code = "MM 16,2,3,4,5" # smus 1-4 (slots 2-5) to Multi channel sweep (mode 16)
		self.instrument.write(code)
		# set hold & delaty time to 0
		self.instrument.write("WT 0,0")

		
	def integration_time(self,type):
		if type!="SHOR" and type!="MED" and type!="LONG":
			type = "MED"
		cmd = ":PAGE:MEAS:MSET:ITIM " + type
		self.instrument.write(cmd)


	def save_result(self,destination,namefile, delimiter = "TAB"):
		# destination = INTernal|NET1|NET2|NET3|NET4
		destination_array = ["INT","NET1","NET2","NET3","NET4"]
		if destination in destination_array:
			cmd = ":MMEM:DEST " + destination
			self.instrument.write(cmd)
			# set delimiter (SPACe, TAB, COMMa)
			cmd = ":MMEM:STOR:SSH:DEL " + delimiter
			self.instrument.write(cmd)
			# save all values
			cmd = ":MMEM:STOR:SSH:LIND 1,MAX"
			self.instrument.write(cmd)
			# no marks
			cmd = ":MMEM:STOR:SSH:SMARK NONE"
			self.instrument.write(cmd)
			# no units
			cmd = ":MMEM:STOR:SSH:UNIT OFF"
			self.instrument.write(cmd)
			# file name
			cmd = ":MMEM:STOR:SSH '" + namefile + "'"
			self.instrument.write(cmd)
	


