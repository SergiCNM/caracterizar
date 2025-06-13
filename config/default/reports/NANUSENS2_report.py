# BASIC report
import os
import io, sys
import importlib

from PySide6.QtWidgets import QFileDialog

from functions import messageBox
from modules import ResultFile

# FOR testing
if 'config.default.reports' in sys.modules:
    del sys.modules['config.default.reports']

if 'config.default.reports.NANUSENS2' in sys.modules:
    del sys.modules['config.default.reports.NANUSENS2']

from config.default.reports import NANUSENS2
from fpdf import FPDF
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

import datetime

# report options
options = {"wafermap": True, "histogram": True, "plot": True,
           "data": True, "image": True, "plot": True,
           "data_folder": 'data', "image_folder": 'photos', "plot_folder": 'plots', "comparative" : "comparative",
           "excluded_parameters": []}

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
        NANUSENS = NANUSENS2(widgets, options, directoryName, self.config)
        for wafer in NANUSENS.wafers:
            dir_wafer = directoryName + "/" + wafer
            dir_data = dir_wafer + "/" + options["data_folder"]
            filename_results = os.path.join(dir_wafer, wafer + ".dat")
            widgets.txtResultReport.appendPlainText("Creating report NANUSENS for wafer " + wafer + " ...")
            QApplication.processEvents()
            result_file = ResultFile(filename_results)
            print(result_file.info())
            # Make pdf report for every wafer
            NANUSENS.print_report(wafer)
        # print comparative
        # NANUSENS.print_comparative()

        NANUSENS.output(filename_pdf)
        widgets.txtResultReport.appendPlainText("Merging files...")
        QApplication.processEvents()
        filename_annex = "C:\\GITHUB\\Python\\caracterizar\\config\\default\\reports\\assets\\annexNANUSENS2.pdf"
        merger = PdfMerger()
        pdfs = [filename_pdf, filename_annex]
        # pdfs = [filename_pdf]
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(filename_pdf.replace(".pdf", "_final.pdf"))
        merger.close()

        widgets.txtResultReport.appendHtml('<br />Report done!<br />')
    except Exception as e:
        widgets.txtResultReport.appendHtml('<br />ERROR: ' + str(e) + '<br />')

else:
    widgets.txtResultReport.appendPlainText("No report created!")