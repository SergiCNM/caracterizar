# EAD report Class
from fpdf import FPDF
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
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
import math

class EAD(FPDF):
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
        if self.error:
            self.widgets.txtResultReport.appendPlainText(f"Error creating report: {self.errorMessage}")
        self.config_toml = dict()
        self.get_toml()
        self.xips_number = 1452  # 4" 708, 6" 1452
        base_dejavu_path = 'C:\\WINDOWS\\Fonts\\'
        self.add_font('DejaVu', '', os.path.join(base_dejavu_path, 'DejaVuSerif.ttf'), uni=True)
        self.add_font('DejaVu', 'B', os.path.join(base_dejavu_path, 'DejaVuSerif-Bold.ttf'), uni=True)
        self.add_font('DejaVu', 'I', os.path.join(base_dejavu_path, 'DejaVuSerif-Italic.ttf'), uni=True)

    def header(self, title="EAD REPORT"):
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
        self.widgets.txtResultReport.setPlainText("")
        # remove comparative
        if "COMPARATIVE_FOLDER" in self.options:
            if os.path.exists(self.path_run + "/" + self.options["COMPARATIVE_FOLDER"]):
                shutil.rmtree(self.path_run + "/" + self.options["COMPARATIVE_FOLDER"])
        for directory in sorted(os.listdir(self.path_run)):
            if os.path.isdir(self.path_run + "/" + directory):
                self.wafers.append(directory)
        if len(self.wafers) > 0:
            for wafer in self.wafers:
                dir_wafer = self.path_run + "/" + wafer + "/"
                filename_results = [dir_wafer + wafer + "_forward.dat", dir_wafer + wafer + "_reverse.dat"]
                for filename_result in filename_results:
                    if not os.path.isfile(filename_result):
                        self.error = True
                        self.errorMessage = "Filename DAT for wafer " + wafer + " doesn't exists!"
                        break
                # creating dirs for wafer
                for option in self.options:
                    if "_FOLDER" in option:
                        if not os.path.exists(dir_wafer + self.options[option]):
                            os.mkdir(dir_wafer + self.options[option])
                # create plots
                if "PLOT" in self.options and self.options["PLOT"]:
                    path_plot_forward = dir_wafer + self.options["PLOT_FORWARD_FOLDER"] + "/"
                    path_plot_reverse = dir_wafer + self.options["PLOT_REVERSE_FOLDER"] + "/"
                    path_data_forward = dir_wafer + self.options["DATA_FORWARD_FOLDER"] + "/"
                    path_data_reverse = dir_wafer + self.options["DATA_REVERSE_FOLDER"] + "/"
                    # check plots forward
                    self.save_graphs(wafer, path_plot_forward, path_data_forward, type_graph="forward")
                    self.save_graphs(wafer, path_plot_reverse, path_data_reverse, type_graph="reverse")

        else:
            self.error = True
            self.errorMessage = "No wafers found in dir " + self.path_run

    def save_graphs(self, wafer, path_plot, path_data, type_graph):
        self.widgets.txtResultReport.appendPlainText(f"Saving graphs for wafer {wafer} {type_graph}")
        existsPlot = False
        if len(os.listdir(path_plot)) > 0:
            existsPlot = True
        if not existsPlot:
            # create plots
            counter = 0
            for filedata in sorted(os.listdir(path_data)):
                QApplication.processEvents()
                if os.path.isfile(path_data + filedata) and self.run in filedata:
                    # create plot in path_plot
                    # first column voltage, second capacitance, thrid conductance (CV_run-wafer_pos_module)
                    df = pd.read_csv(path_data + filedata, sep=',')
                    ax = plt.gca()
                    df.plot(kind='line', x=df.columns[0], y=df.columns[1], ax=ax, label="I-V",
                            color="blue", grid=True)
                    plt.title(f"{type_graph} I-V")
                    plt.xlabel("Voltage (V)")
                    plt.ylabel("Current (F)")
                    plt.subplots_adjust(bottom=0.15)

                    filePlot = path_plot + filedata.replace(".txt", ".png")
                    plt.savefig(filePlot, dpi=100)
                    plt.clf()
                    counter += 1

            self.widgets.txtResultReport.appendPlainText(
                f" - Created {str(counter)} graphs {type_graph} for wafer: {wafer}")

    def get_toml(self):
        path_config_file = self.path_run + "/" + self.run + ".toml"
        if os.path.exists(path_config_file):
            with open(path_config_file, mode="r", encoding='utf8') as fp:
                config = toml.load(fp)
                self.config_toml = config

    def page_header(self):
        QApplication.processEvents()
        title = self.config["reports"]["title"]
        if self.run in self.config_toml and "title" in self.config_toml[self.run]:
            title = self.config_toml[self.run]["title"]
        subtitle = self.config["reports"]["subtitle"]
        if self.run in self.config_toml and "subtitle" in self.config_toml[self.run]:
            subtitle = self.config_toml[self.run]["subtitle"]
        date = self.config["reports"]["date"]
        if self.run in self.config_toml and "date" in self.config_toml[self.run]:
            date = self.config_toml[self.run]["date"]
        author = self.config["reports"]["author"]
        if self.run in self.config_toml and "author" in self.config_toml[self.run]:
            author = self.config_toml[self.run]["author"]

        self.set_y(100)

        self.set_font('Dejavu', 'B', 24)
        self.cell(0, 10, title, 0, 1, 'C')
        self.set_font('Dejavu', 'B', 18)
        self.cell(0, 10, subtitle, 0, 1, 'C')
        self.set_y(250)

        if self.config["reports"]["date"] != "":
            self.set_font('Dejavu', 'B', 12)
            self.cell(150, 6, "Date: ", 0, 0, 'R');
            self.set_font('Dejavu', '', 10)
            self.cell(60, 6, date, 0, 1, 'L')
        if author != "":
            self.set_font('Dejavu', 'B', 12)
            self.cell(150, 6, "Author: ", 0, 0, 'R');
            self.set_font('Dejavu', '', 10)
            self.cell(60, 6, author, 0, 1, 'L')

    def page_conditions(self):
        QApplication.processEvents()
        conditions = self.config_toml[self.run]["conditions"]
        self.set_y(30)
        self.set_font('Dejavu', 'B', 11)
        self.cell(0, 10, "Measurement conditions:", 0, 1, 'L')
        self.set_font('Dejavu', '', 10)
        self.cell(50, 5, "- PC: ", 0, 0, 'L')
        self.cell(50, 5, conditions["pc"], 0, 1, 'L')
        self.cell(50, 5, "- Software: ", 0, 0, 'L')
        self.cell(50, 5, conditions["software"], 0, 1, 'L')
        self.cell(50, 5, "- Capacimeter: ", 0, 0, 'L')
        self.cell(50, 5, conditions["analyzer"], 0, 1, 'L')
        self.cell(50, 5, "- Prober: ", 0, 0, 'L')
        self.cell(50, 5, conditions["prober"], 0, 1, 'L')
        self.cell(50, 5, "- Wafermap file: ", 0, 0, 'L')
        self.cell(50, 5, conditions["wafermap_file"], 0, 1, 'L')
        self.cell(50, 5, "- Temperature: ", 0, 0, 'L')
        self.cell(50, 5, str(conditions["temperature"]), 0, 1, 'L')

    def insert_image(self, image_path, y):
        img = Image.open(image_path)
        width = img.width
        height = img.height
        factor = width / height
        width_norm = self.WIDTH / 1.15
        height_norm = width_norm / factor
        if y + height_norm > self.HEIGHT:
            self.add_page
            y = 30  # header page height
        self.image(image_path, 15, y, width_norm, height_norm)
        return y + int(height_norm)

    def print_report(self, wafer):
        # Generates the report
        plt.style.use('default')  # for prevent mpl uses inside Caracterizar
        # Print title (only first wafer), with page info + page conditions
        if self.page_no() == 0:
            self.add_page()
            self.page_header()
            if self.run in self.config_toml and "conditions" in self.config_toml[self.run]:
                self.add_page()
                self.page_conditions()
                # print table conditions
                units = dict()
                units["forward"] = {"START": "V", "STOP": "V", "STEP": "V", "COMPLIANCE": "A"}
                units["reverse"] = {"START": "V", "STOP": "V", "STEP": "V", "COMPLIANCE": "A"}
                y = 100
                self.table_conditions("forward", wafer, y, units)
                y = y + 30
                self.table_conditions("reverse", wafer, y, units)
                y = y + 30
        # print wafermap & histogram
        wafer_path = self.path_run + "/" + wafer

        # get data for reverse wafermap
        file_results = wafer_path + "/" + wafer + "_reverse.dat"
        result_file = ResultFile(file_results)
        statistics = dict()
        statistics["last_voltage"] = list()
        statistics["last_current"] = list()
        if not result_file.error:
            for die in result_file.dies:
                for module in result_file.modules:
                    voltage = result_file.data[die][module]['V(V)']
                    current = result_file.data[die][module]['I(A)']
                    last_voltage = 0
                    last_current = 0
                    if len(voltage) > 0:
                        last_voltage = voltage[-1]
                        last_current = current[-1]
                    statistics["last_voltage"].append(last_voltage)
                    statistics["last_current"].append(last_current)
        else:
            self.widgets.txtResultReport.appendPlainText(f"Error in result file: {result_file.error_message}")
        left = True

        wafermap_file = ""
        if "wafermap_file" in self.config_toml[self.run]["conditions"]:
            wafermap_file = self.config_toml[self.run]["conditions"]["wafermap_file"]
        if "wafermap_file" in self.config_toml[wafer]["conditions"]:
            wafermap_file = self.config_toml[wafer]["conditions"]["wafermap_file"]

        if "WAFERMAP" in self.options and self.options["WAFERMAP"]:
            # print reverse wafermap
            self.add_page()
            self.set_x(10)
            x_texto = 20
            self.set_y(30)
            self.set_font('Dejavu', 'B', 10)
            self.text(x_texto, 35, wafer)
            self.set_font('Dejavu', '', 9)
            self.text(x_texto, 40, "Reverse wafermap")
            # get np_array
            np_array,_ = self.print_mapa_wafer_6(wafermap_file)
            np_array_reverse = self.numpy_array_print_to_wafer_reverse(np_array, statistics, left)

        # self.print_wafermap_reverse_barriers(wafer_path, wafer, np_array)  # other method, doesn't works well



        # ahora quiero imprimir otro wafermap de forward en este caso usando los valores que obtengo de get_forward_errors
        if "WAFERMAP" in self.options and self.options["WAFERMAP"]:
            self.add_page()
            self.set_x(10)
            x_texto = 20
            self.set_y(30)
            self.set_font('Dejavu', 'B', 10)
            self.text(x_texto, 35, wafer)
            self.set_font('Dejavu', '', 9)
            self.text(x_texto, 40, "Forward wafermap")
            # get np_array
            np_array, lista_chips = self.print_mapa_wafer_6(wafermap_file)
            bad_list, alturas_barrera = self.get_forward_errors(wafer, lista_chips)
            np_array_forward = self.numpy_array_print_to_wafer_errors(np_array, bad_list, alturas_barrera, lista_chips, left)

        # ahora quiero imprimir otro wafermap con el combinado
        if "WAFERMAP" in self.options and self.options["WAFERMAP"]:
            self.add_page()
            self.set_x(10)
            x_texto = 20
            self.set_y(30)
            self.set_font('Dejavu', 'B', 10)
            self.text(x_texto, 35, wafer)
            self.set_font('Dejavu', '', 9)
            self.text(x_texto, 40, "Combined wafermap")
            self.numpy_array_print_to_wafer_combinado(np_array_reverse, statistics, np_array_forward, alturas_barrera, left)


    def print_wafermap_reverse_barriers(self, wafer_path, wafer, np_array):
        # get data for forward wafermap
        file_results = wafer_path + "/" + wafer + "_forward.dat"
        result_file = ResultFile(file_results)
        statistics = dict()
        statistics["num_barriers"] = list()
        umbral_picos = 5
        umbral_valles = 10
        if not result_file.error:
            for die in result_file.dies:
                for module in result_file.modules:
                    voltage = [float(valor) for valor in result_file.data[die][module]['V(V)']]
                    current = [float(valor) for valor in result_file.data[die][module]['I(A)']]
                    # calcular derivada
                    dI_dV = np.gradient(current, voltage)
                    # Encontrar la tasa de cambio promedio en la curva de single barrier
                    average_rate_of_change = np.mean(np.diff(current) / np.diff(voltage))
                    umbral_picos = average_rate_of_change * 0.1
                    umbral_picos = 0.1
                    # Identificar picos y valles en la derivada.
                    peaks, _ = find_peaks(dI_dV, height=umbral_picos)
                    # Determinar el número probable de barreras.
                    num_barriers = len(peaks)
                    statistics["num_barriers"].append(num_barriers)
        else:
            self.widgets.txtResultReport.appendPlainText(f"Error in result file: {result_file.error_message}")

        left = True
        if "WAFERMAP" in self.options and self.options["WAFERMAP"]:
            # print forward wafermap
            self.add_page()
            self.set_x(10)
            x_texto = 20
            self.set_y(30)
            self.set_font('Dejavu', 'B', 10)
            self.text(x_texto, 35, wafer)
            self.set_font('Dejavu', '', 9)
            self.numpy_array_print_to_wafer(np_array, statistics, left, wafermap_type="forward")
            # print forward wafermap

    @staticmethod
    def print_mapa_wafer():
        rows = 30
        cols = 30
        num_devices = 708
        # set blank values 708 devices
        zero_values = [
            [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 18], [0, 19], [0, 20], [0, 21], [0, 22], [0, 23], [0, 24], [0, 25], [0, 26], [0, 27], [0, 28], [0, 29], \
            [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [1, 7], [1, 18], [1, 19], [1, 20], [1, 21], [1, 22], [1, 23], [1, 24], [1, 25], [1, 26], [1, 27], [1, 28], [1, 29], \
            [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6], [2, 7], [2, 22], [2, 23], [2, 24], [2, 25], [2, 26], [2, 27], [2, 28], [2, 29], \
            [3, 0], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 22], [3, 23], [3, 24], [3, 25], [3, 26], [3, 27], [3, 28], [3, 29], \
            [4, 0], [4, 1], [4, 2], [4, 3], [4, 24], [4, 25], [4, 26], [4, 27], [4, 28], [4, 29], \
            [5, 0], [5, 1], [5, 2], [5, 3], [5, 24], [5, 25], [5, 26], [5, 27], [5, 28], [5, 29], \
            [6, 0], [6, 1], [6, 26], [6, 27], [6, 28], [6, 29], \
            [7, 0], [7, 1], [7, 26], [7, 27], [7, 28], [7, 29], \
            [8, 28], [8, 29], \
            [9, 28], [9, 29], \
            [10, 28], [10, 29], \
            [11, 28], [11, 29], \
            [18, 28], [18, 29], \
            [19, 28], [19, 29], \
            [20, 28], [20, 29], \
            [21, 28], [21, 29], \
            [22, 28], [22, 29], \
            [23, 28], [23, 29], \
            [24, 0], [24, 1], [24, 26], [24, 27], [24, 28], [24, 29], \
            [25, 0], [25, 1], [25, 26], [25, 27], [25, 28], [25, 29], \
            [26, 0], [26, 1], [26, 2], [26, 3], [26, 24], [26, 25], [26, 26], [26, 27], [26, 28], [26, 29], \
            [27, 0], [27, 1], [27, 2], [27, 3], [27, 24], [27, 25], [27, 26], [27, 27], [27, 28], [27, 29], \
            [28, 0], [28, 1], [28, 2], [28, 3], [28, 4], [28, 5], [28, 6], [28, 7], [28, 20], [28, 21], [28, 22], [28, 23], [28, 24], [28, 25], [28, 26], [28, 27], [28, 28], [28, 29], \
            [29, 0], [29, 1], [29, 2], [29, 3], [29, 4], [29, 5], [29, 6], [29, 7], [29, 20], [29, 21], [29, 22], [29, 23], [29, 24], [29, 25], [29, 26], [29, 27], [29, 28], [29, 29], \
            ]

        np_array = np.ones((rows, cols), dtype=int)
        for zero in zero_values:
            np_array[zero[0], zero[1]] = 0

        # only 1 cases:
        if num_devices == 708:
            np_array[np_array > 0] = 2

        return np_array


    def print_mapa_wafer_6(self, wafermap_file):
        global wafer_parameters
        matrix_size = 44
        matrix = np.zeros((matrix_size, matrix_size), dtype=int)
        # get wafer_positions, real_origin_chip = "-21 -4" from wafermap file
        runfile = os.path.join(os.getcwd(), "config", "default", "wafermaps", wafermap_file + "_wafermap.py")
        if os.path.exists(runfile):
            with open(runfile, "r") as rnf:
                try:
                    content = rnf.read()
                    exec(content)
                except Exception as ex:
                    print(str(ex))
        else:
            print(f"File {runfile} doesn't exists!")

        wafer_positions_all = ['0 0', '-1 0', '-2 0', '-3 0', '-4 0', '-5 0', '-6 0', '-7 0', '4 -1', '3 -1', '2 -1',
                           '1 -1', '0 -1', '-1 -1', '-2 -1', '-3 -1', '-4 -1', '-5 -1', '-6 -1', '-7 -1', '-8 -1',
                           '-9 -1', '-10 -1', '-11 -1', '6 -2', '5 -2', '4 -2', '3 -2', '2 -2', '1 -2', '0 -2', '-1 -2',
                           '-2 -2', '-3 -2', '-4 -2', '-5 -2', '-6 -2', '-7 -2', '-8 -2', '-9 -2', '-10 -2', '-11 -2',
                           '-12 -2', '-13 -2', '8 -3', '7 -3', '6 -3', '5 -3', '4 -3', '3 -3', '2 -3', '1 -3', '0 -3',
                           '-1 -3', '-2 -3', '-3 -3', '-4 -3', '-5 -3', '-6 -3', '-7 -3', '-8 -3', '-9 -3', '-10 -3',
                           '-11 -3', '-12 -3', '-13 -3', '-14 -3', '-15 -3', '9 -4', '8 -4', '7 -4', '6 -4', '5 -4',
                           '4 -4', '3 -4', '2 -4', '1 -4', '0 -4', '-1 -4', '-2 -4', '-3 -4', '-4 -4', '-5 -4', '-6 -4',
                           '-7 -4', '-8 -4', '-9 -4', '-10 -4', '-11 -4', '-12 -4', '-13 -4', '-14 -4', '-15 -4',
                           '-16 -4', '10 -5', '9 -5', '8 -5', '7 -5', '6 -5', '5 -5', '4 -5', '3 -5', '2 -5', '1 -5',
                           '0 -5', '-1 -5', '-2 -5', '-3 -5', '-4 -5', '-5 -5', '-6 -5', '-7 -5', '-8 -5', '-9 -5',
                           '-10 -5', '-11 -5', '-12 -5', '-13 -5', '-14 -5', '-15 -5', '-16 -5', '-17 -5', '11 -6',
                           '10 -6', '9 -6', '8 -6', '7 -6', '6 -6', '5 -6', '4 -6', '3 -6', '2 -6', '1 -6', '0 -6',
                           '-1 -6', '-2 -6', '-3 -6', '-4 -6', '-5 -6', '-6 -6', '-7 -6', '-8 -6', '-9 -6', '-10 -6',
                           '-11 -6', '-12 -6', '-13 -6', '-14 -6', '-15 -6', '-16 -6', '-17 -6', '-18 -6', '12 -7',
                           '11 -7', '10 -7', '9 -7', '8 -7', '7 -7', '6 -7', '5 -7', '4 -7', '3 -7', '2 -7', '1 -7',
                           '0 -7', '-1 -7', '-2 -7', '-3 -7', '-4 -7', '-5 -7', '-6 -7', '-7 -7', '-8 -7', '-9 -7',
                           '-10 -7', '-11 -7', '-12 -7', '-13 -7', '-14 -7', '-15 -7', '-16 -7', '-17 -7', '-18 -7',
                           '-19 -7', '13 -8', '12 -8', '11 -8', '10 -8', '9 -8', '8 -8', '7 -8', '6 -8', '5 -8', '4 -8',
                           '3 -8', '2 -8', '1 -8', '0 -8', '-1 -8', '-2 -8', '-3 -8', '-4 -8', '-5 -8', '-6 -8',
                           '-7 -8', '-8 -8', '-9 -8', '-10 -8', '-11 -8', '-12 -8', '-13 -8', '-14 -8', '-15 -8',
                           '-16 -8', '-17 -8', '-18 -8', '-19 -8', '-20 -8', '14 -9', '13 -9', '12 -9', '11 -9',
                           '10 -9', '9 -9', '8 -9', '7 -9', '2 -9', '1 -9', '0 -9', '-1 -9', '-2 -9', '-3 -9', '-4 -9',
                           '-5 -9', '-6 -9', '-7 -9', '-8 -9', '-9 -9', '-14 -9', '-15 -9', '-16 -9', '-17 -9',
                           '-18 -9', '-19 -9', '-20 -9', '-21 -9', '15 -10', '14 -10', '13 -10', '12 -10', '11 -10',
                           '10 -10', '9 -10', '8 -10', '7 -10', '2 -10', '1 -10', '0 -10', '-1 -10', '-2 -10', '-3 -10',
                           '-4 -10', '-5 -10', '-6 -10', '-7 -10', '-8 -10', '-9 -10', '-14 -10', '-15 -10', '-16 -10',
                           '-17 -10', '-18 -10', '-19 -10', '-20 -10', '-21 -10', '-22 -10', '15 -11', '14 -11',
                           '13 -11', '12 -11', '11 -11', '10 -11', '9 -11', '8 -11', '7 -11', '6 -11', '5 -11', '4 -11',
                           '3 -11', '2 -11', '1 -11', '0 -11', '-1 -11', '-2 -11', '-3 -11', '-4 -11', '-5 -11',
                           '-6 -11', '-7 -11', '-8 -11', '-9 -11', '-10 -11', '-11 -11', '-12 -11', '-13 -11',
                           '-14 -11', '-15 -11', '-16 -11', '-17 -11', '-18 -11', '-19 -11', '-20 -11', '-21 -11',
                           '-22 -11', '16 -12', '15 -12', '14 -12', '13 -12', '12 -12', '11 -12', '10 -12', '9 -12',
                           '8 -12', '7 -12', '6 -12', '5 -12', '4 -12', '3 -12', '2 -12', '1 -12', '0 -12', '-1 -12',
                           '-2 -12', '-3 -12', '-4 -12', '-5 -12', '-6 -12', '-7 -12', '-8 -12', '-9 -12', '-10 -12',
                           '-11 -12', '-12 -12', '-13 -12', '-14 -12', '-15 -12', '-16 -12', '-17 -12', '-18 -12',
                           '-19 -12', '-20 -12', '-21 -12', '-22 -12', '-23 -12', '16 -13', '15 -13', '14 -13',
                           '13 -13', '12 -13', '11 -13', '10 -13', '9 -13', '8 -13', '7 -13', '6 -13', '5 -13', '4 -13',
                           '3 -13', '2 -13', '1 -13', '0 -13', '-1 -13', '-2 -13', '-3 -13', '-4 -13', '-5 -13',
                           '-6 -13', '-7 -13', '-8 -13', '-9 -13', '-10 -13', '-11 -13', '-12 -13', '-13 -13',
                           '-14 -13', '-15 -13', '-16 -13', '-17 -13', '-18 -13', '-19 -13', '-20 -13', '-21 -13',
                           '-22 -13', '-23 -13', '17 -14', '16 -14', '15 -14', '14 -14', '13 -14', '12 -14', '11 -14',
                           '10 -14', '9 -14', '8 -14', '7 -14', '6 -14', '5 -14', '4 -14', '3 -14', '2 -14', '1 -14',
                           '0 -14', '-1 -14', '-2 -14', '-3 -14', '-4 -14', '-5 -14', '-6 -14', '-7 -14', '-8 -14',
                           '-9 -14', '-10 -14', '-11 -14', '-12 -14', '-13 -14', '-14 -14', '-15 -14', '-16 -14',
                           '-17 -14', '-18 -14', '-19 -14', '-20 -14', '-21 -14', '-22 -14', '-23 -14', '-24 -14',
                           '17 -15', '16 -15', '15 -15', '14 -15', '13 -15', '12 -15', '11 -15', '10 -15', '9 -15',
                           '8 -15', '7 -15', '6 -15', '5 -15', '4 -15', '3 -15', '2 -15', '1 -15', '0 -15', '-1 -15',
                           '-2 -15', '-3 -15', '-4 -15', '-5 -15', '-6 -15', '-7 -15', '-8 -15', '-9 -15', '-10 -15',
                           '-11 -15', '-12 -15', '-13 -15', '-14 -15', '-15 -15', '-16 -15', '-17 -15', '-18 -15',
                           '-19 -15', '-20 -15', '-21 -15', '-22 -15', '-23 -15', '-24 -15', '17 -16', '16 -16',
                           '15 -16', '14 -16', '13 -16', '12 -16', '11 -16', '10 -16', '9 -16', '8 -16', '7 -16',
                           '6 -16', '5 -16', '4 -16', '3 -16', '2 -16', '1 -16', '0 -16', '-1 -16', '-2 -16', '-3 -16',
                           '-4 -16', '-5 -16', '-6 -16', '-7 -16', '-8 -16', '-9 -16', '-10 -16', '-11 -16', '-12 -16',
                           '-13 -16', '-14 -16', '-15 -16', '-16 -16', '-17 -16', '-18 -16', '-19 -16', '-20 -16',
                           '-21 -16', '-22 -16', '-23 -16', '-24 -16', '17 -17', '16 -17', '15 -17', '14 -17', '13 -17',
                           '12 -17', '11 -17', '10 -17', '9 -17', '8 -17', '7 -17', '6 -17', '5 -17', '4 -17', '3 -17',
                           '2 -17', '1 -17', '0 -17', '-1 -17', '-2 -17', '-3 -17', '-4 -17', '-5 -17', '-6 -17',
                           '-7 -17', '-8 -17', '-9 -17', '-10 -17', '-11 -17', '-12 -17', '-13 -17', '-14 -17',
                           '-15 -17', '-16 -17', '-17 -17', '-18 -17', '-19 -17', '-20 -17', '-21 -17', '-22 -17',
                           '-23 -17', '-24 -17', '18 -18', '17 -18', '16 -18', '15 -18', '14 -18', '13 -18', '12 -18',
                           '11 -18', '10 -18', '9 -18', '8 -18', '7 -18', '6 -18', '5 -18', '4 -18', '3 -18', '2 -18',
                           '1 -18', '0 -18', '-1 -18', '-2 -18', '-3 -18', '-4 -18', '-5 -18', '-6 -18', '-7 -18',
                           '-8 -18', '-9 -18', '-10 -18', '-11 -18', '-12 -18', '-13 -18', '-14 -18', '-15 -18',
                           '-16 -18', '-17 -18', '-18 -18', '-19 -18', '-20 -18', '-21 -18', '-22 -18', '-23 -18',
                           '-24 -18', '-25 -18', '18 -19', '17 -19', '16 -19', '15 -19', '14 -19', '13 -19', '12 -19',
                           '11 -19', '10 -19', '9 -19', '8 -19', '7 -19', '6 -19', '5 -19', '4 -19', '3 -19', '2 -19',
                           '1 -19', '0 -19', '-1 -19', '-2 -19', '-3 -19', '-4 -19', '-5 -19', '-6 -19', '-7 -19',
                           '-8 -19', '-9 -19', '-10 -19', '-11 -19', '-12 -19', '-13 -19', '-14 -19', '-15 -19',
                           '-16 -19', '-17 -19', '-18 -19', '-19 -19', '-20 -19', '-21 -19', '-22 -19', '-23 -19',
                           '-24 -19', '-25 -19', '18 -20', '17 -20', '16 -20', '15 -20', '14 -20', '13 -20', '12 -20',
                           '11 -20', '10 -20', '9 -20', '8 -20', '7 -20', '6 -20', '5 -20', '4 -20', '3 -20', '2 -20',
                           '1 -20', '0 -20', '-1 -20', '-2 -20', '-3 -20', '-4 -20', '-5 -20', '-6 -20', '-7 -20',
                           '-8 -20', '-9 -20', '-10 -20', '-11 -20', '-12 -20', '-13 -20', '-14 -20', '-15 -20',
                           '-16 -20', '-17 -20', '-18 -20', '-19 -20', '-20 -20', '-21 -20', '-22 -20', '-23 -20',
                           '-24 -20', '-25 -20', '18 -21', '17 -21', '16 -21', '15 -21', '8 -21', '7 -21', '6 -21',
                           '5 -21', '4 -21', '3 -21', '2 -21', '1 -21', '0 -21', '-1 -21', '-2 -21', '-3 -21', '-4 -21',
                           '-5 -21', '-6 -21', '-7 -21', '-8 -21', '-9 -21', '-10 -21', '-11 -21', '-12 -21', '-13 -21',
                           '-14 -21', '-15 -21', '-22 -21', '-23 -21', '-24 -21', '-25 -21', '18 -22', '17 -22',
                           '16 -22', '15 -22', '8 -22', '7 -22', '6 -22', '5 -22', '4 -22', '3 -22', '2 -22', '1 -22',
                           '0 -22', '-1 -22', '-2 -22', '-3 -22', '-4 -22', '-5 -22', '-6 -22', '-7 -22', '-8 -22',
                           '-9 -22', '-10 -22', '-11 -22', '-12 -22', '-13 -22', '-14 -22', '-15 -22', '-22 -22',
                           '-23 -22', '-24 -22', '-25 -22', '18 -23', '17 -23', '16 -23', '15 -23', '14 -23', '13 -23',
                           '12 -23', '11 -23', '10 -23', '9 -23', '8 -23', '7 -23', '6 -23', '5 -23', '4 -23', '3 -23',
                           '2 -23', '1 -23', '0 -23', '-1 -23', '-2 -23', '-3 -23', '-4 -23', '-5 -23', '-6 -23',
                           '-7 -23', '-8 -23', '-9 -23', '-10 -23', '-11 -23', '-12 -23', '-13 -23', '-14 -23',
                           '-15 -23', '-16 -23', '-17 -23', '-18 -23', '-19 -23', '-20 -23', '-21 -23', '-22 -23',
                           '-23 -23', '-24 -23', '-25 -23', '18 -24', '17 -24', '16 -24', '15 -24', '14 -24', '13 -24',
                           '12 -24', '11 -24', '10 -24', '9 -24', '8 -24', '7 -24', '6 -24', '5 -24', '4 -24', '3 -24',
                           '2 -24', '1 -24', '0 -24', '-1 -24', '-2 -24', '-3 -24', '-4 -24', '-5 -24', '-6 -24',
                           '-7 -24', '-8 -24', '-9 -24', '-10 -24', '-11 -24', '-12 -24', '-13 -24', '-14 -24',
                           '-15 -24', '-16 -24', '-17 -24', '-18 -24', '-19 -24', '-20 -24', '-21 -24', '-22 -24',
                           '-23 -24', '-24 -24', '-25 -24', '18 -25', '17 -25', '16 -25', '15 -25', '14 -25', '13 -25',
                           '12 -25', '11 -25', '10 -25', '9 -25', '8 -25', '7 -25', '6 -25', '5 -25', '4 -25', '3 -25',
                           '2 -25', '1 -25', '0 -25', '-1 -25', '-2 -25', '-3 -25', '-4 -25', '-5 -25', '-6 -25',
                           '-7 -25', '-8 -25', '-9 -25', '-10 -25', '-11 -25', '-12 -25', '-13 -25', '-14 -25',
                           '-15 -25', '-16 -25', '-17 -25', '-18 -25', '-19 -25', '-20 -25', '-21 -25', '-22 -25',
                           '-23 -25', '-24 -25', '-25 -25', '17 -26', '16 -26', '15 -26', '14 -26', '13 -26', '12 -26',
                           '11 -26', '10 -26', '9 -26', '8 -26', '7 -26', '6 -26', '5 -26', '4 -26', '3 -26', '2 -26',
                           '1 -26', '0 -26', '-1 -26', '-2 -26', '-3 -26', '-4 -26', '-5 -26', '-6 -26', '-7 -26',
                           '-8 -26', '-9 -26', '-10 -26', '-11 -26', '-12 -26', '-13 -26', '-14 -26', '-15 -26',
                           '-16 -26', '-17 -26', '-18 -26', '-19 -26', '-20 -26', '-21 -26', '-22 -26', '-23 -26',
                           '-24 -26', '17 -27', '16 -27', '15 -27', '14 -27', '13 -27', '12 -27', '11 -27', '10 -27',
                           '9 -27', '8 -27', '7 -27', '6 -27', '5 -27', '4 -27', '3 -27', '2 -27', '1 -27', '0 -27',
                           '-1 -27', '-2 -27', '-3 -27', '-4 -27', '-5 -27', '-6 -27', '-7 -27', '-8 -27', '-9 -27',
                           '-10 -27', '-11 -27', '-12 -27', '-13 -27', '-14 -27', '-15 -27', '-16 -27', '-17 -27',
                           '-18 -27', '-19 -27', '-20 -27', '-21 -27', '-22 -27', '-23 -27', '-24 -27', '17 -28',
                           '16 -28', '15 -28', '14 -28', '13 -28', '12 -28', '11 -28', '10 -28', '9 -28', '8 -28',
                           '7 -28', '6 -28', '5 -28', '4 -28', '3 -28', '2 -28', '1 -28', '0 -28', '-1 -28', '-2 -28',
                           '-3 -28', '-4 -28', '-5 -28', '-6 -28', '-7 -28', '-8 -28', '-9 -28', '-10 -28', '-11 -28',
                           '-12 -28', '-13 -28', '-14 -28', '-15 -28', '-16 -28', '-17 -28', '-18 -28', '-19 -28',
                           '-20 -28', '-21 -28', '-22 -28', '-23 -28', '-24 -28', '17 -29', '16 -29', '15 -29',
                           '14 -29', '13 -29', '12 -29', '11 -29', '10 -29', '9 -29', '8 -29', '7 -29', '6 -29',
                           '5 -29', '4 -29', '3 -29', '2 -29', '1 -29', '0 -29', '-1 -29', '-2 -29', '-3 -29', '-4 -29',
                           '-5 -29', '-6 -29', '-7 -29', '-8 -29', '-9 -29', '-10 -29', '-11 -29', '-12 -29', '-13 -29',
                           '-14 -29', '-15 -29', '-16 -29', '-17 -29', '-18 -29', '-19 -29', '-20 -29', '-21 -29',
                           '-22 -29', '-23 -29', '-24 -29', '16 -30', '15 -30', '14 -30', '13 -30', '12 -30', '11 -30',
                           '10 -30', '9 -30', '8 -30', '7 -30', '6 -30', '5 -30', '4 -30', '3 -30', '2 -30', '1 -30',
                           '0 -30', '-1 -30', '-2 -30', '-3 -30', '-4 -30', '-5 -30', '-6 -30', '-7 -30', '-8 -30',
                           '-9 -30', '-10 -30', '-11 -30', '-12 -30', '-13 -30', '-14 -30', '-15 -30', '-16 -30',
                           '-17 -30', '-18 -30', '-19 -30', '-20 -30', '-21 -30', '-22 -30', '-23 -30', '16 -31',
                           '15 -31', '14 -31', '13 -31', '12 -31', '11 -31', '10 -31', '9 -31', '8 -31', '7 -31',
                           '6 -31', '5 -31', '4 -31', '3 -31', '2 -31', '1 -31', '0 -31', '-1 -31', '-2 -31', '-3 -31',
                           '-4 -31', '-5 -31', '-6 -31', '-7 -31', '-8 -31', '-9 -31', '-10 -31', '-11 -31', '-12 -31',
                           '-13 -31', '-14 -31', '-15 -31', '-16 -31', '-17 -31', '-18 -31', '-19 -31', '-20 -31',
                           '-21 -31', '-22 -31', '-23 -31', '15 -32', '14 -32', '13 -32', '12 -32', '11 -32', '10 -32',
                           '9 -32', '8 -32', '7 -32', '6 -32', '5 -32', '4 -32', '3 -32', '2 -32', '1 -32', '0 -32',
                           '-1 -32', '-2 -32', '-3 -32', '-4 -32', '-5 -32', '-6 -32', '-7 -32', '-8 -32', '-9 -32',
                           '-10 -32', '-11 -32', '-12 -32', '-13 -32', '-14 -32', '-15 -32', '-16 -32', '-17 -32',
                           '-18 -32', '-19 -32', '-20 -32', '-21 -32', '-22 -32', '15 -33', '14 -33', '13 -33',
                           '12 -33', '11 -33', '10 -33', '9 -33', '8 -33', '7 -33', '2 -33', '1 -33', '0 -33', '-1 -33',
                           '-2 -33', '-3 -33', '-4 -33', '-5 -33', '-6 -33', '-7 -33', '-8 -33', '-9 -33', '-14 -33',
                           '-15 -33', '-16 -33', '-17 -33', '-18 -33', '-19 -33', '-20 -33', '-21 -33', '-22 -33',
                           '14 -34', '13 -34', '12 -34', '11 -34', '10 -34', '9 -34', '8 -34', '7 -34', '2 -34',
                           '1 -34', '0 -34', '-1 -34', '-2 -34', '-3 -34', '-4 -34', '-5 -34', '-6 -34', '-7 -34',
                           '-8 -34', '-9 -34', '-14 -34', '-15 -34', '-16 -34', '-17 -34', '-18 -34', '-19 -34',
                           '-20 -34', '-21 -34', '13 -35', '12 -35', '11 -35', '10 -35', '9 -35', '8 -35', '7 -35',
                           '6 -35', '5 -35', '4 -35', '3 -35', '2 -35', '1 -35', '0 -35', '-1 -35', '-2 -35', '-3 -35',
                           '-4 -35', '-5 -35', '-6 -35', '-7 -35', '-8 -35', '-9 -35', '-10 -35', '-11 -35', '-12 -35',
                           '-13 -35', '-14 -35', '-15 -35', '-16 -35', '-17 -35', '-18 -35', '-19 -35', '-20 -35',
                           '12 -36', '11 -36', '10 -36', '9 -36', '8 -36', '7 -36', '6 -36', '5 -36', '4 -36', '3 -36',
                           '2 -36', '1 -36', '0 -36', '-1 -36', '-2 -36', '-3 -36', '-4 -36', '-5 -36', '-6 -36',
                           '-7 -36', '-8 -36', '-9 -36', '-10 -36', '-11 -36', '-12 -36', '-13 -36', '-14 -36',
                           '-15 -36', '-16 -36', '-17 -36', '-18 -36', '-19 -36', '11 -37', '10 -37', '9 -37', '8 -37',
                           '7 -37', '6 -37', '5 -37', '4 -37', '3 -37', '2 -37', '1 -37', '0 -37', '-1 -37', '-2 -37',
                           '-3 -37', '-4 -37', '-5 -37', '-6 -37', '-7 -37', '-8 -37', '-9 -37', '-10 -37', '-11 -37',
                           '-12 -37', '-13 -37', '-14 -37', '-15 -37', '-16 -37', '-17 -37', '-18 -37', '10 -38',
                           '9 -38', '8 -38', '7 -38', '6 -38', '5 -38', '4 -38', '3 -38', '2 -38', '1 -38', '0 -38',
                           '-1 -38', '-2 -38', '-3 -38', '-4 -38', '-5 -38', '-6 -38', '-7 -38', '-8 -38', '-9 -38',
                           '-10 -38', '-11 -38', '-12 -38', '-13 -38', '-14 -38', '-15 -38', '-16 -38', '-17 -38',
                           '9 -39', '8 -39', '7 -39', '6 -39', '5 -39', '4 -39', '3 -39', '2 -39', '1 -39', '0 -39',
                           '-1 -39', '-2 -39', '-3 -39', '-4 -39', '-5 -39', '-6 -39', '-7 -39', '-8 -39', '-9 -39',
                           '-10 -39', '-11 -39', '-12 -39', '-13 -39', '-14 -39', '-15 -39', '-16 -39', '8 -40',
                           '7 -40', '6 -40', '5 -40', '4 -40', '3 -40', '2 -40', '1 -40', '0 -40', '-1 -40', '-2 -40',
                           '-3 -40', '-4 -40', '-5 -40', '-6 -40', '-7 -40', '-8 -40', '-9 -40', '-10 -40', '-11 -40',
                           '-12 -40', '-13 -40', '-14 -40', '-15 -40', '6 -41', '5 -41', '4 -41', '3 -41', '2 -41',
                           '1 -41', '0 -41', '-1 -41', '-2 -41', '-3 -41', '-4 -41', '-5 -41', '-6 -41', '-7 -41',
                           '-8 -41', '-9 -41', '-10 -41', '-11 -41', '-12 -41', '-13 -41', '4 -42', '3 -42', '2 -42',
                           '1 -42', '0 -42', '-1 -42', '-2 -42', '-3 -42', '-4 -42', '-5 -42', '-6 -42', '-7 -42',
                           '-8 -42', '-9 -42', '-10 -42', '-11 -42', '0 -43', '-1 -43', '-2 -43', '-3 -43', '-4 -43',
                           '-5 -43', '-6 -43', '-7 -43']

        real_origin_chip_all = "-21 -4"
        real_origin_chip = "-21 -4"
        wafer_positions = wafer_positions_all
        if "real_origin_chip" in wafer_parameters:
            real_origin_chip = wafer_parameters["real_origin_chip"]
        if "wafer_positions" in wafer_parameters:
            wafer_positions = wafer_parameters["wafer_positions"]
        if "nchips" in wafer_parameters:
            self.xips_number = int(wafer_parameters["nchips"])

        x_real_position = 18
        y_real_position = 0

        difx = int(real_origin_chip_all.split()[0]) - int(real_origin_chip.split()[0])
        dify = int(real_origin_chip_all.split()[1]) - int(real_origin_chip.split()[1])

        wafer_coordinates = [(-int(y) + y_real_position , -int(x) + x_real_position)
                             for x, y in [pos.split() for pos in wafer_positions_all]]

        wafer_coordinates_dif = [(-int(y) + y_real_position + dify, -int(x) + x_real_position + difx)
                             for x, y in [pos.split() for pos in wafer_positions]]

        xips_position = []
        xip_position = 0
        for x in range(matrix_size):
            for y in range(matrix_size):
                if (x, y) in wafer_coordinates:
                    xip_position += 1
                    matrix[x, y] = 3 # por si esta rota, lo pondremos en gris
                    if (x, y) in wafer_coordinates_dif:
                        # indicamos qué chips estan dentro
                        # podemos verificar en función wafer_positions enviados y real_origin_chip
                        matrix[x, y] = 2
                        xips_position.append(xip_position)


        return [matrix, xips_position]

    def get_forward_errors(self, wafer, lista_chips):
        wafer_path = self.path_run + "/" + wafer
        directorio = wafer_path + "/forward"

        # Tensiones específicas
        tensiones_objetivo = [0.2, 0.3, 0.4, 0.5]

        # Diccionario para almacenar los valores de corriente para cada tensión
        resultados = {tension: [] for tension in tensiones_objetivo}

        # Iterar sobre los archivos en el directorio
        for archivo_nombre in os.listdir(directorio):
            if archivo_nombre.endswith(".txt"):
                ruta_archivo = os.path.join(directorio, archivo_nombre)

                # Leer el archivo y extraer los valores de corriente para las tensiones específicas
                with open(ruta_archivo, "r") as archivo:
                    for linea in archivo:
                        if not linea.startswith("V,I"):
                            valores = [float(valor) for valor in linea.strip().split(",")]
                            tension, corriente = valores
                            if tension in tensiones_objetivo:
                                resultados[tension].append(np.log(corriente))

        # Calcular la media y la desviación estándar para cada tensión
        estadisticas = {}
        for tension, valores in resultados.items():
            media = np.mean(valores)
            desviacion_std = np.std(valores)
            estadisticas[tension] = {"media": media, "desviacion_std": desviacion_std}

        # Identificar los archivos que están fuera del promedio más un sigma
        archivos_fuera_de_rango = []
        chip_fuera_de_rango = []
        alturas_barrera = []
        if "temperature" in self.config_toml[self.run]["conditions"]:
            T = self.config_toml[self.run]["conditions"]["temperature"]
        else:
            T = 25  # 25 grados, habría que pasar de temperature conditions del toml
        T_abs = T + 273.15
        k = 1.380649E-23
        q = 1.602176634E-19
        V_T = k * T_abs / q
        Area = 3.92 # mm2
        # create file csv to save data (altura_barrera) for all chips. Name file with wafer name. Save in root path
        with open(self.path_run + "/altura_barrera_" + wafer + ".csv", "w+") as archivo_resumen:
            archivo_resumen.write("fichero,chip,altura_barrera\n")
            # sort files in directory for name. Ex: 16894_W03_1_1.txt, 16894_W03_2_1.txt, 16894_W03_3_1.txt,...16894_W03_100_1.txt,
            name_files = sorted(os.listdir(directorio), key=lambda x: int(x.split("_")[-2]))
            j = 0
            for archivo_nombre in name_files:
                if archivo_nombre.endswith(".txt"):
                    ruta_archivo = os.path.join(directorio, archivo_nombre)

                    with open(ruta_archivo, "r") as archivo:
                        valores_fuera_de_rango = 0
                        corrientes_objetivo = []
                        for linea in archivo:
                            if not linea.startswith("V,I"):
                                valores = [float(valor) for valor in linea.strip().split(",")]
                                tension, corriente = valores
                                if tension in tensiones_objetivo:
                                    log_corriente = np.log(corriente)
                                    corrientes_objetivo.append(log_corriente)
                                    # log_corriente = corriente
                                    media = estadisticas[tension]["media"]
                                    desviacion_std = estadisticas[tension]["desviacion_std"]
                                    if not (media - desviacion_std <= log_corriente <= media + desviacion_std):
                                        valores_fuera_de_rango += 1
                        # get m, b x=tensiones_objetivo, y=corrientes_objetivo
                        m, b = np.polyfit(tensiones_objetivo, corrientes_objetivo, 1)
                        n = m * V_T
                        ls = np.exp(b)
                        Js = ls / Area
                        # 0.02535 es V_T = KT/q a 21ºC
                        # 14600 es la constante de Richarson para la unión W con 4H-SiC, que vale 146 A/cm2K2 = 14600 A/mm2K2
                        altura_barrera = -0.02535*math.log(Js/(14600*T_abs*T_abs))
                        # save data in csv file
                        archivo_resumen.write(f"{archivo_nombre},{lista_chips[j]},{altura_barrera}\n")
                        j += 1
                        alturas_barrera.append(altura_barrera)

                        # if valores_fuera_de_rango == len(tensiones_objetivo):
                        if valores_fuera_de_rango > 0:
                            archivos_fuera_de_rango.append(archivo_nombre)
                            partes = archivo_nombre.split("_")
                            if len(partes) >= 2:
                                identificador = partes[-2]
                                chip_fuera_de_rango.append(int(identificador))


        return sorted(chip_fuera_de_rango), alturas_barrera

    def numpy_array_print_to_wafer_reverse(self, np_array, statistics, left=True):
        np_array_reverse = np_array.copy()
        rows_num, cols_num = np_array.shape
        # fit middle page, calc width cell (same height), put value to make margin
        margin = 50
        width_cell = round((self.WIDTH-margin) / rows_num)
        height_cell = width_cell
        self.set_fill_color(255, 255, 255) # blanco por defecto
        self.ln(5)
        counter = 1
        counters = dict()

        counters["verde"] = 0
        counters["azul"] = 0
        counters["naranja"] = 0
        counters["blanco"] = 0
        counters["rojo"] = 0
        num_device = 0
        self.set_font('Dejavu', '', 3)
        for row in range(0, rows_num):
            extra_cell = False  # control extra cell at start (if right)
            for column in range(0, cols_num):
                ln = 0
                if not left and not extra_cell:
                    self.cell(int(self.WIDTH))
                    extra_cell = True
                if column == cols_num - 1:
                    ln = 1
                if np_array[row][column] == 0: # Celda en blanco
                    name_sensor = ""
                    fill = False
                    border = 0
                    self.cell(w=width_cell, h=height_cell, txt=name_sensor, ln=ln, border=border, fill=fill)
                else:
                    if np_array[row][column] == 3: # celda en gris, oblea rota
                        fill = True
                        border = 1
                        name_sensor = "C" + str(counter).zfill(3)
                        counter += 1
                        color = "gris"
                        self.set_fill_color(207, 207, 207)
                        np_array_reverse[row][column] = 3
                    if np_array[row][column] == 2:  # celda con algo
                        fill = True
                        border = 1
                        name_sensor = "C" + str(counter).zfill(3)
                        # miramos valores para el sensor
                        # asignamos valores en np_array
                        voltage_value= float(statistics["last_voltage"][num_device])
                        current_value = abs(float(statistics["last_current"][num_device]))
                        if int(voltage_value) != -250:
                            color = "blanco"
                            self.set_fill_color(255, 255, 255)
                            np_array_reverse[row][column] = 1
                        else:
                            if current_value < 1E-6:
                                color = "verde"
                                self.set_fill_color(34, 139, 34)  # verde bosque (#228b22)
                            elif 1E-6 <= current_value < 10E-6:
                                color = "azul"
                                self.set_fill_color(0, 150, 255)
                            elif 10E-6 <= current_value < 100E-6:
                                color = "naranja"
                                self.set_fill_color(255, 165, 0)
                            else:
                                color = "rojo" # not possible, compliance 100uA
                                self.set_fill_color(255, 0, 0)

                        counters[color] += 1
                        # self.page_link[name_sensor] = self.add_link()
                        counter += 1
                        num_device += 1

                    # if np_array[row][column] == 1:
                    #     name_sensor = "C" + str(counter).zfill(3)
                    #     print(name_sensor)
                    #     fill = False
                    #     border = 1
                    #     counters["blanco"] += 1
                    #     counter += 1
                    self.cell(w=width_cell, h=height_cell, txt=name_sensor, ln=ln, border=border, fill=fill, align='C')

        # Print counters
        self.ln(10)
        self.set_font('Dejavu', 'B', 10)
        wh = 8
        self.set_fill_color(255, 255, 255)
        if not left: self.cell(int(self.WIDTH))
        percentage = "{:.2%}".format(float((counters["blanco"] / self.xips_number)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=40, h=wh, txt="Vbr < 250V : ", ln=0, fill=False)
        self.cell(w=40, h=wh, txt=str(counters["blanco"]) + f" devices ({percentage})", ln=1, fill=False)
        self.ln(2)
        self.set_fill_color(34, 139, 34)
        if not left: self.cell(int(self.WIDTH))
        percentage = "{:.2%}".format(float((counters["verde"] / self.xips_number)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=40, h=wh, txt="I < 1uA : ", ln=0, fill=False)
        self.cell(w=40, h=wh, txt=str(counters["verde"]) + f" devices ({percentage})", ln=1, fill=False)
        self.ln(2)
        self.set_fill_color(0, 150, 255)
        if not left: self.cell(int(self.WIDTH))
        percentage = "{:.2%}".format(float((counters["azul"] / self.xips_number)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=40, h=wh, txt="I 1uA-10uA : ", ln=0, fill=False)
        self.cell(w=40, h=wh, txt=str(counters["azul"]) + f" devices ({percentage})", ln=1, fill=False)
        self.ln(2)
        self.set_fill_color(255, 165, 0)
        if not left: self.cell(int(self.WIDTH))
        percentage = "{:.2%}".format(float((counters["naranja"] / self.xips_number)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=40, h=wh, txt="I 10uA-100uA : ", ln=0, fill=False)
        self.cell(w=40, h=wh, txt=str(counters["naranja"]) + f" devices ({percentage})", ln=1, fill=False)
        self.ln(2)


        return np_array_reverse

    def assign_color(self, valor, min_val, max_val):
        # Degradado de colores
        gradient = [
            (189, 255, 189),
            (169, 236, 170),
            (149, 217, 152),
            (129, 197, 133),
            (109, 178, 114),
            (90, 159, 96),
            (70, 140, 77),
            (50, 120, 58),
            (30, 101, 40),
            (10, 82, 21)
        ]

        # # Normalizar el valor en función del rango (0-1)
        # normalized_value = (float(valor) - min_val) / (max_val - min_val)
        #
        # # Encontrar el índice del color en el degradado
        # index = int(normalized_value * (len(gradient) - 1))
        #
        # # Devolver el color correspondiente
        # return gradient[index]
        # Calcular los cuartiles del rango de valores
        quartiles = [min_val] + [min_val + (max_val - min_val) * (i / 10) for i in range(1, 10)] + [max_val]

        # Determinar en qué cuartil se encuentra el valor
        for i in range(len(quartiles) - 1):
            if quartiles[i] <= valor <= quartiles[i + 1]:
                index = i
                break

        # Devolver el color correspondiente al cuartil
        return gradient[index]
    def numpy_array_print_to_wafer_errors(self, np_array, bad_list, alturas_barrera, lista_chips, left=True):
        # get median of alturas_barrera (without bad_list)
        alturas_barrera_good = [alturas_barrera[i] for i in range(len(alturas_barrera)) if i not in bad_list]
        median_alturas_barrera = np.median(alturas_barrera_good)
        # get max value of alturas_barrera (without bad_list)
        max_alturas_barrera = max(alturas_barrera_good)
        # get min value of alturas_barrera (without bad_list)
        min_alturas_barrera = min(alturas_barrera_good)
        np_array_final = np_array.copy()
        rows_num, cols_num = np_array.shape
        # fit middle page, calc width cell (same height), put value to make margin
        margin = 50
        width_cell = round((self.WIDTH-margin) / rows_num)
        height_cell = width_cell
        self.set_fill_color(255, 255, 255) # blanco por defecto
        self.ln(5)
        counter = 1
        counters = dict()
        counters["blanco"] = 0
        counters["verde"] = 0
        num_device = 1
        num_device_good = 0
        self.set_font('Dejavu', '', 3)
        for row in range(0, rows_num):
            extra_cell = False  # control extra cell at start (if right)
            for column in range(0, cols_num):
                np_array_final[row][column] = np_array[row][column]
                ln = 0
                if not left and not extra_cell:
                    self.cell(int(self.WIDTH))
                    extra_cell = True
                if column == cols_num - 1:
                    ln = 1
                if np_array[row][column] == 0:
                    name_sensor = ""
                    fill = False
                    border = 0
                    self.cell(w=width_cell, h=height_cell, txt=name_sensor, ln=ln, border=border, fill=fill)
                else:
                    value_barrier = ""
                    if np_array[row][column] == 3: # celda en gris, oblea rota
                        fill = True
                        border = 1
                        name_sensor = "C" + str(counter).zfill(3)
                        counter += 1
                        color = "gris"
                        self.set_fill_color(207, 207, 207)
                        np_array_final[row][column] = 3
                    if np_array[row][column] == 2:
                        fill = True
                        border = 1
                        name_sensor = "C" + str(counter).zfill(3)

                        if num_device in bad_list:
                            color = "blanco"
                            self.set_fill_color(255, 255, 255)
                            np_array_final[row][column] = 1
                        else:
                            color = "verde"
                            # set green color for good devices. This color is a green degraded en function value of alturas_barrera chip

                            #self.set_fill_color(34, 139, 34)  # verde bosque (#228b22)
                            value_barrier = round(alturas_barrera_good[num_device_good], 3)
                            color_chip = self.assign_color(alturas_barrera_good[num_device_good], min_alturas_barrera, max_alturas_barrera)
                            num_device_good += 1
                            self.set_fill_color(color_chip[0], color_chip[1], color_chip[2])

                        counters[color] += 1
                        # self.page_link[name_sensor] = self.add_link()
                        counter += 1
                        num_device += 1

                    if np_array[row][column] == 1:
                        name_sensor = "C" + str(counter).zfill(3)
                        fill = False
                        border = 1
                        counters["blanco"] += 1
                        counter += 1
                    self.cell(w=width_cell, h=height_cell, txt=name_sensor, ln=ln, border=border, fill=fill,
                              align='C')

        # Print counters
        self.ln(10)
        self.set_font('Dejavu', 'B', 10)
        wh = 8
        self.set_fill_color(34, 139, 34)
        if not left: self.cell(int(self.WIDTH))
        percentage = "{:.2%}".format(float((counters["verde"] / self.xips_number)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=40, h=wh, txt="Single barrier : ", ln=0, fill=False)
        self.cell(w=40, h=wh, txt=str(counters["verde"]) + f" devices ({percentage})", ln=1, fill=False)
        self.ln(2)
        self.set_fill_color(255, 255, 255)
        if not left: self.cell(int(self.WIDTH))
        percentage = "{:.2%}".format(float((counters["blanco"] / self.xips_number)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=40, h=wh, txt="Multiple barrier : ", ln=0, fill=False)
        self.cell(w=40, h=wh, txt=str(counters["blanco"]) + f" devices ({percentage})", ln=1, fill=False)
        self.ln(2)
        # print gradient colors for min_alturas_barrera to max_alturas_barrera
        gradient = [
            (189, 255, 189),
            (169, 236, 170),
            (149, 217, 152),
            (129, 197, 133),
            (109, 178, 114),
            (90, 159, 96),
            (70, 140, 77),
            (50, 120, 58),
            (30, 101, 40),
            (10, 82, 21)
        ]
        ln=0
        self.set_font('Dejavu', 'B', 8)
        for i in range(10):
            if i==0:
                # format value min_alturas_barrera to 3 decimals
                min_alturas_barrera = round(min_alturas_barrera, 3)
                self.cell(w=wh, h=wh, txt=str(min_alturas_barrera), fill=False, border=0, ln=ln)
            else:
                if i==9:
                    ln=1
                    max_alturas_barrera = round(max_alturas_barrera, 3)
                    self.cell(w=wh, h=wh, txt=str(max_alturas_barrera), fill=False, border=0, ln=ln)
                else:
                    self.cell(w=wh, h=wh, txt="", fill=False, border=0, ln=ln)

        for i in range(10):
            self.set_fill_color(gradient[i][0], gradient[i][1], gradient[i][2])
            ln = 0
            if i==9: ln = 1
            self.cell(w=wh, h=wh, txt="", fill=True, border=1, ln=ln)
        self.ln(2)

        self.cell(w=wh, h=wh, txt=f"Median: {str(round(median_alturas_barrera, 3))}", fill=False, border=0, ln=1)




        return np_array_final

    def table_conditions(self, type, wafer, y, units):
        # coge las condiciones de los ficheros forward.json y reverse.json que estan dentro de la carpeta de cada wafer
        # sino coge las generales
        wafer_path = self.path_run + "/" + wafer
        file_config = wafer_path + "/" + type + ".json"
        file_config_general = self.path_run + "/" + type + ".json"
        self.set_font('Dejavu', 'B', 8)
        fill_color_rgb = [137, 207, 240]  # baby blue (https://htmlcolorcodes.com/colors/shades-of-blue/)
        self.set_fill_color(fill_color_rgb[0], fill_color_rgb[1], fill_color_rgb[2])
        config = None
        if os.path.exists(file_config):
            f = open(file_config, mode='r', encoding='utf8')
            config = json.loads(f.read())
            f.close()
        elif os.path.exists(file_config_general):  # buscamos fichero general
            f = open(file_config_general, mode='r', encoding='utf8')
            config = json.loads(f.read())
            f.close()

        if config:
            y = y + 2
            self.set_y(y)
            # self.cell(w=120, h=5, txt="", ln=0, fill=False, align='C')
            self.cell(w=45, h=5, txt=type + " conditions", ln=1, fill=True, align='C')
            self.set_font('Dejavu', '', 7)
            fill_color_rgb = [240, 255, 255]  # azure (https://htmlcolorcodes.com/colors/shades-of-blue/)
            self.set_fill_color(fill_color_rgb[0], fill_color_rgb[1], fill_color_rgb[2])
            for param, value in config.items():
                # self.cell(w=120, h=3, txt="", ln=0, fill=False, align='C')
                self.cell(w=25, h=3, txt=param, ln=0, fill=True, align='R')
                txtValue = str(value)
                if param in units[type]:
                    txtValue += " " + units[type][param]
                self.cell(w=20, h=3, txt=txtValue, ln=1, fill=True)

    def numpy_array_print_to_wafer_combinado(self, np_array_reverse, statistics, np_array_filtro, alturas_barrera, left=True):

        # np_array = np.where(np_array_filtro == 2, np_array_reverse, np.where(np_array_filtro == 0, 1, 0))
        # np_array = np.where(
        #     np_array_filtro == 1,
        #     np.where(np_array_reverse == 2, 1, np_array_reverse),
        #     np_array_reverse
        # )

        # np_array = np.where(np_array_filtro == 2, np_array_reverse, 0)
        rows_num, cols_num = np_array_reverse.shape
        i = 0
        alturas_barrera_good = []
        np_array = np.zeros((rows_num, cols_num))
        for row in range(0, rows_num):
            for column in range(0, cols_num):
                if np_array_filtro[row][column] == 1 or np_array_reverse[row][column] == 1:
                    np_array[row][column] = 1
                else:
                    np_array[row][column] = np_array_reverse[row][column]
                    if np_array[row][column] == 2:
                        alturas_barrera_good.append(alturas_barrera[i])
                        i += 1
        # get median and std for alturas_barrera_good
        median_barrier_height = np.median(alturas_barrera_good)
        std_barrier_height = np.std(alturas_barrera_good)
        # print("Median barrier height: ", median_barrier_height)
        # print("std barrier height: ", std_barrier_height)
        # print("Len alturas barrera good: ", len(alturas_barrera_good))
        # fit middle page, calc width cell (same height), put value to make margin
        margin = 50
        width_cell = round((self.WIDTH-margin) / rows_num)
        height_cell = width_cell
        self.set_fill_color(255, 255, 255) # blanco por defecto
        self.ln(5)
        counter = 1
        counters = dict()

        counters["verde"] = 0
        counters["azul"] = 0
        counters["naranja"] = 0
        counters["blanco"] = 0
        counters["negro"] = 0
        counters["gris"] = 0
        num_device = 0
        self.set_font('Dejavu', '', 3)
        for row in range(0, rows_num):
            extra_cell = False  # control extra cell at start (if right)
            for column in range(0, cols_num):
                ln = 0
                if not left and not extra_cell:
                    self.cell(int(self.WIDTH))
                    extra_cell = True
                if column == cols_num - 1:
                    ln = 1
                if np_array[row][column] == 0:
                    name_sensor = ""
                    fill = False
                    border = 0
                    self.cell(w=width_cell, h=height_cell, txt=name_sensor, ln=ln, border=border, fill=fill)
                else:
                    name_sensor = "C" + str(counter).zfill(3)
                    border = 1
                    color = "blanco"
                    fill = True
                    if np_array[row][column] == 2:
                        # miramos valores para el sensor
                        # asignamos valores en np_array
                        # voltage_value= float(statistics["last_voltage"][num_device])
                        current_value = abs(float(statistics["last_current"][num_device]))

                        if current_value < 1E-6:
                            color = "verde"
                            self.set_fill_color(34, 139, 34)  # verde bosque (#228b22)
                        elif 1E-6 <= current_value < 10E-6:
                            color = "azul"
                            self.set_fill_color(0, 150, 255)
                        elif 10E-6 <= current_value < 100E-6:
                            color = "naranja"
                            self.set_fill_color(255, 165, 0)
                        else:
                            color = "negro" # not possible, compliance 100uA
                            self.set_fill_color(0, 0, 0)

                        num_device += 1
                        # self.page_link[name_sensor] = self.add_link()

                    if np_array[row][column] == 1:
                        self.set_fill_color(255, 255, 255)
                        num_device += 1
                    if np_array[row][column] == 3: # celda en gris, oblea rota
                        color = "gris"
                        self.set_fill_color(207, 207, 207)
                    counters[color] += 1
                    self.cell(w=width_cell, h=height_cell, txt=name_sensor, ln=ln, border=border, fill=fill, align='C')
                    # num_device += 1
                    counter += 1

        # Print counters
        self.ln(10)
        self.set_font('Dejavu', 'B', 10)
        wh = 8
        self.set_fill_color(255, 255, 255)
        if not left: self.cell(int(self.WIDTH))
        percentage = "{:.2%}".format(float((counters["blanco"] / self.xips_number)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=40, h=wh, txt="Bad diodes: ", ln=0, fill=False)
        self.cell(w=40, h=wh, txt=str(counters["blanco"]) + f" devices ({percentage})", ln=1, fill=False)
        self.ln(2)
        self.set_fill_color(34, 139, 34)
        if not left: self.cell(int(self.WIDTH))
        percentage = "{:.2%}".format(float((counters["verde"] / self.xips_number)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=40, h=wh, txt="I < 1uA : ", ln=0, fill=False)
        self.cell(w=40, h=wh, txt=str(counters["verde"]) + f" devices ({percentage})", ln=1, fill=False)
        self.ln(2)
        self.set_fill_color(0, 150, 255)
        if not left: self.cell(int(self.WIDTH))
        percentage = "{:.2%}".format(float((counters["azul"] / self.xips_number)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=40, h=wh, txt="I 1uA-10uA : ", ln=0, fill=False)
        self.cell(w=40, h=wh, txt=str(counters["azul"]) + f" devices ({percentage})", ln=1, fill=False)
        self.ln(2)
        self.set_fill_color(255, 165, 0)
        if not left: self.cell(int(self.WIDTH))
        percentage = "{:.2%}".format(float((counters["naranja"] / self.xips_number)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=40, h=wh, txt="I 10uA-100uA : ", ln=0, fill=False)
        self.cell(w=40, h=wh, txt=str(counters["naranja"]) + f" devices ({percentage})", ln=1, fill=False)
        self.ln(2)
        # format float value to string with 2 decimals
        median_barrier_height = "{:.3f}".format(median_barrier_height)
        std_barrier_height = "{:.2f}".format(std_barrier_height)
        self.set_font('Dejavu', 'I', 8)
        self.cell(w=100, h=wh, txt="Barrier height: " + median_barrier_height + " ± " + std_barrier_height + " (V)", ln=1, fill=False)



