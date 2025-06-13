# RELAYS CNM instrument driver
import serial
import time


class CNM_RELAYS:
	def __init__(self,parameters):
		ser = serial.Serial()
		# configure baudrate & port 
		ser.baudrate = parameters["baudrate"] # 19200 (int)
		ser.port = parameters["port"] # 'COM1' (Device name or None)
		# configure timeout
		if "timeout" in parameters: 
			ser.timeout = parameters["timeout"]
		self.address = ser.port
		# configure bytsize, stopbits and parity
		bytesize = self.set_bytesize(parameters["bytesize"])
		if bytesize!="":
			ser.bytesize = bytesize

		stopbits = self.set_stopbits(parameters["stopbits"])
		if stopbits!="":
			ser.stopbits = stopbits
		
		parity = self.set_parity(parameters["parity"])
		if parity!="":
			ser.parity = parity
		

		self.instrument = ser

		if bytesize!="" and stopbits!="" and parity!="":	
			try	:
				ser.open()
				self.open = ser.is_open
			except:
				print("Serial port not opened!")
		else:
			self.open = False

	def set_bytesize(self,bytesize):
		# Possible values: FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
		bytesize_array = { 5 : serial.FIVEBITS, 6 : serial.SIXBITS, 7 : serial.SEVENBITS, 8 : serial.EIGHTBITS}
		if bytesize>=5 and bytesize<=8:
			return bytesize_array[bytesize]
		return ""

	def set_stopbits(self,stopbits):
		# Possible values: STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO
		stopbits_array = { 1 : serial.STOPBITS_ONE, 1.5 : serial.STOPBITS_ONE_POINT_FIVE, 2 : serial.STOPBITS_TWO}
		if stopbits==1 or stopbits==2 or stopbits==1.5:
			return stopbits_array[stopbits]
		return ""

	def set_parity(self,parity):
		# Possible values: PARITY_NONE, PARITY_EVEN, PARITY_ODD PARITY_MARK, PARITY_SPACE
		parity_array = { "none" : serial.PARITY_NONE, "even" : serial.PARITY_EVEN, "odd" : serial.PARITY_ODD, "mark" : serial.PARITY_MARK, "space" : serial.PARITY_SPACE}
		paritys = ["none", "even", "odd", "mark", "space"]
		if parity in paritys:
			return parity_array[parity]
		return ""



	def close(self):
		self.instrument.close()

	def light(self,mode):
		try:
			if str(mode)=="1" or str(mode)=="0":
				packet = bytearray()
				packet.append(0x03)
				packet.append(int(mode))
				self.instrument.write(packet)
				# Antes del return deberíamos comprobar que todo está ok (leer entradas analógicas)
				return True

		except:
			return False

		
