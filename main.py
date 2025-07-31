# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform
import toml
import logging
from logging.handlers import RotatingFileHandler

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
# general functions
from functions import *
# all other functions
from modules import *

from widgets import *

os.environ["QT_FONT_DPI"] = "96"  # FIX Problem for High DPI and Scale above 100%
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"  # options qtgraph

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

# ///////////////////////////////////////////////////////////////
# imports LOGIN & splash screen
# ///////////////////////////////////////////////////////////////
import time
# import hashlib # md5 pass generate
import bcrypt
import mysql.connector
from mysql.connector import errorcode

from screens.ui_login import Ui_LoginWindow
from screens.ui_splash_screen import Ui_SplashScreen
# from widgets.circular_progress.circular_progress import CircularProgress

# import images screen login
import resources_rc

# para que se pueda importar correctamente icono app en barra tareas
import ctypes
import platform
from config.default.tests.Keithley_4200.instrcomms import Communications

if platform.system() == "Windows":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
# datetime
from datetime import datetime
# PyVISA 1.11.3
# https://pyvisa.readthedocs.io/en/latest/
import pyvisa
import importlib
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import norm
# correlation imports
from scipy.stats import pearsonr, spearmanr, kendalltau, chisquare, chi2_contingency, linregress
from numpy.random import randn
from numpy.random import seed

# import matplotlib histograms
# from matplotlib.backends.qt_compat import QtWidgets
# from matplotlib.backends.backend_qtagg import (
#     FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from PySide6 import QtWidgets
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import mplcursors
# style for matplotlib
import matplotlib as mpl
from qbstyles import mpl_style

from config.functions import *
from config.default.devices import *  # instruments & probers configuration address

from config.default.instruments import *
from config.default.probers import *
from config.default.reports import *

import pyqtgraph as pg

# options qtgraph
QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
# QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
# QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

from functools import partial
import traceback

class NavigationToolbarMod(NavigationToolbar):
    # only display the buttons we need

    def __init__(self, figure_canvas, MainWindow, where):
        NavigationToolbar.__init__(self, figure_canvas, parent=None)
        self.where = where
        self.MainWindowClass = MainWindow

    NavigationToolbar.toolitems = (
        ('Home', 'Reset original view', 'home', 'home'),
        ('Back', 'Back to previous view', 'back', 'back'),
        ('Forward', 'Forward to next view', 'forward', 'forward'),
        (None, None, None, None),
        ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
        ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
        ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
        (None, None, None, None),
        (None, None, None, None),
        # ('Save', 'Save the figure', 'filesave', 'save_graph'), # save_figure modification
    )

class ScriptRunner(QThread):
    finished = Signal()
    error = Signal(str)
    plot_ready = Signal(dict)
    request_message_box = Signal(str, str, str)  # title, message, buttons

    def __init__(self, filepath, main_context):
        super().__init__()
        self.filepath = filepath
        self.main_context = main_context  # `self` del programa principal
        self.message_box_result = None  # Para almacenar el resultado

    def run(self):
        try:
            with open(self.filepath, "r") as rnf:
                content = rnf.read()
                context = globals().copy()
                context["main"] = self.main_context
                context["emit_plot"] = self.plot_ready.emit
                exec(content, context)
                # print(">> [ScriptRunner.run] Script executed")
        except Exception as ex:
            import traceback
            error_msg = (
                f"Error ejecutando {self.filepath}:\n{type(ex)}\n{ex}\n{traceback.format_exc()}"
            )
            # print(">> [ScriptRunner.run] Error caught")
            self.error.emit(error_msg)
        finally:
            # print(">> [ScriptRunner.run] Emitting finished")
            self.finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        global username
        self.script_running = False
        self.script_signals_connected = False
        widgets.chkViewGraph.setChecked(True)

        if username == "":
            username = "default"
        self.username = username
        # ---------------------------
        # logging 
        # ---------------------------
        logfile = './log/app.log'
        handler = RotatingFileHandler(
            logfile,
            mode='a',
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding='UTF-8'
        )

        logging.basicConfig(
            format='%(asctime)s|%(levelname)s|%(process)s|%(funcName)s|%(lineno)d|%(message)s',
            level=logging.INFO,
            datefmt='%y-%m-%d %H:%M:%S',
            handlers=[
                handler
            ]
        )
        self.log = logging.getLogger()
        # ---------------------------
        # LOAD configuration TOML
        # ---------------------------
        self.path_config_file = os.path.join(os.getcwd(), 'config', 'config.toml')
        # self.load_config()
        # Load config file
        cfg = Config(self.path_config_file)
        self.config = cfg.getConfig()
        print(">> [MainWindow.__init__] Config loaded from %s" % self.path_config_file)
        print(f">> [MainWindow.__init__] Config: {self.config}")
        if cfg.error:
            messageBox(self, "Error loading CONFIG", cfg.error_message, "error")
            self.log.error("Error loading CONFIG: %s" % cfg.error_message)
            QApplication.exit()
        # ---------------------------

        self.threadpool = QThreadPool()
        logging.info("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.prober = ""
        self.name_prober = ""
        self.waferwindow = ""
        self.parameterwindow = None
        # process control variables
        global measurement_status, test_status, contact_status
        global contact_test, contact_errors, actual_height  # control progressive contact

        measurement_status = MeasurementStatus()
        test_status = TestStatus()
        contact_status = ContactStatus()
        contact_test = -1
        contact_errors = 0
        actual_height = 0
        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "CARACTERIZAR - Sofware Instrument Control"
        description = "CARACTERIZAR - Software Instrument Control for Lab Users"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # LEFT MENUS
        widgets.btn_page_home.clicked.connect(self.buttonClick)
        widgets.btn_page_measurements.clicked.connect(self.buttonClick)
        widgets.btn_page_instruments.clicked.connect(self.buttonClick)
        widgets.btn_page_probers.clicked.connect(self.buttonClick)
        widgets.btn_page_estepa.clicked.connect(self.buttonClick)
        widgets.btn_page_consult.clicked.connect(self.buttonClick)
        widgets.btn_page_inbase.clicked.connect(self.buttonClick)
        widgets.btn_page_reports.clicked.connect(self.buttonClick)

        # PAGE MEASUREMENTS
        widgets.btnStart.clicked.connect(self.MeasurementClick)
        widgets.btnPause.clicked.connect(self.MeasurementClick)
        widgets.btnStop.clicked.connect(self.MeasurementClick)
        widgets.cmbInstruments.currentIndexChanged.connect(self.load_tests)
        widgets.cmbTests.currentIndexChanged.connect(self.get_test)
        widgets.cmbWafermaps.currentIndexChanged.connect(self.get_wafermap)
        widgets.btnSaveDescription.clicked.connect(self.save_process_description)
        widgets.btnClearDescription.clicked.connect(self.clear_process_description)
        widgets.btnViewWafermap.clicked.connect(partial(self.view_wafermap, enable=True))
        widgets.btnGoHome.clicked.connect(self.go_home)
        widgets.btnParameters.clicked.connect(self.parameters_config)


        # LOAD FROM FILES
        widgets.btnLoadFiles.clicked.connect(self.load_from_files)
        widgets.btnAnalyzeFiles.clicked.connect(self.analyze_files)
        widgets.btnCorrelationFiles.clicked.connect(self.correlation_files)

        # LOAD FROM BBDD
        widgets.optLoadFiles.clicked.connect(self.viewOptionsEstepa)
        widgets.optLoadBBDD.clicked.connect(self.viewOptionsEstepa)
        widgets.cmbTechnology.currentIndexChanged.connect(self.load_cmbRuns)
        widgets.cmbRuns.currentIndexChanged.connect(self.load_cmbWafers)
        widgets.cmbWafers.currentIndexChanged.connect(self.load_cmbParametersBBDD)
        widgets.cmbParametersFile.editTextChanged.connect(self.update_cmbParametersFile)
        widgets.cmbParametersBBDD.editTextChanged.connect(self.update_cmbParametersBBDD)
        widgets.btnAnalyzeBBDD.clicked.connect(self.analyze_BBDD)
        widgets.btnCorrelationBBDD.clicked.connect(self.correlation_files)



        # Buttons save & clear results
        widgets.btnSaveDataValues.clicked.connect(self.saveResults)
        widgets.btnClearDataValues.clicked.connect(lambda: widgets.txtDataValues.setPlainText(""))
        widgets.btnSaveParametersResult.clicked.connect(self.saveResults)
        widgets.btnClearParametersResult.clicked.connect(lambda: widgets.txtParametersResult.setPlainText(""))
        widgets.btnSaveWafermap.clicked.connect(self.saveResults)
        widgets.btnClearWafermap.clicked.connect(self.clearWafermap)
        widgets.btnSaveHistogram.clicked.connect(self.saveResults)
        widgets.btnClearHistogram.clicked.connect(self.clearHistogram)
        widgets.btnSaveGraph.clicked.connect(self.saveResults)
        widgets.btnClearGraph.clicked.connect(self.clearGraph)
        # widgets.btnSaveWafermap.clicked.connect(self.saveResults)

        widgets.btnNextParamFiles.clicked.connect(self.nextParamFiles)
        widgets.btnNextParamFiles.setVisible(False)
        widgets.btnPreviousParamFiles.clicked.connect(self.nextParamFiles)
        widgets.btnPreviousParamFiles.setVisible(False)
        widgets.txtParamSelectedFiles.setVisible(False)
        widgets.btnNextParamBBDD.clicked.connect(self.nextParamBBDD)
        widgets.btnNextParamBBDD.setVisible(False)
        widgets.btnPreviousParamBBDD.clicked.connect(self.nextParamBBDD)
        widgets.btnPreviousParamBBDD.setVisible(False)
        widgets.txtParamSelectedBBDD.setVisible(False)
        widgets.btnSaveWafermap.setVisible(False)
        widgets.btnClearWafermap.setVisible(False)
        widgets.btnSaveHistogram.setVisible(False)
        widgets.btnClearHistogram.setVisible(False)
        widgets.btnSaveGraph.setVisible(False)
        widgets.btnClearGraph.setVisible(False)

        # configuration estepa
        widgets.scrollHistogramChunks.valueChanged.connect(
            lambda: widgets.txtHistogramChunks.setText(str(widgets.scrollHistogramChunks.value())))
        widgets.txtHistogramChunks.textChanged.connect(self.save_config_estepa_file)
        # get values from toml config & set widgets
        self.methods = ["none", "f-spread", "k-sigma"]
        widgets.cmbOutlinerMethod.setCurrentIndex(self.methods.index(self.config["estepa"]["method"]))
        widgets.chkNonAutomaticLimits.setChecked(self.config["estepa"]["lna"])
        if self.config["estepa"]["lna"]:
            widgets.optionsNonAutomatic.setCurrentWidget(widgets.config_nonAutomatic)
        else:
            widgets.optionsNonAutomatic.setCurrentWidget(widgets.config_Automatic)

        widgets.chkGetAutoLimits.setChecked(self.config["estepa"]["autolimits"])

        widgets.txtLimitMin.setText(str(self.config["estepa"]["limmin"]))
        widgets.txtLimitMax.setText(str(self.config["estepa"]["limmax"]))

        # configuration labels for version and credits
        widgets.version.setText(f"v{self.config['version']}")
        widgets.creditsLabel.setText(f"Developed by {self.config['author']}")


        widgets.cmbOutlinerMethod.currentIndexChanged.connect(self.save_config_estepa_file)
        widgets.chkNonAutomaticLimits.stateChanged.connect(self.save_config_estepa_file)
        widgets.txtLimitMin.textChanged.connect(self.save_config_estepa_file)
        widgets.txtLimitMax.textChanged.connect(self.save_config_estepa_file)
        widgets.chkGetAutoLimits.stateChanged.connect(self.save_config_estepa_file)

        widgets.cmbTechnologyUpload.currentIndexChanged.connect(self.updateTextTechnologyUpload)
        widgets.cmbMaskUpload.currentIndexChanged.connect(self.updateTextMaskUpload)
        widgets.txtDateUpload.setText(datetime.today().strftime('%Y-%m-%d'))
        widgets.btnUploadFiles.clicked.connect(self.UploadFiles)
        widgets.btnClearImportReport.clicked.connect(lambda: widgets.txtImportReport.setPlainText(""))
        widgets.btnSaveImportReport.clicked.connect(self.save_import_report)

        widgets.txtReportTitle.textEdited.connect(self.save_config_report_file)
        widgets.txtReportSubtitle.textEdited.connect(self.save_config_report_file)
        widgets.txtReportDate.textEdited.connect(self.save_config_report_file)
        widgets.txtReportAuthor.textEdited.connect(self.save_config_report_file)

        widgets.btnOpenDataFile.clicked.connect(self.open_file_dat)
        widgets.btnOpenWafermapFile.clicked.connect(self.open_file_ppg)

        # PAGE INBASE
        widgets.btnOpenDataFileInbase.clicked.connect(self.open_file_dat)
        widgets.btnOpenWafermapFileInbase.clicked.connect(self.open_file_ppg)

        # PAGE CONSULT
        widgets.optionsHistorical.setCurrentWidget(widgets.NoHistorical)
        widgets.optValues.setChecked(True)
        widgets.chkHistorical.stateChanged.connect(self.optionsHistorical)
        widgets.cmbTechnologyConsult.currentIndexChanged.connect(self.load_cmbRunsConsult)
        widgets.cmbRunsConsult.currentIndexChanged.connect(self.load_cmbWafersConsult)
        widgets.cmbWafersConsult.editTextChanged.connect(self.load_cmbParametersConsult)
        widgets.cmbParametersConsult.editTextChanged.connect(self.load_controlsConsult)
        widgets.btnAddWafers.clicked.connect(self.add_wafers_to_ListBox)
        widgets.lbWafers.itemDoubleClicked.connect(self.remove_item_ListBox)
        widgets.lbWafers.clear()
        widgets.btnConsult.clicked.connect(self.consult)
        widgets.btnClearDiagram.clicked.connect(self.clearDiagram)
        widgets.btnClearDiagram.setVisible(False)
        widgets.btnSaveDiagram.setVisible(False)
        widgets.lblLoadingConsult.setVisible(False)
        widgets.btnPreviousParamConsult.clicked.connect(self.nextParamConsult)
        widgets.btnNextParamConsult.clicked.connect(self.nextParamConsult)
        self.load_controlsConsult()
        widgets.btnClearDataValuesConsult.clicked.connect(lambda: widgets.txtDataValuesConsult.setPlainText(""))
        widgets.btnSaveHistorical.clicked.connect(self.saveResults)
        widgets.btnUploadHistorical.clicked.connect(self.uploadHistorical)
        widgets.btnSaveDiagram.clicked.connect(self.saveResults)

        # PAGE REPORT
        widgets.btnReport.clicked.connect(self.create_report_file)
        widgets.btnParametersReport.clicked.connect(self.parameters_report_config)

        # configuration pages (at beggining, measurements)
        widgets.stackedWidget_configuration.setCurrentWidget(widgets.configuration_measurements)
        widgets.chkDarkMode.stateChanged.connect(self.IsDarkMode)
        mpl_style(dark=self.IsDarkMode())
        widgets.chkDebugMode.stateChanged.connect(self.IsDebugMode)

        # TRICK
        widgets.btn_message.clicked.connect(self.test_status_reset)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)

        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)

        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # CONFIGURE progressBar to show decimals
        widgets.progressBar.setMaximum(100 * 100)
        widgets.progressBar.setValue(0)
        widgets.progressBar.setFormat('%.02f %%' % 0)
        widgets.progressBar.setAlignment(Qt.AlignCenter)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()
        # self.loading_drivers(username)

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\py_dracula_dark.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_page_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_page_home.styleSheet()))

        self.estepa = None
        if self.config["mecao"]["loadStart"]:
            self.estepa = Estepa(self.config["mecao"])
            if not self.estepa.error:
                self.load_cmbTechnology()
                self.load_cmbMask()
            else:
                messageBox(self, "Error loading ESTEPA class", self.estepa.error_message, "error")
        widgets.cmbParametersFile.clear()
        widgets.cmbParametersBBDD.clear()

        # load instruments, probers and waferwaps
        self.load_instruments()
        self.load_probers()
        self.load_wafermaps()
        self.load_reports()


        # set default variables
        widgets.chkDebugMode.setChecked(self.config["defaults"]["debugmode"])
        widgets.chkDarkMode.setChecked(self.config["defaults"]["darkmode"])
        widgets.chkViewEstepa.setChecked(self.config["defaults"]["estepa"])
        widgets.txtProcess.setText(self.config["defaults"]["txtprocess"])
        widgets.txtLot.setText(self.config["defaults"]["txtlot"])
        widgets.txtWafer.setText(self.config["defaults"]["txtwafer"])
        widgets.txtMask.setText(self.config["defaults"]["txtmask"])
        widgets.txtTemperature.setText(self.config["defaults"]["txttemperature"])
        widgets.txtHumidity.setText(self.config["defaults"]["txthumidity"])

        # text configuration
        widgets.txtProcess.textChanged.connect(self.save_config_parameters_file)
        widgets.txtLot.textChanged.connect(self.save_config_parameters_file)
        widgets.txtWafer.textChanged.connect(self.save_config_parameters_file)
        widgets.txtMask.textChanged.connect(self.save_config_parameters_file)
        widgets.txtTemperature.textChanged.connect(self.save_config_parameters_file)
        widgets.txtHumidity.textChanged.connect(self.save_config_parameters_file)


        widgets.txtReportTitle.setText(self.config["reports"]["title"])
        widgets.txtReportSubtitle.setText(self.config["reports"]["subtitle"])
        widgets.txtReportDate.setText(self.config["reports"]["date"])
        widgets.txtReportAuthor.setText(self.config["reports"]["author"])
        # habilite or disable estepa
        widgets.btn_page_estepa.setVisible(self.config["defaults"]["estepa"])
        widgets.btn_page_inbase.setVisible(self.config["defaults"]["estepa"])
        widgets.btn_page_consult.setVisible(self.config["defaults"]["estepa"])

        # set default values
        widgets.chkCartoMeas.setChecked(False)
        widgets.chkCartoMeas.stateChanged.connect(self.changeCartoMeas)
        widgets.cmbProbers.setVisible(False)
        widgets.cmbWafermaps.setVisible(False)
        widgets.btnViewWafermap.setVisible(False)
        widgets.btnGoHome.setVisible(False)

        widgets.chkViewEstepa.clicked.connect(self.clickViewEstepa)

    # CONFIG FILE FUNCTIONS (toml)
    def save_config_report_file(self):
        # change text fields
        self.config["reports"]["title"] = widgets.txtReportTitle.text()
        self.config["reports"]["subtitle"] = widgets.txtReportSubtitle.text()
        self.config["reports"]["date"] = widgets.txtReportDate.text()
        self.config["reports"]["author"] = widgets.txtReportAuthor.text()
        print(self.config["reports"])
        toml_file = open(self.path_config_file, "w", encoding="utf-8")
        toml.dump(self.config, toml_file)
        toml_file.close()

    def save_config_parameters_file(self):
        # change text fields
        self.config["defaults"]["debugmode"] = widgets.chkDebugMode.isChecked()
        self.config["defaults"]["darkmode"] = widgets.chkDarkMode.isChecked()
        self.config["defaults"]["txtprocess"] = widgets.txtProcess.text()
        self.config["defaults"]["txtlot"] = widgets.txtLot.text()
        self.config["defaults"]["txtwafer"] = widgets.txtWafer.text()
        self.config["defaults"]["txtmask"] = widgets.txtMask.text()
        self.config["defaults"]["txttemperature"] = widgets.txtTemperature.text()
        self.config["defaults"]["txthumidity"] = widgets.txtHumidity.text()
        print(self.config)
        print(">> [MainWindow.save_config_parameters_file] Saving config parameters to %s" % self.path_config_file)
        toml_file = open(self.path_config_file, "w", encoding="utf-8")
        toml.dump(self.config, toml_file)
        toml_file.close()

    # ----------------
    # GRAPH FUNCTIONS
    # ----------------
    def show_graph(self, plot_parameters):
        global widgets
        self.clearGraph()
        QApplication.processEvents()
        layout = widgets.horizontalLayout_graph
        layout_buttons = widgets.horizontalLayout_btnGraph

        # create a FigureCanvas & add to layout
        static_canvas = FigureCanvas(Figure())

        static_canvas_buttons = FigureCanvas(Figure())
        static_canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        static_canvas.updateGeometry()

        toolbar = NavigationToolbarMod(static_canvas, self, "graph")

        layout_buttons.addWidget(toolbar)
        layout.addWidget(static_canvas)
        # check first minimal plot_parameters
        if "x" in plot_parameters and "y1" in plot_parameters:
            _static_ax = static_canvas.figure.subplots()
            # set grid
            if "showgrid" in plot_parameters:
                if "x" in plot_parameters["showgrid"] and plot_parameters["showgrid"]["x"]:
                    _static_ax.xaxis.grid(plot_parameters["showgrid"]["x"], color='gray')
                if "y" in plot_parameters["showgrid"] and plot_parameters["showgrid"]["y"]:
                    _static_ax.yaxis.grid(plot_parameters["showgrid"]["y"], color='gray')
                # _static_ax.grid(True, color='gray')

            if "y2" in plot_parameters:
                _static_ax2 = _static_ax.twinx()

            # set titles
            left_title = ""
            right_title = ""
            bottom_title = ""
            if "titles" in plot_parameters:
                if "title" in plot_parameters["titles"]:
                    _static_ax.set_title(plot_parameters["titles"]["title"])
                if "left" in plot_parameters["titles"]:
                    left_title = plot_parameters["titles"]["left"]
                    if "units" in plot_parameters and "left" in plot_parameters["units"]:
                        left_title += r" (" + plot_parameters["units"]["left"] + ")"
                    _static_ax.set_ylabel(left_title)

                if "bottom" in plot_parameters["titles"]:
                    bottom_title = plot_parameters["titles"]["bottom"]
                    if "units" in plot_parameters and "bottom" in plot_parameters["units"]:
                        bottom_title += r" (" + plot_parameters["units"]["bottom"] + ")"
                    _static_ax.set_xlabel(bottom_title)

                if "right" in plot_parameters["titles"]:
                    right_title = plot_parameters["titles"]["right"]
                    if "units" in plot_parameters and "right" in plot_parameters["units"]:
                        right_title += r" (" + plot_parameters["units"]["right"] + ")"
                    _static_ax2.set_ylabel(right_title)

            # graphs
            if "y2" in plot_parameters:
                _static_ax2.plot(plot_parameters["x"], plot_parameters["y2"], color='blue', label=right_title)
            _static_ax.plot(plot_parameters["x"], plot_parameters["y1"], color='green', label=left_title)

            # legends
            if "legend" in plot_parameters and plot_parameters["legend"]:
                #  static_canvas.figure.legend(loc="upper right")
                static_canvas.figure.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=_static_ax.transAxes)

            widgets.btnSaveGraph.setVisible(True)
            widgets.btnClearGraph.setVisible(True)

    # ----------------
    # ESTEPA FUNCTIONS
    # ----------------

    def clickViewEstepa(self):
        if widgets.chkViewEstepa.isChecked():
            messageBox(self, "Change view estepa not available", "Contact with administrator to change this option", "info")
            widgets.chkViewEstepa.setChecked(False)

    def load_from_files(self):
        file_dat = widgets.txtDataFile.text()
        file_ppg = widgets.txtWafermapFile.text()
        file_result = ResultFile(file_dat)
        file_wafermap = WafermapFile(file_ppg)
        parameters_list = file_result.params_list
        parameters_list.insert(0, "All parameters")
        widgets.cmbParametersFile.addItems(parameters_list)
        if len(parameters_list) > 1:
            widgets.cmbParametersFile.showPopup()

    def print_histogram(self, data, parameters_list, param_selected):

        mu, std = norm.fit(data)
        layout, layout_buttons = self.clearHistogram()

        if len(data) > 0:
            # create a FigureCanvas & add to layout

            _static_ax = self.create_static_ax(layout, layout_buttons, "histogram")
            _static_ax.grid(True, color='gray')

            # Plot the histogram.
            num_chunks = int(widgets.txtHistogramChunks.text())
            _static_ax.hist(data, bins=num_chunks, density=True, histtype='step', alpha=1, color='#ff79c6')
            # Plot the PDF.
            xmin, xmax = min(data), max(data)
            x = np.linspace(xmin, xmax, 100)
            p = norm.pdf(x, mu, std)

            _static_ax.plot(x, p, 'k', linewidth=2)
            # Put title in histogram
            title = parameters_list[param_selected]
            _static_ax.set_title(title)

            widgets.btnSaveHistogram.setVisible(True)
            widgets.btnClearHistogram.setVisible(True)

    def create_static_ax(self, layout, layout_buttons, name):
        # create a FigureCanvas & add to layout
        static_canvas = FigureCanvas(Figure())

        static_canvas_buttons = FigureCanvas(Figure())
        static_canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        static_canvas.updateGeometry()

        toolbar = NavigationToolbarMod(static_canvas, self, name)

        layout_buttons.addWidget(toolbar)
        layout.addWidget(static_canvas)
        _static_ax = static_canvas.figure.subplots()

        return _static_ax

    def print_correlation(self, data1, data2, param1_name, param2_name):
        # Delete all widgets in layout

        self.clearWafermap()
        layout, layout_buttons = self.clearHistogram()

        _static_ax = self.create_static_ax(layout, layout_buttons, "correlation")
        _static_ax.grid(True, color='gray')
        _static_ax.scatter(data1, data2)

        # linear regression
        m, b = np.polyfit(data1, data2, 1)
        data22 = [float(x) * m + b for x in data1]
        _static_ax.plot(data1, data22, color='green')

        _static_ax.set_title(param1_name + " vs " + param2_name)

        widgets.btnSaveHistogram.setVisible(True)
        widgets.btnClearHistogram.setVisible(True)

    def show_analysis(self, data, data_values, parameters_list, param_selected=0):
        # check if btn Analysis is File or BBDD (btnAnalyzeFiles or btnAnalyzeBBDD)
        widgets.tabGraphs.setTabText(1, "Histogram")
        QApplication.processEvents()
        # 1) print data values in widget Plain text 
        widgets.txtDataValues.setPlainText("X\tY\tMeasurement")
        for chip in data_values:
            widgets.txtDataValues.setPlainText(
                widgets.txtDataValues.toPlainText() + "\n" + "\t".join(str(chip).split(" ")) + "\t" + str(
                    data_values[chip]))

        # 2) print histogram
        self.print_histogram(data, parameters_list, param_selected)

        # 3) print wafermap
        param = parameters_list[param_selected]
        self.print_wafermap(data_values, param)

    def print_wafermap(self, data_values, param):
        self.clearWafermap()
        layout = widgets.horizontalLayout_wafermap
        layout_buttons = widgets.horizontalLayout_btnWafermap

        def selection(sel):
            x = round(sel.target[0]) * -1
            y = round(sel.target[1]) * -1
            coord = str(x) + " " + str(y)
            if coord in data_values_real:
                if data_values_real[coord] == error_value:
                    text_insert = '{} [{} {}] = {}'.format(title, x, y, " ERROR value")
                else:
                    text_insert = '{} [{} {}] = {}'.format(title, x, y, '%.2f' % data_values_real[coord])
                sel.annotation.set_text(text_insert)
                sel.annotation.get_bbox_patch().set(fc=color_out, alpha=0.8)

                # ax.annotate(text_insert, xy=(x,y),bbox=dict(boxstyle="square", fc="w"))
            else:
                sel.annotation.set_text('')

        btn = self.sender()
        btnName = btn.objectName()
        if btnName == "btnAnalyzeFiles" or btnName == "btnNextParamFiles" or btnName == "btnPreviousParamFiles":
            fileName = widgets.txtWafermapFile.text()
            file_wafermap = WafermapFile(fileName)
            wafer = Wafer(file_wafermap.wafer_parameters)
        else:
            # BBDD
            wafer = widgets.cmbWafers.currentText()
            wafer_parameters = self.estepa.get_wafer_parameters(widgets.cmbWafers.currentText())
            print(wafer_parameters)
            wafer = Wafer(wafer_parameters)

        if not wafer.wafer_error:
            # get real xmax & ymax
            xmax_real = wafer.wafer_size_mm * 1000 / (wafer.xsize)
            ymax_real = wafer.wafer_size_mm * 1000 / (wafer.ysize)
            # Prepare 3 lists: X, Y, Values real
            data_values_real = dict()
            data_values_min = 1E99
            data_values_max = -1E99
            error_value = 1E30
            errors_found = False
            outliers_found = False
            X = [*range(0, int(xmax_real) * -1, -1)]
            Y = [*range(0, int(ymax_real) * -1, -1)]
            # get min & max values in data values
            for k, v in data_values.items():
                new_coord = wafer.calculate_real_coordinate(k)
                data_values_real[new_coord] = v
                if (v > data_values_max and v < error_value): data_values_max = v
                if (v < data_values_min): data_values_min = v
                if (v == error_value): errors_found = True
            # fill values, assign value_in & value_out & value_errors & value_outliers
            values = list()
            num_colors = 15

            data_list_without_outliers = list()
            list_data_values = list(data_values.values())
            if len(list_data_values) > 2:
                statistics_estepa = StatisticsEstepa(param, list_data_values, self.config["estepa"])
                data_list_without_outliers = statistics_estepa.data_list
            if len(data_list_without_outliers) > 0:
                if len(list(data_values.values())) != len(data_list_without_outliers):
                    outliers_found = True
                    # redifinir valors
                    data_values_max = max(data_list_without_outliers)
                    data_values_min = min(data_list_without_outliers)

                dif = data_values_max - data_values_min
                value_in = data_values_min - (dif * 10 / 100)  # in
                value_out = data_values_min - (dif * 20 / 100)  # out

                value_outliers = data_values_max + (dif * 10 / 100)
                value_errors = data_values_max + (dif * 20 / 100)

                for y_axis in Y:
                    y_axis_list = list()
                    for x_axis in X:
                        coord = str(x_axis) + " " + str(y_axis)
                        if coord not in data_values_real:
                            if wafer.is_in(x_axis, y_axis):
                                value_add = value_in
                            else:
                                value_add = value_out
                        else:
                            if data_values_real[coord] == error_value:
                                value_add = value_errors
                            elif data_values_real[coord] not in data_list_without_outliers:
                                value_add = value_outliers
                            else:
                                value_add = data_values_real[coord]

                        y_axis_list.append(value_add)
                    values.append(y_axis_list)

                # set colors
                background_options = ["white", "black", "mpl_style"]
                if self.IsDarkMode():
                    background = "black"
                else:
                    background = "white"

                if background == "white":
                    color_out = background
                if background == "black":
                    color_out = "#0C1C23"
                    plt.style.use('dark_background')
                    mpl.rcParams["figure.facecolor"] = "#0C1C23"
                    mpl.rcParams["axes.facecolor"] = "#0C1C23"
                    mpl.rcParams["savefig.facecolor"] = "#0C1C23"
                if background == "mpl_style":
                    color_out = "#0C1C23"
                    mpl_style(True)

                color_in = '#FFFDD0'
                color_outliers = 'Blue'
                color_error = 'Red'
                cmap_reds = plt.get_cmap('Greens')
                colors = [color_out, color_in] + [cmap_reds(i / num_colors) for i in range(2, num_colors)]
                if outliers_found: colors = colors + [color_outliers]
                if errors_found: colors = colors + [color_error]

                cmap = LinearSegmentedColormap.from_list('', colors, num_colors)

                # create a FigureCanvas & add to layout
                static_canvas = FigureCanvas(Figure())

                static_canvas_buttons = FigureCanvas(Figure())
                static_canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                static_canvas.updateGeometry()

                toolbar = NavigationToolbarMod(static_canvas, self, "wafermap")

                layout_buttons.addWidget(toolbar)
                fig = static_canvas.figure
                ax = static_canvas.figure.subplots()
                # construct figure, axis
                # fig, ax = plt.subplots()
                im = ax.imshow(np.array(values), interpolation='nearest', aspect='auto', cmap=cmap)

                # add space for colour bar
                fig.subplots_adjust(right=0.85)
                cbar_ax = fig.add_axes([0.88, 0.15, 0.04, 0.7])
                cbar_ax.grid(False)  # warning  message in console

                # get ticks: value_0 + value_ 1 + 12 colors from data_values_min to data_values_max + ERROR
                dif_value = data_values_min + (dif / 2)
                ticks = [value_out, value_in, data_values_min, dif_value, data_values_max]
                yticks_list = ["OUT", "IN", str('%.2f' % data_values_min), str('%.2f' % dif_value),
                               str('%.2f' % data_values_max)]
                if outliers_found:
                    ticks.append(value_outliers)
                    yticks_list.append("OUTLIER")
                if errors_found:
                    ticks.append(value_errors)
                    yticks_list.append("ERROR")
                cbar = fig.colorbar(im, cax=cbar_ax, ticks=ticks)
                cbar.ax.set_yticklabels(yticks_list)

                # Show all ticks and label them with the respective list entries
                ax.set_xticks(np.arange(len(X)), labels=X)
                ax.set_yticks(np.arange(len(Y)), labels=Y)

                ax.locator_params(axis='y', nbins=6)
                ax.locator_params(axis='x', nbins=10)

                # Rotate the tick labels and set their alignment.
                # plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

                # Loop over data dimensions and create text annotations.
                for i in range(len(Y)):
                    for j in range(len(X)):
                        if wafer.is_home(j, i):
                            text = ax.text(j, i, "H", ha="center", va="center", color="w", fontsize=10)
                            # text = ax.text(j, i, "%.2f" % df.iloc[i, j],ha="center", va="center", color="w", fontsize=8)
                        if wafer.is_origin(j, i):
                            text = ax.text(j, i, "O", ha="center", va="center", color="w", fontsize=10)
                title = param
                ax.set_title(title)

                # set cursors
                crs = mplcursors.cursor(ax, hover=False)
                crs.connect("add", selection)
                # insert in layout
                layout.addWidget(static_canvas)
                static_canvas.draw()

                widgets.btnSaveWafermap.setVisible(True)
                widgets.btnClearWafermap.setVisible(True)

    def nextParamFiles(self):

        btn = self.sender()
        btnName = btn.objectName()

        txt_param_selected = widgets.txtParamSelectedFiles.text()
        parameters_file = widgets.cmbParametersFile.currentText()
        parameters_file_list = parameters_file.split(", ")
        position = parameters_file_list.index(txt_param_selected)
        elements = widgets.cmbParametersFile.itemsChecked()

        if btnName == "btnNextParamFiles":
            if position + 1 < elements:
                next_position = position + 1
            else:
                next_position = 0
        else:
            if position > 0:
                next_position = position - 1
            else:
                next_position = elements - 1

        self.analyze_files(next_position)

    def nextParamConsult(self):

        btn = self.sender()
        btnName = btn.objectName()

        txt_param_selected = widgets.txtParamSelectedConsult.text()
        parameters_file = widgets.cmbParametersConsult.currentText()
        parameters_file_list = parameters_file.split(", ")
        position = parameters_file_list.index(txt_param_selected)
        elements = widgets.cmbParametersConsult.itemsChecked()

        if btnName == "btnNextParamConsult":
            if position + 1 < elements:
                next_position = position + 1
            else:
                next_position = 0
        else:
            if position > 0:
                next_position = position - 1
            else:
                next_position = elements - 1
        self.consult(next_position, False)

    def nextParamBBDD(self):
        btn = self.sender()
        btnName = btn.objectName()

        txt_param_selected = widgets.txtParamSelectedBBDD.text()
        parameters_BBDD = widgets.cmbParametersBBDD.currentText()
        parameters_BBDD_list = parameters_BBDD.split(", ")
        position = parameters_BBDD_list.index(txt_param_selected)
        elements = widgets.cmbParametersBBDD.itemsChecked()

        if btnName == "btnNextParamBBDD":
            if position + 1 < elements:
                next_position = position + 1
            else:
                next_position = 0
        else:
            if position > 0:
                next_position = position - 1
            else:
                next_position = elements - 1
        self.analyze_BBDD(next_position)

    def analyze_files(self, param_selected=0):
        parameters_file = widgets.cmbParametersFile.currentText()  # get text of combo Parameters
        parameters_file_list = parameters_file.split(", ")  # split to create list

        # self.view_paramFile() # show/hide buttons next & previous and text param selected
        widgets.txtParamSelectedFiles.setText(parameters_file_list[param_selected])

        FileName = widgets.txtDataFile.text()
        result_file = ResultFile(FileName)
        if not result_file.error:
            if parameters_file != "":
                # GET parameters result
                measurements = result_file.get_params(parameters_file_list)
                widgets.txtParametersResult.setPlainText("")
                for parameter in parameters_file_list:
                    estadistica = StatisticsEstepa(parameter, measurements[parameter]["medida"],
                                                   (self.config["estepa"]))
                    widgets.txtParametersResult.setPlainText(
                        widgets.txtParametersResult.toPlainText() + "\n" + estadistica.print_statistics())
                # GET DATA VALUES, HISTOGRAM & WAFERMAP IF PARAM==1
                # Get data values from result_file
                data_values = result_file.get_data_values(parameters_file_list[param_selected])
                # Put info in data values, histogram & wafermap
                parameter = parameters_file_list[param_selected]
                self.show_analysis(measurements[parameter]["medida"], data_values, parameters_file_list, param_selected)

            else:
                retval = messageBox(self, "Error getting parameters list", "Please, select at least one parameter!",
                                    "warning")

        else:
            retval = messageBox(self, "Error getting Result File", result_file.error_message, "warning")

    def correlation_files(self):
        error = False
        if widgets.optLoadFiles.isChecked():
            txt_param_selected = widgets.txtParamSelectedFiles.text()
            parameters = widgets.cmbParametersFile.currentText()
            parameters_list = parameters.split(", ")
            FileName = widgets.txtDataFile.text()
            result_file = ResultFile(FileName)
            if not result_file.error:
                if len(parameters_list) == 2:
                    measurements = result_file.get_params(parameters_list)
                    data1 = measurements[parameters_list[0]]["medida"]
                    data2 = measurements[parameters_list[1]]["medida"]
                else:
                    error = True
                    retval = messageBox(self, "Error selecting variables", "Select 2 parameters for correlation",
                                        "warning")
            else:
                error = True
                retval = messageBox(self, "Error getting Result File", result_file.error_message, "warning")
        else:
            txt_param_selected = widgets.txtParamSelectedBBDD.text()
            parameters = widgets.cmbParametersBBDD.currentText()
            parameters_list = parameters.split(", ")
            wafer = widgets.cmbWafers.currentText()
            measurements = self.estepa.get_medidas(wafer, parameters_list)
            if not self.estepa.error:
                if len(parameters_list) == 2:
                    # get data1 & data2
                    data1 = measurements[parameters_list[0]]["medida"]
                    data2 = measurements[parameters_list[1]]["medida"]
                else:
                    error = True
                    retval = messageBox(self, "Error selecting variables", "Select 2 parameters for correlation",
                                        "warning")
            else:
                error = True
                retval = messageBox(self, "Error getting measurements Estepa", self.estepa.error_message, "warning")

        if not error:
            statistics_correlation = StatisticsEstepa(parameters_list[0], data1, self.config["estepa"], data2)
            data1 = statistics_correlation.data_list
            data2 = statistics_correlation.data_list2
            statistics_correlation = StatisticsEstepa(parameters_list[1], data2, self.config["estepa"], data1)
            data2 = statistics_correlation.data_list
            data1 = statistics_correlation.data_list2
            widgets.tabGraphs.setTabText(1, "Correlation")
            widgets.tabGraphs.setCurrentIndex(1)
            widgets.tabCalcs.setCurrentIndex(1)
            QApplication.processEvents()
            # calculate Pearson's correlation
            corr, pvalue = pearsonr(data1, data2)  # Pearson's r, valor p
            corr2, pvalue2 = spearmanr(data1, data2)  # Spearman's rho, valor p
            corr3, pvalue3 = kendalltau(data1, data2)  # Kendall's tau, valor p
            salto_linea = "<br />"
            texto = "<strong>Correlation result (" + parameters_list[0] + "-" + parameters_list[
                1] + ")</strong>" + salto_linea
            texto += '- Pearsons correlation: %.3f , %.3f' % (corr, pvalue) + salto_linea
            texto += '- Spearmanr correlation: %.3f , %.3f' % (corr2, pvalue2) + salto_linea
            texto += '- Kendalltau correlation: %.3f , %.3f' % (corr3, pvalue3) + salto_linea
            kf_data = np.array([data1, data2])
            kf = chi2_contingency(kf_data)
            # print('chisq-statistic=%.4f, p-value=%.4f, df=%i expected_frep=%s'%kf)
            texto += '- Chi-square values: %.3f, %.3f, %.3f' % (kf[0], kf[1], kf[2]) + salto_linea + salto_linea
            kf_data2 = np.array([[data1, data2]]).T
            kf = chisquare(kf_data2)
            print(kf)
            # texto += '- Chi-square values: %.3f, %.3f' % (kf[0], kf[1]) + salto_linea + salto_linea
            # linregress
            result = linregress(data1, data2)
            texto += f"Intercept (a): {result.intercept:.3f}" + salto_linea
            texto += f"Slope (b): {result.slope:.3f}" + salto_linea
            texto += f"Standard error of the estimated intercept (siga): {result.intercept_stderr:.3f}" + salto_linea
            texto += f"Standard error of the estimated slope (sigb): {result.stderr:.3f}" + salto_linea
            texto += f"The Pearson correlation coefficient: {result.rvalue:.3f}" + salto_linea
            texto += f"p-value: {result.pvalue:.3f}" + salto_linea

            # delete dataValues
            widgets.btnClearDataValues.clicked.emit()
            # delete Parameters Result
            widgets.btnClearParametersResult.clicked.emit()
            # set texto in parameters result
            widgets.txtParametersResult.setPlainText("")
            widgets.txtParametersResult.appendHtml(texto)
            self.print_correlation(data1, data2, parameters_list[0], parameters_list[1])

    def open_file_dat(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Open .dat file", "D:\\GITHUB\\Python\\caracterizar\\proves",
                                                  "Dat Files (*.dat);; All files (*.*)")

        if fileName:
            file_result = ResultFile(fileName)
            if not file_result.error:
                if btnName == "btnOpenDataFileInbase":
                    widgets.txtDataFileInbase.setText(fileName)
                    widgets.txtRunUpload.setText(file_result.lot)
                    widgets.txtWaferUpload.setText(file_result.wafer)
                if btnName == "btnOpenDataFile":
                    widgets.txtDataFile.setText(fileName)

                print(file_result.info())
            else:
                # show error
                retval = messageBox(self, "Error loading DAT File", file_result.error_message, "error")
                if btnName == "btnOpenDataFileInbase":
                    widgets.txtDataFileInbase.setText("")
                if btnName == "btnOpenDataFile":
                    widgets.txtDataFile.setText("")

    def open_file_ppg(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()
        fileName, _ = QFileDialog.getOpenFileName(self,
                                                  "Open wafermap file", "D:\\GITHUB\\Python\\caracterizar\\proves",
                                                  "PPG py Files (*_wafermap.py);; PPG Files (*.ppg);; All files (*.*)")

        if fileName:
            file_wafermap = WafermapFile(fileName)
            if not file_wafermap.error:
                if btnName == "btnOpenWafermapFileInbase":
                    widgets.txtWafermapFileInbase.setText(fileName)
                if btnName == "btnOpenWafermapFile":
                    widgets.txtWafermapFile.setText(fileName)

                print(file_wafermap.info())

            else:
                # show error
                retval = messageBox(self, "Error loading PPG File", file_wafermap.error_message, "error")
                if btnName == "btnOpenDataFileInbase":
                    widgets.txtDataFileInbase.setText("")
                if btnName == "btnOpenDataFile":
                    widgets.txtDataFile.setText("")

    def save_import_report(self):
        global widgets
        texto = widgets.txtImportReport.toPlainText()
        destFile = self.getFiles("import_report")
        with open(destFile, 'w') as f:
            f.write(texto)

    def save_lists_to_txt(self, namefile, var_list, separation=",", headers=[]):
        """
        Save lists vars to txt file
        :param namefile:
        :param var_list: list of vars in order
        :return:
        """
        with open(namefile, 'w') as f:
            # get len of var_list
            number_vars = len(var_list)
            number_samples = len(var_list[0])
            # write to file all vars in order with separation
            for i in range(0, number_samples):
                text_to_print = ""
                for j in range(0, number_vars):
                    if headers and i==0 and j==0:
                        for header in headers:
                            text_to_print += header + separation
                        text_to_print = text_to_print[:-1] + "\n"
                    text_to_print += str(var_list[j][i]) + separation
                # trim last separator
                text_to_print = text_to_print[:-1] + "\n"
                f.write(text_to_print)


    def updateTextImportReport(self, texto, color="NORMAL"):
        global widgets
        date_today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        colors = {"NORMAL": "#FFFFFF", "ERROR": "#FF3300", "WARNING": "orange"}
        if not color in colors:
            color = "NORMAL"
        texto_final = '<span style="color: #ff79c6">' + "[" + date_today + "]</span>" + "<br />" + '<span style="color: ' + \
                      colors[color] + '">' + texto + "</span>"

        widgets.txtImportReport.appendHtml(texto_final)
        QApplication.processEvents()

    def UploadFiles(self):
        try:
            CheckParameteres = True
            txtDataFileInbase = widgets.txtDataFileInbase.text()
            txtWafermapFileInbase = widgets.txtWafermapFileInbase.text()
            # first check all parameters
            if txtDataFileInbase == "" or not os.path.exists(txtDataFileInbase):
                CheckParameteres = False
                self.updateTextImportReport("- File DATA doesn't selected or path not exists!", "WARNING")

            if txtWafermapFileInbase == "" or not os.path.exists(txtWafermapFileInbase):
                CheckParameteres = False
                self.updateTextImportReport("- File WAFERMAP doesn't selected or path not exists!", "WARNING")

            if CheckParameteres:
                # first load files (data file & wafermap)

                while True:
                    # check other parameters
                    txtRunUpload = widgets.txtRunUpload.text().strip()
                    txtWaferUpload = widgets.txtWaferUpload.text().strip()
                    txtDateUpload = widgets.txtDateUpload.text().strip()
                    txtTechnologyUpload = widgets.txtTechnologyUpload.text().strip()
                    txtMaskUpload = widgets.txtMaskUpload.text().strip()
                    txtLocalizationUpload = widgets.txtLocalizationUpload.text().strip()
                    txtCommentUpload = widgets.txtCommentUpload.text().strip()
                    if txtTechnologyUpload == "":
                        self.updateTextImportReport("- Technology not selected!", "WARNING")
                        CheckParameteres = False
                        break
                    if txtMaskUpload == "":
                        self.updateTextImportReport("- Mask not selected!", "WARNING")
                        CheckParameteres = False
                        break

                    if txtRunUpload == "":
                        self.updateTextImportReport("- Run not selected!", "WARNING")
                        CheckParameteres = False
                        break

                    if txtWaferUpload == "":
                        self.updateTextImportReport("- Wafer not selected!", "WARNING")
                        CheckParameteres = False
                        break

                    if txtDateUpload == "":
                        self.updateTextImportReport("- Date not selected!", "WARNING")
                        CheckParameteres = False
                        break
                    else:
                        # check date format
                        formato = "%Y-%m-%d"
                        if not datetime.strptime(txtDateUpload, formato):
                            self.updateTextImportReport("- Date format not correct!", "WARNING")
                            CheckParameteres = False
                            break
                    break

            if CheckParameteres:
                # import data
                dataFile = ResultFile(txtDataFileInbase)
                wafermapFile = WafermapFile(txtWafermapFileInbase)
                if len(dataFile.dies) == int(wafermapFile.wafer_parameters["nchips"]):
                    if dataFile.error:
                        retval = messageBox(self, "Error loading DAT File", dataFile.error_message, "error")
                    elif wafermapFile.error:
                        retval = messageBox(self, "Error loading PPG File", wafermapFile.error_message, "error")
                    else:

                        self.updateTextImportReport("START import process")
                        # get parameters
                        inbase_parameters = {
                            "dataFile": txtDataFileInbase,
                            "wafermapFile": txtWafermapFileInbase,
                            "run": txtRunUpload,
                            "wafer": txtRunUpload + "-" + txtWaferUpload,
                            "date": txtDateUpload,
                            "technology": txtTechnologyUpload,
                            "mask": txtMaskUpload,
                            "localization": txtLocalizationUpload,
                            "comment": txtCommentUpload
                        }
                        # put all info in estepa database
                        putAllInfo = False
                        virtual_wafer = inbase_parameters["wafer"]
                        # first search for measurement of this wafer in database
                        if self.estepa.exists_measurements(inbase_parameters["wafer"]):
                            retval = messageBox(self, "Measurements for this wafer exists",
                                                "Do you want to CREATE new virtual wafer for run " + txtRunUpload + " and wafer " + txtWaferUpload + " ?",
                                                "question")
                            if retval == QMessageBox.Yes:
                                virtual_wafer = self.estepa.get_virtual_wafer(inbase_parameters["wafer"])
                                print("Virtual wafer: " + virtual_wafer)
                                putAllInfo = True
                        else:
                            retval = messageBox(self, "Measurements for this wafer not exists",
                                                "The process INSERTS the results for run " + txtRunUpload + " and wafer " + txtWaferUpload + " automatically!",
                                                "question")
                            if retval == QMessageBox.Yes:
                                putAllInfo = True

                        # put the virtual wafer into inbase parameters
                        inbase_parameters["virtual_wafer"] = virtual_wafer

                        if putAllInfo:

                            # then put measurements in database
                            self.updateTextImportReport("UPLOADING results, please wait...")
                            retVal = self.estepa.inbase(self, inbase_parameters)
                            self.updateTextImportReport("FINISH import process")
                            if retVal[0]:
                                retval = messageBox(self, "Error uploading info to database", retVal[1], "error")
                            else:
                                retval = messageBox(self, "Success upload",
                                                    "Uploaded all information to database successfully!", "info")

                        else:
                            self.updateTextImportReport("Process aborted!")
                else:
                    self.updateTextImportReport("Error in selected files: Different number of chips!", "ERROR")
                    retval = messageBox(self, "Error in selected files", "Different number of chips!", "error")


            else:
                self.updateTextImportReport("Parameters error: Problems checking parameters", "WARNING")
                retval = messageBox(self, "Parameters error", "Problems checking parameters", "warning")

        except Exception as error:
            self.updateTextImportReport("Some error occurs!", "ERROR")

    def updateTextTechnologyUpload(self):
        if widgets.cmbTechnologyUpload.currentIndex() > 0:
            widgets.txtTechnologyUpload.setText(str(widgets.cmbTechnologyUpload.currentText()))

    def updateTextMaskUpload(self):
        if widgets.cmbMaskUpload.currentIndex() > 0:
            widgets.txtMaskUpload.setText(str(widgets.cmbMaskUpload.currentText()))

    def get_rangos(self):
        parametersBBDD_list = widgets.cmbParametersBBDD.currentText().split(",")
        if len(parametersBBDD_list) == 1:
            if widgets.cmbParametersBBDD.currentText() != "All parameters" and widgets.cmbParametersBBDD.currentText() != "":
                # only one parameter selected, search rangos
                rangos = self.estepa.get_rangos(widgets.cmbTechnology.currentText(),
                                                widgets.cmbParametersBBDD.currentText())
                # if rangos is not empty assign to texts
                if len(rangos) == 2:
                    widgets.txtLimitMin.setText(str(rangos[0]))
                    widgets.txtLimitMax.setText(str(rangos[1]))

    def save_config_estepa_file(self):
        # change in chk non automatic limits or cmb otuliers method => save estepa file
        chkNonAutomaticLimits = widgets.chkNonAutomaticLimits.isChecked()
        chkGetAutoLimits = widgets.chkGetAutoLimits.isChecked()
        if chkNonAutomaticLimits:
            widgets.optionsNonAutomatic.setCurrentWidget(widgets.config_nonAutomatic)
            # get rangos
            if chkGetAutoLimits:
                self.get_rangos()
        else:
            widgets.optionsNonAutomatic.setCurrentWidget(widgets.config_Automatic)

        cmbOutlinerMethod = widgets.cmbOutlinerMethod.currentText()
        txtLimitMax = int(widgets.txtLimitMax.text())
        txtLimitMin = int(widgets.txtLimitMin.text())
        txtHistogramChunks = int(widgets.txtHistogramChunks.text())
        try:
            if str(txtLimitMin) != "" and str(txtLimitMax) != "" and isinstance(int(txtLimitMin), int) and isinstance(
                    int(txtLimitMax), int):
                self.config["estepa"]["method"] = cmbOutlinerMethod
                self.config["estepa"]["lna"] = chkNonAutomaticLimits
                self.config["estepa"]["autolimits"] = chkGetAutoLimits
                self.config["estepa"]["limmin"] = txtLimitMin
                self.config["estepa"]["limmax"] = txtLimitMax
                self.config["estepa"]["chunks"] = txtHistogramChunks
                toml_file = open(self.path_config_file, "w", encoding="utf-8")
                toml.dump(self.config, toml_file)
                toml_file.close()
            else:
                # get from file
                widgets.txtLimitMin.setText(str(self.config["estepa"]["limmin"]))
                widgets.txtLimitMax.setText(str(self.config["estepa"]["limmax"]))
        except:
            pass

    def load_cmbMask(self):
        # load estepa combo technology
        widgets.cmbMaskUpload.clear()
        widgets.cmbMaskUpload.addItem("Select mask")
        widgets.cmbMaskUpload.addItems(self.estepa.get_masks())
        widgets.txtMaskUpload.setText("")

    def load_cmbTechnology(self):
        # load estepa combo technology in pages estepa, upload and consult
        widgets.cmbTechnology.clear()
        widgets.cmbTechnologyUpload.clear()
        widgets.cmbTechnologyConsult.clear()
        widgets.cmbTechnology.addItem("Select technology")
        widgets.cmbTechnologyUpload.addItem("Select technology")
        widgets.cmbTechnologyConsult.addItem("Select technology")
        lista_technologies = self.estepa.get_technologies()
        widgets.cmbTechnology.addItems(lista_technologies)
        widgets.cmbTechnologyUpload.addItems(lista_technologies)
        widgets.cmbTechnologyConsult.addItems(lista_technologies)
        widgets.cmbParametersBBDD.clear()
        widgets.txtTechnologyUpload.setText("")
        widgets.cmbParametersConsult.clear()

    def load_cmbRuns(self):
        widgets.cmbRuns.clear()
        widgets.cmbRuns.addItem("Select run")
        technology = widgets.cmbTechnology.currentText()
        if technology != "Select technology" and technology != "":
            widgets.cmbRuns.addItems([str(x) for x in self.estepa.get_runs(technology)])
        widgets.cmbParametersBBDD.clear()

    def load_cmbWafers(self):
        widgets.cmbWafers.clear()
        widgets.cmbWafers.addItem("Select wafer")
        run = widgets.cmbRuns.currentText()
        if run != "Select run" and run != "":
            widgets.cmbWafers.addItems([str(x) for x in self.estepa.get_wafers(run)])
        widgets.cmbParametersBBDD.clear()

    def load_cmbParametersBBDD(self):
        widgets.cmbParametersBBDD.clear()
        widgets.cmbParametersBBDD.addItem("Select parameters")
        wafer = widgets.cmbWafers.currentText()
        if wafer != "Select wafer" and wafer != "":
            widgets.cmbParametersBBDD.addItems([str(x) for x in self.estepa.get_parameters(wafer)])
        else:
            widgets.cmbParametersBBDD.clear()

    def view_paramFile(self):
        parameters_file = widgets.cmbParametersFile.currentText()  # get text of combo Parameters
        parameters_file_list = parameters_file.split(", ")  # split to create list

        widgets.btnNextParamFiles.setVisible(len(parameters_file_list) > 1)  # show/hide next parameter button
        widgets.btnPreviousParamFiles.setVisible(len(parameters_file_list) > 1)  # show/hide next parameter button
        widgets.txtParamSelectedFiles.setVisible(len(parameters_file_list) > 1)  # show/hide txtParam Selected

        widgets.txtParamSelectedFiles.setText(parameters_file_list[0])

    def view_paramBBDD(self):
        parameters_BBDD = widgets.cmbParametersBBDD.currentText()  # get text of combo Parameters
        parameters_BBDD_list = parameters_BBDD.split(", ")  # split to create list

        widgets.btnNextParamBBDD.setVisible(len(parameters_BBDD_list) > 1)  # show/hide next parameter button
        widgets.btnPreviousParamBBDD.setVisible(len(parameters_BBDD_list) > 1)  # show/hide next parameter button
        widgets.txtParamSelectedBBDD.setVisible(len(parameters_BBDD_list) > 1)  # show/hide txtParam Selected

        widgets.txtParamSelectedBBDD.setText(parameters_BBDD_list[0])

    def update_cmbParametersFile(self):
        self.view_paramFile()

    def update_cmbParametersBBDD(self):
        self.view_paramBBDD()

    def viewOptionsEstepa(self):

        if widgets.optLoadFiles.isChecked():
            widgets.optionsESTEPA.setCurrentIndex(0)
        if widgets.optLoadBBDD.isChecked():
            widgets.optionsESTEPA.setCurrentIndex(1)

    def analyze_BBDD(self, param_selected=0):
        parametersBBDD = widgets.cmbParametersBBDD.currentText()
        parametersBBDD_list = parametersBBDD.split(', ')
        counter = widgets.cmbParametersBBDD.count()

        widgets.btnNextParamBBDD.setVisible(len(parametersBBDD_list) > 1)  # show/hide next parameter button
        widgets.btnPreviousParamBBDD.setVisible(len(parametersBBDD_list) > 1)  # show/hide previous parameter button
        widgets.txtParamSelectedBBDD.setVisible(len(parametersBBDD_list) > 1)  # show/hide txtParam Selected
        widgets.txtParamSelectedBBDD.setText(parametersBBDD_list[param_selected])

        if parametersBBDD != "" and parametersBBDD != "Select parameters":
            run = widgets.cmbRuns.currentText()
            wafer = widgets.cmbWafers.currentText()
            widgets.txtParametersResult.setPlainText("")
            if parametersBBDD == "All parameters":
                parametersBBDD_list = [widgets.cmbParametersBBDD.itemText(i) for i in
                                       range(1, widgets.cmbParametersBBDD.count())]
            measurements = self.estepa.get_medidas(wafer, parametersBBDD_list)

            for parameter in parametersBBDD_list:
                estadistica = StatisticsEstepa(parameter, measurements[parameter]["medida"], self.config["estepa"])
                widgets.txtParametersResult.setPlainText(
                    widgets.txtParametersResult.toPlainText() + "\n" + estadistica.print_statistics())

            # GET DATA VALUES, HISTOGRAM & WAFERMAP 
            # Get data values from result_file
            data_values = self.estepa.get_data_values(wafer, parametersBBDD_list[param_selected])
            # Put info in data values, histogram & wafermap
            parameter = parametersBBDD_list[param_selected]
            self.show_analysis(measurements[parameter]["medida"], data_values, parametersBBDD_list, param_selected)


        else:
            widgets.txtParametersResult.setPlainText(
                widgets.txtParametersResult.toPlainText() + "\n" + "No parameters selected!")

    def saveResults(self, where=""):
        # Click on Save buttons (Data Values, Results, Histogram, Correlation, Wafermap)
        # GET BUTTON CLICKED
        name_file = ""
        errorSaving = False
        errorSavingMessage = ""
        run, wafer, parameter = ["", "", ""]

        def get_run_wafer_from_filename(fileName):
            file_result = ResultFile(fileName)
            return file_result.lot, file_result.wafer

        btn = self.sender()
        btnName = btn.objectName()
        # btnSaveHistogram, btnSaveWafermap, btnSaveCorrelation btnSaveDataValues, btnSaveParametersResult, btnSaveHistorical
        texto = str(btnName).replace("btnSave", "")
        if texto != "Historical" and texto != "Diagram":
            # GET run, wafer, & parameter values
            if widgets.optLoadFiles.isChecked():
                fileName = widgets.txtDataFile.text()
                if fileName != "":
                    run, wafer = get_run_wafer_from_filename(fileName)
                    parameter = widgets.txtParamSelectedFiles.text()
                    parameters = widgets.cmbParametersFile.currentText()
            else:
                run = widgets.cmbRuns.currentText()
                wafer = widgets.cmbWafers.currentText()
                parameter = widgets.txtParamSelectedBBDD.text()
                parameters = widgets.cmbParametersBBDD.currentText()
        else:
            wafer = widgets.lbWafers.item(0).text()
            run = wafer.split("-")[0]
            parameter = widgets.txtParamSelectedConsult.text()

        if run == "" or wafer == "" or parameter == "":
            retval = messageBox(self, "Problem saving " + texto, "Run, wafer or parameter is missing!", "warning")
        else:
            # save image
            if texto == "Wafermap" or texto == "Histogram" or texto == "Correlation" or texto == "Diagram":
                if texto == "Diagram":
                    name_file = results_dir + "/" + parameter + "_" + texto + ".png"
                else:
                    name_file = results_dir + "/" + run + "-" + wafer + "_" + parameter + "_" + texto + ".png"
                try:
                    if texto == "Wafermap":
                        widgets.horizontalLayout_wafermap.itemAt(0).widget().figure.savefig(name_file, dpi=300)
                    elif texto == "Diagram":
                        widgets.verticalLayout_diagrams.itemAt(0).widget().figure.savefig(name_file, dpi=300)
                    else:
                        texto = widgets.tabGraphs.tabText(1)
                        if texto == "Correlation":
                            name_file = results_dir + "/" + run + "-" + wafer + "_" + parameters.replace(", ",
                                                                                                         "-") + "_" + texto + ".png"
                        widgets.verticalLayout_histogram.itemAt(0).widget().figure.savefig(name_file, dpi=300)
                except Exception as e:
                    errorSaving = True
                    errorSavingMessage = e
            else:
                # save file
                try:
                    if texto == "DataValues":
                        name_file = results_dir + "/" + run + "-" + wafer + "_" + parameter + "_" + texto + ".dat"
                        text_save = widgets.txtDataValues.toPlainText()
                    if texto == "ParametersResult":
                        name_file = results_dir + "/" + run + "-" + wafer + "_" + texto + ".dat"
                        text_save = widgets.txtParametersResult.toPlainText()
                    if texto == "Historical":
                        name_file = results_dir + "/" + texto + ".dat"
                        text_save = widgets.txtDataValuesConsult.toPlainText()

                    if name_file != "" and text_save != "":
                        # save file
                        file_result = open(name_file, "w")
                        file_result.write(text_save)
                        file_result.close()
                    else:
                        errorSaving = True
                        errorSavingMessage = "Information or filename missed!"
                except Exception as e:
                    errorSaving = True
                    errorSavingMessage = e
            if not errorSaving:
                retval = messageBox(self, "Save " + texto, "Info correctly saved into file:\n" + name_file, "info")
            else:
                retval = messageBox(self, "Save " + texto,
                                    "Some error occurs while saving file:\n" + name_file + "\n" + errorSavingMessage,
                                    "warning")

    # end ESTEPA functions
    # --------------------

    # Functions to clear layouts
    # --------------------------
    def clear_layouts(self, layout, layout_buttons):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()
            layout.itemAt(i).widget().setParent(None)
        for i in reversed(range(layout_buttons.count())):
            layout_buttons.itemAt(i).widget().deleteLater()
            layout_buttons.itemAt(i).widget().setParent(None)

        QApplication.processEvents()

    def clearGraph(self):
        global widgets

        layout = widgets.horizontalLayout_graph
        layout_buttons = widgets.horizontalLayout_btnGraph # TODO: ?Change BtnGraph to btnGraph in main.ui
        self.clear_layouts(layout, layout_buttons)
        # for i in reversed(range(widgets.horizontalLayout_graph.count())):
        #     widgets.horizontalLayout_graph.itemAt(i).widget().deleteLater()
        # for i in reversed(range(widgets.horizontalLayout_btnGraph.count())):
        #     widgets.horizontalLayout_btnGraph.itemAt(i).widget().deleteLater()
        widgets.btnSaveGraph.setVisible(False)
        widgets.btnClearGraph.setVisible(False)

        QApplication.processEvents()

        return layout, layout_buttons

    def clearWafermap(self):
        global widgets

        layout = widgets.horizontalLayout_wafermap
        layout_buttons = widgets.horizontalLayout_btnWafermap
        self.clear_layouts(layout, layout_buttons)
        # for i in reversed(range(widgets.horizontalLayout_wafermap.count())):
        #     widgets.horizontalLayout_wafermap.itemAt(i).widget().deleteLater()
        # for i in reversed(range(widgets.horizontalLayout_btnWafermap.count())):
        #     widgets.horizontalLayout_btnWafermap.itemAt(i).widget().deleteLater()
        widgets.btnSaveWafermap.setVisible(False)
        widgets.btnClearWafermap.setVisible(False)

        return layout, layout_buttons

    def clearHistogram(self):
        global widgets

        # Delete all widgets in layout
        layout = widgets.verticalLayout_histogram
        layout_buttons = widgets.horizontalLayout_btnHistogram
        self.clear_layouts(layout, layout_buttons)

        widgets.btnSaveHistogram.setVisible(False)
        widgets.btnClearHistogram.setVisible(False)

        return layout, layout_buttons

    def clearDiagram(self):
        global widgets

        # Delete all widgtets in layout
        layout = widgets.verticalLayout_diagrams
        layout_buttons = widgets.horizontalLayout_btnDiagrams
        self.clear_layouts(layout, layout_buttons)

        widgets.btnSaveDiagram.setVisible(False)
        widgets.btnClearDiagram.setVisible(False)

        return layout, layout_buttons

    # --------------------------
    # CONSULT functions
    # -----------------

    def optionsHistorical(self):
        if widgets.chkHistorical.isChecked():
            widgets.optionsHistorical.setCurrentWidget(widgets.YesHistorical)
        else:
            widgets.optionsHistorical.setCurrentWidget(widgets.NoHistorical)

    def uploadHistorical(self):
        texto = widgets.txtDataValuesConsult.toPlainText()
        retval = messageBox(self, "Upload historical", f"Do you want to upload historical data to BBDD?\n{texto}", "question")
        if retval == QMessageBox.Yes:
            texto = texto.split("\n")
            if len(texto) > 1:
                runs_info = {}
                wafers_info = {}
                run_detected = ""
                wafer_detected = ""
                for i in range(0, len(texto)):
                    line = texto[i]
                    if line != "":
                        if "Run: " in line:
                            wafer_detected = ""
                            run_detected = line.split(" ")[1]
                            runs_info[run_detected] = []
                        if "Wafer: " in line:
                            runs_detected = ""
                            wafer_detected = line.split(" ")[1]
                            wafers_info[wafer_detected] = []
                        if not "Parameter " in line and not "Wafer: " in line and not "Run: " in line:
                            if run_detected!="":
                                runs_info[run_detected].append(line)
                            if wafer_detected!="":
                                wafers_info[wafer_detected].append(line)

                # Upload runs
                if len(runs_info)>0:
                    for run_info in runs_info:
                        run = run_info
                        run_list = runs_info[run]
                        for valores in run_list:
                            parametro, media, desv_est, mediana, puntos, met_elim_outliers = valores.split(" ")
                            puntos, total_puntos = puntos.split("/")
                            insert = True
                            if self.estepa.exists_analisis_runs(run, parametro):
                                retval = messageBox(self, "Analisis run exists",
                                                    f"Do you want to insert results for run '{run}' and parameter '{parametro}'?",
                                                    "question")
                                if retval == QMessageBox.No:
                                    insert = False
                            if insert:
                                self.estepa.upload_analisis_runs(run, valores)

                # Upload wafers
                if len(wafers_info)>0:
                    for wafer_info in wafers_info:
                        wafer = wafer_info
                        wafer_list = wafers_info[wafer]
                        for valores in wafer_list:
                            parametro, media, desv_est, mediana, puntos, met_elim_outliers = valores.split(" ")
                            puntos, total_puntos = puntos.split("/")
                            insert = True
                            if self.estepa.exists_analisis(wafer, parametro):
                                retval = messageBox(self, "Analisis exists",
                                                    f"Do you want to insert results for wafer '{wafer}' and parameter '{parametro}'?",
                                                    "question")
                                if retval == QMessageBox.No:
                                    insert = False
                            if insert:
                                self.estepa.upload_analisis(wafer, valores)
                print(runs_info)
                print()
                print(wafers_info)
                messageBox(self, "Upload historical", "Historical data uploaded to BBDD", "information")
            else:
                messageBox(self, "Upload historical", "No data to upload", "information")


    def load_cmbRunsConsult(self):
        widgets.cmbRunsConsult.clear()
        widgets.cmbRunsConsult.addItem("Select run")
        technology = widgets.cmbTechnologyConsult.currentText()
        if technology != "Select technology" and technology != "":
            widgets.cmbRunsConsult.addItems([str(x) for x in self.estepa.get_runs(technology)])
        widgets.cmbParametersConsult.clear()

    def load_cmbWafersConsult(self):
        widgets.cmbWafersConsult.clear()
        widgets.cmbWafersConsult.addItem("Select wafer")
        run = widgets.cmbRunsConsult.currentText()
        if run != "Select run" and run != "":
            wafers_list = [str(x) for x in self.estepa.get_wafers(run)]
            wafers_list.insert(0, "All wafers")
            widgets.cmbWafersConsult.addItems(wafers_list)
        widgets.cmbParametersConsult.clear()

    def load_cmbParametersConsult(self):
        widgets.cmbParametersConsult.clear()
        widgets.cmbParametersConsult.addItem("Select parameters")
        wafers = widgets.cmbWafersConsult.currentText()
        if wafers != "Select wafer" and wafers != "":
            wafers_list = wafers.split(", ")
            # agafem només primera wafer seleccionada
            parameters_list = [str(x) for x in self.estepa.get_parameters(wafers_list[0])]
            widgets.cmbParametersConsult.addItems(parameters_list)
        else:
            widgets.cmbParametersConsult.clear()

    def load_controlsConsult(self):
        activate = widgets.cmbParametersConsult.currentText() != ""
        widgets.btnPreviousParamConsult.setVisible(activate)
        widgets.btnNextParamConsult.setVisible(activate)
        widgets.txtParamSelectedConsult.setVisible(activate)
        if activate:
            # view parameters in txtParamSelectedConsult
            parameters_list = widgets.cmbParametersConsult.currentText().split(", ")
            widgets.txtParamSelectedConsult.setText(parameters_list[0])

    def add_wafers_to_ListBox(self):
        wafers = widgets.cmbWafersConsult.currentText()
        if wafers != "Select wafers" and wafers != "":
            wafers_list = wafers.split(", ")
            items_lbWafers = self.get_items_ListBox()
            for wafer in wafers_list:
                if wafer not in items_lbWafers:
                    widgets.lbWafers.addItem(wafer)

    def get_items_ListBox(self):
        items = []
        for index in range(widgets.lbWafers.count()):
            items.append(widgets.lbWafers.item(index).text())
        return items

    def remove_item_ListBox(self, item):
        row = widgets.lbWafers.row(item)
        widgets.lbWafers.takeItem(row)

    def get_options_Consult(self):
        option_checked = "Wafers"
        option_historical = "No"
        option_values = "Values"
        if widgets.optRunsConsult.isChecked():
            option_checked = "Runs"
        if widgets.chkHistorical.isChecked():
            option_historical = "Yes"
            if widgets.optYield.isChecked():
                option_values = "Yield"
        # option_checked = Wafers or Runs
        # option_historical = Yes or No
        # option_values = Values or Yield
        options = [option_checked, option_historical, option_values]
        return options

    def consult(self, param_selected=0, calcDataValues=True):

        parameters_consult = widgets.cmbParametersConsult.currentText()  # get text of combo Parameters
        parameters_consult_list = parameters_consult.split(", ")  # split to create list
        parameter_selected = parameters_consult_list[param_selected]
        widgets.txtParamSelectedConsult.setText(parameter_selected)
        tecnologia_consult = widgets.cmbTechnologyConsult.currentText()
        list_wafers = [widgets.lbWafers.item(i).text() for i in range(widgets.lbWafers.count())]
        movie = QMovie("images\images\loading.gif")
        widgets.lblLoadingConsult.setMovie(movie)
        if len(list_wafers) > 0 and len(parameters_consult_list) > 0:
            options = self.get_options_Consult()
            movie.start()
            widgets.lblLoadingConsult.setVisible(True)
            QApplication.processEvents()
            list_all_values = []
            list_values_yields_param = []
            list_runs_wafers_param = []
            # get all lists for parameters
            if calcDataValues:
                widgets.txtDataValuesConsult.setPlainText("")
                for parameter in parameters_consult_list:
                    QApplication.processEvents()
                    list_values_yields, list_runs_wafers, list_historical_found = \
                        self.consult_get_parameter(list_wafers, options, parameter)

                    # for graph save the parameter selected
                    if parameter == parameter_selected:
                        list_values_yields_param = list_values_yields
                        list_runs_wafers_param = list_runs_wafers
                    list_all_values.append([ list_runs_wafers, list_values_yields, list_historical_found])
                # print text in data values
                list_all_runs_wafers = list_all_values[0][0];
                list_all_historical_found = list_all_values[0][2];
                header = "Parameter Mean Stdev Median Points Method"
                new_text = ""
                break_line = "<br />"
                runs = False
                if widgets.optRunsConsult.isChecked():
                    runs = True
                for i, run_wafer in enumerate(list_all_runs_wafers):
                    QApplication.processEvents()
                    if runs:
                        match_wafers = [wafer for wafer in list_wafers if run_wafer in wafer]
                        new_text += "Run: " + run_wafer + " (" + ", ".join(match_wafers) + ")" + break_line
                    else:
                        new_text += "Wafer: " + run_wafer + break_line
                    new_text += header + break_line

                    for j, parameter in enumerate(parameters_consult_list):
                        QApplication.processEvents()
                        values = ""
                        span_color_text = "white"
                        for k in range(0, 6):
                            if k >= 0 and k <= 2:
                                values += f"{list_all_values[j][1][i][k]:.3f} "
                            elif k == 4:
                                values += str(list_all_values[j][1][i][k-1]) + "/" + str(list_all_values[j][1][i][k]) + " "
                            elif k == 5:
                                values += str(list_all_values[j][1][i][k])

                        if list_all_values[j][2][i]:
                            span_color_text = "red"
                        new_text += '<span style="color: ' + span_color_text + '">' + parameter + " " + values + '</span>' + break_line
                    new_text += break_line
                widgets.txtDataValuesConsult.appendHtml(new_text)
            else:
                list_values_yields_param, list_runs_wafers_param, _ = \
                    self.consult_get_parameter(list_wafers, options, parameter_selected)
            QApplication.processEvents()
            # get list_rangos
            list_rangos = self.estepa.get_rangos(tecnologia_consult, parameter_selected)
            # print graphs only for parameter selected
            self.print_consult(list_values_yields_param, list_runs_wafers_param, parameter_selected, options, list_rangos)
            movie.stop()
            widgets.lblLoadingConsult.setVisible(False)

        else:
            messageBox(self, "Wafers or parameters not selected",
                       "Please, select at least one wafer and parameter to consult", "warning")

    def print_consult(self, values_yields, runs_wafers, parameter, options, list_rangos):

        layout, layout_buttons = self.clearDiagram()
        _static_ax = self.create_static_ax(layout, layout_buttons, "diagram")
        list_rangos_min = []
        list_rangos_max = []
        if options[2] == "Values":
            means = []
            val_X = []

            for i, _ in enumerate(runs_wafers):
                mean = float(values_yields[i][0])
                median = float(values_yields[i][2])
                stdev = float(values_yields[i][1])
                means.append(mean)
                val_X.append(i + 1)
                if len(list_rangos)==2:
                    list_rangos_min.append(list_rangos[0])
                    list_rangos_max.append(list_rangos[1])

                value_max = mean + stdev
                value_min = mean - stdev
                label_stdev = ""
                label_median = ""
                label_mean = ""
                if i == 0:
                    # add label
                    label_stdev = "stdev"
                    label_median = "median"
                    label_mean = "mean"

                _static_ax.scatter(val_X[i], value_max, marker="+", color="blue", label=label_stdev)
                _static_ax.scatter(val_X[i], value_min, marker="+", color="blue")
                _static_ax.scatter(val_X[i], mean, marker="o", color="green", label=label_mean)
                _static_ax.scatter(val_X[i], median, marker="^", color="red", label=label_median)

            if len(means) > 1:
                _static_ax.plot(val_X, means, color="green")
        else:
            yield_values = []
            val_X = []

            for i, _ in enumerate(runs_wafers):
                label_yield = ""
                if i == 0:
                    label_yield = "yield"
                val_X.append(i + 1)
                points_ini = values_yields[i][3]
                points_end = values_yields[i][4]
                yield_value = round((points_ini * 100 / points_end), 2)
                yield_values.append(yield_value)
                _static_ax.scatter(val_X[i], yield_value, marker="+", color="gray", label=label_yield)

            if len(yield_values) > 1:
                _static_ax.plot(val_X, yield_values, color="gray")

        # Add rangos
        if len(list_rangos)==2 and options[2] == "Values":
            _static_ax.plot(val_X, list_rangos_min, color="gray", linestyle="--")
            _static_ax.plot(val_X, list_rangos_max, color="gray", linestyle="--")
        # Add a title and axis labels
        if options[1] == "Yes":
            title = "Historical graph "
        else:
            title = "Graph "
        title += "of " + options[2].lower() + " for " + parameter
        # Set the x-axis to display variable names
        _static_ax.set_xticks(val_X)
        _static_ax.set_xticklabels(runs_wafers)
        # Add a legend
        _static_ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        # etiquetas
        _static_ax.set_xlabel(options[0])
        _static_ax.set_ylabel(parameter)
        _static_ax.set_title(title)

        widgets.btnSaveDiagram.setVisible(True)
        widgets.btnClearDiagram.setVisible(True)

    def consult_get_parameter(self, list_wafers, options, parameter):
        # check parameters in wafers
        list_values_yields = []
        list_runs_wafers = []
        list_historical_found = []
        check_parameter = True
        for wafer in list_wafers:
            QApplication.processEvents()
            if not self.estepa.exists_parameter_in_wafer(wafer, parameter):
                check_parameter = False
                break;

        if check_parameter:
            if options[0] == "Runs":
                # format lists wafers in list of list
                # order list and get list_wafers (runs) list of lists
                list_wafers_sort = sorted(list_wafers)
                list_wafers_runs = []
                run_prev = ""
                run_list = []
                for wafer in list_wafers_sort:
                    QApplication.processEvents()
                    run = wafer.split("-")[0]
                    if run == run_prev:
                        run_list.append(wafer)
                    else:
                        if run_prev != "": list_wafers_runs.append(run_list)
                        run_list = []
                        run_list.append(wafer)
                        run_prev = run
                list_wafers_runs.append(run_list)
                list_wafers = list_wafers_runs

            for wafer in list_wafers:
                # if historical try to get values saved
                QApplication.processEvents()
                list_values = []
                stat_list = []
                historical_found = False
                if options[1] == "Yes":
                    list_values, run = self.estepa.get_medida_historical_consult(wafer, parameter, options)
                if len(list_values) == 0:
                    list_values, run = self.estepa.get_medida_consult(wafer, parameter)
                    stat = StatisticsEstepa(parameter, list_values, self.config["estepa"])
                    # get list of [mean, median, stdev, points_end, points_ini]
                    if stat.error:
                        messageBox(self, "Error in statistics", stat.error_message, "warning")
                    else:
                        stat_list = stat.get_parameters()
                else:
                    historical_found = True
                    # Historical get values (create statistics with values returned)
                    if len(list_values) == 1:
                        stat_list = list_values
                    else:
                        means = []
                        medians = []
                        stdevs = []
                        points_end = 0
                        points_total = 0
                        for lv in list_values:
                            means.append(lv[0])
                            stdevs.append(lv[1])
                            medians.append(lv[2])
                            points_end += lv[3]
                            points_total += lv[4]

                        stat_list = [statistics.mean(means), statistics.mean(stdevs), statistics.mean(medians),
                                     points_end, points_total, self.config["estepa"]["method"]]

                if len(stat_list) > 0:
                    # if options[2] == "Values":
                    #     # get values
                    #     stat_list = stat_list[:3]
                    # else:
                    #     stat_list = stat_list[3:5]
                    list_values_yields.append(stat_list)
                    list_runs_wafers.append(run)
                    list_historical_found.append(historical_found)
                else:
                    messageBox(self, "Values not found", f"Value not found for parameter '{parameter}'", "warning")

        else:
            messageBox(self, "Parameter not found in wafer", f"Parameter '{parameter}' not found in wafer: {wafer}!",
                       "warning")

        return list_values_yields, list_runs_wafers, list_historical_found

    # end CONSULT functions

    # ---------------------
    # REPORTS functions
    # -----------------
    def create_report_file(self):
        # execute cmbReports file selected
        filename_report = self.get_filename_report()
        if filename_report != "":
            self.run(filename_report, "reports")

    def parameters_report_config(self):
        if widgets.cmbReports.currentIndex() > 0:
            report_selected = widgets.cmbReports.currentText()
            filename_parameters = os.path.join(self.getDirs("reports"), report_selected + ".toml")
            if os.path.exists(filename_parameters):
                self.parameterwindow = ParametersWindow(filename_parameters)
                if not self.parameterwindow.error:
                    try:
                        self.parameterwindow.show()
                    except Exception as e:
                        print(str(e))
                else:
                    retval = messageBox(self, "Error getting parameters from file", self.parameterwindow.error_message,
                                        "critical")
            else:
                print(f"{filename_parameters} doesn't exists!")
                messageBox(self, "Error getting parameters from file",
                                    f"{filename_parameters} doesn't exists!", "warning")
    # end REPORTS functions
    # ---------------------

    def test_status_reset(self):
        global test_status, measurement_status
        retval = messageBox(self, "Reset TEST", "Do you want to reset (IDLE) the test status?", "question")
        if retval == QMessageBox.Yes:
            test_status.status = "IDLE"
            measurement_status.status == "IDLE"

    def go_home(self):
        self.name_prober = self.get_prober_selected()
        if self.name_prober != "":
            self.prober = eval(self.name_prober)(probers[self.name_prober])
            idn = self.prober.idn()
            if idn != "":
                print("Go home!")
                self.prober.move_home()

    def closeEvent(self, event):
        global test_status
        self.log.info("Test Status: %s", test_status.status)
        if test_status.status == "IDLE" or \
                test_status.status == "FINISHED" or \
                test_status.status == "ABORTED":
            event.accept()
            if self.estepa:
                self.estepa.close_connection()  # close connection to estepa
            self.close()
            QCoreApplication.quit()
        else:
            retval = messageBox(self, "Test in progress", "Please, stop the test first!", "error")
            retval = messageBox(self, "Stop process?", "Do you want to stop the process?", "question")
            if retval == QMessageBox.Yes:
                widgets.btnStop.clicked.emit()
            event.ignore()

    def loading_drivers(self, username):

        instruments = "config." + username + ".instruments"
        importlib.import_module(instruments)
        print("instruments loaded...")
        # from config.default.instruments import *

    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        global measurement_status, test_status
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()
        # by default show configuration options for home
        widgets.stackedWidget_configuration.setCurrentWidget(widgets.configuration_measurements)
        # SHOW HOME PAGE
        if btnName == "btn_page_home":
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW HOME ESTEPA
        if btnName == "btn_page_estepa":
            # show estepa configuration
            widgets.stackedWidget_configuration.setCurrentWidget(widgets.configuration_estepa)
            # show estepa page
            widgets.stackedWidget.setCurrentWidget(widgets.estepa)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_page_consult":
            # show estepa configuration
            widgets.stackedWidget_configuration.setCurrentWidget(widgets.configuration_estepa)
            # show estepa page
            widgets.stackedWidget.setCurrentWidget(widgets.consult_estepa)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        if btnName == "btn_page_inbase":
            # show estepa configuration
            widgets.stackedWidget_configuration.setCurrentWidget(widgets.configuration_estepa)
            # show estepa page
            widgets.stackedWidget.setCurrentWidget(widgets.inbase)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_page_measurements":
            widgets.stackedWidget.setCurrentWidget(widgets.measurements)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            # if measurement_status.status == "IDLE" and test_status.status == "IDLE":
            #     # load instruments, probers and waferwaps
            #     self.load_instruments()
            #     self.load_probers()
            #     self.load_wafermaps()

        # SHOW NEW PAGE
        if btnName == "btn_page_instruments":
            widgets.stackedWidget.setCurrentWidget(widgets.instruments)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

        if btnName == "btn_page_probers":
            widgets.stackedWidget.setCurrentWidget(widgets.probers)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

        if btnName == "btn_page_reports":
            # show estepa configuration
            widgets.stackedWidget_configuration.setCurrentWidget(widgets.configuration_reports)
            widgets.stackedWidget.setCurrentWidget(widgets.reports)  # SET PAGE
            UIFunctions.resetStyle(self, btnName)  # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))  # SELECT MENU

        # PRINT BTN NAME
        # print(f'Button "{btnName}" pressed!')

    def IsMeasurement(self):
        if widgets.cmbTests.currentIndex() > 0 and widgets.cmbInstruments.currentIndex() > 0:
            return True
        return False

    def IsDarkMode(self):
        status = widgets.chkDarkMode.isChecked()
        mpl_style(dark=status)
        self.config["defaults"]["darkmode"] = status
        return status

    def IsDebugMode(self):
        status = widgets.chkDebugMode.isChecked()
        if status:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)
        self.config["defaults"]["debugmode"] = status
        return status

    def IsCartographyMeasurement(self):
        return widgets.chkCartoMeas.isChecked()

    def changeCartoMeas(self):
        global cartographic_measurement
        cartographic_measurement = self.IsCartographyMeasurement()
        widgets.cmbProbers.setVisible(cartographic_measurement)
        widgets.cmbWafermaps.setVisible(cartographic_measurement)
        widgets.btnViewWafermap.setVisible(cartographic_measurement)
        widgets.btnGoHome.setVisible(cartographic_measurement)
        self.load_wafermaps()

    # BUTTONS CLICK on MEASUREMENTS PAGE
    # ///////////////////////////////////////////////////////////////
    def MeasurementClick(self):
        # GET BUTTON CLICKED
        global measurement_status, test_status, file_measurement, connDeep
        btn = self.sender()
        btnName = btn.objectName()
        measurement_status_previous = measurement_status.status
        test_status_previous = test_status.status
        # SHOW HOME PAGE
        if btnName == "btnStart":
            if self.IsMeasurement():
                if self.IsCartographyMeasurement():
                    # START OR CONTINUE
                    self.change_state_process("START")  # update status global (need previous state)
                    if test_status_previous != "PAUSED":

                        # Start cartographic measurement
                        retval = messageBox(self, "Starting cartographic measurement!", "Are you sure?", "question")
                        if retval == QMessageBox.Yes:
                            # create header file
                            # create file measurement
                            process_name = widgets.txtProcess.text()
                            lot_name = widgets.txtLot.text()
                            wafer_name = widgets.txtWafer.text()
                            mask_name = widgets.txtMask.text()
                            operator_name = username
                            filename_test = self.get_filename_test()
                            parameters = {
                                "process_name": process_name,
                                "lot_name": lot_name,
                                "wafer_name": wafer_name,
                                "mask_name": mask_name,
                                "operator_name": operator_name,
                                "filename_test": filename_test,
                                "date": "",
                                "time": "",
                                "waferinfo":""
                            }
                            file_measurement = MeasurementFile(parameters)
                            if file_measurement.created:
                                if file_measurement.MeasurementHeaderFile():
                                    widgets.btnPause.setEnabled(True)
                                    widgets.btnStop.setEnabled(True)
                                    # Estado de la medida en START
                                    measurement_status.status = "START"
                                    # iniciamos medida cartográfica
                                    self.updateTextDescription("START CARTOGRAPHIC MEASUREMENT")
                                    self.execute_cartographic_measurement()
                                    self.updateTextDescription("FINISH CARTOGRAPHIC MEASUREMENT")
                                    QApplication.processEvents()
                                else:
                                    retval = messageBox(self, "Not header file created!",
                                                        "An error occurs while adding header to measurement file",
                                                        "warning")
                            else:
                                retval = messageBox(self, "Not file created!",
                                                    "An error occurs while creating measurement file", "warning")

                        self.change_state_process("FINISH")

                else:
                    test_status.status = "IDLE"
                    contact_status.status = "IDLE"
                    # Normal measurement
                    # Put progressBar to 0% and btnStart False
                    self.change_state_process("START")
                    # Estado de la medida en START + STOP (cuando acaba)
                    self.updateTextDescription("Start single measure")
                    # Execute single measurement
                    self.execute_measurement()
                    # When finish 100% and btnStart true
                    while measurement_status.status != "FINISH":
                        QApplication.processEvents()
                        QThread.msleep(50)
                    #
                    self.updateTextDescription("Finish single measure")
                    QApplication.processEvents()

            else:
                retval = messageBox(self, "Not a valid measurement!",
                                    "Please, select an instrument & test before Start measurement", "warning")

        # SHOW WIDGETS PAGE
        if btnName == "btnPause":
            self.change_state_process("PAUSE")
            QApplication.processEvents()
            # retval = messageBox(self,"Cartographic measurement state","Are you sure to pause the process?","question")
            # if retval == QMessageBox.Yes:

        if btnName == "btnStop":
            retval = messageBox(self, "Cartographic Test status", "Are you sure to STOP the process?", "question")
            if retval == QMessageBox.Yes:
                test_status.status = "STOP"
                self.change_state_process("STOP")

    def change_state_process(self, status):
        global measurement_status, test_status

        if status == "START":
            if self.IsCartographyMeasurement():
                if test_status.status == "PAUSED":
                    # Continue
                    widgets.btnStart.setEnabled(False)
                    widgets.btnPause.setEnabled(True)
                    widgets.btnStop.setEnabled(True)
                else:
                    # Start 
                    widgets.progressBar.setValue(0)
                    widgets.progressBar.setFormat('%.02f %%' % 0)
                    widgets.btnStart.setEnabled(False)
                    widgets.btnPause.setEnabled(False)
                    widgets.btnStop.setEnabled(False)

                test_status.status = "STARTED"

            else:
                # Ponemos el progressBar en 0%
                widgets.progressBar.setValue(0)
                widgets.progressBar.setFormat('%.02f %%' % 0)
                widgets.btnStart.setEnabled(False)

                measurement_status.status = "START"
            widgets.btnSaveDescription.setEnabled(False)
            widgets.btnClearDescription.setEnabled(False)

        if status == "PAUSE":
            if self.IsCartographyMeasurement():
                test_status.status = "PAUSED"
            else:
                measurement_status.status = "PAUSE"

            widgets.btnStart.setEnabled(True)
            widgets.btnStop.setEnabled(True)
            widgets.btnPause.setEnabled(False)
            widgets.btnSaveDescription.setEnabled(False)
            widgets.btnClearDescription.setEnabled(False)

        if status == "STOP":
            # problem with measurement or test
            if self.IsCartographyMeasurement():
                test_status.status = "ABORTED"
                measurement_status.status = "STOP"
            else:
                measurement_status.status = "STOP"
            widgets.btnStart.setEnabled(True)
            widgets.btnStop.setEnabled(False)
            widgets.btnPause.setEnabled(False)
            widgets.btnSaveDescription.setEnabled(True)
            widgets.btnClearDescription.setEnabled(True)

        if status == "FINISH":
            # measurement or test FINISHED OK
            if self.IsCartographyMeasurement():
                test_status.status = "FINISHED"
                measurement_status.status = "IDLE"
            else:
                measurement_status.status = "FINISH"
            widgets.btnStart.setEnabled(True)
            widgets.btnStop.setEnabled(False)
            widgets.btnPause.setEnabled(False)
            widgets.btnSaveDescription.setEnabled(True)
            widgets.btnClearDescription.setEnabled(True)
            widgets.progressBar.setValue(100 * 100)
            widgets.progressBar.setFormat('%.02f %%' % 100)

        QApplication.processEvents()

    def toggle_widgets(self, estado):
        widgets.cmbInstruments.setEnabled(estado)
        widgets.cmbTests.setEnabled(estado)
        widgets.cmbProbers.setEnabled(estado)
        widgets.cmbWafermaps.setEnabled(estado)
        widgets.chkViewPosition.setEnabled(estado)
        widgets.chkViewGraph.setEnabled(estado)

    def updateTextDescription(self, texto, color="NORMAL"):
        global widgets
        date_today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        colors = {"NORMAL": "#FFFFFF", "ERROR": "#FF3300", "WARNING": "orange"}
        if not color in colors:
            color = "NORMAL"
        texto_final = '<span style="color: #ff79c6">' + "[" + date_today + "]</span>" + "<br />" + '<span style="color: ' + \
                      colors[color] + '">' + texto + "</span>"

        widgets.pteDescription.appendHtml(texto_final)

    def run(self, runfile, folder):
        # print(">> [run] runfile: " + runfile)
        runfile = self.get_base_path(folder) + runfile
        if os.path.exists(runfile):
            with open(runfile, "r") as rnf:
                try:
                    content = rnf.read()
                    exec(content)
                except Exception as ex:
                    retval = messageBox(self, "Problem executing file",
                                        "Problem exists while exec file's content: " + runfile + "\n" + str(
                                            type(ex)) + "\n" + str(ex), "critical")
                    print(traceback.print_exc())
                    if folder == "tests":
                        self.change_state_process("STOP")

        else:
            retval = messageBox(self, "Problem searching file", "File: '" + runfile + "' not found!", "critical")

    def execute_measurement(self):
        global dieActual, moduleActual, wafer_parameters, file_measurement, connDeep
        # print(">> [execute_measurement] START")
        if self.script_running:
            # print(">> [execute_measurement] Script already running, abort.")
            return  # Evita doble ejecución

        self.script_running = True  # Marca como "en ejecución"
        # print(">> [execute_measurement] Marked script_running = True")

        self.toggle_widgets(False)
        QApplication.processEvents()

        test_file = self.get_filename_test()
        test_folder = "tests" + "/" + self.get_instrument_selected()
        runfile = self.get_base_path(test_folder) + test_file

        if not os.path.exists(runfile):
            messageBox(self, "Error", f"Archivo '{runfile}' no encontrado.", "critical")
            self.toggle_widgets(True)
            self.script_running = False
            return

        # Si ya hay un thread anterior, desconecta sus señales
        if hasattr(self, "script_thread") and self.script_thread is not None:
            try:
                self.script_thread.finished.disconnect(self.on_script_finished)
                # print(">> [execute_measurement] Disconnected previous finished")
            except (TypeError, RuntimeError):
                print(">> [execute_measurement] No previous finished to disconnect or already disconnected")
            try:
                self.script_thread.error.disconnect(self.on_script_error)
            except Exception:
                pass
            try:
                self.script_thread.plot_ready.disconnect(self.show_graph)
            except Exception:
                pass
            try:
                self.script_thread.request_message_box.disconnect(self.show_message_box)
            except Exception:
                pass

        self.script_thread = ScriptRunner(runfile, main_context=self)
        # print(f">> [execute_measurement] Created ScriptRunner ID: {id(self.script_thread)}")

        self.script_thread.finished.connect(self.on_script_finished)
        self.script_thread.error.connect(self.on_script_error)
        self.script_thread.plot_ready.connect(self.show_graph)
        self.script_thread.request_message_box.connect(self.show_message_box)
        # print(">> [execute_measurement] Connected signals")

        self.script_thread.start()
        # print(">> [execute_measurement] Script started")

    def show_message_box(self, title, message, buttons_type):
        if buttons_type == "yes_cancel":
            result = QMessageBox.question(
                self,
                title,
                message,
                buttons=QMessageBox.Yes | QMessageBox.Cancel,
                defaultButton=QMessageBox.Yes,
            )

        elif buttons_type == "ok_cancel":
            result = QMessageBox.question(
                self,
                title,
                message,
                buttons=QMessageBox.Ok | QMessageBox.Cancel,
                defaultButton=QMessageBox.Ok,
            )

        elif buttons_type == "ok_error":
            result = QMessageBox.critical(
                self,
                title,
                message,
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok,
            )

        else:   # buttons_type == "ok" or another option
            result = QMessageBox.information(
                self,
                title,
                message,
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok,
            )

        self.script_thread.message_box_result = result


    def on_script_finished(self):
        global dieActual, moduleActual, wafer_parameters, file_measurement, measurement_status

        if not self.script_running:
            # print(">> [on_script_finished] Already finished, skipping")
            return

        # print(">> [on_script_finished] CALLED")
        self.script_running = False

        if not self.IsCartographyMeasurement():
            # print(">> [on_script_finished] Non-cartography mode")
            self.toggle_widgets(True)
            self.change_state_process("FINISH")
            # print(">> [on_script_finished] Reset script_running = False")
            return

        # print(">> [on_script_finished] Cartography mode")
        die = int(dieActual) - 1
        module = int(moduleActual) - 1
        variables = self.waferwindow.meas_result[die][module]["variables"]

        if variables:
            if not isinstance(variables, list):
                file_measurement.MeasurementSectionFile(section="MODTEST", tag="BEG")
                file_measurement.MeasurementVariablesFile(variables)
                file_measurement.MeasurementSectionFile(section="MODTEST", tag="END")
            else:
                for count, var in enumerate(variables, start=1):
                    file_measurement.MeasurementSectionFile(section="MODTEST", tag="BEG", modtest=count)
                    file_measurement.MeasurementVariablesFile(var)
                    file_measurement.MeasurementSectionFile(section="MODTEST", tag="END", modtest=count)

        measurement_status.status = "FINISH"
        # print(">> [on_script_finished] Reset script_running = False")

    def on_script_error(self, error_message):
        print(error_message)
        messageBox(self, "Error ejecutando script", error_message, "critical")
        self.change_state_process("STOP")
        self.toggle_widgets(True)
        self.script_running = False

    def execute_measurement_old(self):
        # without threads
        global dieActual, moduleActual, wafer_parameters, file_measurement, connDeep


        # load test and run
        self.toggle_widgets(False)
        QApplication.processEvents()
        self.run(self.get_filename_test(), "tests" + "/" + self.get_instrument_selected())

        if not self.IsCartographyMeasurement():
            self.toggle_widgets(True)
        else:
            # update dieActual status (moduleActual?)
            # transfor wafer_parameters["wafer_positions"] coord to real name button
            # waferwindow_btn = self.waferwindow.centralWidget().findChild(QPushButton, "btn_0_0")
            # waferwindow_btn.btnType = meas_result["meas_status"]
            # waferwindow_btn.message = meas_result["meas_message"]

            # save file measurement
            # check for multi-test
            die = int(dieActual) - 1
            module = int(moduleActual) - 1
            variables = self.waferwindow.meas_result[die][module]["variables"]
            list_check = isinstance(variables, list)
            if not list_check:
                file_measurement.MeasurementSectionFile(section="MODTEST", tag="BEG")
                file_measurement.MeasurementVariablesFile(variables)
                file_measurement.MeasurementSectionFile(section="MODTEST", tag="END")
            else:
                count = 1
                for var in variables:
                    file_measurement.MeasurementSectionFile(section="MODTEST", tag="BEG", modtest=count)
                    file_measurement.MeasurementVariablesFile(var)
                    file_measurement.MeasurementSectionFile(section="MODTEST", tag="END", modtest=count)
                    count += 1

    def init_prober(self):

        # 1) load prober file
        filename_prober = self.get_filename_prober()
        if filename_prober != "":
            self.run(filename_prober, "probers")
            # 2) Loading prober file class prober is available & configure communication
            self.name_prober = self.get_prober_selected()
            # pass all dict to the prober for configuration
            if self.name_prober != "":
                nameprober = self.name_prober
                self.prober = eval(nameprober)(probers[nameprober])

    def parameters_config(self):
        instrument_selected = self.get_instrument_selected()
        if instrument_selected != "":
            filename_parameters = os.path.join(self.getDirs("tests"), instrument_selected,
                                               self.get_filename_test().replace("_test.py", ".toml"))
            if os.path.exists(filename_parameters):
                self.parameterwindow = ParametersWindow(filename_parameters)
                if not self.parameterwindow.error:
                    try:
                        self.parameterwindow.show()
                    except Exception as e:
                        print(str(e))
                else:
                    retval = messageBox(self, "Error getting parameters from file", self.parameterwindow.error_message,
                                        "critical")

    def execute_cartographic_measurement(self):
        global measurement_status, wafer_parameters, test_status, contact_status, contact_test, contact_errors, actual_height, file_measurement
        global dieActual, moduleActual
        global total_meas  # dict with meas, in , out, meas_success, meas_warning & meas_error numbers

        contact_errors = 0
        test_status.status = "STARTED"
        self.toggle_widgets(False)
        # load ppg file
        self.run(self.get_filename_wafermap(), "wafermaps")
        # 0) create wafer class & check wafer parameters
        wafer = Wafer(wafer_parameters)
        if wafer.check_wafer_parameters():
            # then we can start with the process
            self.updateTextDescription("- Wafer parameters loaded for " + wafer.wafer_name + "...")
            total_chips = int(wafer.nchips)

            init_chip = int(wafer_parameters.get("init_chip", 1))  # por defecto 1
            end_chip = int(wafer_parameters.get("end_chip", total_chips))  # por defecto último chip
            widgets.dieActual.setText(str(int(init_chip)))
            widgets.dieTotal.setText(str(int(end_chip)))
            widgets.moduleActual.setText("1")
            widgets.moduleTotal.setText(str(int(wafer.nmodules)))
            try:
                self.init_prober()
                idn = ""
                if self.prober != "":
                    idn = self.prober.idn()
                if idn != "":
                    self.updateTextDescription("- Prober " + self.name_prober + " class loaded...<br />" + idn)
                    # 3) Check vacuum
                    vacuum = self.prober.get_vacuum_status("Wafer")
                    if str(vacuum) == "0":
                        retval = messageBox(self, "Not vacuum detected",
                                            "Do you want to continue the cartographic process anyway?", "question")
                        if retval == QMessageBox.Yes:
                            vacuum = "1"
                            self.updateTextDescription("- Vacuum not detected but continue...")
                    else:
                        self.updateTextDescription("- Vacuum detected...")

                    if str(vacuum) == "1":
                        # 4) put message to user to advice process
                        retval = messageBox(self, "Cartographic process starting",
                                            "Please, check you are in HOME position. The system will go to the ORIGIN position and starts process automatically! Are you ready?",
                                            "question")
                        if retval == QMessageBox.Yes:
                            self.prober.move_separation()
                            contact_status.status = "SEPARATION"
                            # move origin to home
                            # We are in HOME position and will go to ORIGIN 
                            # check if we are yet in HOME position, X,Y from Home must be 0,0
                            X, Y = self.prober.get_chuck_xy("Home")
                            if float(X) == 0.0 and float(Y) == 0.0:
                                # if yes we go to ORIGIN
                                X, Y = wafer.calculate_init_prober_movement()
                            else:
                                self.updateTextDescription("- Not in HOME position")
                                retval = messageBox(self, "Home detection failed",
                                                    "Do you want to go to the HOME position automatically! Are you ready?",
                                                    "question")
                                if retval == QMessageBox.Yes:
                                    self.prober.move_home()
                                    self.updateTextDescription("- Go to HOME position")
                                    X, Y = wafer.calculate_init_prober_movement()
                                else:
                                    self.updateTextDescription("- Test aborted...")
                                    test_status.status = "ABORTED"


                            if test_status.status != "ABORTED":
                                breaker = False
                                measure_always = True
                                contact_test = 2
                                self.updateTextDescription("- Test started...")
                                test_status.status = "STARTED"

                                if probers[self.name_prober]["progressive_contact"]["enable"]:
                                    # get variables to progressive contact
                                    step = float(probers[self.name_prober]["progressive_contact"]["steps"])
                                    max_tries = float(probers[self.name_prober]["progressive_contact"]["max_tries"])
                                    reach_contact = float(
                                        probers[self.name_prober]["progressive_contact"]["reach_contact"])
                                    measure_always = float(
                                        probers[self.name_prober]["progressive_contact"]["measure_always"])
                                    heights = self.prober.get_chuck_site_heights("Wafer")
                                    contact_height = float(heights[0])
                                    separation_height = float(heights[1])
                                    overtravel_height = float(heights[2])
                                    hover_height = float(heights[3])
                                    difference_height = contact_height - separation_height
                                    step_height = difference_height / step
                                    actual_height = separation_height
                                date_init = datetime.now()
                                date_today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                                widgets.timeInit.setText(date_today)
                                widgets.timeFinish.setText("")
                                # View wafermap if checked & create self.waferwindow
                                self.view_wafermap(False)
                                total_meas = self.waferwindow.total_meas()  # update totals
                                # Create BEG WAFER section
                                file_measurement.MeasurementSectionFile(section="WAFER", tag="BEG")
                                # Control init chip in wafer parameters (case fail wafers or semi-wafers)
                                init_chip = 1
                                if "init_chip" in wafer_parameters and wafer_parameters["init_chip"] != "1":
                                    # set first position to init_chip
                                    init_chip = wafer_parameters["init_chip"]
                                    dieActual = str(init_chip)
                                    # go to init chip from home
                                    from_coordinate = wafer.wafer_positions[0]
                                    to_coordinate = wafer.wafer_positions[int(init_chip) - 2]
                                    X, Y = wafer.calculate_prober_movement(from_coordinate, to_coordinate)
                                    self.prober.move_chuck_xy("R", X, Y)



                                # Validaciones
                                if not (1 <= init_chip <= total_chips):
                                    raise ValueError(
                                        f"init_chip debe estar entre 1 y {total_chips}, recibido: {init_chip}")

                                if not (1 <= end_chip <= total_chips):
                                    raise ValueError(
                                        f"end_chip debe estar entre 1 y {total_chips}, recibido: {end_chip}")

                                if init_chip > end_chip:
                                    raise ValueError(
                                        f"init_chip ({init_chip}) no puede ser mayor que end_chip ({end_chip})")

                                # Construcción del rango
                                chip_range = range(init_chip - 1, end_chip)  # -1 porque el índice interno empieza en 0

                                for die in chip_range:
                                    die_position = self.waferwindow.wafer_parameters["wafer_positions"][die]
                                    dieActual = str(die + 1)
                                    widgets.dieActual.setText(dieActual)
                                    # Create BEG DIE section
                                    file_measurement.MeasurementSectionFile(section="DIE", tag="BEG",
                                                                            die_position=die_position)
                                    QApplication.processEvents()
                                    if die > 0:
                                        # get movement XY
                                        from_coordinate = wafer.wafer_positions[die - 1]
                                        to_coordinate = wafer.wafer_positions[die]
                                        X, Y = wafer.calculate_prober_movement(from_coordinate, to_coordinate)
                                    # prober move to die coordinates
                                    self.prober.move_chuck_xy("R", X, Y)
                                    # if int(wafer.nmodules) > 1:
                                    #     menu_modules = QMenu()
                                    x_modules_sum = 0.0
                                    y_modules_sum = 0.0
                                    for module in range(int(wafer.nmodules)):
                                        if "wafer_modules_name" in self.waferwindow.wafer_parameters:
                                            module_position = self.waferwindow.wafer_parameters["wafer_modules_name"][module]
                                        else:
                                            module_position = self.waferwindow.wafer_parameters["wafer_modules"][module]
                                        moduleActual = str(module + 1)
                                        widgets.moduleActual.setText(moduleActual)
                                        # Create BEG MODULE section
                                        file_measurement.MeasurementSectionFile(section="MODULE", tag="BEG",
                                                                                module_position=module_position)
                                        QApplication.processEvents()
                                        pos_XY_to = wafer.wafer_modules[module].split()  # get XY pos
                                        self.prober.move_chuck_xy("R", pos_XY_to[0], pos_XY_to[1])
                                        x_modules_sum += float(pos_XY_to[0])
                                        y_modules_sum += float(pos_XY_to[1])
                                        # prober contact
                                        if probers[self.name_prober]["progressive_contact"]["enable"]:
                                            contact_status.status = "IDLE"
                                            for h in np.arange(separation_height, contact_height, step_height):
                                                QApplication.processEvents()
                                                actual_height = self.prober.move_chuck_z("Relative", step_height)
                                                self.run(probers[self.name_prober]["progressive_contact"]["program"],
                                                         "probers")
                                                if contact_test != 0:
                                                    break
                                            if contact_test == 2:
                                                contact_status.status = "CONTACT_PROGRESSIVE"
                                                QApplication.processEvents()
                                            if contact_test == 1:
                                                for tries in range(0, int(max_tries)):
                                                    QApplication.processEvents()
                                                    actual_height = self.prober.get_chuck_z("Zero")
                                                    if float(actual_height) + float(step_height) < float(
                                                            contact_height):
                                                        actual_height = self.prober.move_chuck_z("Relative",
                                                                                                 step_height)
                                                    else:
                                                        actual_height = self.prober.move_contact()
                                                    self.run(
                                                        probers[self.name_prober]["progressive_contact"]["program"],
                                                        "probers")
                                                    if contact_test == 2:
                                                        contact_status.status = "CONTACT_PROGRESSIVE"
                                                        QApplication.processEvents()
                                                        break
                                            if contact_test != 2:
                                                # contact not ok (0 or 1)
                                                actual_height = self.prober.get_chuck_z("Zero")
                                                # last try?
                                                if float(actual_height) < float(contact_height) and reach_contact:
                                                    # try to reach contact with move_contact
                                                    actual_height = self.prober.move_contact()
                                                    contact_status.status = "CONTACT"
                                                    self.run(
                                                        probers[self.name_prober]["progressive_contact"]["program"],
                                                        "probers")

                                        else:
                                            actual_height = self.prober.get_chuck_z("Zero")
                                            self.prober.move_contact()
                                            contact_status.status = "CONTACT"
                                        # testing
                                        if measure_always or contact_test == 2:
                                            # contact_status.status = "CONTACT"
                                            actual_height = self.prober.get_chuck_z("Zero")
                                            self.updateTextDescription(
                                                "- Testing die " + dieActual + " & module " + moduleActual + "<br />" + "Contact height: " + str(
                                                    actual_height) + "um")
                                            # execute measure
                                            measurement_status.status = "START"
                                            QApplication.processEvents()
                                            self.execute_measurement()
                                            while measurement_status.status != "FINISH":
                                                QApplication.processEvents()
                                                QThread.msleep(50)  # pequeño delay para no saturar la CPU
                                            QApplication.processEvents()
                                        # Create END MODULE section
                                        file_measurement.MeasurementSectionFile(section="MODULE", tag="END",
                                                                                module_position=module_position)

                                        # prober separation
                                        self.prober.move_separation()
                                        contact_status.status = "SEPARATION"
                                        if test_status.status == "PAUSED":
                                            self.updateTextDescription(
                                                "- Test paused, press START button to continue...")
                                            while (test_status.status == "PAUSED"):
                                                QApplication.processEvents()
                                                time.sleep(1)

                                        if test_status.status == "ABORTED":
                                            self.updateTextDescription("- Test aborted...")
                                            breaker = True
                                            break
                                        # update percentage & finish time estimation
                                        percentage = wafer.calculate_process_percentage(dieActual, moduleActual, init_chip, end_chip)
                                        finish_time = wafer.calculate_finish_time(date_init, dieActual, moduleActual, init_chip, end_chip)
                                        widgets.progressBar.setValue(percentage * 100)
                                        widgets.progressBar.setFormat('%.02f %%' % percentage)
                                        widgets.timeFinish.setText(finish_time)
                                        # update meas_result in btn waferwindow
                                        real_origin_chip = self.waferwindow.wafer_parameters["real_origin_chip"]
                                        coord = self.waferwindow.wafer_parameters["wafer_positions"][die]
                                        x, y = coord.split()
                                        x = int(x) * -1
                                        y = int(y) * -1
                                        coord_to_origin = change_coord_to_origin(x, y, real_origin_chip)
                                        coord_x, coord_y = coord_to_origin.split()
                                        btnName = get_btnName(int(coord_x), int(coord_y))
                                        waferwindow_btn = self.waferwindow.centralWidget().findChild(QPushButton,
                                                                                                     btnName)
                                        waferwindow_btn.btnType = self.waferwindow.meas_result[die][module]["status"]
                                        waferwindow_btn.message = self.waferwindow.meas_result[die][module]["message"]
                                        # contact_height set here, other in test
                                        self.waferwindow.meas_result[die][module]["contact_height"] = str(actual_height)
                                        # volvemos a comprobar estados check
                                        self.show_wafermap()
                                        plot_parameters = self.waferwindow.meas_result[die][module]["plot_parameters"]

                                        # show graph in same window
                                        self.show_graph(plot_parameters)
                                        QApplication.processEvents()
                                        # update total_meas info
                                        total_meas = self.waferwindow.total_meas()  # update totals
                                        QApplication.processEvents()
                                    # Create END DIE section

                                    file_measurement.MeasurementSectionFile(section="DIE", tag="END",
                                                                            die_position=die_position)

                                    # GO BACK to 0.0 if nmodules > 1
                                    if int(wafer.nmodules) > 1:
                                        self.prober.move_chuck_xy("R", x_modules_sum * -1, y_modules_sum * -1)
                                    if breaker:
                                        break

                                test_status.status = "FINISHED"
                                # Create END WAFER section
                                file_measurement.MeasurementSectionFile(section="WAFER", tag="END")
                                # print(self.waferwindow.meas_result)
                        else:
                            test_status.status = "FINISHED"
                    else:
                        self.updateTextDescription("=> Error checking vacuum")
                        retval = messageBox(self, "Error checking vacuum", "Vacuum not detected!", "critical")
                        self.change_state_process("STOP")
                else:
                    self.updateTextDescription("=> Error loading prober file")
                    retval = messageBox(self, "Error loading prober file", "Prober class doesn't exists!", "critical")
                    self.change_state_process("STOP")
            except Exception as ex:
                self.updateTextDescription("=> Error in cartographic process")
                retval = messageBox(self, "Error in cartographic process", "Some error occurs during the process!\n" + str(ex),
                                    "critical")
                self.change_state_process("STOP")
        else:
            self.updateTextDescription("=> Error checking wafer parameters")
            retval = messageBox(self, "Error checking wafer parameters", "Please, review the wafer file parameters...",
                                "warning")
            self.change_state_process("STOP")
        # n = 0
        # while measurement_state == MeasurementState.START or measurement_state == MeasurementState.PAUSE:
        #     time.sleep(0.5)
        #     QApplication.processEvents()
        #     widgets.progressBar.setValue(n)
        #     if measurement_state == MeasurementState.START:
        #         n += 1
        self.toggle_widgets(True)

    def show_wafermap(self):
        if widgets.chkViewPosition.isChecked():
            self.waferwindow.show()

    def getDirs(self, dirname):
        # get Dirs from config.toml
        if dirname != "results":
            return os.path.join(os.getcwd(), self.config["dirs"]["base"], self.username, self.config["dirs"][dirname])
        else:
            return os.path.join(os.getcwd(), self.config["dirs"][dirname], self.username)

    def getFiles(self, filename):
        # get Files from config.toml
        return os.path.join(os.getcwd(), self.config["files"][filename])

    def load_wafermaps(self):
        global widgets
        dir_wafermaps = self.getDirs("wafermaps") + "/"
        contenido = os.listdir(dir_wafermaps)
        widgets.cmbWafermaps.clear()
        widgets.cmbWafermaps.addItem("Select wafermap")
        for fichero in contenido:
            if os.path.isfile(os.path.join(dir_wafermaps, fichero)) and fichero.endswith('_wafermap.py'):
                widgets.cmbWafermaps.addItem(fichero.replace("_wafermap.py", ""))

    def load_probers(self):
        global widgets
        dir_probers = self.getDirs("probers") + "/"
        contenido = os.listdir(dir_probers)
        widgets.cmbProbers.clear()
        widgets.cmbProbers_2.clear()
        widgets.cmbProbers.addItem("Select prober")
        widgets.cmbProbers_2.addItem("Select prober")
        for fichero in contenido:
            if os.path.isfile(os.path.join(dir_probers, fichero)) and fichero.endswith('_prober.py'):
                widgets.cmbProbers.addItem(fichero.replace("_prober.py", ""))
                widgets.cmbProbers_2.addItem(fichero.replace("_prober.py", ""))

    def load_instruments(self):
        global widgets
        dir_instruments = self.getDirs("instruments") + "/"
        contenido = os.listdir(dir_instruments)
        widgets.cmbInstruments.clear()
        widgets.cmbInstruments_2.clear()
        widgets.cmbInstruments.addItem("Select instrument")
        widgets.cmbInstruments_2.addItem("Select instrument")
        for fichero in contenido:
            if os.path.isfile(os.path.join(dir_instruments, fichero)) and fichero.endswith('_instrument.py'):
                widgets.cmbInstruments.addItem(fichero.replace("_instrument.py", ""))
                widgets.cmbInstruments_2.addItem(fichero.replace("_instrument.py", ""))

    def load_tests(self):
        global widgets
        instrument_selected = widgets.cmbInstruments.currentText()

        if widgets.cmbInstruments.currentIndex() > 0:
            dir_tests = self.getDirs("tests") + "/" + instrument_selected + "/"
            dirExist = os.path.exists(dir_tests)
            if not dirExist:
                os.makedirs(dir_tests)
            contenido = os.listdir(dir_tests)
            widgets.cmbTests.clear()
            widgets.cmbTests.addItem("Select test")
            for fichero in contenido:
                if os.path.isfile(os.path.join(dir_tests, fichero)) and fichero.endswith('_test.py'):
                    widgets.cmbTests.addItem(fichero.replace("_test.py", ""))
        else:
            widgets.cmbTests.clear()
            widgets.cmbTests.addItem("Select test")

    def load_reports(self):
        global widgets
        dir_reports = self.getDirs("reports") + "/"
        contenido = os.listdir(dir_reports)
        widgets.cmbReports.clear()
        widgets.cmbReports.addItem("Select report")
        for fichero in contenido:
            if os.path.isfile(os.path.join(dir_reports, fichero)) and fichero.endswith('_report.py'):
                widgets.cmbReports.addItem(fichero.replace("_report.py", ""))

    def get_test(self):
        global widgets
        if widgets.cmbTests.currentIndex() > 0:
            self.set_test_description()
        else:
            widgets.pteTest.setPlainText("")

    def get_wafermap(self):
        global widgets
        if widgets.cmbWafermaps.currentIndex() > 0:
            self.set_wafermap_description()
        else:
            widgets.pteWafermap.setPlainText("")

    def get_filename_test(self):
        global widgets
        test_selected = self.get_test_selected()
        instrument_selected = self.get_instrument_selected()
        if instrument_selected != "" and test_selected != "":
            return test_selected + "_test.py"
        return ""

    def get_filename_wafermap(self):
        global widgets
        wafermap_selected = self.get_wafermap_selected()
        if wafermap_selected != "":
            return wafermap_selected + "_wafermap.py"
        return ""

    def get_filename_prober(self):
        global widgets
        prober_selected = self.get_prober_selected()
        if prober_selected != "":
            return prober_selected + "_prober.py"
        return ""

    def get_filename_report(self):
        global widgets
        report_selected = self.get_report_selected()
        if report_selected != "":
            return report_selected + "_report.py"
        return ""

    def get_test_selected(self):
        global widgets
        if widgets.cmbTests.currentIndex() > 0:
            return widgets.cmbTests.currentText()
        return ""

    def get_instrument_selected(self):
        global widgets
        if widgets.cmbInstruments.currentIndex() > 0:
            return widgets.cmbInstruments.currentText()
        return ""

    def get_prober_selected(self):
        global widgets
        if widgets.cmbProbers.currentIndex() > 0:
            return widgets.cmbProbers.currentText()
        return ""

    def get_wafermap_selected(self):
        global widgets
        if widgets.cmbWafermaps.currentIndex() > 0:
            return widgets.cmbWafermaps.currentText()
        return ""

    def get_report_selected(self):
        global widgets
        if widgets.cmbReports.currentIndex() > 0:
            return widgets.cmbReports.currentText()
        return ""

    def get_base_path(self, folder=""):
        global username
        get_base_path = os.path.join(os.getcwd(), "config", username, folder)
        if folder != "":
            get_base_path = get_base_path + "/"
        return get_base_path

    def set_test_description(self):
        global widgets
        test_selected = self.get_test_selected()
        instrument_selected = self.get_instrument_selected()
        widgets.pteTest.setPlainText("")
        # read file
        dir_tests = self.getDirs("tests") + "/" + instrument_selected + "/"
        namefile = dir_tests + test_selected + "_test.py"
        #namefile = namefile.replace("/", "\\")
        f = open(namefile, "r")
        widgets.pteTest.setPlainText(f.read())
        f.close()

    def set_wafermap_description(self):
        global widgets
        wafermap_selected = self.get_wafermap_selected()
        widgets.pteWafermap.setPlainText("")
        if wafermap_selected != "":
            # read file
            dir_wafermaps = self.getDirs("wafermaps") + "/"
            namefile = dir_wafermaps + wafermap_selected + "_wafermap.py"
            #namefile = namefile.replace("/", "\\")
            f = open(namefile, "r")
            widgets.pteWafermap.setPlainText(f.read())
            f.close()

    def save_process_description(self):
        global widgets
        texto = widgets.pteDescription.toPlainText()
        print(texto)
        destFile = self.getFiles("process")
        with open(destFile, 'w') as f:
            f.write(texto)

    def clear_process_description(self):
        global widgets
        widgets.pteDescription.setPlainText("")

    def view_wafermap(self, enable):
        global widgets, wafer_parameters
        filename_wafermap = self.get_filename_wafermap()
        if filename_wafermap != "":
            self.run(self.get_filename_wafermap(), "wafermaps")
            wafer = Wafer(wafer_parameters)
            if not wafer.wafer_error:
                self.waferwindow = wafer.create_wafer_window(enable)
                if widgets.chkViewPosition.isChecked():
                    self.waferwindow.show()
                    self.waferwindow.total_meas()
                else:
                    #retval = messageBox(self, "Wafermap not view", "Activate check to view wafermap", "warning")
                    # message yes or no to activate check to view Position
                    retval = messageBox(self, "Wafermap not view", "Activate check to view wafermap", "question")
                    if retval == QMessageBox.Yes:
                        widgets.chkViewPosition.setChecked(True)
                        self.waferwindow.show()
                        self.waferwindow.total_meas()
            else:
                retval = messageBox(self, "Wafermap error", "Error loading wafermap", "warning")

        else:
            retval = messageBox(self, "Wafermap not selected", "Please, select a wafermap first...", "warning")

    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        # self.dragPos = event.globalPos()
        p = event.globalPosition()
        globalPos = p.toPoint()
        self.dragPos = globalPos

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            pass
            # print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            pass
            # print('Mouse click: RIGHT CLICK')


# ///////////////////////////////////////////////////////////////
# class SplashScreen & LoginWindow
# ///////////////////////////////////////////////////////////////

class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        # REMOVE TITLE BAR
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # IMPORT circular progress
        self.progress = CircularProgress()
        self.progress.width = 270
        self.progress.height = 270
        self.progress.value = 0  # init to 0%
        # Fix the position
        self.progress.setFixedSize(self.progress.width, self.progress.height)
        self.progress.move(15, 15)

        self.progress.font_size = 40
        self.progress.add_shadow(True)
        self.progress.bg_color = QColor(68, 71, 90, 140)
        self.progress.text_color = QColor(98, 114, 164)
        self.progress.progress_color = QColor(98, 114, 164)
        self.progress.setParent(self.ui.centralwidget)
        self.progress.show()

        # add DRROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.setGraphicsEffect(self.shadow)

        # TIMER (desactivado para control por login)
        self.timer = QTimer()
        # Variables de control para el login
        self.ok = 0
        self.user_id = 0
        self.password_db = ""
        counter = 0
        errorLogin = False
        self.timer.timeout.connect(self.update)
        self.timer.start(30)
        self.show()

    # UPDATE PROGRESS BAR
    def update(self):
        global counter
        global username, password
        global user_id_db, username_db, email_db
        global errorLogin
        global connection

        # pass for ssanchez in Labs table: Labs12345

        # set value to progress bar
        self.progress.set_value(counter)
        # verify username exists
        if counter == 0:
            err_text = ""
            try:
                connection = mysql.connector.connect(host=mysqlhost, database=mysqldatabase, user=mysqluser,
                                                     password=mysqlpassword)
                if connection.is_connected():
                    db_Info = connection.get_server_info()
                    self.ui.lblStatus.setText("Connected to MySQL Server v." + db_Info)
                else:
                    self.ui.lblStatus.setText("Not connected to MySQL Server")
                    errorLogin = True

            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    err_text = "Something is wrong with your MySQL user/password"
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    err_text = "Database does not exist"
                else:
                    err_text = err
                self.ui.lblStatus.setText("MySQL error: " + str(err_text))
                print("MySQL error: " + str(err_text))
                errorLogin = True

        if counter == 33:
            # USER VERIFY
            if not errorLogin:
                # try to connect to users table
                try:
                    cursor = connection.cursor()
                    query = "SELECT count(*) as ok, id as user_id, password, username, email FROM users WHERE username='" + username + "' OR email='" + username + "' GROUP BY id"
                    # password_hexhash = hashlib.sha512(password.encode()).hexdigest()
                    cursor.execute(query)
                    result = cursor.fetchall()
                    for row in result:
                        self.ok = row[0]
                        self.user_id = row[1]
                        self.password_db = row[2]
                        user_id_db = row[1]
                        username_db = row[3]
                        email_db = row[4]
                    if self.ok == 1:
                        self.ui.lblStatus.setText("User exists!")
                    elif str(self.ok) == "0":
                        self.ui.lblStatus.setText("Sorry, user '" + username + "' doesn't exists!")
                        errorLogin = True
                    else:
                        self.ui.lblStatus.setText("Error, more than one user!")
                        errorLogin = True
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                        err_text = "Something is wrong with your user name"
                    elif err.errno == errorcode.ER_BAD_DB_ERROR:
                        err_text = "Database does not exist"
                    elif err.errno == 2003:
                        err_text = "Can't connect to MySQL Server"
                    else:
                        err_text = err
                    self.ui.lblStatus.setText("MySQL error: " + str(err_text))
                    print("MySQL error: " + str(err_text))
                    errorLogin = True

        if counter == 50:
            # PASSWORD VERIFY
            if not errorLogin:
                if bcrypt.checkpw(password.encode(), self.password_db.encode()):
                    self.ui.lblStatus.setText("User login correctly!")
                else:
                    self.ui.lblStatus.setText("Password doesn't match!")
                    errorLogin = True
        if counter == 75:
            if not errorLogin:
                # user exists, verify active status
                try:
                    cursor = connection.cursor()
                    query = "SELECT count(*) as ok, user_id FROM user_details WHERE user_id=" + str(
                        self.user_id) + " and active=1 and disabled=0"
                    cursor.execute(query)
                    result = cursor.fetchall()
                    for row in result:
                        self.ok = row[0]
                    if self.ok == 1:
                        self.ui.lblStatus.setText("User is active!")
                    else:
                        self.ui.lblStatus.setText("Sorry, user is not active!")
                        errorLogin = True
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                        err_text = "Something is wrong with your user name or password"
                    elif err.errno == errorcode.ER_BAD_DB_ERROR:
                        err_text = "Database does not exist"
                    else:
                        err_text = err
                    self.ui.lblStatus.setText("MySQL error: " + str(err_text))
                    print("MySQL error: " + str(err_text))
                    errorLogin = True

        if counter == 90:
            connection.close()
            self.ui.lblStatus.setText("MySQL connection is closed")
        # CLOSE SPLASH SCREEN AND OPEN MAIN APP
        if counter >= 100:
            # stop timer
            self.timer.stop()
            # show main window
            self.main = MainWindow()
            self.main.show()
            # close splash screen
            self.close()

        counter += 1

        if errorLogin:
            self.ui.lblStatus.setStyleSheet("color: #ff5555");  # red color
            self.progress.set_value(counter)  # para refresh
            # Volvemos a pantalla login
            self.timer.stop()
            time.sleep(3)
            self.ui.lblStatus.setText("")
            self.destroy()
            self.login = LoginWindow()
            self.login.show()
            self.login.ui.username.setText(username)
            self.login.ui.password.setText(password)


class LoginWindow(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)

        def moveWindow(event):
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos - self.dragPos)
                self.dragPos == event.globalPos()
                event.accept()

        # REMOVE TITLE BAR
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # connect buttons minimize & close
        self.ui.btnClose.clicked.connect(self.close_window)
        self.ui.btnMinimize.clicked.connect(self.minimize_window)
        self.ui.btnToggle.clicked.connect(self.toggle_password)

        # connect login button
        self.ui.btnLogin.clicked.connect(self.login_function)

        # default values
        self.ui.username.setText("sergi.sanchez@imb-cnm.csic.es")
        # put icon eye
        self.ui.password

        self.ui.version.mouseMoveEvent = moveWindow

        # set version in splash screen
        self.ui.version.setText(version)
        self.offset = QPoint()
        self.show()

    def toggle_password(self):
        if self.ui.password.echoMode() == QLineEdit.Normal:
            self.ui.password.setEchoMode(QLineEdit.Password)
        else:
            self.ui.password.setEchoMode(QLineEdit.Normal)

    def minimize_window(self):
        self.showMinimized()

    def close_window(self):
        self.waferwindow.moduleswindow.close()
        self.waferwindow.close()
        self.close()
        QCoreApplication.quit()

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        # offset from top left corner
        # p = event.globalPosition();
        # offset = p.toPoint()

        self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def login_function(self):
        global username, password, counter, errorLogin
        username = self.ui.username.text()
        password = self.ui.password.text()

        self.splash = SplashScreen()
        counter = 0
        errorLogin = False
        self.splash.show()
        self.destroy()
        self.splash.ui.version.setText(version)
        self.splash.ui.lblStatus.setText("Verifying log in access...")


class MeasurementStatus(MainWindow):
    def __init__(self):
        self._status = "IDLE"

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value == "IDLE" or value == "START" or value == "PAUSE" or value == "STOP" or value == "FINISH":
            self._status = value
            if value == "IDLE":
                widgets.measurement_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: #333333; border-radius: 10px;}')
            if value == "START":
                widgets.measurement_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: green; border-radius: 10px;}')
            if value == "PAUSE":
                widgets.measurement_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: orange; border-radius: 10px;}')
            if value == "STOP":
                widgets.measurement_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: red; border-radius: 10px;}')
            if value == "FINISH":
                widgets.measurement_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: blue; border-radius: 10px;}')

            widgets.measurement_status.setToolTip(value)

    @status.deleter
    def status(self):
        del self._status


class TestStatus(MainWindow):
    def __init__(self):
        self._status = "IDLE"

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value == "IDLE" or value == "STARTED" or value == "PAUSED" or value == "ABORTED" or value == "FINISHED":
            self._status = value
            if value == "IDLE":
                widgets.test_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: #333333; border-radius: 10px;}')
            if value == "STARTED":
                widgets.test_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: green; border-radius: 10px;}')
            if value == "PAUSED":
                widgets.test_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: orange; border-radius: 10px;}')
            if value == "ABORTED":
                widgets.test_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: red; border-radius: 10px;}')
            if value == "FINISHED":
                widgets.test_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: blue; border-radius: 10px;}')

            widgets.test_status.setToolTip(value)

    @status.deleter
    def status(self):
        del self._status


class ContactStatus(MainWindow):
    def __init__(self):
        self._contact = "IDLE"

    @property
    def contact(self):
        return self._contact

    @contact.setter
    def contact(self, value):
        if value == "IDLE" or value == "CONTACT" or value == "SEPARATION" or value == "CONTACT_PROGRESSIVE":
            self._contact = value
            widgets.contact_status.setToolTip("IDLE")
            widgets.separation_status.setToolTip("IDLE")
            if value == "IDLE":
                widgets.contact_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: #333333; border-radius: 10px;}')
                widgets.separation_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: #333333; border-radius: 10px;}')
            if value == "CONTACT":
                widgets.contact_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: green; border-radius: 10px;}')
                widgets.separation_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: #333333; border-radius: 10px;}')
                widgets.contact_status.setToolTip(value)
            if value == "SEPARATION":
                widgets.separation_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: green; border-radius: 10px;}')
                widgets.contact_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: #333333; border-radius: 10px;}')
                widgets.separation_status.setToolTip(value)
            if value == "CONTACT_PROGRESSIVE":
                # almost in contact (progressive contact)
                widgets.contact_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: orange; border-radius: 10px;}')
                widgets.separation_status.setStyleSheet(
                    'QLabel {font: 8pt "Segoe UI"; background-color: #333333; border-radius: 10px;}')
                widgets.contact_status.setToolTip(value)

    @contact.deleter
    def status(self):
        del self._contact


class Canvas(QLabel):

    def __init__(self):
        super().__init__()
        self.pen_color = None
        pixmap = QPixmap(600, 300)
        self.setPixmap(pixmap)

        self.last_x, self.last_y = None, None
        # self.pen_color = QColor('#000000')
        self.set_pen_color('#000000')

    def set_pen_color(self, c):
        self.pen_color = QColor(c)

    def mouseMoveEvent(self, e):
        """
        mouseMoveEvent overrides
        :param e:
        :return:
        """
        if self.last_x is None:  # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return  # Ignore the first time.

        painter = QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(4)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(QPixmap("images/caracterizar.png")))
    window = MainWindow()  # MainWindow or LoginWindow
    main = window
    sys.exit(app.exec())
