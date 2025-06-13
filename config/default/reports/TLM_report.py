# ADD report
import os
import sys
import toml
from PySide6.QtWidgets import QFileDialog

from modules import ResultFile

# FOR testing

if 'config.default.reports' in sys.modules:
	del sys.modules['config.default.reports']

if 'config.default.reports.EAD' in sys.modules:
	del sys.modules['config.default.reports.TLM']

from config.default.reports import TLM

# load from external toml file in tests_dir (if exists, if not default values)
filename_config = os.getcwd() + base_dir + reports_dir + '/TLM.toml'
file_exists = os.path.exists(filename_config)
if file_exists:
	toml_info = toml.load(filename_config)
	options = toml_info["parameters"]


exists_result_file = False
filename_results = ""
widgets.txtResultReport.setPlainText("")
cuartos = ["UP_LEFT", "UP_RIGHT", "DOWN_LEFT", "DOWN_RIGHT"]
# cuartos = ["UP_LEFT"]
file_error = ""

directoryName = QFileDialog.getExistingDirectory(self, "Select RUN folder", results_dir,  QFileDialog.ShowDirsOnly)
if directoryName != "":
	wafers_list = list()
	for directory in sorted(os.listdir(directoryName)):
		if os.path.isdir(directoryName + "/" + directory):
			wafers_list.append(directory)
	if len(wafers_list)>0:
		exists_result_file = True
		for wafer in wafers_list:
			# check if exists 92 TXT files inside wafer folder + cuartos folder + data folder for UP cuartos and 90 TXT files for DOWN cuartos
			print("Checking wafer " + wafer)
			if "UP_LEFT" in wafer or "UP_RIGHT" in wafer:
				dies_total = 92
			else:
				dies_total = 90
			print("Dies total: " + str(dies_total))
			# check if exists 92*12 TXT total files inside wafer folder + cuartos folder + data folder for UP cuartos
			for die in range(1, dies_total+1):
				for module in range(1, 13):
					namefile = "IV_" + str(die) + "_" + str(module) + ".TXT"
					if not os.path.isfile(directoryName + "/" + wafer + "/data/" + namefile):
						file_error = directoryName + "/" + wafer + "/data/" + namefile
						exists_result_file = False
						break

get_report = False
if not exists_result_file:
	messageBox(self, "Result file error", f"Some result file ({file_error}) doesn't exists in this path!", "info")
else:
	get_report = True
if get_report:
	wafer = ""
	try:
		widgets.txtResultReport.setPlainText("")
		QApplication.processEvents()
		# create pdf file in directoryName
		filename_pdf = directoryName + "/" + os.path.basename(os.path.normpath(directoryName)) + ".pdf"
		widgets.txtResultReport.appendPlainText("Checking information and creating plot graphs...")
		QApplication.processEvents()
		TLM = TLM(widgets, options, directoryName, self.config)
		print(TLM.wafers)
		for wafer in sorted(TLM.wafers):
			widgets.txtResultReport.appendPlainText("Creating report TLM for wafer " + wafer + " ...")
			QApplication.processEvents()
			# ADD report
			TLM.print_report(wafer)

		TLM.output(filename_pdf)
		QApplication.processEvents()
		widgets.txtResultReport.appendHtml('<br />Report done!<br />')

	except Exception as e:
		widgets.txtResultReport.appendHtml('<br />ERROR: ' + str(e) + '<br />' + 'While processing wafer ' + wafer + '<br />')



