# HP4155B instrument driver
import pyvisa
import time


class HP_4155B:
	# destinations = INTernal|NET1|NET2|NET3|NET4
	destinations = ["INT", "NET1", "NET2", "NET3", "NET4"]

	def __init__(self, parameters):
		"""
		Init instrument
		:param parameters: dictionary with parameters
		:return: None
		"""
		rm = pyvisa.ResourceManager()
		inst = rm.open_resource(parameters["address"])
		self.instrument = inst
		self.address = parameters["address"]
		self.read_termination(parameters["read_termination"])
		self.write_termination(parameters["write_termination"])
		if "timeout" in parameters:
			self.timeout(int(parameters["timeout"]))

	def reset(self):
		"""
		Reset instrument
		"""
		self.instrument.write('*RST')

	def timeout(self,timeout):
		self.instrument.timeout = timeout

	def read_termination(self, read_termination):
		"""
		Set read termination character
		:param read_termination: termination character
		"""
		self.instrument.read_termination = read_termination

	def write_termination(self, write_termination):
		"""
		Set write termination character
		:param write_termination: termination character
		:return: None
		"""
		self.instrument.write_termination = write_termination

	def idn(self):
		"""
		Identification
		:return: identification string
		"""
		return self.instrument.query('*IDN?')

	def srq(self):
		"""
		Service request
		"""
		self.instrument.write('*STB?')

	def wait(self):
		"""
		Wait until all operations are completed
		"""
		self.instrument.write('*WAI')

	def load_mes(self, destination, namefile):
		"""
		Load MES file
		:param destination: INTernal|NET1|NET2|NET3|NET4
		:param namefile: name of file
		:return: None
		"""
		cmd = ":MMEM:DEST " + destination
		self.instrument.write(cmd)
		cmd = ":MMEM:LOAD:STAT 0, '" + namefile + "'"
		self.instrument.write(cmd)

	def view_graph(self):
		"""
		View graph
		"""
		cmd = ":PAGE:GRAP"
		self.instrument.write(cmd)

	def autoscale(self):
		"""
		Autoscale
		"""
		cmd = ":PAGE:GLIS:SCAL:AUTO ONCE"
		self.instrument.write(cmd)	

	def marker(self, state):
		"""
		Marker on/off
		:param state: ON|OFF|1|0
		:return: None
		"""
		if state == "ON" or state == "OFF" or state == "1" or state == "0":
			cmd = ":PAGE:GLIS:MARK:STAT " + state
			self.instrument.write(cmd)

	def view_errors(self):
		"""
		View errors
		:return: list of errors
		"""
		cmd = ":SYST:ERR?"
		self.instrument.write(cmd)
		txtError = self.instrument.read()
		sysError =  txtError.split(",")
		# en sysError(0) tenemos código error y en sysError(1) tenemos el mensaje de error
		return sysError

	def single(self):
		"""
		Single measurement
		"""
		cmd = ":PAGE:SCON:SING"
		self.instrument.write(cmd)

	def append(self):
		"""
		Append measurement
		"""
		cmd = ":PAGE:SCON:APP"
		self.instrument.write(cmd)

	def repeat(self):
		"""
		Repeat measurement
		"""
		cmd = ":PAGE:SCON:REP"
		self.instrument.write(cmd)

	def stop(self):
		"""
		Stop measurement
		"""
		cmd = ":PAGE:SCON:STOP"
		self.instrument.write(cmd)

	def dataReady(self):
		"""
		Wait until data is ready
		"""
		cmd = ":PAGE:SCON:STAT?"
		res = self.instrument.query(cmd)
		while res != 'IDLE':
			res = self.instrument.query(cmd)
			time.sleep(0.1)	

	def integration_time(self, type):
		"""
		Set integration time
		:param type: SHORt|MEDium|LONG
		:return: None
		"""
		if type != "SHOR" and type != "MED" and type != "LONG":
			type = "MED"
		cmd = ":PAGE:MEAS:MSET:ITIM " + type
		self.instrument.write(cmd)

	def save_result(self, destination, namefile, delimiter="TAB"):
		"""
		Save result
		:param destination: INTernal|NET1|NET2|NET3|NET4
		:param namefile: name of file
		:param delimiter: SPACe|TAB|COMMa
		:return: None
		"""
		if destination in self.destinations:
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
			time.sleep(3)

	def refresh_net(self, MES_parameters):
		"""
		Refresh NET
		"""
		destinationUpdate = MES_parameters["NET_UPDATE"]
		destination = MES_parameters["NET"]
		time.sleep(2)
		cmd = ":MMEM:DEST " + destinationUpdate
		self.instrument.write(cmd)
		time.sleep(5)
		cmd = ":MMEM:DEST " + destination
		self.instrument.write(cmd)
		time.sleep(5)

	@staticmethod
	def move_files_txt(MES_parameters):
		"""
		Move files from NET to disk path
		:param MES_parameters: dictionary with parameters
		:return: None
		"""
		import shutil
		import os
		# get path from MES_parameters
		path = MES_parameters["FITXERS_FOLDER"]
		destination = MES_parameters["DISK_FOLDER"]
		# move files from NET to disk path
		for file in os.listdir(destination):
			if file.endswith(".txt"):
				shutil.move(os.path.join(destination, file), os.path.join(path, file))


