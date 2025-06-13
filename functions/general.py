#GENERAL FUNCTION
import os
import json
from PySide6.QtWidgets import *

def messageBox(self,title,message,type):
	if type == "information" or type == "info":
		retval = QMessageBox.information(
		    self,
		    title,
		    message,
		    buttons=QMessageBox.Ok ,
		    defaultButton=QMessageBox.Ok,
		)
	if type == "warning":
		retval = QMessageBox.warning(
			self,
		    title,
		    message,
		    buttons=QMessageBox.Ok ,
		    defaultButton=QMessageBox.Ok,
		)
	if type == "error" or type == "critical":
		retval = QMessageBox.critical(
		    self,
		    title,
		    message,
		    buttons=QMessageBox.Ok ,
		    defaultButton=QMessageBox.Ok,
		)
	if type == "question":
		retval = QMessageBox.question(
		    self,
		    title,
		    message,
		    buttons=QMessageBox.Yes | QMessageBox.No ,
            defaultButton=QMessageBox.Yes,
		)
	return retval
	
def get_json_file(filename, var_name):
	# if configuration json file exists load configuratión from file
	filename_config = os.getcwd() + '/modules/' + filename + '.json'
	file_exists = os.path.exists(filename_config)
	try :
		if file_exists:
			with open(filename_config) as json_file:
				return json.load(json_file)
		else:
			# generate json file default
			return ""
	except:
		return ""

	return var_name
