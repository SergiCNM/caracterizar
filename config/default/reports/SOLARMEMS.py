# SOLARMEMS class
from fpdf import FPDF
import os
import pandas as pd
import numpy as np
from pandas.plotting import table 
import matplotlib.pyplot as plt


from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from decimal import Decimal
from PIL import Image # compress images


class SOLARMEMS(FPDF):
	def __init__(self, widgets, options, path_results, dir_assets='config/default/reports/assets/'):
		super().__init__()
		self.WIDTH = 210
		self.HEIGHT = 297
		self.options = options
		self.path_results = path_results
		self.filename = os.path.basename(path_results)
		self.filename_pdf = ""
		self.dir_assets = dir_assets
		self.path_abs = self.path_results.replace(self.filename,"")
		self.error = False
		self.errorMessage = ""
		self.widgets = widgets
		self.pages_links = {}
		self.pages_links["page1"] = None
		self.leakage_current_level = 10E-9
		self.photo_current_level = 5E-6
		self.coefVar_level = 0.05
		# creating dirs
		for option in self.options:
			if "_folder" in option:
				if not os.path.exists(self.path_abs + self.options[option]):
					os.mkdir(self.path_abs + self.options[option])
		# get header (with lines_header) and num_devices
		f = open(self.path_results)
		self.header_text = 'HEADER RESULT FILE: ' + self.filename + "\n"
		self.num_devices = 0
		lines_header = 0
		lectura = f.readline()
		while lectura.strip()!="":
			if not "Delivery#:" in lectura:
				self.header_text += lectura
			if "Devices#:" in lectura:
				self.num_devices = int(lectura.replace("Devices#:","").strip())
			lectura = f.readline()
			lines_header+= 1
		# get other => results (statistics)
		self.results = f.read()
		f.close()
		# read file TXT with pandas
		try: 
			df = pd.read_csv(self.path_results, header=lines_header, sep=";")
			if len(df[df.columns[0]])!=self.num_devices:
				self.error = True
				self.errorMessage = "Número de dispositivos en header ({}) distintos de los obtenido con los datos ({})". \
					format(self.num_devices, len(df[df.columns[0]]))
		except Exception as ex:
			self.error = true
			self.errorMessage = ex

	def header(self, title="SOLAMEMS REPORT"):
		# Custom logo and positioning
		# Create an `assets` folder and put any wide and short image inside
		# Name the image `logo.png`
		#self.image(os.getcwd() + "/" + self.dir_assets + 'logo.png', 10, 8, 50, 16, link = self.pages_links["page1"])
		self.image(os.getcwd() + "/" + self.dir_assets + 'logo.svg', 10, 8, 50, 16, link = self.pages_links["page1"])
		self.set_font('Helvetica', 'B', 11)
		self.cell(self.WIDTH - 80)
		self.cell(60, 1, title, 0, 0, 'R')
		self.ln(5)
		self.cell(self.WIDTH - 80)
		self.set_font('Helvetica', '', 10)
		self.cell(60, 1, self.filename, 0, 0, 'R')
		self.ln(20)
	

	def footer(self, page_txt="Page "):
		# Page numbers in the footer
		self.set_y(-15)
		self.set_font('Helvetica', 'I', 8)
		self.set_text_color(128)
		self.cell(0, 10, page_txt + str(self.page_no()), 0, 0, 'C')

	def page_header(self):
		self.pages_links["page1"] = self.add_link()
		self.set_link(self.pages_links["page1"],y=0,page=1)
		self.set_y(30)
		font_size = 12
		header_list = self.header_text.split("\n")
		
		for line in header_list:
			# empty temperature or rh
			if line=="Temperature: ":
				line = line + self.widgets.txtTemperature.text() + " ºC"
			if line=="Humidity: ":
				line = line + self.widgets.txtHumidity.text() + " % RH"
			
			self.set_font('Helvetica', 'B', font_size)
			self.cell(w=60, h=1, txt=line, align='L')
			self.ln(5)
			font_size = 8
		if "wafermap" in self.options:
			if self.options["wafermap"]:
				self.set_left_margin(50)
				np_array = self.print_mapa_wafer()
				self.numpy_array_print_to_wafer(np_array)


		self.widgets.txtResultReport.appendHtml('&nbsp;- Page header done!')
		QApplication.processEvents()

	def page_results(self):
		self.set_y(30)
		fill_color = 140
		fill = True
		self.set_font('Helvetica', 'B', 6)
		self.set_fill_color(fill_color)
		x = 10
		self.cell(w=x, h=3, txt="Device ID",align='C', fill=True)
		x = 60
		self.cell(w=x, h=3,txt="Leakage current @ 3.3 [A]",align='C', fill=True)
		x = 60
		self.cell(w=x, h=3, txt="Photo current @ 3.3 [A]", align='C', fill=True)
		x = 60
		self.cell(w=x, h=3, txt="Statistics 3.3V light", align='C', fill=True)
		self.cell(4, 3,"",0,1,'C', fill=False) # Dummy cell
		x = 15
		self.cell(10, 3,"",0,0,'C', fill=True)  # Dummy cell
		self.cell(x, 3,"I1 [A]",0,0,'C', fill=True)
		self.cell(x, 3,"I2 [A]",0,0,'C', fill=True)
		self.cell(x, 3,"I3 [A]",0,0,'C', fill=True)
		self.cell(x, 3,"I4 [A]",0,0,'C', fill=True)
		self.cell(x, 3,"I1 [A]",0,0,'C', fill=True)
		self.cell(x, 3,"I2 [A]",0,0,'C', fill=True)
		self.cell(x, 3,"I3 [A]",0,0,'C', fill=True)
		self.cell(x, 3,"I4 [A]",0,0,'C', fill=True)
		self.cell(x, 3,"Mean",0,0,'C', fill=True)
		self.cell(x, 3,"DesvEst",0,0,'C', fill=True)
		self.cell(x, 3,"CoefVar",0,0,'C', fill=True)
		self.cell(x, 3,"Stability CV",0,0,'C', fill=True) 
		self.cell(4, 3,"",0,1,'C', fill=False) 
		
		self.ln(1)
		
		# Get dataframe from text
		data = self.results
		# if x!="" last line empty in self.results
		df = pd.DataFrame([x.split(';') for x in data.split('\n')[1:] if x!=""], columns=[x for x in data.split('\n')[0].split(';')])
		# del info current 9.9V leakage & photo
		for i in range(1,5):
			df.pop("I" + str(i) + " [A] Leakage current @ 9.9V")
			df.pop("I" + str(i) + " [A] Photo current @ 9.9V")

		fill_color = 200
		fill = True
		self.set_font('Helvetica', '', 5)
		self.set_fill_color(fill_color)

		for index, row in df.iterrows():
			x = 10
			contador = 0  #  campos
			for data in row.values:
				# format values
				if len(str(data))>12:
					data = "{:.4e}".format(Decimal(data))
				# leakage current
				if contador>=1 and contador<=4:
					if abs(float(data))>=self.leakage_current_level:
						self.set_text_color(255,0,0)
						# state_leakage = False
				# photo current
				if contador>=5 and contador<=8:
					if abs(float(data))<self.photo_current_level:
						self.set_text_color(255,0,0)
						# state_photo = False

				# coefvar
				if contador==11:
					CoefVar = '1'
					if abs(float(data))>self.coefVar_level:
						self.set_text_color(255,0,0)
						CoefVar = '0'
						# state_coefVar = False
				if contador==12:
					if CoefVar=='0':
						data = CoefVar
						self.set_text_color(255,0,0)
					
				link = ""
				if contador==0 and self.options["wafermap"]:

					link = self.pages_links[str(data)]
				self.cell(w=x, h=1.8,txt=str(data),align='C',fill=fill, link=link)
				self.set_text_color(0,0,0)
				x = 15
				contador += 1
			
			
			df_row = df.iloc[index]
			# miramos valores para el sensor
			# asignamos valores en np_array (1 = verde, 2= naranja, 3= naranja_rojo, 4 = rojo)
			color = self.color_sensor(df_row)
			if color == "verde": self.set_fill_color(34,139,34) # verde
			if color == "naranja": self.set_fill_color(255,165,0) # naranja
			if color == "naranja-rojo": self.set_fill_color(255,69,0) # rojo-naranja
			if color == "rojo": self.set_fill_color(255,0,0) # rojo

			
			# print cell color state
			self.cell(w=4, h=1.8,txt="",align='C',fill=True, link="")
			# reseteamos fill color
			fill_color = 200
			self.set_fill_color(fill_color)
			self.ln(2)
			fill = not fill
		
		# Print mean of means photo currents
		self.cell(w=10, h=3,txt="",align='C',fill=False)
		for i in range(0,8):
			self.cell(w=15, h=3,txt="",align='C',fill=False)
		df["Mean Photo current @ 3.3V"] = df["Mean Photo current @ 3.3V"].astype(float)
		mean_photo_currents = df["Mean Photo current @ 3.3V"].mean()
		
		self.set_font('Helvetica', 'B', 6)
		self.set_fill_color(34,139,34) # verde
		if abs(mean_photo_currents)<self.photo_current_level:
			self.set_fill_color(255,0,0) # rojo
		if len(str(mean_photo_currents))>12:
			mean_photo_currents = "{:.4e}".format(Decimal(mean_photo_currents))
		self.set_text_color(255,255,255)
		self.cell(w=15, h=3,txt=str(mean_photo_currents),align='C',fill=True)
		self.set_text_color(0,0,0)
		

	
	def print_mapa_wafer(self):
		rows = 15
		cols = 15
		
		# set blank values 175 devices
		zero_values = [[0,0],[0,1],[0,2],[0,3],[0,4],[0,10],[0,11],[0,12],[0,13],[0,14], \
		[1,0],[1,1],[1,2],[1,12],[1,13],[1,14], \
		[2,0],[2,1],[2,13],[2,14], \
		[3,0],[3,14], \
		[4,0],[4,14], \
		[7,1],[7,13], \
		[10,0],[10,14], \
		[11,0],[11,14], \
		[12,0],[12,1],[12,13],[12,14], \
		[13,0],[13,1],[13,2],[13,12],[13,13],[13,14], \
		[14,0],[14,1],[14,2],[14,3],[14,4],[14,10],[14,11],[14,12],[14,13],[14,14]]

		np_array = np.ones((rows,cols), dtype= int)
		for zero in zero_values:
			np_array[zero[0],zero[1]] = 0

			# S016 => [2,4], S022 => [2,10]
		# S085 =>  [7, 7]
		# S152 => [12,4], S158 => [12,10]
		one_values_ref = [[2,4],[2,10],[7,7],[12,4],[12,10]]
		
		# only 2 cases: 
		if self.num_devices==175: 
			np_array[np_array > 0] = 2
		else:
			# case 5 devices (refs devices)
			for one in one_values_ref:
				np_array[one[0],one[1]] = 2			

		return np_array

	def numpy_array_print_to_wafer(self, np_array):
		
		rows_num, cols_num = np_array.shape
		# fit middle page, calc width cell (same height)
		width_cell = round((self.WIDTH/2)/rows_num)
		height_cell = width_cell
		self.set_font('Helvetica','B',6)
		self.set_fill_color(34,139,34)  # verde bosque
		self.ln(5)
		counter = 0
		counter_chip2 = 0
		# get colors from dataframe
		data = self.results
		df = pd.DataFrame([x.split(';') for x in data.split('\n')[1:]], columns=[x for x in data.split('\n')[0].split(';')])
		# del info current 9.9V leakage & photo
		for i in range(1,5):
			df.pop("I" + str(i) + " [A] Leakage current @ 9.9V")
			df.pop("I" + str(i) + " [A] Photo current @ 9.9V")

		counters = dict()
		counters["verde"] = 0
		counters["naranja"] = 0
		counters["naranja-rojo"] = 0
		counters["rojo"] = 0
		counters["blanco"] = 0
		for row in range(0, rows_num):
			for column in range(0, cols_num):
				# np_array[row][column] == 0
				ln = 0
				if column == cols_num-1:
					ln = 1
				if np_array[row][column] == 0:
					name_sensor = ""
					fill = False
					border = 0
					self.cell(w=width_cell, h=height_cell, txt=name_sensor, ln=ln, border= border, fill=fill)
				else:
				
					if np_array[row][column] == 2:
						fill = True
						border = 1
						df_row = df.iloc[counter_chip2]
						name_sensor = "S" + str(counter).zfill(3)
						# miramos valores para el sensor
						# asignamos valores en np_array (1 = verde, 2= naranja, 3= naranja_rojo, 4 = rojo)
						color = self.color_sensor(df_row)
						if color == "verde": self.set_fill_color(34,139,34) # verde
						if color == "naranja": self.set_fill_color(255,165,0) # naranja
						if color == "naranja-rojo": self.set_fill_color(255,69,0) # rojo-naranja
						if color == "rojo": self.set_fill_color(255,0,0) # rojo
						counters[color] += 1
						self.pages_links[name_sensor] = self.add_link()
						counter += 1
						counter_chip2 +=1
					if np_array[row][column] == 1:
						name_sensor = "S" + str(counter).zfill(3)
						fill = False
						border = 1
						self.pages_links[name_sensor] = None
						counters["blanco"] += 1
						counter += 1
					self.cell(w=width_cell, h=height_cell, txt=name_sensor, ln=ln, border=border, fill=fill, link=self.pages_links[name_sensor])
				


		# Print counters
		self.ln(10)
		self.set_font('Helvetica' ,'B', 10)
		wh = 8
		self.set_fill_color(34,139,34)
		self.cell(w=wh, h=wh,txt="",fill=True,border=1)
		self.cell(w=80,h=wh,txt=str(counters["verde"]) + " good devices",ln=1, fill=False)
		self.ln(2)
		self.set_fill_color(255,165,0)
		self.cell(w=wh,h=wh,txt="",fill=True,border=1)
		self.cell(w=80,h=wh,txt=str(counters["naranja"])+ " defective leakage devices",ln=1, fill=False)
		self.ln(2)
		self.set_fill_color(255,69,0)
		self.cell(w=wh,h=wh,txt="",fill=True,border=1)
		self.cell(w=80,h=wh,txt=str(counters["naranja-rojo"])+ " defective CoefVar devices",ln=1, fill=False)
		self.ln(2)
		self.set_fill_color(255,0,0)
		self.cell(w=wh,h=wh,txt="",fill=True,border=1)
		self.cell(w=80,h=wh,txt=str(counters["rojo"])+ " defective both leakage and CoefVar devices",ln=1, fill=False)
		yield_value = '0%'
		if int(counters["verde"])!=0:
			yield_value = '{:.1%}'.format(1-((counters["naranja"] + counters["naranja-rojo"] + counters["rojo"]) / counters["verde"]))
		self.ln(2)

		self.cell(w=wh,h=wh,txt="",fill=False,border=0)
		self.cell(w=80,h=wh,txt="Yield: " + str(yield_value),ln=1, fill=False)

	def color_sensor(self, row):
		state_leakage = True
		state_photo = True
		state_coefVar =True
		# leakage current
		if abs(float(row["I1 [A] Leakage current @ 3.3V"]))>=self.leakage_current_level or \
			abs(float(row["I2 [A] Leakage current @ 3.3V"]))>=self.leakage_current_level  or \
			abs(float(row["I3 [A] Leakage current @ 3.3V"]))>=self.leakage_current_level  or \
			abs(float(row["I4 [A] Leakage current @ 3.3V"]))>=self.leakage_current_level:
			state_leakage = False
		# photo current
		if abs(float(row["I1 [A] Photo current @ 3.3V"]))<self.photo_current_level or \
			abs(float(row["I2 [A] Photo current @ 3.3V"]))<self.photo_current_level  or \
			abs(float(row["I3 [A] Photo current @ 3.3V"]))<self.photo_current_level  or \
			abs(float(row["I4 [A] Photo current @ 3.3V"]))<self.photo_current_level:
			state_photo = False
		# coefvar
		if abs(float(row["CoefVar Photo current @ 3.3V"]))>self.coefVar_level:
			state_coefVar = False

		if not state_leakage:
			if state_coefVar:
				return "naranja"
			else:
				return "rojo"
		else:
			if not state_coefVar:
				return "naranja-rojo"
		
		return "verde"

	def page_sensor(self, name_sensor, texto, df, type_meas="dark"):
		self.add_page()
		self.set_y(30)
		x = 20
		if "sensor_data" in self.options and self.options["sensor_data"]:
			if type_meas=="dark":
				self.set_link(self.pages_links[name_sensor], y=5, page=int(self.page_no()))
			# print info file (first line)
			self.set_font('Helvetica', 'B', 7)
			texto_lines = texto.split("\n")
			self.cell(30, 1, texto_lines[0], 0, 0, 'L')
			self.ln(5)
			# second line with columns
			df.columns = texto_lines[1].split(";")
			self.set_font('Helvetica', 'B', 6)
			x = 20
			fill_color = 150
			self.set_fill_color(fill_color)
			for column in df.columns:
				self.cell(x, 3,str(column),0,0,'',True)
			self.ln(4)
			# print values
			self.set_font('Helvetica', '', 5)
			fill = False
			for index, row in df.iterrows():
				fill_color = 200
				self.set_fill_color(fill_color)
				for data in row.values:
					self.set_text_color(0,0,0)
					if str(row.values[0]) == '-3.3':
						self.set_fill_color(173,216,230) # azul claro
						if type_meas=="dark":
							if abs(float(data))>=self.leakage_current_level:
								self.set_text_color(255,0,0)
						else:
							if abs(float(data))<self.photo_current_level:
								self.set_text_color(255,0,0)
					self.cell(x, 1.8,str(data),0,0,'',fill)
				self.ln(2)
				fill = not fill
			# set new x for images
			x = 120
		# create image
		y = 30
		if "sensor_plot" in self.options and self.options["sensor_plot"]:
			ax = plt.gca()
			df.plot(kind='line', x =df.columns[0], y=df.columns[1], ax=ax)
			df.plot(kind='line', x =df.columns[0], y=df.columns[2], ax=ax)
			df.plot(kind='line', x =df.columns[0], y=df.columns[3], ax=ax)
			df.plot(kind='line', x =df.columns[0], y=df.columns[4], ax=ax)
			plt.title(name_sensor + " " + type_meas)
			path_plot = self.path_abs + self.options["plot_folder"] + "/" + name_sensor + "_" + type_meas + '.png'
			plt.savefig(path_plot)
			plt.clf()
			# include plot in page
			self.image(path_plot, x, y, 90)
			y = 110
		if "sensor_image" in self.options and self.options["sensor_image"] and type_meas=="light":
			# create link here
			if not self.options["sensor_data"]:
				self.set_link(self.pages_links[name_sensor], y=5, page=self.page_no())
			# compress images then get
			txtCompressed = ""
			path_image = self.path_abs + self.options["image_folder"] + "/" + name_sensor + ".jpg"
			self.image(path_image, x+10, y, 70)

	def page_photos(self):
		path_photos = self.path_abs + self.options["image_folder"]
		ficheros_photos = os.listdir(path_photos)
		if len(ficheros_photos) != self.num_devices:
			self.error = True
			self.errorMessage = "Photos not equals to num devices!"
			self.widgets.txtResultReport.appendHtml('Error: ' + self.errorMessage)
		else:
			contador_filas = 0
			x = 20
			y = 30
			self.add_page()
			for sensor in range(0,self.num_devices):
				# 2 options: 5 devices or 175
				name_sensor = "S" + str(sensor).zfill(3)
				self.set_link(link=self.pages_links[name_sensor], y=y, page=int(self.page_no()))
				path_image = path_photos + "/" + name_sensor + '.jpg'
				if "compressed" in self.options and self.options["compressed"]<100 and self.options["compressed"]>0:
					path_image_c = path_image.replace(".jpg","_c.jpg")				
					picture = Image.open(path_image)	
					picture.save(path_image_c, quality=int(self.options["compressed"]), optimize=True)
					path_image = path_image_c

				self.image(path_image, x, y, 70)
				if "compressed" in self.options and self.options["compressed"]:
					os.remove(path_image)
				if x == 20:
					x = 110
				else:
					x = 20
					y = y + 50
					contador_filas += 1
				if contador_filas == 5:
					self.add_page()
					x = 20
					y = 30
					contador_filas = 0
				self.widgets.txtResultReport.appendHtml('&nbsp;- Page sensor: ' + name_sensor + ' done!')
				QApplication.processEvents()
			self.widgets.txtResultReport.appendHtml('Generating pdf report, please wait!')
			QApplication.processEvents()



	def print_report(self):
		# Generates the report
		# Print header page
		self.add_page()
		self.set_left_margin(10)
		# check wafermap inside page_header
		self.page_header()
		self.set_left_margin(10)
		# Check result file

		if "results" in self.options and self.options["results"]:
			self.add_page()
			self.page_results()
		
		# Check sensors pages
		if "sensor" in self.options and "dark_folder" in self.options and "light_folder" in self.options:
			dark_folder = self.options["dark_folder"]
			light_folder = self.options["light_folder"]
			# read all txt files & check if number of files == num_devices
			dark_folder_path = self.path_abs + dark_folder + "/"
			light_folder_path = self.path_abs + light_folder + "/"

			if self.options["sensor"]:
				try:
					ficheros_dark = os.listdir(dark_folder_path)
					ficheros_light = os.listdir(light_folder_path)
					if len(ficheros_dark) != self.num_devices or len(ficheros_light) != self.num_devices:
						self.error = True
						self.errorMessage = "Files not equals to num devices!"
					else:
						only_photos = False
						for fichero in ficheros_dark:
							name_sensor = fichero.replace(".txt","")
							f = open(dark_folder_path + fichero)
							lectura_dark = f.read()
							f.close()
							f = open(light_folder_path + fichero)
							lectura_light = f.read()
							f.close()
							df_dark = pd.read_csv(dark_folder_path + fichero, header=None, skiprows=2, sep=',')
							df_light = pd.read_csv(light_folder_path + fichero, header=None, skiprows=2, sep=',')
							if "sensor_data" in self.options and self.options["sensor_data"]:
								self.page_sensor(name_sensor,lectura_dark, df_dark, "dark")
								self.page_sensor(name_sensor,lectura_light, df_light, "light")
							else:
								only_photos = True
								break
								
							self.widgets.txtResultReport.appendHtml('&nbsp;- Page sensor: ' + name_sensor + ' done!')
							QApplication.processEvents()
						if "sensor_image" in self.options and self.options["sensor_image"] and only_photos:
							# only images
							self.page_photos()
								
				except Exception as ex:
					self.error = True
					self.errorMessage = ex
					print(self.errorMessage)
			

		if self.error:
			print(self.errorMessage)
		self.widgets.txtResultReport.appendHtml('<br />Report done ' + self.filename_pdf + '!<br />')

	def __del__(self):
		pass
				
