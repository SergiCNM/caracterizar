# CAP report
import os
import io, sys
import importlib

from PySide6.QtWidgets import QFileDialog

from functions import messageBox
from modules import ResultFile

# FOR testing
if 'config.default.reports' in sys.modules:
    del sys.modules['config.default.reports']

if 'config.default.reports.CAP' in sys.modules:
    del sys.modules['config.default.reports.CAP']

from config.default.reports import CAP
from fpdf import FPDF
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

import datetime


def order_wafer(elem):
    return int(elem.split("-")[1])

# report options
options = {"wafermap": True, "histogram": True, "plot": True,
           "cap_data": True, "cap_image": True, "cap_plot": True,
           "data_folder": 'data', "image_folder": 'photos', "plot_folder": 'plots', "comparative": "comparative"}

exists_result_file = False
filename_results = ""

directoryName = QFileDialog.getExistingDirectory(self, "Select RUN folder", results_dir, QFileDialog.ShowDirsOnly)
if directoryName != "":
    wafers_list = list()
    for dir in os.listdir(directoryName):
        if os.path.isdir(directoryName + "/" + dir):
            if "comparative" in options and dir != options["comparative"]:
                wafers_list.append(dir)
    if len(wafers_list) > 0:
        exists_result_file = True
        for wafer in wafers_list:
            filename_results = directoryName + "/" + wafer + "/" + wafer + ".dat"
            if not os.path.isfile(filename_results):
                exists_result_file = False
                break

get_report = False
if exists_result_file:
    get_report = True
else:
    if filename_results != "":
        messageBox(self, "Result file error", "Result file: " + filename_results + " doesn't exists in this path!",
                   "info")

if get_report:
    try:
        widgets.txtResultReport.setPlainText("")
        QApplication.processEvents()
        # create pdf file in directoryName
        filename_pdf = directoryName + "/" + os.path.basename(os.path.normpath(directoryName)) + ".pdf"
        widgets.txtResultReport.appendPlainText("Checking information and creating plot graphs...")
        QApplication.processEvents()
        CAP = CAP(widgets, options, directoryName, self.config)
        for wafer in sorted(CAP.wafers, key=order_wafer):
            dir_wafer = directoryName + "/" + wafer
            dir_data = dir_wafer + "/" + options["data_folder"]
            filename_results = dir_wafer + "/" + wafer + ".dat"
            widgets.txtResultReport.appendPlainText("Creating report CAP for wafer " + wafer + " ...")
            QApplication.processEvents()
            result_file = ResultFile(filename_results)
            # 1) TRANSFORM dat old format to metrics format
            if result_file.mode_type == "old":
                # pass to metrics format, generate metrics, rename to old
                parameters = result_file.get_parameters()

                # fill operator & mask name
                if parameters["mask_name"] == "":
                    parameters["mask_name"] = self.ui.txtMask.text()
                if parameters["operator_name"] == "":
                    parameters["operator_name"] = username
                if parameters["filename_test"] == "":
                    parameters["filename_test"] = "CV"
                if "waferinfo" not in parameters:
                    parameters["waferinfo"] = ""
                filename = dir_wafer + "/" + wafer + "_metrics"  # without extension .dat
                measurement_file = MeasurementFile(parameters, filename)
                if not measurement_file.created:
                    messageBox(self, "Error creating object",
                               "Measurement object nor created.\n" + measurement_file.error_message, "info")
                else:
                    measurement_file.MeasurementHeaderFile(True)  # overwrite
                    if not measurement_file.created:
                        messageBox(self, "Error creating file", measurement_file.error_message, "info")
                    else:
                        # construct measurement file
                        measurement_file.MeasurementSectionFile(section="WAFER", tag="BEG")
                        for number_die, die in enumerate(result_file.dies):
                            measurement_file.MeasurementSectionFile(section="DIE", tag="BEG", die_position=die)
                            for number_module, module in enumerate(result_file.modules):
                                measurement_file.MeasurementSectionFile(section="MODULE", tag="BEG",
                                                                        module_position=module)
                                variables = dict()
                                variables["params"] = list()
                                variables["data"] = list()
                                # get data from files (V, C & G)
                                # name file: CV_15813-1_1_1.txt (wafer 1, die 1, module 1)
                                namefile_data = dir_data + "/CV_" + wafer + "_" + str(number_die + 1) + "_" + str(
                                    number_module + 1) + ".txt"
                                f = open(namefile_data, "r")
                                lines = f.readlines()
                                voltage = []
                                capacitance = []
                                conductance = []
                                for x in lines:
                                    x_array = x.replace("\n", "").split(' ')
                                    voltage.append(x_array[0])
                                    capacitance.append(x_array[1])
                                    conductance.append(x_array[2])
                                f.close()
                                for param, value in result_file.params[die][module].items():
                                    variables["params"].append({"name": param, "value": value})
                                variables["data"].append({"name": "Voltage", "values": voltage, "units": "V"})
                                variables["data"].append({"name": "Capacitance", "values": capacitance, "units": "F"})
                                variables["data"].append({"name": "Conductance", "values": conductance, "units": "S"})
                                measurement_file.MeasurementVariablesFile(variables)
                                measurement_file.MeasurementSectionFile(section="MODULE", tag="END",
                                                                        module_position=module)
                            measurement_file.MeasurementSectionFile(section="DIE", tag="END", die_position=die)
                        measurement_file.MeasurementSectionFile(section="WAFER", tag="END")
                        # rename files .dat to .old
                        os.rename(filename_results, filename_results.replace(".dat", ".old"))
                        # rename files _metrics.dat to .dat
                        filename_metrics = filename + ".dat"
                        os.rename(filename_metrics, filename_metrics.replace("_metrics", ""))
                        # new object result_file with metrics format
                        result_file = ResultFile(filename_results)

            # continue with process with metrics format in filename_results
            # getting info for all parameters
            # 2) Make pdf report for every wafer
            CAP.print_report(wafer)
        # print comparative
        CAP.print_comparative()

        CAP.output(filename_pdf)
        widgets.txtResultReport.appendPlainText("Merging files...")
        QApplication.processEvents()
        # get actual dir
        actual_path = os.path.dirname(os.path.abspath(__file__))
        mask_name = self.ui.txtMask.text()
        path_annex = os.path.join("config", "default", "reports", "assets", "ANEXOCAP_" + mask_name + ".pdf")
        filename_annex = os.path.join(actual_path, path_annex)
        # comprobar si existe el fichero de informe para adjuntar
        path_informe = os.path.join("results", "default", CAP.run, "Informe_" + CAP.run + ".pdf")
        filename_informe = os.path.join(actual_path, path_informe)
        # merge de todos los ficheros
        merger = PdfMerger()
        # comprobar que existen los ficheros filename_informe y filename_annex
        pdfs = [filename_pdf]
        if os.path.exists(filename_informe):
            pdfs.append(filename_informe)
        else:
            widgets.txtResultReport.appendHtml('<br />WARNING: Informe ' + filename_informe + ' not found!<br />')

        if os.path.exists(filename_annex):
            pdfs.append(filename_annex)
        else:
            widgets.txtResultReport.appendHtml('<br />WARNING: Annex ' + filename_annex + ' not found!<br />')
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(filename_pdf.replace(".pdf", "_final.pdf"))
        merger.close()

        widgets.txtResultReport.appendHtml('<br />Report done!<br />')
    except Exception as e:
        widgets.txtResultReport.appendHtml('<br />ERROR: ' + str(e) + '<br />')
