from functions import *
from . result_file import *
from . wafermap_file import *

import psycopg2 
import numpy as np

from config.functions import *


class Estepa():
	def __init__(self, config_estepa):
		try:
			self.error = False
			self.error_message = ""
			parameters = ["host","port","user","database","password"]
			parameters_found = True
			for param in parameters:
				if not param in config_estepa:
					parameters_found = False
					break

			if parameters_found:
				self.host = config_estepa["host"]
				self.port = config_estepa["port"]
				self.user = config_estepa["user"]
				self.database = config_estepa["database"]
				self.password = config_estepa["password"]
				# set timeout = 1 seconds
				if "timeout" in config_estepa:
					self.timeout = config_estepa["timeout"]
				else:
					self.timeout = 5 # 1 sec

				self.conn = psycopg2.connect(self.get_connect_string())
				

				# set autocommit
				if "autocommit" in config_estepa:
					self.conn.autocommit = config_estepa["autocommit"]
				else:
					self.conn.autocommit = False
				
				# create a cursor
				self.cur = self.conn.cursor()
				# execute a statement
				self.cur.execute('SELECT version()')

				# display the PostgreSQL database server version
				self.db_version = self.cur.fetchone()
				

			else:
				self.error = True
				self.error_message = "Parameters not found"


			
		except (Exception, psycopg2.DatabaseError) as error:
			self.error = True
			self.error_message = str(error)

		# finally:
		# 	if self.conn is not None:
		# 		self.conn.close()
		# 		print('Database connection closed.')

	def close_connection(self):
		# close the communication with the PostgreSQL
		if not self.error:
			# self.cur.close()
			if self.conn is not None:
				self.conn.close()


	def get_connect_string(self):
		pass_string = ""
		if self.password!="":
			pass_string = " password=" + str(self.password)
		return "host=" + self.host + " dbname=" + str(self.database) + " port=" + str(self.port) + " user=" + str(self.user) + pass_string + " connect_timeout = " + str(self.timeout)


	def get_technologies(self,run=""):
		get_technologies = list()
		sql = "select distinct tecnologia from runs"
		if run!="":
			sql += " WHERE run='" + run + "'"
		self.cur.execute(sql)
		if self.cur.rowcount>0:
			row = self.cur.fetchone()
			while row is not None:
				get_technologies.append(row[0])
				row = self.cur.fetchone()

		return get_technologies

	def create_technology(self,run,fecha,tecnologia):
		create_technology = True
		try:
			sql = "INSERT INTO runs (run,fecha,tecnologia) VALUES (%s,%s,%s)"
			self.cur.execute(sql,(str(run),str(fecha),str(tecnologia)))
		except:
			create_technology = False

		return create_technology


	def get_runs(self,tecnologia):
		get_runs = list()
		sql = "select DISTINCT run from runs where tecnologia='" + tecnologia + "' order by run"
		self.cur.execute(sql)
		if self.cur.rowcount>0:
			row = self.cur.fetchone()
			while row is not None:
				get_runs.append(row[0])
				row = self.cur.fetchone()

		return get_runs

	def get_wafers(self,run):
		get_wafers = list()
		sql = "select DISTINCT oblea_virtual from obleas where run='" + run + "' order by oblea_virtual"
		self.cur.execute(sql)
		if self.cur.rowcount>0:
			row = self.cur.fetchone()
			while row is not None:
				get_wafers.append(row[0])
				row = self.cur.fetchone()

		return get_wafers

	def get_parameters(self,oblea_virtual):
		# TODO: Get parameters from historical saved (analisis or analisis_runs)
		get_parameters = list()
		sql = "select distinct parametro from medidas where oblea_virtual='" + oblea_virtual + "' order by parametro;"
		self.cur.execute(sql)
		if self.cur.rowcount>0:
			get_parameters.append("All parameters")
			row = self.cur.fetchone()
			while row is not None:
				get_parameters.append(row[0])
				row = self.cur.fetchone()

		return get_parameters

	def get_medidas(self,oblea_virtual,parameters_list):

		get_medidas = dict()
		sql = "select * from medidas where oblea_virtual LIKE '" + oblea_virtual + "%' and parametro IN('" + "','".join(parameters_list) + "') order by parametro, chip;"
		self.cur.execute(sql)
		if self.cur.rowcount>0:
			row = self.cur.fetchone()

			while row is not None:
				parametro = row[1]
				chip = row[2]
				medida = row[3]
				if parametro not in get_medidas:
					get_medidas[parametro] = dict()
					get_medidas[parametro]["chip"] = list()
					get_medidas[parametro]["medida"] = list()
				get_medidas[parametro]["chip"].append(chip)
				get_medidas[parametro]["medida"].append(medida)
				row = self.cur.fetchone()
		
		return get_medidas

	def get_data_values(self,oblea_virtual,parametro):
		# get data values chip + medida for printing in QPlainText
		sql = "select * from medidas where oblea_virtual LIKE '" + oblea_virtual + "%' and parametro = '" + parametro + "';"
		self.cur.execute(sql)
		if self.cur.rowcount>0:
			row = self.cur.fetchone()
			get_data_values = {}
			while row is not None:
				parametro = row[1]
				chip = row[2].replace("(","").replace(")","").replace(","," ") # without parentesis (0,0) => 0 0
				medida = row[3]
				get_data_values[chip] = dict()					
				get_data_values[chip] = medida
				row = self.cur.fetchone()

		return get_data_values

	def get_regexp(self, wafers):
		run = wafers[0].split("-")[0]
		wafers_list = [ wafer.split("-")[1] for wafer in wafers ]
		regexp = "'^" + run +"-("
		for wafer in wafers_list:
			regexp += wafer + "[a-z]?|"
		regexp = regexp[:-1] + ")$'"
		return regexp

	def get_medida_consult(self, oblea_virtual, parameter):
		# get only field medida (values)
		# exclude from list -9000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
		val_remove = -9000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
		if type(oblea_virtual) == list:
			run = oblea_virtual[0].split("-")[0]
			regexp = self.get_regexp(oblea_virtual)
			sql = f"select medida from medidas where oblea_virtual ~ {regexp} and parametro = '{parameter}' and medida != {val_remove}"
		else:
			run = oblea_virtual
			sql = f"select medida from medidas where oblea_virtual LIKE '{oblea_virtual}%' and parametro = '{parameter}' and medida != {val_remove}"
		self.cur.execute(sql)
		get_medida_consult = [ item[0] for item in self.cur.fetchall() ]

		return get_medida_consult, run

	def get_medida_historical_consult(self, oblea_virtual, parameter, options):
		table_analisis = "analisis_runs"
		if options[0] == "Wafers":
			table_analisis = "analisis"
		# get only field medida (values)
		if type(oblea_virtual) == list:
			run = oblea_virtual[0].split("-")[0]
			if options[0] == "Wafers":
				txt_oblea_virtual = "%, ".join(oblea_virtual)
				sql = f"select media, desv_est, mediana, puntos, total_puntos from {table_analisis} "\
					  f"where oblea_virtual IN {txt_oblea_virtual} and parametro = '{parameter}';"
			else:
				sql = f"select media, desv_est, mediana, puntos, total_puntos from {table_analisis} "\
					  f"where run = '{run}' and parametro = '{parameter}' and actualizado = True;"
		else:
			run = oblea_virtual.split("-")[0]
			if options[0] == "Wafers":
				sql = f"select media, desv_est, mediana, puntos, total_puntos from {table_analisis} "\
					  f"where oblea_virtual LIKE '" + oblea_virtual + "%' and parametro = '" + parameter + "';"
			else:
				sql = f"select media, desv_est, mediana, puntos, total_puntos from {table_analisis} "\
					  f"where run = '{run}' and parametro = '{parameter}' and actualizado = True;"

		self.cur.execute(sql)
		get_medida_consult = [ list(item) for item in self.cur.fetchall() ]
		return get_medida_consult, run


	def get_rangos(self,tecnologia,parametro):
		get_rangos = list()
		sql = "select minimo, maximo FROM rangos WHERE tecnologia='" + tecnologia + "' and parametro='" + parametro + "'"
		self.cur.execute(sql)
		if self.cur.rowcount>0:
			row = self.cur.fetchone()
			minimo = row[0]
			maximo = row[1]
			get_rangos.append(minimo)
			get_rangos.append(maximo)

		return get_rangos

	def get_masks(self,wafer=""):
		get_masks = list()
		sql = "select distinct mascara from mascaras"
		if wafer!="":
			sql += " WHERE oblea='" + wafer + "'"
		self.cur.execute(sql)
		if self.cur.rowcount>0:
			row = self.cur.fetchone()
			while row is not None:
				get_masks.append(row[0])
				row = self.cur.fetchone()

		return get_masks


	def create_mask(self,mascara,oblea):
		create_mask = True
		try:
			sql = "INSERT INTO mascaras (mascara,oblea) VALUES (%s,%s)"
			self.cur.execute(sql, (str(mascara),str(oblea)))
		except:
			create_mask = False

		return create_mask

	def create_fechas(self,oblea_virtual,fecha_medida):
		create_fechas = True
		try:
			sql = "SELECT * FROM fechas WHERE oblea_virtual='" + oblea_virtual + "'"
			self.cur.execute(sql)
			if self.cur.rowcount==1:
				# update
				sql_update = """UPDATE fechas SET fecha_medida=%s WHERE oblea_virtual=%s"""
				self.cur.execute(sql_update,(fecha_medida, oblea_virtual))
				# self.conn.commit()
			else:
				# insert
				sql_insert = "INSERT INTO fechas (oblea_virtual,fecha_medida) VALUES (%s,%s)"
				self.cur.execute(sql_insert,(oblea_virtual,fecha_medida))
				# self.conn.commit()
		except:
			create_fechas = False

		return create_fechas

	def create_geometrias(self,wafer_parameters):
		# ---------------------------------------------------------
		# get variables from wafer_parameters
		# ---------------------------------------------------------
		geometria = wafer_parameters["wafer_name"]
		wafer_size = wafer_parameters["wafer_size"]
		xsize = wafer_parameters["xsize"]
		ysize = wafer_parameters["ysize"]
		xmaxim = wafer_parameters["xmax"]
		ymaxim = wafer_parameters["ymax"]
		nchips = wafer_parameters["nchips"]
		nmodules = wafer_parameters["nmodules"]
		origin_chip = wafer_parameters["origin_chip"]
		home_chip = wafer_parameters["home_chip"]
		flat_orientation = wafer_parameters["flat_orientation"]
		wafer_modules = ','.join(wafer_parameters["wafer_modules"])
		real_origin_chip = wafer_parameters["real_origin_chip"]
		navigation_options = wafer_parameters["navigation_options"]
		navigation_position = navigation_options[0]
		navigation_direction = navigation_options[1]
		navigation_movement = navigation_options[2]
		# ---------------------------------------------------------
		create_geometrias = True
		try:
			sql = "SELECT * FROM geometrias WHERE geometria='" + geometria + "'"
			self.cur.execute(sql)
			if self.cur.rowcount==0:
				# insert
				sql_insert = "INSERT INTO geometrias (geometria,wafer_size,xsize,ysize,xmaxim,ymaxim,nchips) VALUES	(%s, %s, %s, %s, %s, %s, %s)"
				self.cur.execute(sql_insert, (geometria, wafer_size, xsize, ysize,xmaxim,ymaxim,nchips))
			else:
				sql_update = "UPDATE geometrias SET wafer_size = %s, xsize = %s, ysize = %s, xmaxim = %s, ymaxim = %s, nchips = %s WHERE geometria = %s"
				self.cur.execute(sql_update, (wafer_size, xsize, ysize,xmaxim,ymaxim,nchips,geometria))

			# also in new geometrias_extra table
			sql = "SELECT * FROM geometrias_extra WHERE geometria='" + geometria + "'"
			self.cur.execute(sql)
			if self.cur.rowcount==0:
				# insert
				sql_insert = "INSERT INTO geometrias_extra (geometria,nmodules,origin_chip,home_chip,flat_orientation,wafer_modules,real_origin_chip,navigation_position,navigation_direction,navigation_movement) VALUES	(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
				self.cur.execute(sql_insert, (geometria,nmodules,origin_chip,home_chip,flat_orientation,wafer_modules,real_origin_chip,navigation_position,navigation_direction,navigation_movement))
			else:
				sql_update = "UPDATE geometrias_extra SET nmodules = %s, origin_chip = %s, home_chip = %s, flat_orientation = %s, wafer_modules = %s, real_origin_chip = %s, navigation_position = %s, navigation_direction = %s, navigation_movement = %s WHERE geometria = %s"
				self.cur.execute(sql_update, (nmodules,origin_chip,home_chip,flat_orientation, wafer_modules,real_origin_chip,navigation_position,navigation_direction,navigation_movement,geometria))
		except:
			create_geometrias = False

		return create_geometrias

	def create_obleageom(self,oblea_virtual,geometria):
		create_obleageom = True
		try:
			sql = "SELECT * FROM obleageom WHERE oblea_virtual='" + oblea_virtual + "'"
			self.cur.execute(sql)
			if self.cur.rowcount==1:
				# update
				sql_update = "UPDATE obleageom SET geometria=%s WHERE oblea_virtual=%s"
				self.cur.execute(sql_update,(geometria,oblea_virtual))
				# self.conn.commit()
			else:
				# insert
				sql_insert = "INSERT INTO obleageom (oblea_virtual,geometria) VALUES (%s,%s)"
				self.cur.execute(sql_insert,(oblea_virtual,geometria))
				# self.conn.commit()
		except:
			create_obleageom = False

		return create_obleageom

	def create_obleas(self,run,oblea,oblea_virtual,comentario):
		create_obleas = True
		try:
			sql = "SELECT * FROM obleas WHERE run = '" + run + "' and oblea='" + oblea + "' and oblea_virtual='" + oblea_virtual + "'"
			self.cur.execute(sql)
			if self.cur.rowcount==1:
				# update
				sql_update = "UPDATE obleas SET comentario=%s WHERE run = %s and oblea=%s and oblea_virtual=%s"
				self.cur.execute(sql_update,(comentario,run,oblea,oblea_virtual))
				# self.conn.commit()
			else:
				# insert
				sql_insert = "INSERT INTO obleas (run,oblea,oblea_virtual,comentario) VALUES (%s,%s,%s,%s)"
				self.cur.execute(sql_insert,(run,oblea,oblea_virtual,comentario))
				# self.conn.commit()
		except:
			create_obleas = False

		return create_obleas

	def create_runs(self,run,fecha,tecnologia):
		create_runs = True
		try:
			sql = "SELECT * FROM runs WHERE run ='" + run + "'"
			self.cur.execute(sql)
			if self.cur.rowcount==1:
				# update
				sql_update = "UPDATE runs SET fecha=%s, tecnologia = %s WHERE run = %s"
				self.cur.execute(sql_update,(fecha,tecnologia,run))
				# self.conn.commit()
			else:
				# insert
				sql_insert = "INSERT INTO runs (run,fecha,tecnologia) VALUES (%s,%s,%s)"
				self.cur.execute(sql_insert,(run,fecha,tecnologia))
				# self.conn.commit()
				
		except:
			create_runs = False

		return create_runs


	def create_localizaciones(self,oblea,localizacion,standard=False):
		create_localizaciones = True
		try:
			sql = "SELECT * FROM localizaciones WHERE oblea='" + oblea + "'"
			self.cur.execute(sql)
			if self.cur.rowcount==1:
				# update
				sql_update = "UPDATE localizaciones SET localizacion=%s, standard=%s WHERE oblea=%s"
				self.cur.execute(sql_update,(localizacion,standard,oblea))
				# self.conn.commit()
			else:
				# insert
				sql_insert = "INSERT INTO localizaciones (oblea,localizacion,standard) VALUES (%s,%s,%s)"
				self.cur.execute(sql_insert,(oblea,localizacion,standard))
				# self.conn.commit()
		except:
			create_localizaciones = False

		return create_localizaciones

	def create_medidas(self,mainWindow, inbase_parameters):
		create_medidas = True
		insert_medidas = list()
		try:
			# create result file
			result_file = ResultFile(inbase_parameters["dataFile"])
			num_modules = len(result_file.modules)
			params_list = list()
			for die in result_file.params:
				die_txt = "(" + die.replace(" ",",") + ")"
				for module in range(1,num_modules+1):
					for param in result_file.params[die][str(module)]:
						medida = result_file.params[die][str(module)][param]
						insert_medidas.append((inbase_parameters["virtual_wafer"],param,die_txt,float(medida)))
						if param not in params_list:
							params_list.append(param)
						
			mainWindow.updateTextImportReport(" => Loop finish...")
			if create_medidas:
				mainWindow.updateTextImportReport(" => Inserting medidas...")
				sql_insert = "INSERT INTO medidas (oblea_virtual,parametro,chip,medida) VALUES (%s,%s,%s,%s)"
				self.cur.executemany(sql_insert,insert_medidas)
				# if len(update_medidas)>0:
				# 	mainWindow.updateTextImportReport(" => Updating medidas...")
				# 	sql_update = "UPDATE medidas SET medida=%s WHERE oblea_virtual=%s and parametro=%s and chip=%s"
				# 	self.cur.executemany(sql_update,update_medidas)
				# update analisis_runs actualizado = False where run = run
				run = inbase_parameters["run"]
				for param in params_list:
					sql_update = "UPDATE analisis_runs SET actualizado=%s WHERE run=%s and parametro=%s"
					self.cur.execute(sql_update,(False, run, param))

		except:
			create_medidas = False

		return create_medidas

	def create_medida(self,oblea_virtual,parametro,chip,medida):
		create_medida = [True,"insert"]
		try:
			sql = "SELECT medida FROM medidas WHERE oblea_virtual='" + oblea_virtual + "' and parametro='" + parametro + "' and chip='" + chip + "'" 
			self.cur.execute(sql)
			if self.cur.rowcount==1:
				# update
				create_medida = [True,"update"]
				#sql_update = "UPDATE medidas SET medida=%s WHERE oblea_virtual=%s and parametro=%s and chip=%s"
				#self.cur.execute(sql_update,(float(medida),oblea_virtual,parametro,chip))

				# insert
				# sql_insert = "INSERT INTO medidas (oblea_virtual,parametro,chip,medida) VALUES (%s,%s,%s,%s)"
				# self.cur.execute(sql_insert, (oblea_virtual,parametro,chip,float(medida)))
				# self.conn.commit()
		except:
			create_medida = [False,""]

		return create_medida


	def exists_measurements(self,oblea_virtual):
		exists_measurement = False
		sql = "SELECT * FROM medidas WHERE oblea_virtual LIKE '" + oblea_virtual + "%'"
		self.cur.execute(sql)
		if self.cur.rowcount>0:
			exists_measurement = True

		return exists_measurement

	def exists_analisis_runs(self, run, parametro):
		exists_analisis_run = False
		sql = "SELECT * FROM analisis_runs WHERE run='" + run + "' and parametro='" + parametro + "'"
		self.cur.execute(sql)
		if self.cur.rowcount>0:
			exists_analisis_run = True

		return exists_analisis_run

	def exists_analisis(self, oblea_virtual, parametro):
		exists_analisis = False
		sql = "SELECT * FROM analisis WHERE oblea_virtual='" + oblea_virtual + "' and parametro='" + parametro + "'"
		self.cur.execute(sql)
		if self.cur.rowcount>0:
			exists_analisis = True

		return exists_analisis

	def get_virtual_wafer(self,oblea):
		letras = {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g', 8:'h', 9:'i', 10:'j', 11:'k', 12:'l', 13:'m', 14:'n', 15:'o', 16:'p', 17:'q', 18:'r', 19:'s', 20:'t', 21:'u', 22:'v', 23:'w', 24:'x', 25:'y', 26:'z'}
		sql = "SELECT * FROM obleas WHERE oblea_virtual LIKE '" + oblea + "%'"
		self.cur.execute(sql)
		numrows = self.cur.rowcount
		if numrows>0:
			if numrows==1:
				virtual_wafer = oblea + "a"
				# update oblea_virtual in all tables without letter to "a"
				sql = "UPDATE fechas SET oblea_virtual = %s WHERE oblea_virtual = %s"
				self.cur.execute(sql,(virtual_wafer,oblea))
				sql = "UPDATE obleageom SET oblea_virtual = %s WHERE oblea_virtual = %s"
				self.cur.execute(sql,(virtual_wafer,oblea))
				sql = "UPDATE obleas SET oblea_virtual = %s WHERE oblea_virtual = %s"
				self.cur.execute(sql,(virtual_wafer,oblea))
				sql = "UPDATE medidas SET oblea_virtual = %s WHERE oblea_virtual = %s"
				self.cur.execute(sql,(virtual_wafer,oblea))


			return oblea + letras[numrows+1]

		return oblea


	def inbase(self, mainWindow, inbase_parameters):
		# inbase_parameters = {
		#           "dataFile" : txtDataFileInbase,
		#           "wafermapFile" : txtWafermapFileInbase,
		#           "run" : txtRunUpload,
		#           "wafer" : txtRunUpload + "-" + txtWaferUpload,
		# 			"virtual_wafer" : txtRunUpload + "-" + txtWaferUpload + letra,
		#           "date" : txtDateUpload,
		#           "technology" : txtTechnologyUpload,
		#           "mask" : txtMaskUpload,
		#           "localization" : txtLocalizationUpload,
		#           "comment" : txtCommentUpload
		#       }

		try:
			error = False
			error_message = ""

			technologies = self.get_technologies(inbase_parameters["run"])
			masks = self.get_masks(inbase_parameters["wafer"])

			if not inbase_parameters["technology"] in technologies:
				# create technology
				mainWindow.updateTextImportReport("- Creating tecnologia...")
				if not self.create_technology(inbase_parameters["run"],inbase_parameters["date"],inbase_parameters["technology"]):
					error = True
					error_message = "Error uploading new technology: " + inbase_parameters["technology"]

			if not inbase_parameters["mask"] in masks:
				# create mask
				mainWindow.updateTextImportReport("- Creating mask...")
				if not self.create_mask(inbase_parameters["mask"],inbase_parameters["wafer"]):
					error = True
					error_message = "Error uploading new mask: " + inbase_parameters["mask"]

			
			if not error:
				mainWindow.updateTextImportReport("- Uploading fechas information...")
				# put all info in tables
				if self.create_fechas(inbase_parameters["virtual_wafer"],inbase_parameters["date"]):
					# create object wafermap file
					wafermap_file = WafermapFile(inbase_parameters["wafermapFile"])
					geometria = wafermap_file.wafer_parameters["wafer_name"]
					mainWindow.updateTextImportReport("- Uploading geometrias information...")
					if self.create_geometrias(wafermap_file.wafer_parameters):
						mainWindow.updateTextImportReport("- Uploading localizaciones information...")
						if self.create_localizaciones(inbase_parameters["wafer"],inbase_parameters["localization"]):
							mainWindow.updateTextImportReport("- Uploading obleageom information...")
							if self.create_obleageom(inbase_parameters["virtual_wafer"],geometria):
								mainWindow.updateTextImportReport("- Uploading obleas information...")
								if self.create_obleas(inbase_parameters["run"],inbase_parameters["wafer"],inbase_parameters["virtual_wafer"],inbase_parameters["comment"]):
									mainWindow.updateTextImportReport("- Uploading runs information...")
									if self.create_runs(inbase_parameters["run"],inbase_parameters["date"],inbase_parameters["technology"]):
										# create measurements
										mainWindow.updateTextImportReport("- Uploading medidas information...")
										if self.create_medidas(mainWindow, inbase_parameters):
											if not self.conn.autocommit:
												mainWindow.updateTextImportReport("COMMIT process...")
												self.conn.commit()
										else:
											error = True
											error_message = "Error uploading medidas information!"
									else:
										error = True
										error_message = "Error uploading runs information!"
								else:
									error = True
									error_message = "Error uploading obleas information!"
							else:
								error = True
								error_message = "Error uploading obleageom information!"
						else:
							error = True
							error_message = "Error uploading localizaciones information!"	
					else:
						error = True
						error_message = "Error uploading geometrias information!"
				else:
					error = True
					error_message = "Error uploading fechas information!"

			if error and not self.conn.autocommit:
				mainWindow.updateTextImportReport("ROLLBACK process...")
				self.conn.rollback()
				error_message = "Error in transaction Reverting all other operations of a transaction: " + error_message

			return [error, error_message]

		except (Exception, psycopg2.DatabaseError) as errorDatabase:
			mainWindow.updateTextImportReport("Error in transaction: " + errorDatabase)
			if not self.conn.autocommit:
				mainWindow.updateTextImportReport("ROLLBACK process...")
				self.conn.rollback()
				return [False, "Error in transaction Reverting all other operations of a transaction: " + errorDatabase]
			return [False, "Error in transaction: " + errorDatabase]


	def get_geometria_obleageom(self,oblea_virtual):
		# pass wafer (without letter), then put LIKE in SQL => geometry is the same for all wafers of run
		get_obleageom = ""
		sql = "select geometria FROM obleageom WHERE oblea_virtual LIKE '" + oblea_virtual +"%'"
		self.cur.execute(sql)
		if self.cur.rowcount>0:
			row = self.cur.fetchone()
			get_obleageom = row[0]


		return get_obleageom

	def get_wafer_positions(self,oblea_virtual):
		get_wafer_positions = list()
		sql = "select DISTINCT chip FROM medidas WHERE oblea_virtual LIKE '" + oblea_virtual +"%'"
		self.cur.execute(sql)
		if self.cur.rowcount>0:
			row = self.cur.fetchone()
			while row is not None:
				chip = row[0].replace("(","").replace(")","").replace(","," ")
				get_wafer_positions.append(chip)
				row = self.cur.fetchone()

		return get_wafer_positions


	def get_xmax_ymax(self, wafer_positions):
		xmax_detected = 0
		ymax_detected = 0
		elementos_x_detected = []
		elementos_y_detected = []
		for elemento in wafer_positions:
			
			elemento_array = elemento.split()
			if len(elemento_array)!=2:
			    check_wafer_parameters = False
			    break
			# init variables
			elemento_x = elemento_array[0]
			elemento_y = elemento_array[1]
			buscar_x = False
			buscar_y = False
			num_elemento_x = 0
			num_elemento_y = 0
			if elemento_x not in elementos_x_detected:
			    elementos_x_detected = np.append(elementos_x_detected, elemento_x)
			    buscar_x = True
			if elemento_y not in elementos_y_detected:
			    elementos_y_detected = np.append(elementos_y_detected, elemento_y)
			    buscar_y = True
			if buscar_x and buscar_y:
			    for elemento_buscar in wafer_positions:
			        elemento_buscar_array = elemento_buscar.split()
			        if elemento_buscar_array[0] == elemento_x:
			            num_elemento_y += 1 # cambiamos el eje porque buscamos sumatorio en vertical
			        if elemento_buscar_array[1] == elemento_y:
			            num_elemento_x += 1 # cambiamos el eje porque buscamos sumatorio en horizontal

			    if num_elemento_x>xmax_detected:
			        xmax_detected = num_elemento_x
			    if num_elemento_y>ymax_detected:
			        ymax_detected = num_elemento_y
		

		return [xmax_detected,ymax_detected]



	def get_geometria(self,geometria):
		# pass wafer (without letter), then put LIKE in SQL => geometry is the same for all wafers of run
		get_geometria = {}
		sql = "select * FROM geometrias WHERE geometria = '" + geometria +"'"
		self.cur.execute(sql)
		if self.cur.rowcount>0:
			row = self.cur.fetchone()
			get_geometria["wafer_name"] = row[0]
			get_geometria["wafer_size"] = row[1]
			get_geometria["xsize"] = row[2]
			get_geometria["ysize"] = row[3]
			get_geometria["xmax"] = row[4]
			get_geometria["ymax"] = row[5]
			get_geometria["nchips"] = row[6]
			get_geometria["wafer_size_mm"], get_geometria["thickness"] = calc_wafer_size(row[1])

			sql = "select * FROM geometrias_extra WHERE geometria = '" + geometria +"'"
			self.cur.execute(sql)
			if self.cur.rowcount>0:
				row = self.cur.fetchone()
				get_geometria["nmodules"] = row[1]
				get_geometria["origin_chip"] = row[2]
				get_geometria["home_chip"] = row[3]
				get_geometria["flat_orientation"] = row[4]
				get_geometria["wafer_modules"] = row[5]
				get_geometria["real_origin_chip"] = row[6]
				get_geometria["navigation_options"] = [row[7],row[8],row[9]]


		return get_geometria

	def get_wafer_parameters(self,wafer):
		# get geometria
		geometria = self.get_geometria_obleageom(wafer)
		# get wafer_parameters BBDD for this geometria
		wafer_parameters = self.get_geometria(geometria)
		# adding wafer_parameters positions
		wafer_parameters["wafer_positions"] = self.get_wafer_positions(wafer)
		# add xmax & ymax
		wafer_parameters["xmax"], wafer_parameters["ymax"] = self.get_xmax_ymax(wafer_parameters["wafer_positions"])

		return wafer_parameters

	def get_heatmap_values(self,data_values,wafer):
		# return numpy array 2D to use in heatmap seaborn
		# pass data_values: dictionary with wafer_positions & value. Ex:
		# {'0 0': 592.58027418, '-3 0': 593.775609049, '-6 0': 598.320966887, ....}

		# first get wafer_parameters for the wafer
		geometria = self.get_geometria_obleageom(wafer)
		wafer_parameters = self.get_geometria(geometria)
		wafer_parameters["wafer_positions"] = self.get_wafer_positions(wafer)
		# 0) set np array 2D with zeros. Calc the number of chips in X & Y
		wafer_parameters["xmax"], wafer_parameters["ymax"] = self.get_xmax_ymax(wafer_parameters["wafer_positions"])

		xsize = float(wafer_parameters["xsize"])
		ysize = float(wafer_parameters["ysize"])
		num_chips_X = float(wafer_parameters["wafer_size_mm"])*1000/xsize
		num_chips_Y = float(wafer_parameters["wafer_size_mm"])*1000/ysize
		# set 2D array with zeros 
		separation_Y = 2 # create extra separation chips Y
		get_heatmap_values = np.empty((int(num_chips_Y + separation_Y),int(num_chips_X)))
		get_heatmap_values.fill(9E99)
		
		# 1) We use the wafermaf class to get wafer_positions, real_origin_chip
		wafer_positions = wafer_parameters["wafer_positions"]
		
		real_origin_chip = wafer_parameters["real_origin_chip"]
		real_origin_chip_x, real_origin_chip_y = real_origin_chip.split()
		
		num_pos = 0
		medidas = list()
		for pos in wafer_positions:
			posx, posy = pos.split()
			wafer_position = wafer_positions[num_pos]
			medida = data_values[wafer_position]
			wafer_position_x, wafer_position_y = wafer_position.split()

			# real wafer position is the wafer_position + real_origin_chip position
			real_wafer_position_x = int(wafer_position_x) + int(real_origin_chip_x)
			real_wafer_position_y = int(wafer_position_y) + int(real_origin_chip_y)

			# for seaborn is positive 
			real_wafer_position_x_sns = int(real_wafer_position_x) * -1
			real_wafer_position_y_sns = int(real_wafer_position_y) * -1

			# set the value for array position (inverted)
			get_heatmap_values[real_wafer_position_y_sns][real_wafer_position_x_sns] = medida
			medidas.append(medida)
			num_pos+=1


		min_value = min(medidas) 
		max_value = max(medidas) 
		
		if max_value<0:
			max_value_replace = max_value - max_value*10/100
		else:
			max_value_replace = max_value + max_value*10/100
		if min_value<0:
			min_value_replace = min_value + min_value*90/100
		else:
			min_value_replace = min_value - min_value*90/100
		
		# Replace values 9E99 for max_value or min_value (depends cmap colors)
		# get_heatmap_values = np.where(get_heatmap_values==9E99,max_value,get_heatmap_values)
		get_heatmap_values = np.where(get_heatmap_values==9E99,min_value_replace,get_heatmap_values)

		return get_heatmap_values

	# CONSULT FUNCTIONS

	def exists_parameter_in_wafer(self, oblea_virtual, parameter):
		exists_parameters_in_wafer = False
		sql = f"SELECT * FROM medidas WHERE oblea_virtual LIKE '{oblea_virtual}%' AND parametro = '{parameter}'"
		self.cur.execute(sql)
		return self.cur.rowcount > 0

	def get_lists_consult(self, list_wafers, parameter):
		"""
		get list values/yield and list runs/wafers
		@param: list_wafer list of wafer
		@param: options: options = [option_checked, option_historical, option_values]
		@param: parameter : parameter
		"""
		list_values = []
		list_wafers = []
		for wafer in list_wafers:
			values_dict = self.get_data_values(wafer, parameter)
			list_values.append(values_dict.values())
			list_wafers.append(wafer)
		return list_values, list_wafers

	def upload_analisis_runs(self, run, valores):
		"""
		upload analisis runs
		@param: runs_info: list of runs info
		"""
		parametro, media, desv_est, mediana, puntos, met_elim_outliers = valores.split(" ")
		puntos, total_puntos = puntos.split("/")

		# upload runs (teorical with inbase this is not necessary)
		sql = f"UPDATE analisis_runs SET actualizado = False " \
			  f"WHERE run = '{run}' AND parametro = '{parametro}'"

		# self.cur.execute(sql)
		# self.conn.commit()
		print(sql)

		actualizado = True
		sql = f"UPDATE analisis_runs SET run = '{run}'," \
			  f" parametro = '{parametro}', " \
			  f" media = {media}, " \
			  f" desv_est = {desv_est}, " \
			  f" mediana = {mediana}, " \
			  f" puntos = {puntos}, " \
			  f" total_puntos = {total_puntos}, " \
			  f" met_elim_outliers = '{met_elim_outliers}', " \
			  f" actualizado = {actualizado} " \
			  f"WHERE run = '{run}' AND parametro = '{parametro}'"

		# self.cur.execute(sql)
		# self.conn.commit()
		print(sql)

	def upload_analisis(self, wafer, valores):
		"""
		upload analisis
		@param: wafers_info: list of wafers info
		"""
		# upload wafers
		actualizado = True
		parametro, media, desv_est, mediana, puntos, met_elim_outliers = valores.split(" ")
		puntos, total_puntos = puntos.split("/")
		sql = f"INSERT INTO analisis (oblea_virtual, parametro, media, desv_est, mediana, puntos, total_puntos, met_elim_outliers) " \
			  f"VALUES ('{wafer}', '{parametro}', {media}, {desv_est}, {mediana}, {puntos}, {total_puntos}, '{met_elim_outliers}')"
		# self.cur.execute(sql)
		# self.conn.commit()
		print(sql)


	def get_autolimits(self, parameter):
		"""
		get autolimits
		@param: parameter: parameter
		"""
		# get autolimits
		sql = f"SELECT minimo, maximo FROM rangos WHERE parametro = '{parameter}'"
		self.cur.execute(sql)
		row = self.cur.fetchone()
		return row


