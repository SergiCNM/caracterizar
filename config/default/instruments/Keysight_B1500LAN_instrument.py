# Keysight B1500 LAN instrument driver
import pyvisa
import time
import numpy as np
from io import StringIO

class Keysight_B1500LAN:
	def __init__(self,parameters):
		rm = pyvisa.ResourceManager()
		inst = rm.open_resource(parameters["address"])
		self.instrument = inst
		self.parameters = parameters
		self.address = parameters["address"]
		self.read_termination(parameters["read_termination"])
		self.write_termination(parameters["write_termination"])
		if "timeout" in parameters:
			self.timeout(int(parameters["timeout"]))


	def read_termination(self,read_termination):
		self.instrument.read_termination = read_termination

	def write_termination(self,write_termination):
		self.instrument.write_termination = write_termination

	def timeout(self,timeout):
		print("setting timeout to: ", timeout)
		self.instrument.timeout = timeout

	def idn(self):
		return self.instrument.query('*IDN?')

	def dataready(self, timeout_ms=120000):
		self.instrument.write('*OPC?')
		start = time.time() * 1000
		while (time.time() * 1000) - start < timeout_ms:
			try:
				self.instrument.timeout = 2000
				return self.instrument.read().strip()
			except pyvisa.VisaIOError:
				pass
		raise TimeoutError(f"dataready timed out after {timeout_ms}ms")

	def open_workspace(self,workspace):
		self.instrument.write(':WORK:OPEN "'+workspace+'"')

	def close_workspace(self):
		self.instrument.write(':WORK:CLOS')		

	def status_workspace(self):
		# OPEN or CLOS is returned
		return self.instrument.query(':WORK:STAT?')	

	def get_name_workspace(self):
		# return name of selected workspace => "name"
		return self.instrument.query(':WORK:SEL:NAME?')		

	def open_preset_group(self,group):
		self.instrument.write(':BENCH:PRES:OPEN "'+group+'"')	
	
	def open_test_preset_group(self,test):
		self.instrument.write(':BENCH:PRES:SET:SEL "'+test+'"')	
	
	def get_catalog_preset_group(self):
		return self.instrument.query(':BENCH:PRES:CAT?')

	def get_name_preset_group(self):
		return self.instrument.query(':BENCH:PRES:SEL:NAME?')

	def get_name_setup(self):
		return self.instrument.query(':BENCH:SEL:NAME?')

	def single(self):
		self.instrument.write(':RUN')

	def get_data(self):
		data_returned = self.instrument.query(':RES:FET?').strip()

		if data_returned.startswith('#'):
			n_digits = int(data_returned[1])
			length = int(data_returned[2:2 + n_digits])
			data = data_returned[2 + n_digits:]
		else:
			data = data_returned

		data = data.replace('\\r\\n', '\r\n')

		return data

	def configure_format(self):
		self.instrument.write(':RES:FORM TEXT') # set output format to text
		self.instrument.write(':RES:FORM:ESC ON') # format escape ON to get all results

	def get_vars(self,texto):
		return texto.split('\r\n')[0].split(',')

	def get_data_numpy(self,texto,variables):
		lines = texto.split('\r\n')
		texto = '\r\n'.join(lines[1:])
		c = StringIO(texto)
		formats = ['f4'] * len(variables)
		results = np.genfromtxt(c, dtype={'names': variables,
	                     'formats': formats}, delimiter=',')
		return results

	

