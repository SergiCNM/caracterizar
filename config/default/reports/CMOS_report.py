# CMOS report
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
    del sys.modules['config.default.reports.CMOS']

from config.default.reports import CMOS
from fpdf import FPDF
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

import datetime

# report options
options = {"wafermap": True, "histogram": True, "plot": True,
           "cmos_data": True, "cmos_image": True, "cmos_plot": True,
           "data_folder": 'data', "image_folder": 'photos', "plot_folder": 'plots', "comparative": "comparative",
           "compensation": True,
           "excluded_parameters": ['idsinvn1', 'idsinvn2', 'idsinvn3', 'idsinvn4', 'idsinvn5', 'idsinvn6', 'idsinvp1', 'idsinvp2', 'idsinvp3', 'idsinvp4', 'idsinvp5', 'idsinvp6']}

exists_result_file = False
filename_results = ""
widgets.txtResultReport.setPlainText("")


def check_file_exists(filename):
    exists_filename = True
    if not os.path.isfile(filename):
        exists_filename = False

    return exists_filename

directoryName = QFileDialog.getExistingDirectory(self, "Select RUN folder", results_dir, QFileDialog.ShowDirsOnly)
print(f"Directory name: {directoryName}")
if directoryName != "":
    wafers_list = list()
    for dir in os.listdir(directoryName):
        if os.path.isdir(directoryName + "/" + dir):
            if "comparative" in options and dir != options["comparative"]:
                wafers_list.append(dir)
    # order wafers list
    wafers_list.sort()
    print(f"Wafers list: {wafers_list}")
    if len(wafers_list) > 0:
        exists_result_file = True
        for wafer in wafers_list:
            if "compensation" in options and options["compensation"]:
                filename_results_C = directoryName + "/" + wafer + "/" + wafer + "_C.dat"  # compensated
                filename_results_NC = directoryName + "/" + wafer + "/" + wafer + "_NC.dat"  # non compensated
                if not check_file_exists(filename_results_C) or not check_file_exists(filename_results_NC):
                    exists_result_file = False
                    break
            else:
                filename_results = directoryName + "/" + wafer + "/" + wafer + ".dat"
                if not check_file_exists(filename_results):
                    exists_result_file = False
                    break
    else:
        widgets.txtResultReport.appendPlainText("No wafers detected...")
get_report = False
if exists_result_file:
    get_report = True
else:
    if filename_results != "":
        messageBox(self, "Result file error", "Result file: " + filename_results + " doesn't exists in this path!",
                   "info")

if get_report:
    try:
        QApplication.processEvents()
        # create pdf file in directoryName
        filename_pdf = directoryName + "/" + os.path.basename(os.path.normpath(directoryName)) + ".pdf"
        widgets.txtResultReport.appendPlainText("Checking information and creating plot graphs...")
        QApplication.processEvents()
        CMOS = CMOS(widgets, options, directoryName, self.config)
        print("Wafers detected")
        print(CMOS.wafers)
        for wafer in CMOS.wafers:
            dir_wafer = directoryName + "/" + wafer.replace("_C", "").replace("_NC", "")
            dir_data = dir_wafer + "/" + options["data_folder"]
            filename_results = dir_wafer + "/" + wafer + ".dat"
            widgets.txtResultReport.appendPlainText("Creating report CMOS for wafer " + wafer + " ...")
            QApplication.processEvents()
            result_file = ResultFile(filename_results, options["excluded_parameters"])
            if result_file.error:
                print(result_file.error_message)
            else:
                print(result_file.info())
            # Make pdf report for every wafer
            print(f"Print report for wafer {wafer}")
            CMOS.print_report(wafer)
        # print comparative
        widgets.txtResultReport.appendPlainText("Creating comparative images...")
        CMOS.print_comparative()

        CMOS.output(filename_pdf)
        widgets.txtResultReport.appendPlainText("Merging files...")
        QApplication.processEvents()
        # filename_annex = "G:\\GITHUB\\Python\\caracterizar\\config\\default\\reports\\assets\\annexMOS.pdf"
        filename_annex = CMOS.dir_assets + "annexCMOS779.pdf"
        merger = PdfMerger()
        pdfs = [filename_pdf, filename_annex]
        # check run-seguimiento pdf file
        filename_seguimiento_titulo = CMOS.dir_assets + "annexCmos_seguimiento.pdf"
        filename_seguimiento = directoryName + "/" + str(CMOS.run) + "-seguimiento.pdf"
        if os.path.isfile(filename_seguimiento):
            pdfs.append(filename_seguimiento_titulo)
            pdfs.append(filename_seguimiento)
        for pdf in pdfs:
            merger.append(pdf)
        merger.write(filename_pdf.replace(".pdf", "_final.pdf"))
        merger.close()

        widgets.txtResultReport.appendHtml('<br />Report done!<br />')
    except Exception as e:
        widgets.txtResultReport.appendHtml('<br />ERROR: ' + str(e) + '<br />')
