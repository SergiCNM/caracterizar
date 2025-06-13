# BASIC report Class
import math

from fpdf import FPDF
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageColor
import os
import pandas as pd
from pandas.plotting import table
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from decimal import Decimal
from modules.result_file import ResultFile
from modules.statistics_estepa import StatisticsEstepa
import toml
import json
import shutil


class NANUSENS(FPDF):
    logo = 'logo.svg'

    def __init__(self, widgets, options, path_run, config, dir_assets='config/default/reports/assets/'):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
        self.options = options
        self.path_run = path_run
        self.config = config
        self.run = os.path.basename(os.path.normpath(path_run))
        self.dir_assets = dir_assets
        self.error = False
        self.errorMessage = ""
        self.widgets = widgets
        self.page_link = {}
        self.wafers = list()
        self.parameter_list = list()
        self.dataWafersParameters_list = list()  # list of list with (wafer, parameter, value)
        self.check_wafers()
        self.config_estepa_toml = dict()
        self.get_toml()
        base_dejavu_path = 'c:\\WINDOWS\\FONTS\\'
        # base_dejavu_path = 'C:\\Users\\Sergi\\Downloads\\DejaVuSerif\\'
        self.add_font('DejaVu', '', os.path.join(base_dejavu_path, 'DejaVuSerif.ttf'))
        self.add_font('DejaVu', 'B', os.path.join(base_dejavu_path, 'DejaVuSerif-Bold.ttf'))
        self.add_font('DejaVu', 'I', os.path.join(base_dejavu_path, 'DejaVuSerif-Italic.ttf'))

    def header(self, title="NANUSENS REPORT"):
        # Custom logo and positioning
        # Create an `assets` folder and put any wide and short image inside
        # Name the image `logo.png`
        if self.widgets.txtReportTitle.text() != "":
            title = self.widgets.txtReportTitle.text()
        self.set_left_margin(20)
        self.page_link["page1"] = self.add_link()
        if self.page_no() == 1:
            self.image(os.getcwd() + "/" + self.dir_assets + self.logo, 20, 8, 50, 16, link=self.page_link["page1"])
            self.set_link(self.page_link["page1"], 80, 1)
        else:
            self.image(os.getcwd() + "/" + self.dir_assets + self.logo, 20, 8, 25, 8, link=self.page_link["page1"])
            self.set_font('Dejavu', 'B', 10)
            self.cell(int(self.WIDTH / 2), 1, "", 0, 0, 'R')
            self.cell(int(self.WIDTH / 2) - 30, 1, title, 0, 0, 'R')
            self.ln(3)
            self.set_font('Dejavu', '', 9)
            self.cell(int(self.WIDTH / 2), 1, "", 0, 0, 'R')
            self.cell(int(self.WIDTH / 2) - 30, 1, self.run, 0, 0, 'R')
            self.ln(20)

    def footer(self, page_txt="Page "):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font('Dejavu', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, page_txt + str(self.page_no()), 0, 0, 'C')

    def check_wafers(self):
        # remove comparative dir if exists
        if "comparative" in self.options:
            if os.path.exists(self.path_run + "/" + self.options["comparative"]):
                shutil.rmtree(self.path_run + "/" + self.options["comparative"])
        for directory in sorted(os.listdir(self.path_run)):
            if os.path.isdir(self.path_run + "/" + directory):
                wafer_add = directory
                self.wafers.append(wafer_add)
        # self.wafers = ['15813-5','15813-6']
        if len(self.wafers) > 0:
            for wafer in self.wafers:
                dir_wafer = self.path_run + "/" + wafer + "/"
                filename_results = dir_wafer + wafer + ".dat"
                if not os.path.isfile(filename_results):
                    self.error = True
                    self.errorMessage = "Filename DAT for wafer " + wafer + " doesn't exists!"
                    break
                # creating dirs for wafer
                for option in self.options:
                    if "_folder" in option:
                        if not os.path.exists(dir_wafer + self.options[option]):
                            os.mkdir(dir_wafer + self.options[option])
                # create data files if not exists (from dat file) print
                path_data = dir_wafer + self.options["data_folder"] + ""
                # save always
                result_file = ResultFile(filename_results, self.options["excluded_parameters"])
                result_file.create_data_files(path_data)

                # create plots
                if "plot" in self.options and self.options["plot"] and "plot_folder" in self.options:
                    path_plot = os.path.join(dir_wafer, self.options["plot_folder"])
                    existsPlot = False
                    if len(os.listdir(path_plot)) > 0:
                        existsPlot = True
                    if not existsPlot:
                        # create plots
                        counter = 0
                        for filedata in os.listdir(path_data):
                            QApplication.processEvents()
                            namefile = os.path.join(path_data, filedata)
                            if os.path.isfile(namefile):
                                # create plot in path_plot
                                if "CV" in filedata:
                                    # first column voltage, second capacitance, thrid conductance (CV_run-wafer_pos_module)
                                    text_plot = filedata.replace("_1.txt", "") + " DIE 01-01_DUT1"
                                    if filedata.endswith("_1.txt"):
                                        text_plot = filedata.replace("_1.txt", "") + " DIE 01-01_DUT1"
                                    elif filedata.endswith("_2.txt"):
                                        text_plot = filedata.replace("_2.txt", "") + " DIE 01-01_DUT4"
                                    elif filedata.endswith("_3.txt"):
                                        text_plot = filedata.replace("_3.txt", "") + " DIE 01-10_DUT1"
                                    elif filedata.endswith("_4.txt"):
                                        text_plot = filedata.replace("_4.txt", "") + " DIE 01-10_DUT4"
                                    df = pd.read_csv(namefile, header=None, sep=' ')
                                    ax = plt.gca()
                                    df.plot(kind='line', x=df.columns[0], y=df.columns[1], ax=ax, label="C-V",
                                            color="blue", grid=True)
                                    plt.title(text_plot)
                                    plt.xlabel("Voltage (V)")
                                    plt.ylabel("Capacitance (fF)")
                                    namefile_plot = os.path.join(path_plot, filedata.replace(".txt", ".png"))
                                    plt.savefig(namefile_plot, dpi=100)
                                    plt.clf()
                                    counter += 1

                        self.widgets.txtResultReport.appendPlainText(
                            " - Created " + str(counter) + " graphs for wafer: " + wafer)
        else:
            self.error = True
            self.errorMessage = "No wafers found in dir " + self.path_run

    def get_toml(self):
        path_config_file = self.path_run + "/" + self.run + ".toml"
        if os.path.exists(path_config_file):
            with open(path_config_file, mode="r", encoding='utf-8') as fp:
                config = toml.load(fp)
                self.config_estepa_toml = config

    def get_estepa_configuration_toml(self, wafer, parameter):
        estepa_configuration = self.config["estepa"]
        if len(self.config_estepa_toml) != 0:
            if self.run in self.config_estepa_toml and wafer in self.config_estepa_toml[self.run] and parameter in \
                    self.config_estepa_toml[self.run][wafer]:
                estepa_configuration = self.config_estepa_toml[self.run][wafer][parameter]
        return estepa_configuration

    def page_header(self):
        QApplication.processEvents()
        self.set_y(100)
        self.set_font('Dejavu', 'B', 24)
        self.cell(0, 10, self.config["reports"]["title"], 0, 1, 'C');
        self.set_font('Dejavu', 'B', 18)
        self.cell(0, 10, self.config["reports"]["subtitle"], 0, 1, 'C');
        self.set_y(250)
        if self.config["reports"]["date"] != "":
            self.set_font('Dejavu', 'B', 12)
            self.cell(150, 6, "Date: ", 0, 0, 'R');
            self.set_font('Dejavu', '', 10)
            self.cell(60, 6, self.config["reports"]["date"], 0, 1, 'L');
        if self.config["reports"]["author"] != "":
            self.set_font('Dejavu', 'B', 12)
            self.cell(150, 6, "Author: ", 0, 0, 'R');
            self.set_font('Dejavu', '', 10)
            self.cell(60, 6, self.config["reports"]["author"], 0, 1, 'L');

    def page_conditions(self):
        QApplication.processEvents()
        conditions = self.config_estepa_toml[self.run]["conditions"]
        self.set_y(30)
        self.set_font('Dejavu', 'B', 11)
        self.cell(0, 10, "Measurement conditions:", 0, 1, 'L')
        self.set_font('Dejavu', '', 10)
        self.cell(50, 5, "- PC: ", 0, 0, 'L')
        self.cell(50, 5, conditions["pc"], 0, 1, 'L')
        self.cell(50, 5, "- Software: ", 0, 0, 'L')
        self.cell(50, 5, conditions["software"], 0, 1, 'L')
        self.cell(50, 5, "- Equipment: ", 0, 0, 'L')
        self.cell(50, 5, conditions["equipment"], 0, 1, 'L')
        self.cell(50, 5, "- Prober: ", 0, 0, 'L')
        self.cell(50, 5, conditions["prober"], 0, 1, 'L')
        self.cell(50, 5, "- Test file: ", 0, 0, 'L')
        self.cell(50, 5, conditions["test_file"], 0, 1, 'L')
        self.cell(50, 5, "- Wafermap file: ", 0, 0, 'L')
        self.cell(50, 5, conditions["wafermap_file"], 0, 1, 'L')
        self.cell(0, 5, "", 0, 1, 'L')
        self.cell(50, 5, "- Start temperature: ", 0, 0, 'L')
        self.cell(50, 5, str(conditions["temperature"]) + " ºC", 0, 1, 'L')
        if "temperature_end" in conditions:
            self.cell(50, 5, "- End temperature: ", 0, 0, 'L')
            self.cell(50, 5, str(conditions["temperature_end"]) + " ºC", 0, 1, 'L')
        if "humidity" in conditions:
            self.cell(50, 5, "- Start humidity: ", 0, 0, 'L')
            self.cell(50, 5, str(conditions["humidity"]) + " %", 0, 1, 'L')
        if "humidity_end" in conditions:
            self.cell(50, 5, "- End humidity: ", 0, 0, 'L')
            self.cell(50, 5, str(conditions["humidity_end"]) + " %", 0, 1, 'L')
        self.cell(0, 5, "", 0, 1, 'L')

    def insert_image(self, image_path, y):
        img = Image.open(image_path)
        width = img.width
        height = img.height
        factor = width / height
        width_norm = self.WIDTH / 1.15
        height_norm = width_norm / factor
        if y + height_norm > self.HEIGHT:
            self.add_page()
            y = 30  # header page height
        self.image(image_path, 15, y, width_norm, height_norm)
        return y + int(height_norm)

    def page_info(self):
        QApplication.processEvents()
        info = self.config_estepa_toml[self.run]["info"]
        self.set_y(30)
        y = 30
        if "objective" in info:
            self.set_font('Dejavu', 'B', 11)
            self.cell(0, 10, "Objective:", 0, 1, 'L')
            y += 10
            self.set_font('Dejavu', '', 10)
            self.multi_cell(0, 10, info["objective"], 0, 'L')
            self.ln()
            y += 15 * (info["objective"].count('\n') + 1)
            self.set_font('Dejavu', 'B', 11)
            self.cell(0, 10, "Run data:", 0, 1, 'L')
            y += 10
            self.set_font('Dejavu', '', 10)
            self.cell(0, 10, "- " + str(info["wafers"]), 0, 1, 'L')
            y += 10
            self.cell(0, 10, "- Mask: " + str(info["mask"]), 0, 1, 'L')
            y += 10
            self.cell(0, 10, "- Run start date: " + str(info["run_start_date"]), 0, 1, 'L')
            y += 10
            self.cell(0, 10, "- Run end date: " + str(info["run_end_date"]), 0, 1, 'L')
            y += 10
            # Compensation INFORMATION
            self.cell(0, 10, "- Compensation info: ", 0, 1, 'L')
            y += 10
            self.multi_cell(0, 10, info["compensation_info"], 0, 'L')
            self.ln()
            y += 15 * (info["compensation_info"].count('\n') + 1)
            # Singularidades INFORMATION
            self.cell(0, 10, "- Singularities: ", 0, 1, 'L')
            y += 10
            self.multi_cell(0, 10, str(info["singularities"]), 0, 'L')
            self.ln()
            y += 15 * (info["singularities"].count('\n') + 1)

            if "singularities_image" in info and str(info["singularities_image"]) != "":
                singularities_images = str(info["singularities_image"]).split("|")
                for singularities_image in singularities_images:
                    image_path = self.path_run + "/" + singularities_image
                    y = self.insert_image(image_path, y)
            self.set_y(y)
            # REMARKABLE INCIDENTS
            if "remarkable_incidents" in info and str(info["remarkable_incidents"]) != "":
                while y > self.HEIGHT - 20:
                    y = y - self.HEIGHT + 20  # 10 plus space
                if y > int(self.HEIGHT / 2):
                    self.add_page()
                else:
                    self.cell(0, 5, "", 0, 1, 'L')  # estra space
                    y += 5
                self.set_font('Dejavu', 'B', 11)
                self.cell(0, 10, "Remarkable incidents:", 0, 1, 'L')
                y += 10
                self.set_font('Dejavu', '', 10)
                self.multi_cell(0, 10, str(info["remarkable_incidents"]), 0, 'L')
                self.ln()
                y += 15 * (info["remarkable_incidents"].count('\n') + 1)

                if "remarkable_incidents_photos" in info and str(info["remarkable_incidents_photos"]) != "":
                    self.add_page()
                    y = 20
                    self.set_y(y)
                    lista_remarkable_incidents_photos = info["remarkable_incidents_photos"].split("|")
                    lista_photos = lista_remarkable_incidents_photos[0::2]
                    lista_textos = lista_remarkable_incidents_photos[1::2]
                    self.set_font('Dejavu', '', 7)  # medida texto menor para fotos
                    for i, photo in enumerate(lista_photos):
                        image_path = self.path_run + "/" + photo
                        y = self.insert_image(image_path, y)
                        self.set_y(y)
                        self.cell(self.WIDTH - 40, 10, lista_textos[i], 0, 1, 'C')
                        y += 15  # 10 text + 5 sep extra
                    self.set_font('Dejavu', '', 10)

    @staticmethod
    def process_data(voltages, capacitances):
        # Convertir listas a DataFrame para facilitar el manejo
        data = pd.DataFrame({'Voltage': voltages, 'Capacitance': capacitances})
        # Obtener la capacidad en 0V
        coff = data.loc[data['Voltage'] == 0, 'Capacitance'].values[0]

        # Encontrar el salto en la capacidad
        capacitance_diff = data['Capacitance'].diff()
        jump_index = capacitance_diff.idxmax()
        pullin_voltage = data.loc[jump_index, 'Voltage']
        capacitance_after_jump = data.loc[jump_index, 'Capacitance']

        return coff, pullin_voltage, capacitance_after_jump

    def print_report(self, wafer):
        # Create report
        plt.style.use('default')  # for prevent mpl uses inside Caracterizar
        # Print title (only first wafer), with page info + page conditions
        if self.page_no() == 0:
            self.add_page()
            self.page_header()
            if self.run in self.config_estepa_toml and "info" in self.config_estepa_toml[self.run]:
                self.add_page()
                self.page_info()
            if self.run in self.config_estepa_toml and "conditions" in self.config_estepa_toml[self.run]:
                self.add_page()
                self.page_conditions()

        # parameters_file_list = list("coff", "pullin_voltage", "capacitance_after_jump")
        parameters_file_list = {
            "DIE 01-01_DUT1/4": {
                "Coff": [],
                "Vpullin": [],
                "Cmax": []
            },
            "DIE 01-10_DUT1/4": {
                "Coff": [],
                "Vpullin": [],
                "Cmax": []
            }
        }
        estadistica = dict()
        estadistica["DIE 01-01_DUT1/4"] = dict()
        estadistica["DIE 01-10_DUT1/4"] = dict()
        estadistica["DIE 01-01_DUT1/4"]["Coff"] = None
        estadistica["DIE 01-01_DUT1/4"]["Vpullin"] = None
        estadistica["DIE 01-01_DUT1/4"]["Cmax"] = None
        estadistica["DIE 01-10_DUT1/4"]["Coff"] = None
        estadistica["DIE 01-10_DUT1/4"]["Vpullin"] = None
        estadistica["DIE 01-10_DUT1/4"]["Cmax"] = None

        parameters_file_list_wafermap = {
            "DIE 01-01_DUT1": {
                "Coff": [],
                "Vpullin": [],
                "Cmax": []
            },
            "DIE 01-01_DUT4": {
                "Coff": [],
                "Vpullin": [],
                "Cmax": []
            },
            "DIE 01-10_DUT1": {
                "Coff": [],
                "Vpullin": [],
                "Cmax": []
            },
            "DIE 01-10_DUT4": {
                "Coff": [],
                "Vpullin": [],
                "Cmax": []
            }
        }
        estadistica_wafermap = dict()
        estadistica_wafermap["DIE 01-01_DUT1"] = dict()
        estadistica_wafermap["DIE 01-01_DUT4"] = dict()
        estadistica_wafermap["DIE 01-10_DUT1"] = dict()
        estadistica_wafermap["DIE 01-10_DUT4"] = dict()
        estadistica_wafermap["DIE 01-01_DUT1"]["Coff"] = None
        estadistica_wafermap["DIE 01-01_DUT4"]["Coff"] = None
        estadistica_wafermap["DIE 01-01_DUT1"]["Vpullin"] = None
        estadistica_wafermap["DIE 01-01_DUT4"]["Vpullin"] = None
        estadistica_wafermap["DIE 01-01_DUT1"]["Cmax"] = None
        estadistica_wafermap["DIE 01-01_DUT4"]["Cmax"] = None
        estadistica_wafermap["DIE 01-10_DUT1"]["Coff"] = None
        estadistica_wafermap["DIE 01-10_DUT4"]["Coff"] = None
        estadistica_wafermap["DIE 01-10_DUT1"]["Vpullin"] = None
        estadistica_wafermap["DIE 01-10_DUT4"]["Vpullin"] = None
        estadistica_wafermap["DIE 01-10_DUT1"]["Cmax"] = None
        estadistica_wafermap["DIE 01-10_DUT4"]["Cmax"] = None

        parameter_units = {
            "Coff": "fF",
            "Vpullin": "V",
            "Cmax": "fF"
        }
        # print parameters
        wafer_path = self.path_run + "/" + wafer
        file_results = wafer_path + "/" + wafer + ".dat"
        result_file = ResultFile(file_results, self.options["excluded_parameters"])

        if not result_file.error:
            # read all data files in data folder
            for die in result_file.dies:
                for module in result_file.modules:
                    voltages = result_file.data[die][module]['V(V)']
                    capacitances = result_file.data[die][module]['C(fF)']
                    # list string to float
                    voltages = [float(i) for i in voltages]
                    capacitances = [float(i) for i in capacitances]
                    coff, vpullin, cmax = self.process_data(voltages, capacitances)
                    where = "DIE 01-01_DUT1/4"
                    where_wafermap = "DIE 01-01_DUT1"
                    match module:
                        case "(1)":
                            where = "DIE 01-01_DUT1/4"
                            where_wafermap = "DIE 01-01_DUT1"
                        case "(2)":
                            where = "DIE 01-01_DUT1/4"
                            where_wafermap = "DIE 01-01_DUT4"
                        case "(3)":
                            where = "DIE 01-10_DUT1/4"
                            where_wafermap = "DIE 01-10_DUT1"
                        case "(4)":
                            where = "DIE 01-10_DUT1/4"
                            where_wafermap = "DIE 01-10_DUT4"

                    parameters_file_list[where]["Coff"].append(coff)
                    parameters_file_list[where]["Vpullin"].append(vpullin)
                    parameters_file_list[where]["Cmax"].append(cmax)

                    parameters_file_list_wafermap[where_wafermap]["Coff"].append(coff)
                    parameters_file_list_wafermap[where_wafermap]["Vpullin"].append(vpullin)
                    parameters_file_list_wafermap[where_wafermap]["Cmax"].append(cmax)

            for module_name in parameters_file_list:
                # Print header page
                self.add_page()
                y = 30
                self.set_y(y)
                self.set_font('Dejavu', 'B', 8)
                fill_color = 200  # gris claro
                self.set_fill_color(fill_color)
                x = 24
                self.cell(w=30, h=5, txt=module_name, align='C', fill=True)
                self.set_font('Dejavu', 'B', 9)
                self.cell(w=x, h=5, txt="Mean", align='C', fill=True)
                self.cell(w=x, h=5, txt="Stddev", align='C', fill=True)
                self.cell(w=x, h=5, txt="Median", align='C', fill=True)
                self.cell(w=x, h=5, txt="Points", align='C', fill=True)
                x = 20
                self.cell(w=x, h=5, txt="Method", align='C', fill=True)
                x = 20
                self.cell(w=x, h=5, txt="Limits", align='C', fill=True)
                self.cell(4, 3, "", 0, 1, 'C', fill=False)  # Dummy cell
                y = y + 5
                self.set_y(y)
                for parameter in parameters_file_list[module_name]:
                    estepa_configuration = self.get_estepa_configuration_toml(wafer, parameter)
                    estadistica[module_name][parameter] = StatisticsEstepa(parameter,
                                                                           parameters_file_list[module_name][parameter],
                                                                           estepa_configuration)
                    if not estadistica[module_name][parameter].error:
                        mean = self.format_param_value(estadistica[module_name][parameter].mean)
                        stdev = self.format_param_value(estadistica[module_name][parameter].stdev)
                        median = self.format_param_value(estadistica[module_name][parameter].median)
                        self.set_font('Dejavu', 'B', 8)
                        x = 24
                        parameter_txt = parameter + " (" + parameter_units[parameter] + ")"
                        self.cell(w=30, h=5, txt=parameter_txt, align='C', fill=False)
                        self.set_font('Dejavu', '', 8)
                        self.cell(w=x, h=5, txt=str(mean), align='C', fill=False)
                        self.cell(w=x, h=5, txt=str(stdev), align='C', fill=False)
                        self.cell(w=x, h=5, txt=str(median), align='C', fill=False)
                        points = str(estadistica[module_name][parameter].points_end) + "/" + str(
                            estadistica[module_name][parameter].points_ini)
                        self.cell(w=x, h=5, txt=points, align='C', fill=False)
                        # print outliers method in table
                        x = 20
                        self.cell(w=x, h=5, txt=estepa_configuration["method"], align='C', fill=False)
                        text_lna = "None"
                        if estepa_configuration["lna"]:
                            text_lna = str(estepa_configuration["limmin"]) + " - " + str(estepa_configuration["limmax"])
                        self.cell(w=x, h=5, txt=text_lna, align='C', fill=False)
                        self.cell(4, 3, "", 0, 1, 'C', fill=False)  # Dummy cell

                    else:
                        y = y + 5
                        self.text(20, y, parameter + " statistics error: " + estadistica[module_name][
                            parameter].error_message + "\nCheck estepa configuration file!")
                # table conditions
                units = dict()
                units["CV"] = {"START": "V", "STOP": "V", "FREQ": "kHz", "OSC": "mV"}
                y = y + 20
                image_CV = os.path.join(wafer_path, "CV_" + module_name.replace("/", "") + ".png")
                print(image_CV)
                if os.path.exists(image_CV):
                    self.image(image_CV, x, y, 90)
                    # print table
                    self.table_conditions("CV", wafer, 120, y, units)
                    y = y + 75
                #self.table_conditions("CV", wafer, 10, y, units)

            # wafermap & histogram
            left = True


            for module_name_wafermap in parameters_file_list_wafermap:
                for parameter_wafermap in parameters_file_list_wafermap[module_name_wafermap]:
                    estepa_configuration = self.get_estepa_configuration_toml(wafer, parameter_wafermap)
                    estadistica_wafermap[module_name_wafermap][parameter_wafermap] = StatisticsEstepa(
                        parameter_wafermap, parameters_file_list_wafermap[module_name_wafermap][parameter_wafermap],
                        estepa_configuration)


                for parameter_wafermap in estadistica_wafermap[module_name_wafermap]:
                    QApplication.processEvents()
                    if "wafermap" in self.options and self.options["wafermap"]:
                        np_array = self.print_mapa_wafer()
                        if left:
                            self.add_page()
                            self.set_x(10)
                            x_texto = 20
                        else:
                            x_texto = int(self.WIDTH / 2) + 20
                            self.set_x(x_texto)
                        self.set_y(30)
                        self.set_font('Dejavu', 'B', 10)
                        self.text(x_texto, 35, module_name_wafermap)
                        self.set_font('Dejavu', '', 9)
                        parameter_wafermap_text = parameter_wafermap + " (" + parameter_units[parameter_wafermap] + ")"
                        self.text(x_texto, 40, parameter_wafermap_text)
                        self.set_y(40)
                        # print count data_list
                        self.numpy_array_print_to_wafer(np_array, estadistica_wafermap[module_name_wafermap][parameter_wafermap], left)

                    print("wafermap " + wafer + " " + module_name_wafermap + " " + parameter_wafermap)

                    # print histogram
                    if "histogram" in self.options and self.options["histogram"]:
                        num_chunks = estadistica_wafermap[module_name_wafermap][parameter_wafermap].config["chunks"]
                        data = estadistica_wafermap[module_name_wafermap][parameter_wafermap].data_list
                        fig = Figure(figsize=(6, 4), dpi=300)
                        fig.subplots_adjust(top=0.8)
                        ax1 = fig.add_subplot(211)
                        ax1.set_ylabel("")
                        ax1.set_title(parameter_wafermap + " histogram")
                        n, bins, patches = ax1.hist(
                            np.array(data), num_chunks, facecolor="#228b22", edgecolor="#228b22"
                        )
                        ax1.grid(True)
                        ax1.set_xlabel(parameter_wafermap)
                        # Converting Figure to an image:
                        canvas = FigureCanvas(fig)
                        canvas.draw()
                        img = Image.fromarray(np.asarray(canvas.buffer_rgba()))
                        if left:
                            self.set_x(0)
                        else:
                            self.set_x(int(self.WIDTH / 2))
                        self.image(img, w=int(self.WIDTH / 2))
                        matplotlib.pyplot.close(
                            fig)  # to prevent warning memory consumed (more than 20 graphs opened)
                    left = not left
        else:
            self.text(20, 35, "Error message wafer " + wafer + ": " + result_file.error_message)

    @staticmethod
    def format_param_value(value):
        if float(value) > 9999.999 or float(value) < -9999.999:
            value = "{:.2e}".format(value)
        else:
            value = "{:.2f}".format(value)
        return value

    @staticmethod
    def print_mapa_wafer():
        rows = 5
        cols = 6
        num_devices = 26
        # set blank values 244 devices
        zero_values = [
            [0, 0], [0, 5], \
            [4, 0], [4, 5] \
            ]

        np_array = np.ones((rows, cols), dtype=int)
        for zero in zero_values:
            np_array[zero[0], zero[1]] = 0

        # only 1 cases:
        if num_devices == 26:
            np_array[np_array > 0] = 2

        return np_array

    def numpy_array_print_to_wafer(self, np_array, estadistica_param, left=True):
        rows_num, cols_num = np_array.shape
        print("rows_num: " + str(rows_num) + " cols_num: " + str(cols_num))
        # fit middle page, calc width cell (same height)
        width_cell = round((self.WIDTH / 2.6) / cols_num)
        height_cell = round((self.WIDTH / 2.6) / rows_num)
        self.set_fill_color(34, 139, 34)  # verde bosque (#228b22)
        self.ln(5)
        counter = 0
        counter_chip2 = 0
        # get colors from dataframe
        parameter = estadistica_param.param
        data_list = estadistica_param.data_list
        data_list_origen = estadistica_param.data_list_origen
        df = pd.DataFrame(data_list_origen, columns=[parameter])
        # sacamos df sin outliers para calcular el valor_min y valor_max
        df_without_outliers = pd.DataFrame(data_list, columns=[parameter])
        valor_min = df_without_outliers[parameter].min()
        valor_max = df_without_outliers[parameter].max()
        paleta_verdes = ['#DEF2B3', '#CDE7A0', '#BDDB8C', '#ACD079', '#9BC565', \
                         '#8BB952', '#7AAE3E', '#69A32B', '#599717', '#488C04']
        step_valores = float((valor_max - valor_min) / 10)
        if valor_max != valor_min and (not math.isnan(valor_min) or not math.isnan(valor_max)):
            paleta_valores = np.arange(valor_min, valor_max, step_valores).tolist()
        # inicializamos variables antes de recorrer datos
        counters = dict()
        counters["verde"] = 0
        counters["outlier"] = 0
        counters["error"] = 0
        counters["blanco"] = 0
        num_device = 0
        self.set_font('Dejavu', '', 6)
        for row in range(0, rows_num):
            extra_cell = False  # control extra cell at start (if right)
            for column in range(0, cols_num):
                ln = 0
                if not left and not extra_cell:
                    self.cell(int((self.WIDTH / 2)))
                    extra_cell = True
                if column == cols_num - 1:
                    ln = 1

                if np_array[row][column] == 0:
                    name_sensor = ""
                    fill = False
                    border = 0
                    self.cell(w=width_cell, h=height_cell, txt=name_sensor, ln=ln, border=border, fill=fill)
                else:
                    if np_array[row][column] == 2:
                        fill = True
                        border = 1
                        name_sensor = "C" + str(counter + 1).zfill(3)
                        # miramos valores para el sensor
                        # asignamos valores en np_array (1 = verde, 2= naranja, 3= naranja_rojo, 4 = rojo)
                        # color = self.color_sensor(df_row)
                        color = "verde"
                        parameter_value = data_list_origen[num_device]
                        if parameter_value not in data_list:
                            color = "outlier"
                        if parameter_value == estadistica_param.ERROR_VALUE2 or valor_max == valor_min:
                            color = "error"
                        if color == "verde":
                            # asignamos color verde flojo a ver oscuro según valor
                            j = 9
                            for i in range(9):  # de 0 a 8
                                if float(parameter_value) <= float(paleta_valores[i]):
                                    j = i
                                    break
                            rgb_color = ImageColor.getcolor(paleta_verdes[j], "RGB")
                            self.set_fill_color(rgb_color[0], rgb_color[1], rgb_color[2])  # verde
                        if color == "outlier": self.set_fill_color(0, 150, 255)  # bright blue rgb(0, 150, 255)
                        if color == "error": self.set_fill_color(255, 0, 0)  # rojo
                        counters[color] += 1
                        # self.page_link[name_sensor] = self.add_link()
                        counter += 1
                        counter_chip2 += 1
                        num_device += 1
                    if np_array[row][column] == 1:
                        name_sensor = "C" + str(counter).zfill(3)
                        fill = False
                        border = 1
                        # self.page_link[name_sensor] = None
                        counters["blanco"] += 1
                        counter += 1
                    # self.cell(w=width_cell, h=height_cell, txt=name_sensor, ln=ln, border= border, fill=fill, link=self.page_link[name_sensor], align='C')
                    texto_print = name_sensor
                    if name_sensor != "":
                        texto_print = str(self.format_param_value(parameter_value))

                    self.cell(w=width_cell, h=height_cell, txt=texto_print, ln=ln, border=border, fill=fill, align='C')

        # Print counters
        self.ln(10)
        self.set_font('Dejavu', 'B', 10)
        wh = 8
        self.set_fill_color(34, 139, 34)
        if not left: self.cell(int((self.WIDTH / 2)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=80, h=wh, txt=str(counters["verde"]) + " good devices", ln=1, fill=False)
        self.ln(2)
        self.set_fill_color(0, 150, 255)
        if not left: self.cell(int((self.WIDTH / 2)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=80, h=wh, txt=str(counters["outlier"]) + " outlier devices", ln=1, fill=False)
        self.ln(2)
        self.set_fill_color(255, 0, 0)
        if not left: self.cell(int((self.WIDTH / 2)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=80, h=wh, txt=str(counters["error"]) + " error devices", ln=1, fill=False)
        yield_value = '0%'
        if int(counters["verde"]) != 0:
            # yield_value = '{:.1%}'.format(1 - ((counters["outlier"] + counters["error"]) / counters["verde"]))
            yield_value = '{:.1%}'.format(
                counters["verde"] / (counters["outlier"] + counters["error"] + counters["verde"]))
        self.ln(2)
        if not left: self.cell(int((self.WIDTH / 2)))
        self.cell(w=wh, h=wh, txt="", fill=False, border=0)
        self.cell(w=80, h=wh, txt="Yield: " + str(yield_value), ln=1, fill=False)

    def table_conditions(self, namefile, wafer, w0, y, units):
        # coge las condiciones de los ficheros CV.json y CW.json que estan dentro de la carpeta de cada wafer
        # sino coge las generales
        wafer_path = self.path_run + "/" + wafer
        file_config = wafer_path + "/" + namefile + ".json"
        file_config_general = self.path_run + "/" + namefile + ".json"
        self.set_font('Dejavu', 'B', 8)
        fill_color_rgb = [137, 207, 240]  # baby blue (https://htmlcolorcodes.com/colors/shades-of-blue/)
        self.set_fill_color(fill_color_rgb[0], fill_color_rgb[1], fill_color_rgb[2])
        config = None
        if os.path.exists(file_config):
            f = open(file_config, mode='r')
            config = json.loads(f.read())
            f.close()
        elif os.path.exists(file_config_general):  # buscamos fichero general
            f = open(file_config_general, mode='r')
            config = json.loads(f.read())
            f.close()
        if config:
            y = y + 2
            self.set_y(y)
            self.cell(w=w0, h=5, txt="", ln=0, fill=False, align='C')
            name = config["NAME"]
            self.cell(w=45, h=5, txt=name + " conditions", ln=1, fill=True, align='C')
            self.set_font('Dejavu', '', 7)
            fill_color_rgb = [240, 255, 255]  # azure (https://htmlcolorcodes.com/colors/shades-of-blue/)
            self.set_fill_color(fill_color_rgb[0], fill_color_rgb[1], fill_color_rgb[2])
            for param, value in config.items():
                if param != "NAME":
                    self.cell(w=w0, h=3, txt="", ln=0, fill=False, align='C')
                    self.cell(w=25, h=3, txt=param, ln=0, fill=True, align='R')
                    txtValue = str(value)
                    if param in units[namefile]:
                        txtValue += " " + units[namefile][param]
                    self.cell(w=20, h=3, txt=txtValue, ln=1, fill=True)

    def print_comparative(self):
        if "comparative" in self.options:
            dataWafersParameters = pd.DataFrame(np.array(self.dataWafersParameters_list),
                                                columns=['Wafer', 'Parameter', 'Value'])
            dir_comparative = self.path_run + "/" + self.options["comparative"] + "/"
            if not os.path.exists(dir_comparative):
                os.mkdir(dir_comparative)
            fileplot_list = list()
            for parameter in self.parameter_list:
                parameter_data = list()
                for wafer in self.wafers:
                    fileplot = dir_comparative + parameter + ".png"
                    parameter_data.append(np.array(dataWafersParameters.loc[(dataWafersParameters["Wafer"] == wafer) & (
                            dataWafersParameters["Parameter"] == parameter), "Value"].astype("float")))
                # fig = plt.figure(figsize=(10, 7))
                # Creating plot
                plt.boxplot(parameter_data)
                # show plot
                plt.title(parameter + " comparative")
                plt.xlabel("Wafers")
                plt.ylabel(parameter)
                # if wafers too large graph comparative is overlapping
                if len(self.wafers) >= 10:
                    # prevent overlapping in ticks labels
                    new_wafers = [valor.split("-")[1] for valor in self.wafers]
                    plt.xticks([i for i in range(1, len(self.wafers) + 1)], new_wafers)
                else:
                    plt.xticks([i for i in range(1, len(self.wafers) + 1)], self.wafers)
                plt.savefig(fileplot, dpi=100)
                fileplot_list.append(fileplot)
                plt.clf()
                plt.close()
            # plt.show()
            # save images into pdf
            self.add_page()
            self.set_font('Dejavu', 'B', 11)
            y = 20
            self.set_y(y)
            self.cell(0, 10, "Comparative graphs:", 0, 1, 'L')
            y = 30
            self.set_y(y)
            for fileplot in fileplot_list:
                self.image(fileplot, 20, y, self.WIDTH / 1.3)
                if y == 30:
                    y = 140
                else:
                    self.add_page()
                    y = 30
                self.set_y(y)
