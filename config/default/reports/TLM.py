# TLM report Class
from sklearn.linear_model import LinearRegression
from scipy.stats import linregress, norm

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

from sklearn.tree import export_text

from modules.result_file import ResultFile
from modules.statistics_estepa import StatisticsEstepa
import toml
import json
import shutil
import math
from glob import glob
import statistics


class TLM(FPDF):
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
        for wafer in self.wafers:
            self.save_graphs(wafer)
        self.config_estepa_toml = dict()
        self.get_toml()
        self.xips_number = 1452  # 4" 708, 6" 1452
        base_dejavu_path = 'C:\\WINDOWS\\Fonts\\'
        self.add_font('DejaVu', '', os.path.join(base_dejavu_path, 'DejaVuSerif.ttf'), uni=True)
        self.add_font('DejaVu', 'B', os.path.join(base_dejavu_path, 'DejaVuSerif-Bold.ttf'), uni=True)
        self.add_font('DejaVu', 'I', os.path.join(base_dejavu_path, 'DejaVuSerif-Italic.ttf'), uni=True)

    def header(self, title="TLM REPORT"):
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
        self.cuartos = ["UP_LEFT", "UP_RIGHT", "DOWN_LEFT", "DOWN_RIGHT"]
        for directory in sorted(os.listdir(self.path_run)):
            if os.path.isdir(self.path_run + "/" + directory):
                self.wafers.append(directory)
        # check if exists 92 TXT files inside wafer folder + cuartos folder + data folder for UP cuartos and 90 TXT files for DOWN cuartos
        if len(self.wafers) > 0:
            for wafer in self.wafers:
                dir_wafer = self.path_run + "/" + wafer + "/"
                # check if exists 92*12 TXT total files inside wafer folder + cuartos folder + data folder for UP cuartos
                if "UP_LEFT" in wafer or "UP_RIGHT" in wafer:
                    dies_total = 92
                else:
                    dies_total = 90

                for die in range(1, dies_total + 1):
                    for module in range(1, 13):
                        namefile = "IV_" + str(die) + "_" + str(module) + ".TXT"
                        if not os.path.isfile(dir_wafer + "/data/" + namefile):
                            self.error = True
                            self.errorMessage = dir_wafer + "/data/" + namefile
                            break

        else:
            self.error = True
            self.errorMessage = "No wafers found in dir " + self.path_run

    def save_graphs(self, wafer):
        self.widgets.txtResultReport.appendPlainText(f"Saving graphs for wafer {wafer}")
        existsPlot = False
        path_plot = self.path_run + "/" + wafer + "/plots/"
        if not os.path.exists(path_plot):
            os.makedirs(path_plot)
        path_data = self.path_run + "/" + wafer + "/data/"
        if len(os.listdir(path_plot)) > 0:
            existsPlot = True
        if not existsPlot:
            # create plots
            counter = 0
            OVERFLOW_REPLACEMENT = np.nan
            for filedata in sorted(os.listdir(path_data)):
                QApplication.processEvents()
                if os.path.isfile(path_data + filedata) and "IV" in filedata:
                    # create plot in path_plot
                    # first column voltage, fourth colum resistance, skipping 4 rows, header None, separation tab
                    df = pd.read_csv(path_data + filedata, sep="\t", skiprows=4, header=None)
                    # check df columns
                    if df.shape[1] < 5:
                        self.widgets.txtResultReport.appendPlainText(
                            f"Error: {filedata} has less than 5 columns, skipping...")
                        continue

                    # Reemplazar "Overflow" y convertir a float
                    df[1] = pd.to_numeric(df[1], errors='coerce')  # Voltaje
                    df[4] = df[4].replace("Overflow", OVERFLOW_REPLACEMENT)
                    df[4] = pd.to_numeric(df[4], errors='coerce')  # Resistencia

                    ax = plt.gca()
                    df.plot(kind='line', x=df.columns[1], y=df.columns[4], ax=ax, label="R-V",
                            color="blue", grid=True)
                    plt.title(f"Resistance vs Voltage {filedata}")
                    plt.xlabel("Voltage (V)")
                    plt.ylabel("Resistance (Ohm)")
                    plt.subplots_adjust(bottom=0.15)

                    filePlot = path_plot + filedata.replace(".TXT", ".png")
                    plt.savefig(filePlot, dpi=100)
                    plt.clf()
                    counter += 1


            self.widgets.txtResultReport.appendPlainText(
                f" - Created {str(counter)} graphs for wafer: {wafer}")

    def get_toml(self):
        path_config_file = self.path_run + "/" + self.run + ".toml"
        if os.path.exists(path_config_file):
            with open(path_config_file, mode="r", encoding='utf-8') as fp:
                config = toml.load(fp)
                self.config_estepa_toml = config

    def page_header(self):
        QApplication.processEvents()
        title = self.config["reports"]["title"]
        if self.run in self.config_estepa_toml and "title" in self.config_estepa_toml[self.run]:
            title = self.config_estepa_toml[self.run]["title"]
        subtitle = self.config["reports"]["subtitle"]
        if self.run in self.config_estepa_toml and "subtitle" in self.config_estepa_toml[self.run]:
            subtitle = self.config_estepa_toml[self.run]["subtitle"]
        date = self.config["reports"]["date"]
        if self.run in self.config_estepa_toml and "date" in self.config_estepa_toml[self.run]:
            date = self.config_estepa_toml[self.run]["date"]
        author = self.config["reports"]["author"]
        if self.run in self.config_estepa_toml and "author" in self.config_estepa_toml[self.run]:
            author = self.config_estepa_toml[self.run]["author"]

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
        conditions = self.config_estepa_toml[self.run]["conditions"]
        self.set_y(30)
        self.set_font('Dejavu', 'B', 11)
        self.cell(0, 10, "Measurement conditions:", 0, 1, 'L')
        self.set_font('Dejavu', '', 10)
        self.cell(50, 5, "- PC: ", 0, 0, 'L')
        self.cell(50, 5, conditions["pc"], 0, 1, 'L')
        self.cell(50, 5, "- Software: ", 0, 0, 'L')
        self.cell(50, 5, conditions["software"], 0, 1, 'L')
        self.cell(50, 5, "- Instrument: ", 0, 0, 'L')
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
            if self.run in self.config_estepa_toml and "conditions" in self.config_estepa_toml[self.run]:
                self.add_page()
                self.page_conditions()
                # print table conditions
                units = dict()
                units["conditions"] = {"START": "V", "STOP": "V", "STEP": "V", "COMPLIANCE": "A"}
                y = 100
                self.table_conditions(wafer, y, units)
                y = y + 30

        def get_mean_resistance(file_path):
            try:
                df = pd.read_csv(file_path, skiprows=4, header=None, sep="\t")
                # # quitamos de df el punto central, para 0V
                # df = df[df[1] != 0]
                # print(f"Media RESISTENCIA para el fichero {file_path}: {df[4].mean()}")
                # return df[4].mean()
                # Extraemos las columnas de voltaje y corriente
                V = df[1].values
                I = df[2].values

                # Aplicamos una máscara para eliminar posibles ceros o valores extremos
                mask = (I != 0) & (V != 0)
                V_clean = V[mask]
                I_clean = I[mask]

                # Hacemos la regresión lineal: V = R * I + b
                slope, intercept, r_value, p_value, std_err = linregress(I_clean, V_clean)

                # La pendiente (slope) es la resistencia media
                return slope
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                return None

        # Constantes c1 y c2 por módulo (indexadas de 1 a 12)
        c1 = {
            1: 0.026317308317, 2: 0.064538521138, 3: 0.095310179804,
            4: 0.125163142954, 5: 0.154150679827, 6: 0.182321556794,
            7: 0.236388778064, 8: 0.287682072452, 9: 0.336472236621,
            10: 0.382992252256, 11: 0.427444014827, 12: 0.510825623766
        }
        c2 = {
            1: 0.013160173160, 2: 0.012916666667, 3: 0.012727272727,
            4: 0.012549019608, 5: 0.012380952381, 6: 0.012222222222,
            7: 0.011929824561, 8: 0.011666666667, 9: 0.011428571429,
            10: 0.011212121212, 11: 0.011014492754, 12: 0.010666666667
        }

        # print wafermap & histogram
        wafer_path = self.path_run + "/" + wafer
        cuarto = wafer.split("_")[1] + "_" + wafer.split("_")[2]
        wafer_data_path = wafer_path + "/data/"
        resistances = dict()

        # get files alphabetic sorted by name (IV_1_1.TXT, IV_1_2.TXT, ... IV_90_12.TXT)
        files = glob(wafer_data_path + "IV_*.TXT")

        def extract_indices(filename):
            basename = os.path.basename(filename)
            parts = basename.replace("IV_", "").replace(".TXT", "").split("_")
            return tuple(map(int, parts))  # (die, modulo)

        for file in sorted(files, key=extract_indices):
            parts = os.path.basename(file).replace("IV_", "").replace(".TXT", "").split("_")
            if len(parts) != 2:
                continue
            die, modulo = map(int, parts)
            mean_res = get_mean_resistance(file)
            if mean_res is not None:
                if modulo not in resistances:
                    resistances[modulo] = []
                resistances[modulo].append((die, mean_res))

        wafermap_file = ""
        if "wafermap_file" in self.config_estepa_toml[self.run]["conditions"]:
            wafermap_file = self.config_estepa_toml[self.run]["conditions"]["wafermap_file"]
        if "wafermap_file" in self.config_estepa_toml[wafer]["conditions"]:
            wafermap_file = self.config_estepa_toml[wafer]["conditions"]["wafermap_file"]
        left = True


        if "WAFERMAP" in self.options and self.options["WAFERMAP"]:
            # means, medians & stdev list
            means = []
            medians = []
            stdevs = []
            # print wafermap for each module in resistances
            for modulo in range(1,13):
                if modulo in resistances:
                    # get wafermap file
                    wafermap_file = self.config_estepa_toml[self.run]["conditions"]["wafermap_file"]
                    if "wafermap_file" in self.config_estepa_toml[wafer]["conditions"]:
                        wafermap_file = self.config_estepa_toml[wafer]["conditions"]["wafermap_file"]
                    # get np_array
                    np_array, _ = self.print_mapa_wafer_6(wafermap_file)
                    self.add_page()
                    self.set_x(10)
                    x_texto = 20
                    self.set_y(30)
                    self.set_font('Dejavu', 'B', 10)
                    self.text(x_texto, 35, wafer)
                    self.set_font('Dejavu', '', 9)
                    self.text(x_texto, 40, "Wafermap module " + str(modulo))
                    np_array_reverse, estadistica, estepa_configuration = self.numpy_array_print_to_wafer(np_array, wafer, resistances, modulo, left)
                    # print table estadistica (estadistica.mean, estadistica.median, estadistica.stddev, estadistica.points_ini, estadistica.points_end)
                    self.ln(2)

                    self.cell(0, 10, "", 0, 1, 'C')
                    self.set_font('Dejavu', '', 8)
                    # print mena with value formatted and grec symbol ohm
                    self.text(x_texto, 50, "Method: " + str(estepa_configuration["method"]))
                    self.text(x_texto, 55, ("Mean: " + str("{:.2f}".format(estadistica.mean)) + " Ω") if abs(estadistica.mean)<1E20 else "Mean: Overflow Ω")
                    self.text(x_texto, 60, ("Median: " + str("{:.2f}".format(estadistica.median)) + " Ω") if abs(estadistica.median)<1E20 else "Median: Overflow Ω")
                    self.text(x_texto, 65, ("Stddev: " + str("{:.2f}".format(estadistica.stdev)) + " Ω") if abs(estadistica.stdev)<1E20 else "Stddev: Overflow Ω")
                    means.append(estadistica.mean)
                    medians.append(estadistica.median)
                    stdevs.append(estadistica.stdev)
                    self.text(x_texto, 70,
                              "Points: " + str(estadistica.points_end) + " / " + str(estadistica.points_ini))

                    if "HISTOGRAM" in self.options and self.options["HISTOGRAM"]:
                        num_chunks = estadistica.config["chunks"]
                        parameter = "RES_mod" + str(modulo)
                        data = estadistica.data_list
                        fig = Figure(figsize=(6, 4), dpi=300)
                        fig.subplots_adjust(top=0.8)
                        ax1 = fig.add_subplot(211)
                        ax1.set_title(parameter + " histogram")

                        # Histograma sin densidad (frecuencias absolutas)
                        n, bins, patches = ax1.hist(
                            np.array(data),
                            num_chunks,
                            facecolor="#228b22",
                            edgecolor="#228b22",
                            alpha=0.6  # transparencia para ver bien la curva encima
                        )

                        # Ajuste Gaussiano
                        # mu, std = norm.fit(data)
                        mu, std = estadistica.mean, estadistica.stdev
                        x = np.linspace(min(bins), max(bins), 100)
                        p = norm.pdf(x, mu, std)

                        # Escalar la curva a la altura del histograma (frecuencias absolutas)
                        bin_width = bins[1] - bins[0]
                        p_scaled = p * len(data) * bin_width

                        # Dibujar la curva ajustada
                        if abs(estadistica.median)<1E20:
                            ax1.plot(x, p_scaled, 'r--', linewidth=2, label=f"Normal fit: μ={mu:.2f}, σ={std:.2f}")
                        else:
                            ax1.plot(x, p_scaled, 'r--', linewidth=2, label="Normal fit: Overflow")

                        # Etiquetas
                        ax1.set_xlabel(parameter)
                        ax1.set_ylabel("Frequency")
                        ax1.grid(True)
                        ax1.legend()

                        # Convertir a imagen
                        canvas = FigureCanvas(fig)
                        canvas.draw()
                        img = Image.fromarray(np.asarray(canvas.buffer_rgba()))
                        matplotlib.pyplot.close(fig)

                        # Insertar en PDF
                        if left:
                            self.set_x(20)
                        else:
                            self.set_x(int(self.WIDTH / 2))
                        self.image(img, w=int(self.WIDTH / 2))

            # Al finalizar los modulos, se añade una página con la gráfica de puntos de todas las medias de los modulos
            # en función del diametro del anillo que es diferente para los 12 modulos
            # d: 4, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 100
            d = [4, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 100]

            self.add_page()
            self.set_x(10)
            x_texto = 20
            self.set_y(30)
            self.set_font('Dejavu', 'B', 10)
            self.text(x_texto, 35, wafer)
            self.set_font('Dejavu', '', 9)
            self.text(x_texto, 40, "Wafermap module all")
            # make a graph: x axis d and y axis medians, with linear regression
            # Convertir a arrays de numpy
            x = np.array(d)
            y = np.array(means)

            # Filtrar los valores válidos: eliminar los marcados como -9e+99
            threshold_error = -1e+50  # margen por si acaso
            valid_indices = y > threshold_error
            invalid_indices = ~valid_indices  # inverso

            # Realizar ajuste solo con los válidos
            x_valid = x[valid_indices]
            y_valid = y[valid_indices]

            if len(x_valid) >= 2:
                # Ajuste lineal: y = m*x + b
                m, b = np.polyfit(x_valid, y_valid, 1)
                fit_line = m * x + b

                # Crear figura
                fig = Figure(figsize=(6, 4), dpi=300)
                ax = fig.add_subplot(111)
                # ax.scatter(x, y, color="blue", label="Data")
                # Dibujar los puntos válidos (azul)
                ax.scatter(x_valid, y_valid, color="blue", label="Valid Data")

                # Dibujar los puntos inválidos (rojo)
                ax.scatter(x[invalid_indices], y[invalid_indices], color="red", label="Discarded Data")

                ax.plot(x, fit_line, color="red", linestyle="--", label=f"Fit: y = {m:.2f}x + {b:.2f}")
                ax.set_title(wafer + " - Mean R vs. Ring Diameter")
                ax.set_xlabel("Ring Diameter (d)")
                ax.set_ylabel("Resistance (R)")
                ax.grid(True)
                ax.legend()

                # Texto con ecuación dentro del plot
                # text = f"y = {m:.2f}x + {b:.2f}"
                # ax.text(0.05, 0.95, text, transform=ax.transAxes, fontsize=10, verticalalignment='top')

                # Convertir a imagen para FPDF
                canvas = FigureCanvas(fig)
                canvas.draw()
                img = Image.fromarray(np.asarray(canvas.buffer_rgba()))
                matplotlib.pyplot.close(fig)

                # Tabla de valores h(d) y g(d)
                h_dict = {
                    4: 0.026317308317, 10: 0.064538521138, 15: 0.095310179804, 20: 0.125163142954,
                    25: 0.154150679827, 30: 0.182321556794, 40: 0.236388778064, 50: 0.287682072452,
                    60: 0.336472236621, 70: 0.382992252256, 80: 0.427444014827, 100: 0.510825623766
                }
                g_dict = {
                    4: 0.013160173160, 10: 0.012916666667, 15: 0.012727272727, 20: 0.012549019608,
                    25: 0.012380952381, 30: 0.012222222222, 40: 0.011929824561, 50: 0.011666666667,
                    60: 0.011428571429, 70: 0.011212121212, 80: 0.011014492754, 100: 0.010666666667
                }

                # Crear matrices para regresión
                # H = np.array([h_dict[val] for val in d])
                # G = np.array([g_dict[val] for val in d])
                # Y = np.array(means)
                H = np.array([h_dict[val] for val in x_valid])
                G = np.array([g_dict[val] for val in x_valid])
                Y = np.array(y_valid)

                # Diseño de matriz (X): columnas h y g
                X = np.column_stack((H, G))

                # Resolución por mínimos cuadrados
                coeffs, residuals, rank, s = np.linalg.lstsq(X, Y, rcond=None)
                A, B = coeffs

                # Cálculo de Rsh y Lt
                Rsh = 2 * np.pi * A
                Lt = B / A

                # Resultados
                print(f"A = {A:.2e}")
                print(f"B = {B:.2e}")
                print(f"Rsh = {Rsh:.2e} Ω")
                print(f"Lt = {Lt:.2f} μm")
                Rc = Rsh * Lt ** 2
                # Rc in Ω·cm²
                Rc = Rc * 1E-8  # convert to Ω·cm²
                print(f"Rc = {Rc:.4e} Ω·cm²")
                # calc ρ(Ωcm) like ρ = Rsh * 0,0003
                p = Rsh * 0.0003
                print(f"ρ = {p:.4e} Ω·cm")
                # Crear tabla
                self.set_x(10)
                x_texto = 20
                self.set_y(30)
                self.set_font('DejaVu', 'B', 10)
                self.text(x_texto, 35, wafer)
                self.set_font('DejaVu', '', 9)
                self.text(x_texto, 55, "A: " + str("{:.2e}".format(A)) + " Ω")
                self.text(x_texto, 60, "B: " + str("{:.2e}".format(B)) + " Ω")
                self.text(x_texto, 65, "Rsh: " + str("{:.4e}".format(Rsh)) + " Ω")
                self.text(x_texto, 70, "Lt: " + str("{:.4f}".format(Lt)) + " μm")
                self.set_font('DejaVu', 'B', 9)
                # Rc and p in cientific notation
                self.text(x_texto, 75, "Rc: " + str("{:.2e}".format(Rc)) + " Ω·cm²")
                self.text(x_texto, 80, "ρ: " + str("{:.2e}".format(p)) + " Ω·cm")

            else:
                # Si no hay suficientes datos válidos
                print("ERROR: No valid data points for fitting.")

                # Puedes hacer un plot solo con los puntos descartados
                fig = Figure(figsize=(6, 4), dpi=300)
                ax = fig.add_subplot(111)

                ax.scatter(x[invalid_indices], y[invalid_indices], color="red", label="Discarded Data")
                ax.set_title(wafer + " - Not enough valid data")
                ax.set_xlabel("Ring Diameter (d)")
                ax.set_ylabel("Resistance (R)")
                ax.grid(True)
                ax.legend()

                canvas = FigureCanvas(fig)
                canvas.draw()
                img = Image.fromarray(np.asarray(canvas.buffer_rgba()))
                matplotlib.pyplot.close(fig)

            # Insertar en el PDF
            if left:
                self.set_x(20)
            else:
                self.set_x(int(self.WIDTH / 2))
            self.set_y(100)
            self.image(img, w=int(self.WIDTH / 2))







    def print_mapa_wafer_6(self, wafermap_file):
        global wafer_parameters
        matrix_size = 34
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

        wafer_positions_all = ['0 0', '-1 0', '-2 0', '-3 0',
                               '1 -1', '0 -1', '-1 -1', '-2 -1', '-3 -1', '-4 -1',
                               '2 -2', '1 -2', '0 -2', '-1 -2', '-2 -2', '-3 -2', '-4 -2', '-5 -2',
                               '2 -3', '1 -3', '0 -3', '-1 -3', '-2 -3', '-3 -3', '-4 -3', '-5 -3',
                               '3 -4', '2 -4', '1 -4', '0 -4', '-1 -4', '-2 -4', '-3 -4', '-4 -4', '-5 -4', '-6 -4',
                               '3 -5', '2 -5', '1 -5', '0 -5', '-1 -5', '-2 -5', '-3 -5', '-4 -5', '-5 -5', '-6 -5',
                               '3 -6', '2 -6', '1 -6', '0 -6', '-1 -6', '-2 -6', '-3 -6', '-4 -6', '-5 -6', '-6 -6',
                               '4 -7', '3 -7', '2 -7', '1 -7', '0 -7', '-1 -7', '-2 -7', '-3 -7', '-4 -7', '-5 -7', '-6 -7', '-7 -7',
                               '4 -8', '3 -8', '2 -8', '1 -8', '0 -8', '-1 -8', '-2 -8', '-3 -8', '-4 -8', '-5 -8', '-6 -8', '-7 -8',
                               '4 -9', '3 -9', '2 -9', '1 -9', '0 -9', '-1 -9', '-2 -9', '-3 -9', '-4 -9', '-5 -9', '-6 -9', '-7 -9',
                               '4 -10', '3 -10', '2 -10', '1 -10', '0 -10', '-1 -10', '-2 -10', '-3 -10', '-4 -10', '-5 -10', '-6 -10', '-7 -10',
                               '4 -11', '3 -11', '2 -11', '1 -11', '0 -11', '-1 -11', '-2 -11', '-3 -11', '-4 -11', '-5 -11', '-6 -11', '-7 -11',
                               '5 -12', '4 -12', '3 -12', '2 -12', '1 -12', '0 -12', '-1 -12', '-2 -12', '-3 -12', '-4 -12', '-5 -12', '-6 -12', '-7 -12', '-8 -12',
                               '5 -13', '4 -13', '3 -13', '2 -13', '1 -13', '0 -13', '-1 -13', '-2 -13', '-3 -13', '-4 -13', '-5 -13', '-6 -13', '-7 -13', '-8 -13',
                               '5 -14', '4 -14', '3 -14', '2 -14', '1 -14', '0 -14', '-1 -14', '-2 -14', '-3 -14', '-4 -14', '-5 -14', '-6 -14', '-7 -14', '-8 -14',
                               '5 -15', '4 -15', '3 -15', '2 -15', '1 -15', '0 -15', '-1 -15', '-2 -15', '-3 -15', '-4 -15', '-5 -15', '-6 -15', '-7 -15', '-8 -15',
                               '4 -16', '3 -16', '2 -16', '1 -16', '0 -16', '-1 -16', '-2 -16', '-3 -16', '-4 -16', '-5 -16', '-6 -16', '-7 -16',
                               '4 -17', '3 -17', '2 -17', '1 -17', '0 -17', '-1 -17', '-2 -17', '-3 -17', '-4 -17', '-5 -17', '-6 -17', '-7 -17',
                               '5 -18', '4 -18', '3 -18', '2 -18', '1 -18', '0 -18', '-1 -18', '-2 -18', '-3 -18', '-4 -18', '-5 -18', '-6 -18', '-7 -18', '-8 -18',
                               '5 -19', '4 -19', '3 -19', '2 -19', '1 -19', '0 -19', '-1 -19', '-2 -19', '-3 -19', '-4 -19', '-5 -19', '-6 -19', '-7 -19', '-8 -19',
                               '5 -20', '4 -20', '3 -20', '2 -20', '1 -20', '0 -20', '-1 -20', '-2 -20', '-3 -20', '-4 -20', '-5 -20', '-6 -20', '-7 -20', '-8 -20',
                               '5 -21', '4 -21', '3 -21', '2 -21', '1 -21', '0 -21', '-1 -21', '-2 -21', '-3 -21', '-4 -21', '-5 -21', '-6 -21', '-7 -21', '-8 -21',
                               '4 -22', '3 -22', '2 -22', '1 -22', '0 -22', '-1 -22', '-2 -22', '-3 -22', '-4 -22', '-5 -22', '-6 -22', '-7 -22',
                               '4 -23', '3 -23', '2 -23', '1 -23', '0 -23', '-1 -23', '-2 -23', '-3 -23', '-4 -23', '-5 -23', '-6 -23', '-7 -23',
                               '4 -24', '3 -24', '2 -24', '1 -24', '0 -24', '-1 -24', '-2 -24', '-3 -24', '-4 -24', '-5 -24', '-6 -24', '-7 -24',
                               '4 -25', '3 -25', '2 -25', '1 -25', '0 -25', '-1 -25', '-2 -25', '-3 -25', '-4 -25', '-5 -25', '-6 -25', '-7 -25',
                               '4 -26', '3 -26', '2 -26', '1 -26', '0 -26', '-1 -26', '-2 -26', '-3 -26', '-4 -26', '-5 -26', '-6 -26', '-7 -26',
                               '3 -27', '2 -27', '1 -27', '0 -27', '-1 -27', '-2 -27', '-3 -27', '-4 -27', '-5 -27', '-6 -27',
                               '3 -28', '2 -28', '1 -28', '0 -28', '-1 -28', '-2 -28', '-3 -28', '-4 -28', '-5 -28', '-6 -28',
                               '3 -29', '2 -29', '1 -29', '0 -29', '-1 -29', '-2 -29', '-3 -29', '-4 -29', '-5 -29', '-6 -29',
                               '2 -30', '1 -30', '0 -30', '-1 -30', '-2 -30', '-3 -30', '-4 -30', '-5 -30',
                               '2 -31', '1 -31', '0 -31', '-1 -31', '-2 -31', '-3 -31', '-4 -31', '-5 -31',
                               '1 -32', '0 -32', '-1 -32', '-2 -32', '-3 -32', '-4 -32']

        real_origin_chip_all = "-6 -1"
        real_origin_chip = "-6 -1"
        wafer_positions = wafer_positions_all
        if "real_origin_chip" in wafer_parameters:
            real_origin_chip = wafer_parameters["real_origin_chip"]
        if "wafer_positions" in wafer_parameters:
            wafer_positions = wafer_parameters["wafer_positions"]
        if "nchips" in wafer_parameters:
            self.xips_number = int(wafer_parameters["nchips"])

        x_real_position = 8
        y_real_position = 0
        # center = matrix_size // 2
        # x_real_position = center + int(real_origin_chip.split()[0])
        # y_real_position = center + int(real_origin_chip.split()[1])

        difx = int(real_origin_chip_all.split()[0]) - int(real_origin_chip.split()[0])
        dify = int(real_origin_chip_all.split()[1]) - int(real_origin_chip.split()[1])

        wafer_coordinates = [(-int(y) + y_real_position , -int(x) + x_real_position)
                             for x, y in [pos.split() for pos in wafer_positions_all]]

        wafer_coordinates_dif = [(-int(y) + y_real_position + dify, -int(x) + x_real_position + difx)
                             for x, y in [pos.split() for pos in wafer_positions]]

        # wafer_coordinates = [(center - int(y), center + int(x)) for x, y in
        #                      [pos.split() for pos in wafer_positions_all]]
        # wafer_coordinates_dif = [(y_real_position - int(y), x_real_position + int(x)) for x, y in
        #                          [pos.split() for pos in wafer_positions]]

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

    def get_estepa_configuration_toml(self, wafer, parameter):
        estepa_configuration = self.config["estepa"]
        print(f"Searching estepa configuration for wafer {wafer} and parameter {parameter}")
        if len(self.config_estepa_toml) != 0:
            if self.run in self.config_estepa_toml:
                estepa_configuration = self.config_estepa_toml[self.run]
                print(f"Found estepa configuration for run {self.run}")
                if wafer in self.config_estepa_toml[self.run]:
                    estepa_configuration = self.config_estepa_toml[self.run][wafer]
                    print(f"Found estepa configuration for wafer {wafer}")
                    if parameter in self.config_estepa_toml[self.run][wafer]:
                        estepa_configuration = self.config_estepa_toml[self.run][wafer][parameter]
                        print(f"Found estepa configuration for wafer {wafer} and parameter {parameter}")
        return estepa_configuration

    def numpy_array_print_to_wafer(self, np_array, wafer, resistances, modulo, left=True):
        np_array_reverse = np_array.copy()
        rows_num, cols_num = np_array.shape
        # fit middle page, calc width cell (same height), put value to make margin
        margin = 100
        width_cell = round((self.WIDTH-margin) / 14)
        height_cell = round((self.WIDTH-margin) / 34)
        self.set_fill_color(255, 255, 255) # blanco por defecto
        self.ln(5)
        counter = 1
        counters = dict()
        resistances_modulo = resistances[modulo]
        # get list from resistances_modulo
        resistances_modulo = [x[1] for x in resistances_modulo]
        print(f"Resistances modulo {modulo}: {resistances_modulo}")
        parameter = "RES_mod" + str(modulo)
        estepa_configuration = self.get_estepa_configuration_toml(wafer, parameter)

        # create statistics estepa
        estadistica = dict()
        estadistica[parameter] = StatisticsEstepa(parameter, resistances_modulo, estepa_configuration)
        print(f"Data list: {estadistica[parameter].data_list}")
        print(f"Estadistica {estadistica[parameter].print_statistics()} ")


        counters["verde"] = 0
        counters["rojo"] = 0
        counters["azul"] = 0
        num_device = 0
        self.set_font('Dejavu', '', 3)
        i = 0
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

                        # print(f"Resistencia para el modulo {modulo} y posición {i}")
                        res_value= float(resistances_modulo[i-1])
                        # print(res_value)
                        # format res_value to text with 2 decimals
                        res_value_txt = str("{:.2f}".format(res_value))
                        # name_sensor = "C" + str(counter).zfill(3)
                        name_sensor = res_value_txt
                        if res_value < estepa_configuration["limmin"] or res_value > estepa_configuration["limmax"]:
                            color = "rojo"
                            self.set_fill_color(255, 0, 0)
                            np_array_reverse[row][column] = 1
                        else:
                            color = "verde"
                            # self.set_fill_color(34, 139, 34)  # verde bosque (#228b22)
                            # set scale green color
                            get_color = self.assign_color(res_value, estadistica[parameter])
                            if get_color == (0, 150, 255):
                                color = "azul"
                            self.set_fill_color(get_color[0], get_color[1], get_color[2])

                        counters[color] += 1
                        # self.page_link[name_sensor] = self.add_link()
                        counter += 1
                        num_device += 1
                        i += 1

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
        # green color
        self.set_fill_color(34, 139, 34)  # forest green (#228b22)
        if not left: self.cell(int(self.WIDTH))
        percentage = "{:.2%}".format(float((counters["verde"] / self.xips_number)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=40, h=wh, txt="Ok : ", ln=0, fill=False)
        self.cell(w=40, h=wh, txt=str(counters["verde"]) + f" devices ({percentage})", ln=1, fill=False)
        self.ln(2)
        #self.set_fill_color(0, 150, 255)
        # fill color red
        self.set_fill_color(255, 0, 0)
        if not left: self.cell(int(self.WIDTH))
        percentage = "{:.2%}".format(float((counters["rojo"] / self.xips_number)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=40, h=wh, txt="Error : ", ln=0, fill=False)
        self.cell(w=40, h=wh, txt=str(counters["rojo"]) + f" devices ({percentage})", ln=1, fill=False)
        self.ln(2)
        # fill color blue
        self.set_fill_color(0, 150, 255)
        if not left: self.cell(int(self.WIDTH))
        percentage = "{:.2%}".format(float((counters["azul"] / self.xips_number)))
        self.cell(w=wh, h=wh, txt="", fill=True, border=1)
        self.cell(w=40, h=wh, txt="Outlier : ", ln=0, fill=False)
        self.cell(w=40, h=wh, txt=str(counters["azul"]) + f" devices ({percentage})", ln=1, fill=False)
        self.ln(2)







        return np_array_reverse, estadistica[parameter], estepa_configuration


    def assign_color(self, valor, estadistica_parameter):
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


        # check if value is an outlier
        if valor not in estadistica_parameter.data_list:
            # set color to blue
            return (0, 150, 255)  # blue

        min_val = min(estadistica_parameter.data_list)
        max_val = max(estadistica_parameter.data_list)

        # Calcular los cuartiles del rango de valores
        quartiles = [min_val] + [min_val + (max_val - min_val) * (i / 10) for i in range(1, 10)] + [max_val]

        # Determinar en qué cuartil se encuentra el valor
        for i in range(len(quartiles) - 1):
            if quartiles[i] <= valor <= quartiles[i + 1]:
                index = i
                break


        # Devolver el color correspondiente al cuartil
        return gradient[index]

    def table_conditions(self, wafer, y, units):
        # coge las condiciones de los ficheros forward.json y reverse.json que estan dentro de la carpeta de cada wafer
        # sino coge las generales
        wafer_path = self.path_run + "/" + wafer
        file_config = wafer_path + "/conditions.json"
        file_config_general = self.path_run + "/conditions.json"
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
            self.cell(w=45, h=5, txt="Conditions", ln=1, fill=True, align='C')
            self.set_font('Dejavu', '', 7)
            fill_color_rgb = [240, 255, 255]  # azure (https://htmlcolorcodes.com/colors/shades-of-blue/)
            self.set_fill_color(fill_color_rgb[0], fill_color_rgb[1], fill_color_rgb[2])
            for param, value in config.items():
                # self.cell(w=120, h=3, txt="", ln=0, fill=False, align='C')
                self.cell(w=25, h=3, txt=param, ln=0, fill=True, align='R')
                txtValue = str(value)
                if param in units["conditions"]:
                    txtValue += " " + units["conditions"][param]
                self.cell(w=20, h=3, txt=txtValue, ln=1, fill=True)





