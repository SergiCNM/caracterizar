import os
import toml

class Config():
	def __init__(self, path_to_file):
		config_string = """
title = "Caracterizar"
version = "2.1.0"
author = "Sergi Sànchez"

[defaults]
debugmode = false
darkmode = true
estepa = true
txtprocess = "11537"
txtlot = "11537"
txtwafer = "1"
txtmask = "SOLARMEMS"
txttemperature = "21"
txthumidity = "35"

[dirs]
base = "config"
instruments = "instruments"
tests = "tests"
probers = "probers"
wafermaps = "wafermaps"
results = "results"
reports = "reports"

[files]
plot = "lecturas.txt"
process = "process.txt"
import_report = "report_import"

[mecao]
loadStart = false
host = "opter6.cnm.es"
port = "5432"
user = "joaquin"
database = "mecao"
password = ""
autocommit = false

[estepa]
method = "f-spread"
lna = false
autolimits = false
limmin = 400
limmax = 500
chunks = 16

[labs]
mysqlhost = "localhost"
mysqluser = "root"
mysqlpassword = "Mysql123" # Mysql123 or blank in cnm
mysqldatabase = "labs_new" # labs_new or labs in cnm

[reports]
title = ""
subtitle = ""
date = ""
author = "Sergi Sánchez"
"""

		self.path_config_file = path_to_file
		self.error = False
		self.error_message = ""
		self.config = None

		try:
			if os.path.exists(self.path_config_file):
				self.load_config_file()
		    
			else:
				# create file toml by default
				print("Toml doesn't exists: " + self.path_config_file + "!")
				toml_file = open(self.path_config_file,"w", encoding="utf-8")
				toml_file.write(config_string)
				toml_file.close()
				self.load_config_file()
		except Exception as e:
			self.error = True
			self.error_message = "ERROR Config file: " + str(e)

	def getConfig(self):
		return self.config

	def saveConfig(self, config):
		try:
			# save config dict to toml file
			with open(self.path_config_file, mode="w", encoding="utf-8") as fp:
				toml.dump(config, fp)
			self.config = config
		except Exception as e:
			self.error = True
			self.error_message = "ERROR saving config file: " + str(e)

	def load_config_file(self):
		try:
			with open(self.path_config_file, mode="r", encoding="utf-8") as fp:
				config = toml.load(fp)
				self.config = config   
		except Exception as e:
			self.error = True
			self.error_message = "ERROR loading config file: " + str(e)
