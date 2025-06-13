# MPI TS2000SE prober driver
import pyvisa
import time


class MPI_TS2000SE:
	def __init__(self, parameters):
		rm = pyvisa.ResourceManager()
		inst = rm.open_resource(parameters["address"])
		self.instrument = inst
		self.address = parameters["address"]
		self.read_termination(parameters["read_termination"])
		self.write_termination(parameters["write_termination"])
		self.timeout(parameters["timeout"])
		if parameters["soft_contact"]:
			# configure MPI contact (first call read_termination & write_termination)
			self.set_soft_contact(1)
			self.set_stepping_contact_mode("StepToSeparation")
		else:
			self.set_soft_contact(0)
			self.set_stepping_contact_mode("StepToSeparation")

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
		
	def set_soft_contact(self,mode):
		# 0 for optimize for speed, and 1 for optimize for accuracy
		if str(mode)=="1" or str(mode)=="0":
			cmd = "set_soft_contact " + str(mode)
			response = self.instrument.query(cmd) # if ok return: 0,0,OK
			if response.split(",")[2]=="OK":
				return True
		return False

	def set_stepping_contact_mode(self,mode):
		# BackToContact optimize for speed/accuracy, LockContact for safety
		if mode=="BackToContact" or mode=="StepToSeparation" or mode=="LockContact":
			cmd = "set_stepping_contact_mode " + str(mode)
			response = self.instrument.query(cmd) # if ok return: 0,0,OK
			if response.split(",")[2]=="OK":
				return True
		return False
	
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

	def get_chuck_xy(self, reference):
		try:
			reference_array = ["Zero","Home","Current","Center"]
			if reference in reference_array:
				cmd = "get_chuck_xy Wafer," + reference
				response = self.instrument.query(cmd) # return new X & Y [um] float respect to Center,Current,Home or Zero
				response_array = response.split(",")
				if len(response_array)==4:
					if response_array[0]=="0" and response_array[1]=="0":
						return [response_array[2] , response_array[3]]
				return False
		except:
			print("Alert, problem with command get chuck xy")
			return False

	def get_chuck_z(self,reference):
		try:
			reference_array = ["Zero","Contact","Separation"]
			if reference in reference_array:
				cmd = "get_chuck_z " + reference
				response = self.instrument.query(cmd) # return Z [um] float respect to Zero, Contact or Separation
				response_array = response.split(",")
				if len(response_array)==3:
					if response_array[0]=="0" and response_array[1]=="0":
						return response_array[2]
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
				cmd = "get_chuck_site_heights " + reference
				response = self.instrument.query(cmd) 
				response_array = response.split(",")
				if len(response_array)==6:
					if response_array[0]=="0" and response_array[1]=="0":
						return [response_array[2] , response_array[3] , response_array[4] , response_array[5]]
				return False
		except:
			print("Alert, problem with command get chuck site heights")
			return False

	def move_chuck_xy(self,reference,x,y):
		reference_array = ["Zero","Home","Relative","Center","User","Z","H","R","C"]
		if reference in reference_array:
			cmd = "move_chuck_xy  " + reference + "," + str(x) + "," + str(y)
			return self.instrument.query(cmd)

	def move_chuck_z(self,reference,z):
		# Moves chuck z relative to a reference point. Movement over maximum permitted height is not 
		# carried out. Maximum permitted height is defined as follows:
		#  Overtravel disabled & Contact height is not set: Max z motion level.
		#  Overtravel disabled & Contact height is set: Contact height.
		#  Overtrevel enabled & Contact height is not set: Max z motion level.
		#  Overtravel enabled & Contact height is set: Contact height + overtravel gap
		reference_array = ["Zero","Contact","Separation","Relative"]
		try:
			if reference in reference_array:
				cmd = "move_chuck_z  " + reference + "," + str(z)
				response = self.instrument.query(cmd) 
				response_array = response.split(",")
				if len(response_array)==3:
					if response_array[0]=="0" and response_array[1]=="0":
						return response_array[2] # returns new Z
			else:
				print("Reference passed not in array!")
			return False
		except:
			print("Alert, problem with command move chuck z")
			return False

	def move_home(self):
		try:
			cmd = "move_chuck_home"
			response = self.instrument.query(cmd) # return new X & Y [um] float respect to zero		
			response_array = response.split(",")
			if len(response_array)==4:
				if response_array[0]=="0" and response_array[1]=="0":
					return [response_array[2] , response_array[3]]
			return False
		except:
			print("Alert, problem with command move home")
			return False

	def move_center(self):
		try:
			cmd = "move_chuck_center"
			response = self.instrument.query(cmd) # return new X & Y [um] float respect to zero
			response_array = response.split(",")
			if len(response_array)==4:
				if response_array[0]=="0" and response_array[1]=="0":
					return [response_array[2] , response_array[3]]
			return False
		except:
			print("Alert, problem with command move center")
			return False

	def move_contact(self):
		try:
			cmd = "move_chuck_contact"
			response = self.instrument.query(cmd) # return new Z[um] float respect to zero
			response_array = response.split(",")
			if len(response_array)==3:
				if response_array[0]=="0" and response_array[1]=="0":
					return response_array[2]
			return False
		except:
			print("Alert, problem with command move contact")
			return False

	def move_separation(self):
		try:
			cmd = "move_chuck_separation"
			response = self.instrument.query(cmd) # return new Z[um] float respect to zero
			response_array = response.split(",")
			if len(response_array)==3:
				if response_array[0]=="0" and response_array[1]=="0":
					return response_array[2]
			return False
		except:
			print("Alert, problem with command move contact")
			return False

	def stop(self):
		cmd = "stop_chuck_xyz"
		self.instrument.write(cmd)		
		self.instrument.read_stb() # per fer el serial poll
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
				cmd = "vis:switch_light Scope," + str(mode)
				response = self.instrument.query(cmd)
				response_array = response.split(",")
				if len(response_array)==3 and response_array[2]=="OK": # if ok return: 0,0,OK
					return True

		except:
			print("Alert, problem with command light")
			return False

	def light_property(self, property, value):
		property_values = ["gain", "exposure", "light", "jpeg_quality"]
		# Sets the exposure time of the scope camera to "value"ms.
		# Sets the ring/coaxial light value of the scope camera to "value" ms.
		try:
			if str(property) in property_values:
				if str(property)=="jpeg_quality":
					if value>=10 and value<=100:
						cmd = "vis:set_prop " + str(property) + "," + str(value)
					else:
						print("Alert, problem with command property light, value jpeg quality not allowed")
						return False
				else:
					cmd = "vis:set_prop " + str(property) + ",scope," + str(value)
					if str(property)=="light":
						# set light type: Coaxial or Ring
						cmd = cmd + ",Coaxial"
				response = self.instrument.query(cmd)
				response_array = response.split(",")
				if len(response_array)==3 and response_array[2]=="OK": # if ok return: 0,0,OK
					return True

		except:
			print("Alert, problem with command property light")
			return False

	def set_vacuum(self,mode):
		try:
			if str(mode)=="1" or str(mode)=="0":
				cmd = "set_vacuum " + str(mode)
				response = self.instrument.query(cmd)	
				response_array = response.split(",")
				if len(response_array)==3 and response_array[2]=="OK": # if ok return: 0,0,OK
					return True
			return False
		except:
			print("Alert, problem with command vacuum")
			return False

	def get_vacuum_status(self,reference):
		# return 0 (OFF) or 1 (ON)
		try:
			reference_array = ["Wafer","AuxRight","AuxRight2","AuxLeft","AuxLeft2"]
			if reference in reference_array:
				cmd = "get_vacuum_status  " + reference 
				response = self.instrument.query(cmd)
				response_array = response.split(",")
				if len(response_array)==3:
					if response_array[0]=="0" and response_array[1]=="0":
						return response_array[2]
				return False
		except:
			print("Alert, problem with command get vacuum status")
			return False

	def image(self,path,with_Overlays=0):
		try:
			cmd = "vis:snap_image " + path + "," + str(with_Overlays)
			response = self.instrument.query(cmd) 
			if response=="OK":
				return True
			return False
		except:
			print("Alert, problem with command image")
			return False

	# TEMP COMMANDS (status)

	def get_chuck_temp_setpoint(self):
		try:
			cmd = "status:get_chuck_temp_setpoint"
			response = self.instrument.query(cmd)
			response_array = response.split(",")
			if len(response_array) == 3:
				if response_array[0] == "0" and response_array[1] == "0":
					return response_array[2]
			return False
		except:
			print("Alert, problem with command get chuck temp setpoint")
			return False

	def get_chuck_temp(self):
		try:
			cmd = "status:get_chuck_temp"
			response = self.instrument.query(cmd)
			response_array = response.split(",")
			if len(response_array) == 3:
				if response_array[0] == "0" and response_array[1] == "0":
					return response_array[2]
			return False
		except:
			print("Alert, problem with command get chuck temp")
			return False

	def get_chuck_thermo_state(self):
		# returns one of this states: Cooling, Heating, Controlling, Standby,  Error,  Uncontrolled
		try:
			cmd = "status:get_chuck_thermo_state"
			response = self.instrument.query(cmd)
			response_array = response.split(",")
			if len(response_array) == 3:
				if response_array[0] == "0" and response_array[1] == "0":
					return response_array[2]
			return False
		except:
			print("Alert, problem with command get chuck thermo state")
			return False

	def set_chuck_temp(self, temperature):
		try:
			cmd = "status:set_chuck_temp " + str(temperature)
			response = self.instrument.query(cmd)
			response_array = response.split(",")
			if len(response_array) == 3 and response_array[2] == "OK":  # if ok return: 0,0,OK
				return True
			return False
		except:
			print("Alert, problem with command set chuck temp")
			return False



	

