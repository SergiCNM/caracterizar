# KARLSUSS PA200 prober driver
import pyvisa
import time
import serial
from config.default.devices import * 
from config.default.instruments import *

class KARLSUSS_PA200:
	def __init__(self,parameters):
		rm = pyvisa.ResourceManager()
		inst = rm.open_resource(parameters["address"])
		self.instrument = inst
		self.address = parameters["address"]
		self.read_termination(parameters["read_termination"])
		self.write_termination(parameters["write_termination"])
		ser = CNM_RELAYS(instruments["CNM_RELAYS"])
		self.ser = ser
		if parameters["soft_contact"]:
			# configure KARLSUSS contact
			self.velocity = 25
			self.timeout(parameters["read_termination"]*3) # put mote timeout
		else:
			self.velocity = 100
			self.timeout(parameters["read_termination"]) # put timeout GPIB in 10 seconds

	def idn(self):
		try:
			return self.instrument.query('*IDN?')
		except:
			return ""

	def timeout(self,time):
		if isinstance(time,int):
			self.instrument.timeout = float(time*1000)


	def read_termination(self,read_termination):
		self.instrument.read_termination = read_termination

	def write_termination(self,write_termination):
		self.instrument.write_termination = write_termination
		

	
	def local(self):
		self.instrument.write('*LOCAL')

	def remote(self):
		self.instrument.write('*REMOTE')

	def dataready(self):
		cmd = "*OPC?"
		free = self.instrument.query(cmd)
		while free=="0":
			free = self.instrument.query(cmd)
			qApp.processEvents()
			time.sleep(0.1)
		return free # if ok returns "1"

	def get_chuck_xy(self,reference):
		try:
			reference_array = ["Zero","Home","Center"]
			if reference in reference_array:
				cmd = "ReadChuckPosition Y " + reference[0:1] # first letter
				response = self.instrument.query(cmd) # return new X & Y [um] float respect to Center,Home or Zero
				response_array = response.split(" ")
				if len(response_array)==4 and response_array[0]=="0:":
					return [response_array[1] , response_array[2]]
				return False
		except:
			print("Alert, problem with command get chuck xy")
			return False

	def get_chuck_z(self,reference):
		try:
			reference_array = ["Zero","Home","Center"]
			if reference in reference_array:
				cmd = "ReadChuckPosition Y " + reference[0:1] # first letter
				response = self.instrument.query(cmd) # return new Z [um] float respect to Center,Home or Zero
				response_array = response.split(" ")
				if len(response_array)==4 and response_array[0]=="0:":
					return response_array[3]
				return False
		except:
			print("Alert, problem with command get chuck z")
			return False

	def get_chuck_site_heights(self,reference):
		# always make progressive contact in Wafer (0)
		# function return height Contact, Separation, Overtravel, Hover
		try:
			reference_array = ["Wafer","AuxRight","AuxLeft","AuxRight2","AuxLeft2","0","1","2","3","4"]
			if reference in reference_array:
				cmd = "ReadChuckHeights Y"
				response = self.instrument.query(cmd) 
				response_array = response.split(",")
				# response array gets: contact, overtravel, aligndist, sepdist, load, EdgeTo
				if len(response_array)==6:
					if response_array[0]=="0:" and response_array[1]!="-1": #if command ok and contact is set
						contact_height = response_array[1]
						separation_height = contact_height - response_array[4] # SepDist
						overtravel = response_array[2]
						hover = response_array[5]
						return [contact_height , separation_height , overtravel , hover]
				return False
		except:
			print("Alert, problem with command get chuck site heights")
			return False

	def move_chuck_xy(self,reference,x,y):
		reference_array = ["Zero","Home","Relative","Center","Z","H","R","C"]
		if reference in reference_array:
			cmd = "MoveChuck " + str(x) + " " + str(y) + " " + reference[0:1]
			return self.instrument.query(cmd)

	def move_chuck_z(self,reference,z):
		# Moves chuck z relative to a reference point. Movement over maximum permitted height is not 
		# carried out. Maximum permitted height is defined as follows:
		#  Overtravel disabled & Contact height is not set: Max z motion level.
		#  Overtravel disabled & Contact height is set: Contact height.
		#  Overtrevel enabled & Contact height is not set: Max z motion level.
		#  Overtravel enabled & Contact height is set: Contact height + overtravel gap
		reference_array = ["Zero","Contact","Separation","Relative","Z","H","R","C"]
		if reference in reference_array:
			cmd = "MoveChuckZ  " + str(z) + " " + reference[0:1] + " Y " + self.velocity
			return self.instrument.query(cmd) # returns new Z

	def move_home(self):
		try:
			cmd = "MoveChuck 0 0 H"
			response = self.instrument.query(cmd) # return new X & Y [um] float respect to zero		
			response_array = response.split(" ")
			if len(response_array)==1:
				if response_array[0]=="0:":
					return self.get_chuck_xy("Zero")
			return False
		except:
			print("Alert, problem with command move home")
			return False

	def move_center(self):
		try:
			cmd = "MoveChuck 0 0 Z"
			response = self.instrument.query(cmd) # return new X & Y [um] float respect to zero		
			response_array = response.split(" ")
			if len(response_array)==1:
				if response_array[0]=="0:":
					return self.get_chuck_xy("Zero")
			return False
		except:
			print("Alert, problem with command move center")
			return False

	def move_contact(self):
		try:
			cmd = "MoveChuckContact"
			response = self.instrument.query(cmd) # return new Z[um] float respect to zero
			response_array = response.split(" ")
			if len(response_array)==1:
				if response_array[0]=="0:":
					return self.get_chuck_z("Zero")
			return False
		except:
			print("Alert, problem with command move contact")
			return False

	def move_separation(self):
		try:
			cmd = "MoveChuckSeparation"
			response = self.instrument.query(cmd) # return new Z[um] float respect to zero
			response_array = response.split(" ")
			if len(response_array)==1:
				if response_array[0]=="0:":
					return self.get_chuck_z("Zero")
			return False
		except:
			print("Alert, problem with command move separation")
			return False

	def stop(self):
		cmd = "StopChuckMovement 7" # stop movement in all axis (Byte0 Xaxis, Byte1 Yaxis, Byte2 Zaxis)
		self.instrument.query(cmd)		
		retval = QMessageBox.critical(
            self,
            "ALERT",
            "Stop button pressed, unload sample to be safe!",
            buttons=QMessageBox.Ok  ,
            defaultButton=QMessageBox.Ok,
        )


	def light(self,mode):
		try:
			if str(mode)=="1" or str(mode)=="0":
				# control by serial port (RELE 1)
				self.ser.light(mode)


		except:
			print("Alert, problem with command light")
			return False

	def set_vacuum(self,mode):
		try:
			if str(mode)=="1" or str(mode)=="0":
				cmd = "SetChuckVacuum " + str(mode)
				response = self.instrument.query(cmd)	
				response_array = response.split(" ")
				if len(response_array)==1 and response_array[0]=="0:": # if ok return: 0:
					return True
			return False
		except:
			print("Alert, problem with command vacuum")
			return False

	def get_vacuum_status(self,reference):
		# return 0 (OFF) or 1 (ON) en byte 5
		try:
			reference_array = ["Wafer","AuxRight","AuxRight2","AuxLeft","AuxLeft2"]
			if reference in reference_array:
				cmd = "ReadChuckStatus"
				response = self.instrument.query(cmd)
				response_array = response.split(" ")
				if len(response_array)==11:
					if response_array[0]=="0:":
						return response_array[6]
				return False
		except:
			print("Alert, problem with command get vacuum status")
			return False

	def image(self,path,scale):
		# not implemented
		try:
			return False
		except:
			print("Alert, problem with command image")
			return False

	

