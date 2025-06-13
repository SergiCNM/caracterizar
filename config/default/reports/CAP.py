# CAP report Class
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


class CAP(FPDF):
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

    def header(self, title="CAP REPORT"):
        # Custom logo and positioning
        # Create an `assets` folder and put any wide and short image inside
        # Name the image `logo.png`
        self.set_left_margin(20)

        self.page_link["page1"] = self.add_link()
        # self.image(os.getcwd() + "/" + self.dir_assets + 'logo.png', 20, 8, 50, 16, link = self.page_link["page1"])
        if self.page_no() == 1:
            self.image(os.getcwd() + "/" + self.dir_assets + 'logo.svg', 20, 8, 50, 16, link=self.page_link["page1"])
            self.set_link(self.page_link["page1"], 80, 1)
        else:
            self.image(os.getcwd() + "/" + self.dir_assets + 'logo.svg', 20, 8, 25, 8, link=self.page_link["page1"])
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
        # remove compartive
        if "comparative" in self.options:
            if os.path.exists(self.path_run + "/" + self.options["comparative"]):
                shutil.rmtree(self.path_run + "/" + self.options["comparative"])
        for dir in sorted(os.listdir(self.path_run)):
            if os.path.isdir(self.path_run + "/" + dir):
                self.wafers.append(dir)
        # self.wafers = ['15813-5','15813-6']
        if len(self.wafers) > 0:
            for wafer in sorted(self.wafers):
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
                # create data files if not exists (from dat file)
                dir_data = dir_wafer + self.options["data_folder"]
                if len(os.listdir(dir_data)) == 1:  # only one CW txt file
                    result_file = ResultFile(filename_results)
                    result_file.create_data_files(dir_data)
                # create plots
                if "cap_plot" in self.options and self.options["cap_plot"]:
                    path_plot = dir_wafer + self.options["plot_folder"] + "/"
                    path_data = dir_wafer + self.options["data_folder"] + "/"
                    existsPlot = False
                    if len(os.listdir(path_plot)) > 0:
                        existsPlot = True
                    if not existsPlot:
                        # create plots
                        counter = 0
                        for filedata in os.listdir(path_data):
                            QApplication.processEvents()
                            if os.path.isfile(path_data + filedata):
                                # create plot in path_plot
                                if "CV" in filedata:
                                    # first column voltage, second capacitance, thrid conductance (CV_run-wafer_pos_module)
                                    df = pd.read_csv(path_data + filedata, header=None, sep=' ')
                                    ax = plt.gca()
                                    df.plot(kind='line', x=df.columns[0], y=df.columns[1], ax=ax, label="C-V",
                                            color="blue", grid=True)
                                    plt.title("Capacitance vs Voltage")
                                    plt.xlabel("Voltage (V)")
                                    plt.ylabel("Capacitance (F)")
                                    fileplot = path_plot + filedata.replace(".txt", ".png")
                                    plt.savefig(fileplot, dpi=100)
                                    plt.clf()
                                    counter += 1
                                if "CW" in filedata:
                                    # first column frequency, second capacitance, thrid conductance (CV_run-wafer_pos_module)
                                    df = pd.read_csv(path_data + filedata, header=None, sep=' ')
                                    bx = plt.gca()
                                    df.plot(kind='line', x=df.columns[0], y=df.columns[1], ax=bx, label="C-W",
                                            color="blue", grid=True)
                                    plt.title("Capacitance vs Frequency")
                                    plt.xlabel("Frequency (kHz)")
                                    plt.ylabel("Capacitance (F)")
                                    plt.xscale('log')
                                    fileplot = path_plot + filedata.replace(".txt", ".png")
                                    plt.savefig(fileplot)
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
        self.cell(50, 5, "- Capacimeter: ", 0, 0, 'L')
        self.cell(50, 5, conditions["capacimeter"], 0, 1, 'L')
        self.cell(50, 5, "- Prober: ", 0, 0, 'L')
        self.cell(50, 5, conditions["prober"], 0, 1, 'L')
        self.cell(50, 5, "- Wafermap file: ", 0, 0, 'L')
        self.cell(50, 5, conditions["wafermap_file"], 0, 1, 'L')
        self.cell(0, 5, "", 0, 1, 'L')
        self.cell(50, 5, "- Capacitance area: ", 0, 0, 'L')
        self.cell(50, 5, conditions["cap"] + " (" + conditions["area"] + ")", 0, 1, 'L')
        self.cell(50, 5, "- Temperature: ", 0, 0, 'L')
        self.cell(50, 5, str(conditions["temperature"]), 0, 1, 'L')
        self.cell(50, 5, "- Potential gate: ", 0, 0, 'L')
        self.cell(50, 5, conditions["gate_potential"], 0, 1, 'L')
        self.cell(50, 5, "- Permittivity: ", 0, 0, 'L')
        self.cell(50, 5, conditions["permittivity"], 0, 1, 'L')

    def insert_image(self, image_path, y):
        img = Image.open(image_path)
        width = img.width
        height = img.height
        factor = width / height
        width_norm = self.WIDTH / 1.4
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
        self.cell(0, 10, "- Diameter: " + str(info["diameter"]) + ". Thickness: " + str(info["thickness"]), 0, 1,
                  'L')
        y += 10
        self.cell(0, 10, "- Resistivity: " + str(info["resistivity"]), 0, 1, 'L')
        y += 10
        self.cell(0, 10, "- Mask: " + str(info["mask"]), 0, 1, 'L')
        y += 10
        # FIELD OXIDE INFORMATION
        self.cell(0, 10, "- Field oxide: " + str(info["field_oxide"]), 0, 1, 'L')
        y += 10
        field_oxide_wafers_list = [x.strip() for x in str(info["field_oxide_wafers"]).splitlines()]
        for field_oxide_wafers in field_oxide_wafers_list:
            self.cell(20, 5, field_oxide_wafers, 0, 1, 'L')
            y += 5
        if "field_oxide_image" in info and str(info["field_oxide_image"]) != "":
            images_field_oxide = str(info["field_oxide_image"]).split("|")
            for image_field_oxide in images_field_oxide:
                image_path = self.path_run + "/" + image_field_oxide
                y = self.insert_image(image_path, y)
        # RECOMBINATION TIME 1
        self.set_y(y)
        if "recombination_time" in info and str(info["recombination_time"]) != "":
            self.cell(0, 10, "- " + str(info["recombination_time"]), 0, 1, 'L')
            y += 10
            recombination_time_wafers_list = [x.strip() for x in str(info["recombination_time_wafers"]).splitlines()]
            for recombination_time_wafers in recombination_time_wafers_list:
                self.cell(20, 5, recombination_time_wafers, 0, 1, 'L')
                y += 5
        # OXIDE INFORMATION (TYPE: DRY, PECVD, NITRURE)
        if "oxide_test" in info and str(info["oxide_test"]) != "":
            # only DRY TYPE?
            self.cell(0, 10, "- " + str(info["oxide_type"]) + " oxide (test wafers): " + str(info["oxide_test"]), 0,
                      1, 'L')
            y += 10
            oxide_wafers_test_list = [x.strip() for x in str(info["oxide_wafers_test"]).splitlines()]
            for oxide_wafers_test in oxide_wafers_test_list:
                self.cell(20, 5, oxide_wafers_test, 0, 1, 'L')
                y += 5
            if "oxide_image_test" in info and str(info["oxide_image_test"]) != "":
                images_test_oxide = str(info["oxide_image_test"]).split("|")
                for image_test_oxide in images_test_oxide:
                    image_path = self.path_run + "/" + image_test_oxide
                    y = self.insert_image(image_path, y)
            self.set_y(y)
        self.cell(0, 10, "- " + str(info["oxide_type"]) + " oxide (process wafers): " + str(info["oxide_process"]),
                  0, 1, 'L')
        y += 10
        oxide_wafers_process_list = [x.strip() for x in str(info["oxide_wafers_process"]).splitlines()]
        for oxide_wafers_process in oxide_wafers_process_list:
            self.cell(20, 5, oxide_wafers_process, 0, 1, 'L')
            y += 5
        if "oxide_image_process" in info and str(info["oxide_image_process"]) != "":
            images_oxide_process = str(info["oxide_image_process"]).split("|")
            for image_oxide_process in images_oxide_process:
                image_path = self.path_run + "/" + image_oxide_process
                y = self.insert_image(image_path, y)
        self.set_y(y)
        if "gate_electrode" in info and str(info["gate_electrode"]) != "":
            self.cell(0, 10, "- Gate electrode: " + str(info["gate_electrode"]), 0, 1, 'L')
            y += 10
        if "back_metallization" in info and str(info["back_metallization"]) != "":
            self.cell(0, 10, "- Back side metallization: " + str(info["back_metallization"]), 0, 1, 'L')
            y += 10
        if "annealing" in info and str(info["annealing"]) != "":
            self.cell(0, 10, "- Annealing: ", 0, 1, 'L')
            y += 10
            self.print_multiple_lines(y, str(info["annealing"]), w=20, h=5, align='L')

        # RECOMBINATION TIME 2
        if "recombination_time" in info and str(info["recombination_time"]) != "":
            self.cell(0, 10, "- " + str(info["recombination_time"]), 0, 1, 'L')
            y += 10
            recombination_time2_wafers_list = [x.strip() for x in str(info["recombination_time2_wafers"]).splitlines()]
            for recombination_time2_wafers in recombination_time2_wafers_list:
                self.cell(20, 5, recombination_time2_wafers, 0, 1, 'L')
                y += 5
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
            remarkable_incidents_list = [x.strip() for x in str(info["remarkable_incidents"]).splitlines()]
            for remarkable_incidents in remarkable_incidents_list:
                # control length
                if len(remarkable_incidents) > 94:
                    remarkable_incidents_words = remarkable_incidents.split(" ")
                    remarkable_incidents_pharse = ""
                    for remarkable_incidents_word in remarkable_incidents_words:
                        if len(remarkable_incidents_pharse) + len(remarkable_incidents_word) > 94:
                            self.cell(20, 5, remarkable_incidents_pharse, 0, 1, 'L')
                            y += 5
                            remarkable_incidents_pharse = remarkable_incidents_word
                        else:
                            remarkable_incidents_pharse += " " + remarkable_incidents_word

                else:
                    # if remarkable_incidents=="": remarkable_incidents = " "
                    self.cell(20, 5, remarkable_incidents, 0, 1, 'L')
                    y += 5
            if "remarkable_incidents_photos" in info and str(info["remarkable_incidents_photos"]) != "":
                self.add_page()
                y = 20
                self.set_y(y)
                lista_remarkable_incidents_photos = info["remarkable_incidents_photos"].split("|")
                lista_photos = lista_remarkable_incidents_photos[0::2]
                lista_textos = lista_remarkable_incidents_photos[1::2]
                for i, photo in enumerate(lista_photos):
                    image_path = self.path_run + "/" + photo
                    y = self.insert_image(image_path, y)
                    self.set_y(y)
                    self.cell(self.WIDTH - 40, 10, lista_textos[i], 0, 1, 'C')
                    y += 20  # 10 text + 10 sep extra


    def print_multiple_lines(self, y, text, w=20, h=5, align='L'):
        x_list = [x.strip() for x in text.splitlines()]
        for x_elem in x_list:
            self.cell(w, h, x_elem, 0, 1, 'L')
            y += 5

    def print_report(self, wafer):
        # Generates the report
        plt.style.use('default')  # for prevent mpl uses inside Caracterizar
        # Print title (only first wafer), with page info + page conditions
        if self.page_no() == 0:
            self.add_page()
            self.page_header()
            if self.run in self.config_estepa_toml and "info" in self.config_estepa_toml[self.run]:
                info = self.config_estepa_toml[self.run]["info"]
                if "objective" in info and str(info["objective"] != ""):
                    self.add_page()
                    self.page_info()
            if self.run in self.config_estepa_toml and "conditions" in self.config_estepa_toml[self.run]:
                self.add_page()
                self.page_conditions()

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
        # print parameters
        wafer_path = self.path_run + "/" + wafer
        file_results = wafer_path + "/" + wafer + ".dat"
        result_file = ResultFile(file_results)
        parameters_file_list = list()
        
        if not result_file.error:
            parameters_file_list = result_file.params_list
            measurements = result_file.get_params(parameters_file_list)
            estadistica = dict()
            for parameter in parameters_file_list:
                if parameter not in self.parameter_list:
                    self.parameter_list.append(parameter)
                # check configuration toml
                # load with default system configuration estepa or toml (if exists)
                estepa_configuration = self.get_estepa_configuration_toml(wafer, parameter)
                data_list = measurements[parameter]["medida"]
                estadistica[parameter] = StatisticsEstepa(parameter, data_list, estepa_configuration)
                # Construct dataWafersParameters (without outliers)
                for value in estadistica[parameter].data_list:
                    self.dataWafersParameters_list.append([wafer, parameter, value])
                    QApplication.processEvents()
                y = y + 5
                self.set_y(y)
                self.set_font('Dejavu', 'B', 8)
                if not estadistica[parameter].error:
                    if parameter == "Na(cm¯³)" or parameter == "Nss(cm¯²)" or parameter == "Na(cm-3)" or parameter == "Nss(cm-2)":
                        # parameter = parameter.replace("-2", "¯²")
                        # parameter = parameter.replace("-3", "¯³")
                        mean = "{:e}".format(estadistica[parameter].mean)
                        stdev = "{:e}".format(estadistica[parameter].stdev)
                        median = "{:e}".format(estadistica[parameter].median)
                    else:
                        mean = "{:.3f}".format(estadistica[parameter].mean)
                        stdev = "{:.3f}".format(estadistica[parameter].stdev)
                        median = "{:.3f}".format(estadistica[parameter].median)
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
                    y = y + 5
                    self.text(20, y, parameter + " statistics error: " + estadistica[
                        parameter].error_message + "\nCheck estepa configuration file!")
        else:
            self.text(20, 35, "Error message wafer " + wafer + ": " + result_file.error_message)

        if self.options["plot"]:
            # get existing CV.png & CW.png in wafer folder
            units = dict()
            units["CV"] = {"START": "V", "STOP": "V", "STEP": "V", "FREQ": "kHz",
                           "OSC": "mV", "HYSTERESIS_TIME": "s", "WAIT_TIME": "s", "LIGHT_TIME": "s",
                           "TEMPERATURE": "ºC", "AREA": "um²"}
            units["CW"] = {"START": "kHz", "STOP": "kHz", "STEP": "kHz", "SPOT": "V", "OSC": "mV"}
            image_CV = wafer_path + "/" + self.options["plot_folder"] + "/CV_" + wafer + "_1_1.png"
            image_CW = wafer_path + "/" + self.options["plot_folder"] + "/CW_" + wafer + "_1_1.png"
            file_config_CV = wafer_path + "/CV.json"
            file_config_CW = wafer_path + "/CW.json"
            config_CV = dict()
            config_CW = dict()
            x = 20
            y = y + 10
            if os.path.exists(image_CV):
                self.image(image_CV, x, y, 90)
                # print table
                self.table_conditions("CV", wafer, y, units)
                y = y + 75

            if os.path.exists(image_CW):
                self.image(image_CW, x, y, 90)
                # print table
                self.table_conditions("CW", wafer, y, units)
        # print wafermap & histogram
        left = True

        for parameter in parameters_file_list:
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
            left = not left

    def print_mapa_wafer(self, mask="cnm004"):
        if mask == "cnm004":
            matrix_size = 45
            matrix = np.zeros((matrix_size, matrix_size), dtype=int)

            wafer_positions = ["0 0", "-3 0", "-6 0", "-9 0", "-12 0",
                               "-15 -4", "-12 -4", "-9 -4", "-6 -4", "-3 -4", "0 -4", "3 -4",
                               "6 -8", "3 -8", "0 -8", "-3 -8", "-6 -8", "-9 -8", "-12 -8", "-15 -8", "-18 -8",
                               "-18 -12", "-15 -12", "-12 -12", "-9 -12", "-6 -12", "-3 -12", "0 -12", "3 -12", "6 -12",
                               "9 -16", "6 -16", "3 -16", "0 -16", "-3 -16", "-6 -16", "-9 -16", "-12 -16", "-15 -16", "-18 -16", "-21 -16",
                               "-21 -20", "-18 -20", "-15 -20", "-12 -20", "-9 -20", "-6 -20", "-3 -20", "0 -20", "3 -20", "6 -20", "9 -20",
                               "9 -24", "6 -24", "3 -24", "0 -24", "-3 -24", "-6 -24", "-9 -24", "-12 -24", "-15 -24", "-18 -24", "-21 -24",
                               "-21 -28", "-18 -28", "-15 -28", "-12 -28", "-9 -28", "-6 -28", "-3 -28", "0 -28", "3 -28", "6 -28", "9 -28",
                               "6 -32", "3 -32", "0 -32", "-3 -32", "-6 -32", "-9 -32", "-12 -32", "-15 -32", "-18 -32",
                               "-18 -36", "-15 -36", "-12 -36", "-9 -36", "-6 -36", "-3 -36", "0 -36", "3 -36", "6 -36",
                               "3 -40", "0 -40", "-3 -40", "-6 -40", "-9 -40", "-12 -40", "-15 -40",
                               "-12 -44", "-9 -44", "-6 -44", "-3 -44", "0 -44"]
            x_real_position = 11
            y_real_position = 0
            wafer_coordinates = [(-int(y) + y_real_position, -int(x) + x_real_position) for x, y in
                                 [pos.split() for pos in wafer_positions]]

            for x in range(matrix_size):
                for y in range(matrix_size):
                    if (x, y) in wafer_coordinates:
                        matrix[x, y] = 2

            return matrix
        else:

            rows = 22
            cols = 15
            num_devices = 141
            # set blank values 141 devices
            zero_values = [
                [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11], [0, 12], [0, 13],
                [0, 14], \
                [1, 0], [1, 1], [1, 2], [1, 3], [1, 5], [1, 7], [1, 9], [1, 11], [1, 12], [1, 13], [1, 14], \
                [2, 0], [2, 1], [2, 2], [2, 3], [2, 5], [2, 7], [2, 9], [2, 11], [2, 12], [2, 13], [2, 14], \
                [3, 0], [3, 1], [3, 3], [3, 5], [3, 7], [3, 9], [3, 11], [3, 13], [3, 14], \
                [4, 0], [4, 1], [4, 3], [4, 5], [4, 7], [4, 9], [4, 11], [4, 13], [4, 14], \
                [5, 0], [5, 1], [5, 3], [5, 5], [5, 7], [5, 9], [5, 11], [5, 13], [5, 14], \
                [6, 0], [6, 1], [6, 3], [6, 5], [6, 7], [6, 9], [6, 11], [6, 13], [6, 14], \
                [7, 1], [7, 3], [7, 5], [7, 7], [7, 9], [7, 11], [7, 13], \
                [8, 1], [8, 3], [8, 5], [8, 7], [8, 9], [8, 11], [8, 13], \
                [9, 1], [9, 3], [9, 5], [9, 7], [9, 9], [9, 11], [9, 13], \
                [10, 1], [10, 3], [10, 5], [10, 7], [10, 9], [10, 11], [10, 13], \
                [11, 1], [11, 3], [11, 5], [11, 7], [11, 9], [11, 11], [11, 13], \
                [12, 0], [12, 1], [12, 3], [12, 5], [12, 7], [12, 9], [12, 11], [12, 13], [12, 14], \
                [13, 1], [13, 3], [13, 5], [13, 7], [13, 9], [13, 11], [13, 13], \
                [14, 1], [14, 3], [14, 5], [14, 7], [14, 9], [14, 11], [14, 13], \
                [15, 1], [15, 3], [15, 5], [15, 7], [15, 9], [15, 11], [15, 13], \
                [16, 1], [16, 3], [16, 5], [16, 7], [16, 9], [16, 11], [16, 13], \
                [17, 1], [17, 3], [17, 5], [17, 7], [17, 9], [17, 11], [17, 13], [17, 14],\
                [18, 0], [18, 1], [18, 3], [18, 5], [18, 7], [18, 9], [18, 11], [18, 13], [18, 14], \
                [19, 0], [19, 1], [19, 3], [19, 5], [19, 7], [19, 9], [19, 11], [19, 13], [19, 14], \
                [20, 0], [20, 1], [20, 3], [20, 5], [20, 7], [20, 9], [20, 11], [20, 13], [20, 14], \
                [21, 0], [21, 1], [21, 2], [21, 3], [21, 5], [21, 7], [21, 9], [21, 11], [21, 12], [21, 13], [21, 14] \
                ]

            np_array = np.ones((rows, cols), dtype=int)
            for zero in zero_values:
                np_array[zero[0], zero[1]] = 0

            # only 1 cases:
            # if num_devices == 141:
            np_array[np_array > 0] = 2

            return np_array

    def numpy_array_print_to_wafer(self, np_array, estadistica_param, left=True):
        rows_num, cols_num = np_array.shape
        # fit middle page, calc width cell (same height)
        width_cell = round((self.WIDTH / 2) / rows_num)
        height_cell = width_cell
        self.set_fill_color(34, 139, 34)  # verde bosque (#228b22)
        self.ln(5)
        counter = 1
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
                # print(f"Row {row}, column {column}")
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
                        name_sensor = "C" + str(counter).zfill(3)
                        # miramos valores para el sensor
                        # asignamos valores en np_array (1 = verde, 2= naranja, 3= naranja_rojo, 4 = rojo)
                        # color = self.color_sensor(df_row)
                        color = "verde"
                        valor_parametro = data_list_origen[num_device]
                        if valor_parametro not in data_list:
                            color = "outlier"
                        if valor_parametro == estadistica_param.ERROR_VALUE2:
                            color = "error"
                        if color == "verde":
                            # asignamos color verde flojo a ver oscuro según valor
                            j = 9
                            for i in range(9):  # de 0 a 8
                                if float(valor_parametro) <= float(paleta_valores[i]):
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
            fileplot_list = list()
            for parameter in self.parameter_list:
                parameter_data = list()
                for wafer in self.wafers:
                    fileplot = dir_comparative + parameter + ".png"
                    parameter_data.append(np.array(dataWafersParameters.loc[(dataWafersParameters["Wafer"] == wafer) & (
                                dataWafersParameters["Parameter"] == parameter), "Value"].astype("float")))
                fig = plt.figure(figsize=(10, 7))
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
                fig = None
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
