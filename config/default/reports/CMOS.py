# CMOS report Class
import math
from typing import List, Any

from fpdf import FPDF
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageColor
import os
import pandas as pd
from PySide6.QtWidgets import *
from matplotlib.pyplot import figure

from modules.result_file import ResultFile
from modules.statistics_estepa import StatisticsEstepa
import toml
import json
import shutil
from modules.estepa import Estepa
import time


class CMOS(FPDF):
    logo = 'logo.svg'

    def __init__(self, widgets, options, path_run, config, dir_assets='config/default/reports/assets/'):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297
        self.options = options
        self.path_run = path_run
        self.config = config
        self.estepa = Estepa(self.config["mecao"])
        self.run = os.path.basename(os.path.normpath(path_run)).lower().strip().replace("run ", "")
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

    def header(self, title="CMOS REPORT"):
        # Custom logo and positioning
        # Create an `assets` folder and put any wide and short image inside
        # Name the image `logo.png`
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
        plt.style.use('default')  # for prevent mpl uses inside Caracterizar
        # remove comparative dir if exists
        print("Checking wafers...")
        if "comparative" in self.options:
            if os.path.exists(self.path_run + "/" + self.options["comparative"]):
                shutil.rmtree(self.path_run + "/" + self.options["comparative"])
        for directory in sorted(os.listdir(self.path_run)):
            if os.path.isdir(self.path_run + "/" + directory):
                wafer_add = directory
                # check compensation
                if "compensation" in self.options and self.options["compensation"]:
                    wafer_add_C = wafer_add + "_C"
                    self.wafers.append(wafer_add_C)
                    wafer_add_NC = wafer_add + "_NC"
                    self.wafers.append(wafer_add_NC)
                else:
                    self.wafers.append(wafer_add)
        # self.wafers = ['15813-5','15813-6']
        if len(self.wafers) > 0:
            for wafer in self.wafers:
                dir_wafer = self.path_run + "/" + wafer.replace("_C", "").replace("_NC", "") + "/"
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
                # create data files if not exists (from dat file)print
                dir_data = dir_wafer + self.options["data_folder"]
                # save always
                result_file = ResultFile(filename_results, self.options["excluded_parameters"])
                result_file.create_data_files(dir_data, prefix="CMOS_", show_die=True, show_module=True,
                                              show_header=True, wafer=wafer, text_die=False, text_module=True)
                # create plots
                if "cmos_plot" in self.options and self.options["cmos_plot"]:
                    path_plot = dir_wafer + self.options["plot_folder"] + "/"
                    path_data = dir_wafer + self.options["data_folder"] + "/"
                    existsPlot = False
                    if len(os.listdir(path_plot)) > 0:
                        existsPlot = True
                    if not existsPlot:
                        # create plots
                        counter_TRT = 0
                        counter_RCM = 0
                        plt.clf()
                        plt.cla()
                        for filedata in os.listdir(path_data):
                            QApplication.processEvents()
                            if os.path.isfile(path_data + filedata):
                                # create plot in path_plot
                                if "TRT" in filedata:
                                    try:

                                        df = pd.read_csv(path_data + filedata, header=0, delim_whitespace=True)
                                        ax = plt.gca()

                                        df.plot(kind='line', x=df.columns[0], y=df.columns[1], ax=ax, label="Id-Vg",
                                                color="blue", grid=True)

                                        plt.subplots_adjust(left=0.2)
                                        plt.title("Id vs Vg " + filedata.replace(".txt", "").split(" ")[-1])
                                        plt.xlabel("Voltage (V)")
                                        plt.ylabel("Drain current (A)")
                                        fileplot = path_plot + filedata.replace(".txt", ".png")
                                        plt.savefig(fileplot, dpi=100)
                                        plt.clf()
                                        counter_TRT += 1
                                    except Exception as e:
                                        print(f"Error procesando {filedata}: {e}")
                                if "RCM" in filedata:
                                    try:
                                        df = pd.read_csv(path_data + filedata, header=0, delim_whitespace=True)
                                        ax = plt.gca()

                                        df.plot(kind='line', x=df.columns[0], y=df.columns[5], ax=ax, label="RC-I",
                                                color="blue", grid=True)

                                        plt.subplots_adjust(left=0.2)
                                        plt.title(filedata.replace(".txt", "").split(" ")[-1])
                                        plt.xlabel("Current (I)")
                                        plt.ylabel("RC (Ohms)")
                                        fileplot = path_plot + filedata.replace(".txt", ".png")
                                        plt.savefig(fileplot, dpi=100)
                                        plt.clf()
                                        counter_RCM += 1
                                    except Exception as e:
                                        print(f"Error procesando {filedata}: {e}")
                        self.widgets.txtResultReport.appendPlainText(
                            " - Created " + str(counter_TRT) + " TRT graphs for wafer: " + wafer +
                            " and " + str(counter_RCM) + " RCM graphs.")
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
        estepa_configuration = self.config["estepa"] # app values
        if len(self.config_estepa_toml) != 0:
            if self.run in self.config_estepa_toml: # values for run
                estepa_configuration = self.config_estepa_toml[self.run]
            if self.run in self.config_estepa_toml and wafer in self.config_estepa_toml[self.run]: # values for wafer
                estepa_configuration = self.config_estepa_toml[self.run][wafer]
            if self.run in self.config_estepa_toml and wafer in self.config_estepa_toml[self.run] and parameter in \
                    self.config_estepa_toml[self.run][wafer]: # values for parameter
                estepa_configuration = self.config_estepa_toml[self.run][wafer][parameter]

        return estepa_configuration

    def page_header(self):
        QApplication.processEvents()
        self.set_y(100)
        self.set_font('Dejavu', 'B', 24)
        self.cell(0, 10, self.config["reports"]["title"], 0, 1, 'C')
        self.set_font('Dejavu', 'B', 18)
        self.cell(0, 10, self.config["reports"]["subtitle"], 0, 1, 'C')
        self.set_y(250)
        if self.config["reports"]["date"] != "":
            self.set_font('Dejavu', 'B', 12)
            self.cell(150, 6, "Date: ", 0, 0, 'R')
            self.set_font('Dejavu', '', 10)
            self.cell(60, 6, self.config["reports"]["date"], 0, 1, 'L')
        if self.config["reports"]["author"] != "":
            self.set_font('Dejavu', 'B', 12)
            self.cell(150, 6, "Author: ", 0, 0, 'R')
            self.set_font('Dejavu', '', 10)
            self.cell(60, 6, self.config["reports"]["author"], 0, 1, 'L')

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
        self.cell(50, 5, "- Temperature: ", 0, 0, 'L')
        self.cell(50, 5, f"{str(conditions['temperature'])} ºC", 0, 1, 'L')

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
            if "singularities" in info and str(info["singularities"]) != "":
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

    def page_info_file(self, result_file):
        """
        Page info file in report
        :param result_file: result_file object
        :return: None
        """
        parameters = result_file.get_parameters()
        QApplication.processEvents()
        self.set_y(30)
        self.set_font('Dejavu', 'B', 11)
        self.cell(0, 10, f"{result_file.filename} details:", 0, 1, 'L')
        self.set_font('Dejavu', '', 10)
        self.cell(50, 5, "- Process: ", 0, 0, 'L')
        self.cell(50, 5, parameters["process_name"], 0, 1, 'L')
        self.cell(50, 5, "- Lot: ", 0, 0, 'L')
        self.cell(50, 5, parameters["lot_name"], 0, 1, 'L')
        self.cell(50, 5, "- Wafer: ", 0, 0, 'L')
        self.cell(50, 5, parameters["wafer_name"], 0, 1, 'L')
        self.cell(50, 5, "- Mask: ", 0, 0, 'L')
        self.cell(50, 5, parameters["mask_name"], 0, 1, 'L')
        self.cell(50, 5, "- Operator: ", 0, 0, 'L')
        self.cell(50, 5, parameters["operator_name"], 0, 1, 'L')
        self.cell(50, 5, "- Temperature: ", 0, 0, 'L')
        self.cell(50, 5, f"{str(parameters['temperature'])} ºC", 0, 1, 'L')
        self.cell(50, 5, "- Humidity: ", 0, 0, 'L')
        self.cell(50, 5, f"{str(parameters['humidity'])} %", 0, 1, 'L')
        self.cell(50, 5, "- Date: ", 0, 0, 'L')
        self.cell(50, 5, parameters["date"], 0, 1, 'L')
        self.cell(50, 5, "- Time: ", 0, 0, 'L')
        self.cell(50, 5, parameters["time"], 0, 1, 'L')

    def print_report(self, wafer):
        # Order list
        parameters_order_list = ['VTN30', 'BETAN30', 'VTP30', 'BETAP30',
                                 'VTN30x3', 'BETAN30x3', 'VTP30x3', 'BETAP30x3',
                                 'VTFN', 'VTFP', 'IOFFN30', 'IOFFP30',
                                 'LEFFN', 'LEFFP', 'RCMP+', 'RCMN+',
                                 'RCMP0', 'RCMP1', 'R#P+', 'R#N+',
                                 'R#P0', 'R#P1', 'R#M1', 'R#NTUB', 'R#P1AA',
                                 'DWP+', 'DWN+', 'DWP0', 'DWP1', 'DWM1', 'DWNTUB', 'DWP1AA']
        parameters_excluded = ['IOFFN30x3', 'IOFFP30x3', 'BETAFN', 'BETAFP', 'IOFFFN', 'IOFFFP']
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

        # get result file object
        wafer_path = self.path_run + "/" + wafer.replace("_C", "").replace("_NC", "")
        file_results = wafer_path + "/" + wafer + ".dat"
        result_file = ResultFile(file_results, self.options["excluded_parameters"])
        # print page info
        self.add_page()
        self.page_info_file(result_file)
        # Print header page
        self.add_page()
        y = 30
        self.set_y(y)
        self.set_font('Dejavu', 'B', 9)
        fill_color = 200  # gris claro
        self.set_fill_color(fill_color)
        x = 25
        self.cell(w=x, h=5, txt=wafer, align='C', fill=True)
        self.cell(w=x, h=5, txt="Mean", align='C', fill=True)
        self.cell(w=x, h=5, txt="Stddev", align='C', fill=True)
        self.cell(w=x, h=5, txt="Median", align='C', fill=True)
        self.cell(w=x, h=5, txt="Points", align='C', fill=True)
        x = 20
        self.cell(w=x, h=5, txt="Method", align='C', fill=True)
        x = 20
        self.cell(w=x, h=5, txt="Limits", align='C', fill=True)
        self.cell(4, 3, "", 0, 1, 'C', fill=False)  # Dummy cell
        # print statistics
        parameters_file_list = list()
        parameters_file_list_sorted = list()
        if not result_file.error:
            parameters_file_list = result_file.params_list
            parameters_file_list = [param for param in parameters_file_list if param not in parameters_excluded]
            parameters_file_list_sorted = sorted(parameters_file_list,
                                                 key=lambda x: parameters_order_list.index(x))
            measurements = result_file.get_params(parameters_file_list)
            estadistica = dict()
            for parameter in parameters_file_list_sorted:
                if parameter not in self.parameter_list:
                    self.parameter_list.append(parameter)
                # check configuration toml
                # load with default system configuration estepa or toml (if exists)
                estepa_configuration = self.get_estepa_configuration_toml(wafer, parameter)
                if "autolimits" in estepa_configuration and estepa_configuration["autolimits"]:
                    autolimits = self.estepa.get_autolimits(parameter)
                    if autolimits is not None:
                        estepa_configuration["limmin"] = autolimits[0]
                        estepa_configuration["limmax"] = autolimits[1]

                data_list = measurements[parameter]["medida"]
                estadistica[parameter] = StatisticsEstepa(parameter, data_list, estepa_configuration)
                # Construct dataWafersParameters (without outliers)
                for value in estadistica[parameter].data_list:
                    if "BETA" in parameter:
                        value = float(value) * 1E6
                    self.dataWafersParameters_list.append([wafer, parameter, value])
                    QApplication.processEvents()
                y = y + 5
                self.set_y(y)
                self.set_font('Dejavu', 'B', 8)
                if not estadistica[parameter].error:
                    mean = self.format_param_value(estadistica[parameter].mean)
                    stdev = self.format_param_value(estadistica[parameter].stdev)
                    median = self.format_param_value(estadistica[parameter].median)
                    if "BETA" in parameter:
                        mean = self.format_param_value(float(mean) * 1E6)
                        stdev = self.format_param_value(float(stdev) * 1E6)
                        median = self.format_param_value(float(median) * 1E6)
                    x = 25
                    self.cell(w=x, h=5, txt=parameter, align='C', fill=False)
                    self.set_font('Dejavu', '', 8)
                    self.cell(w=x, h=5, txt=str(mean), align='C', fill=False)
                    self.cell(w=x, h=5, txt=str(stdev), align='C', fill=False)
                    self.cell(w=x, h=5, txt=str(median), align='C', fill=False)
                    points = str(estadistica[parameter].points_end) + "/" + str(estadistica[parameter].points_ini)
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
                    # ERROR
                    # y = y + 5
                    # self.text(20, y, parameter + " statistics error: " + estadistica[
                    #     parameter].error_message + " Check estepa configuration file!")
                    x = 25
                    self.cell(w=x, h=5, txt=parameter, align='C', fill=False)
                    self.set_font('Dejavu', '', 8)
                    self.cell(w=x, h=5, txt="-", align='C', fill=False)
                    self.cell(w=x, h=5, txt="-", align='C', fill=False)
                    self.cell(w=x, h=5, txt="-", align='C', fill=False)
                    points = "0/" + str(estadistica[parameter].points_ini)
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
            self.text(20, 35, "Error message wafer " + wafer + ": " + result_file.error_message)

        # print wafermap & histogram
        left = True
        for parameter in parameters_file_list_sorted:
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
                self.text(x_texto, 35, wafer)
                self.set_font('Dejavu', '', 9)
                self.text(x_texto, 40, parameter)
                self.numpy_array_print_to_wafer(np_array, estadistica[parameter], left)

            # print histogram
            if "histogram" in self.options and self.options["histogram"]:
                num_chunks = estadistica[parameter].config["chunks"]
                data = estadistica[parameter].data_list
                fig = Figure(figsize=(6, 4), dpi=300)
                fig.subplots_adjust(top=0.8)
                ax1 = fig.add_subplot(211)
                ax1.set_ylabel("")
                ax1.set_title(parameter + " histogram")
                n, bins, patches = ax1.hist(
                    np.array(data), num_chunks, facecolor="#228b22", edgecolor="#228b22"
                )
                ax1.grid(True)
                ax1.set_xlabel(parameter)
                # Converting Figure to an image:
                canvas = FigureCanvas(fig)
                canvas.draw()
                img = Image.fromarray(np.asarray(canvas.buffer_rgba()))
                if left:
                    self.set_x(0)
                else:
                    self.set_x(int(self.WIDTH / 2))
                self.image(img, w=int(self.WIDTH / 2))
                matplotlib.pyplot.close(fig)  # to prevent warning memory consumed (more than 20 graphs opened)
            left = not left

    @staticmethod
    def format_param_value(value):
        if abs(float(value)) > 9999.999 or abs(float(value)) < 0.001:
            value = "{:.3E}".format(value)
        else:
            value = "{:.3f}".format(value)
        return value

    def print_mapa_wafer(self):
        rows = 8
        cols = 8
        num_devices = 48
        # set blank values 141 devices
        zero_values = [
            [0, 0], [0, 1], [0, 6], [0, 7], \
            [1, 0], [1, 7], \
            [2, 0], [2, 7], \
            [5, 0], [5, 7], \
            [6, 0], [6, 7], \
            [7, 0], [7, 1], [7, 6], [7, 7] \
            ]

        np_array = np.ones((rows, cols), dtype=int)
        for zero in zero_values:
            np_array[zero[0], zero[1]] = 0

        # only 1 cases:
        if num_devices == 48:
            np_array[np_array > 0] = 2

        return np_array

    def numpy_array_print_to_wafer(self, np_array, estadistica_param, left=True):
        rows_num, cols_num = np_array.shape
        paleta_valores = []
        # fit middle page, calc width cell (same height)
        width_cell = round((self.WIDTH / 2.5) / rows_num)
        height_cell = width_cell
        self.set_fill_color(34, 139, 34)  # verde bosque (#228b22)
        self.ln(5)
        counter = 1
        counter_chip2 = 1
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
                    name_sensor = ""
                    border = 0
                    fill = False
                    if np_array[row][column] == 2:
                        fill = True
                        border = 1
                        name_sensor = "C" + str(counter).zfill(3)
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
                    self.cell(w=width_cell, h=height_cell, txt=name_sensor, ln=ln, border=border, fill=fill, align='C')
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
            yield_value = '{:.1%}'.format(1 - ((counters["outlier"] + counters["error"]) / counters["verde"]))
        self.ln(2)
        if not left: self.cell(int((self.WIDTH / 2)))
        self.cell(w=wh, h=wh, txt="", fill=False, border=0)
        self.cell(w=80, h=wh, txt="Yield: " + str(yield_value), ln=1, fill=False)

    def table_conditions(self, type, wafer, y, units):
        # coge las condiciones de los ficheros CV.json y CW.json que estan dentro de la carpeta de cada wafer
        # sino coge las generales
        wafer_path = self.path_run + "/" + wafer
        file_config = wafer_path + "/" + type + ".json"
        file_config_general = self.path_run + "/" + type + ".json"
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
            self.cell(w=120, h=5, txt="", ln=0, fill=False, align='C')
            self.cell(w=45, h=5, txt=type + " conditions", ln=1, fill=True, align='C')
            self.set_font('Dejavu', '', 7)
            fill_color_rgb = [240, 255, 255]  # azure (https://htmlcolorcodes.com/colors/shades-of-blue/)
            self.set_fill_color(fill_color_rgb[0], fill_color_rgb[1], fill_color_rgb[2])
            for param, value in config.items():
                self.cell(w=120, h=3, txt="", ln=0, fill=False, align='C')
                self.cell(w=25, h=3, txt=param, ln=0, fill=True, align='R')
                txtValue = str(value)
                if param == "PN":
                    txtValue = "Type "
                    txtValue += ("P" if int(value) == 1 else "N")
                if param in units[type]:
                    txtValue += " " + units[type][param]
                self.cell(w=20, h=3, txt=txtValue, ln=1, fill=True)

    def print_comparative(self):
        if "comparative" in self.options:
            dataWafersParameters = pd.DataFrame(np.array(self.dataWafersParameters_list),
                                                columns=['Wafer', 'Parameter', 'Value'])
            dir_comparative = self.path_run + "/" + self.options["comparative"] + "/"
            if not os.path.exists(dir_comparative):
                os.mkdir(dir_comparative)
            filePlot_list: list[str | Any] = list()
            filePlot = ""
            for parameter in self.parameter_list:
                parameter_data = list()
                for wafer in self.wafers:
                    filePlot = dir_comparative + parameter + ".png"
                    parameter_data.append(np.array(dataWafersParameters.loc[(dataWafersParameters["Wafer"] == wafer) & (
                            dataWafersParameters["Parameter"] == parameter), "Value"].astype("float")))
                # fig = plt.figure(figsize=(10, 7))
                if filePlot != "":
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
                        # reduce text size in x axis & rotation 45º
                        plt.xticks(fontsize=6, rotation=45)

                    else:
                        plt.xticks([i for i in range(1, len(self.wafers) + 1)], self.wafers)

                    plt.savefig(filePlot, dpi=100)
                    filePlot_list.append(filePlot)
                    plt.clf()
                    plt.close()
            # plt.show()
            # save images into pdf
            if filePlot_list:
                self.add_page()
                self.set_font('Dejavu', 'B', 11)
                y = 20
                self.set_y(y)
                self.cell(0, 10, "Comparative graphs:", 0, 1, 'L')
                y = 30
                self.set_y(y)
                for filePlot in filePlot_list:
                    self.image(filePlot, 20, y, self.WIDTH / 1.3)
                    if y == 30:
                        y = 140
                    else:
                        self.add_page()
                        y = 30
                    self.set_y(y)
