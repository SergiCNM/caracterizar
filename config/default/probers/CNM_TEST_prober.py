# MPI TS2000SE prober driver
import pyvisa
import time


class CNM_TEST:
	def __init__(self,parameters):
		self.address = parameters["address"]


	def idn(self):
		return "TEST PROBER CNM"
		
			
	def set_soft_contact(self, mode):
		# 0 for optimize for speed, and 1 for optimize for accuracy
		return True
		

	def set_stepping_contact_mode(self, mode):
		# BackToContact optimize for speed/accuracy, LockContact for safety
		return True
		

	def dataready(self):
		free = "1"
		return free # if ok returns "1"

	def get_chuck_xy(self,reference):
		return [100,100]

	def get_chuck_z(self,reference):
		return 35550

	def get_chuck_site_heights(self,reference):
		# always make progressive contact in Wafer (0)
		# function return height Contact, Separation, Overtravel, Hover
		return [36000,35500,50,10]
		

	def move_chuck_xy(self,reference,x,y):
		return [100,100]

	def move_chuck_z(self, reference, z):
		# Moves chuck z relative to a reference point. Movement over maximum permitted height is not 
		# carried out. Maximum permitted height is defined as follows:
		#  Overtravel disabled & Contact height is not set: Max z motion level.
		#  Overtravel disabled & Contact height is set: Contact height.
		#  Overtrevel enabled & Contact height is not set: Max z motion level.
		#  Overtravel enabled & Contact height is set: Contact height + overtravel gap
		return 35550 + int(z)

	def move_home(self):
		return ["0.0","0.0"]

	def move_center(self):
		return [100,100]

	def move_contact(self):
		return 36000

	def move_separation(self):
		return 35500

	def stop(self):
		cmd = "stop_chuck_xyz"
		
		retval = QMessageBox.critical(
            self,
            "ALERT",
            "Stop button pressed, unload sample to be safe!",
            buttons=QMessageBox.Ok  ,
            defaultButton=QMessageBox.Ok,
        )


	def light(self,mode):
		return True

		
	def set_vacuum(self,mode):
		return True

	def get_vacuum_status(self,reference):
		# return 0 (OFF) or 1 (ON)
		return "1"

	def image(self,path,scale):
		return True

	

