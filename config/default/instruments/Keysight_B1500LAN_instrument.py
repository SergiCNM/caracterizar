# Keysight B1500 LAN instrument driver
import pyvisa
import time
import sys
import numpy as np
from io import StringIO   # StringIO behaves like a file object

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
		self.instrument.timeout = timeout

	def idn(self):
		return self.instrument.query('*IDN?')

	def dataready(self):
		return self.instrument.query('*OPC?')

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
		data_returned = self.instrument.query(':RES:FET?')
		return data_returned.replace('\\r\\n','\r\n')

	def configure_format(self):
		self.instrument.write(':RES:FORM TEXT') # set output format to text
		self.instrument.write(':RES:FORM:ESC ON') # format escape ON to get all results

	def get_vars(self,texto):
		vars_array = str(texto).split('\r\n')[0].split(",")
		longitud = len(vars_array[1]) -1
		# change var [0]
		vars_array[0] = vars_array[0][len(vars_array)+longitud:] # asume always all variables with the same lengnt

		return vars_array

	def get_data_numpy(self,texto,variables):
		c = StringIO(texto) # crete file object from text
		formats = ['f4'] * len(variables) # all variables are floats
		results = np.loadtxt(c, dtype={'names': variables,
	                     'formats': formats}, delimiter=',')
		return results

	

