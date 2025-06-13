# ADD report
import os
import sys
import toml
from PySide6.QtWidgets import QFileDialog

# FOR testing

if 'config.default.reports' in sys.modules:
	del sys.modules['config.default.reports']

if 'config.default.reports.EAD' in sys.modules:
	del sys.modules['config.default.reports.EAD']

from config.default.reports import EAD

# load from external toml file in tests_dir (if exists, if not default values)
filename_config = os.getcwd() + base_dir + reports_dir + '/EAD.toml'
file_exists = os.path.exists(filename_config)
if file_exists:
	toml_info = toml.load(filename_config)
	options = toml_info["parameters"]


exists_result_file = False
filename_results = ""
widgets.txtResultReport.setPlainText("")
file_error = ""

directoryName = QFileDialog.getExistingDirectory(self, "Select RUN folder", results_dir,  QFileDialog.ShowDirsOnly)
if directoryName != "":
	wafers_list = list()
	for directory in sorted(os.listdir(directoryName)):
		if os.path.isdir(directoryName + "/" + directory):
			if "COMPARATIVE_FOLDER" in options and directory != options["COMPARATIVE_FOLDER"]:
				wafers_list.append(directory)
	if len(wafers_list)>0:
		exists_result_file = True
		for wafer in wafers_list:
			filename_results = [directoryName + "/" + wafer + "/" + wafer + "_forward.dat", directoryName + "/" + wafer + "/" + wafer + "_reverse.dat"]
			for filename_result in filename_results:
				if not os.path.isfile(filename_result):
					file_error = filename_result
					exists_result_file = False
					break

get_report = False
if not exists_result_file:
	messageBox(self, "Result file error", f"Some result file ({file_error}) doesn't exists in this path!", "info")
else:
	get_report = True
if get_report:
	try:
		widgets.txtResultReport.setPlainText("")
		QApplication.processEvents()
		# create pdf file in directoryName
		filename_pdf = directoryName + "/" + os.path.basename(os.path.normpath(directoryName)) + ".pdf"
		widgets.txtResultReport.appendPlainText("Checking information and creating plot graphs...")
		QApplication.processEvents()
		EAD = EAD(widgets, options, directoryName, self.config)
		print(EAD.wafers)
		for wafer in sorted(EAD.wafers):
			widgets.txtResultReport.appendPlainText("Creating report EAD for wafer " + wafer + " ...")
			QApplication.processEvents()
			filename_results = directoryName + "/" + wafer + "/" + wafer + "_reverse.dat"
			result_file = ResultFile(filename_results)
			print(result_file.info())
			EAD.print_report(wafer)

		EAD.output(filename_pdf)
		QApplication.processEvents()
		widgets.txtResultReport.appendHtml('<br />Report done!<br />')
	except Exception as e:
		widgets.txtResultReport.appendHtml('<br />ERROR: ' + str(e) + '<br />')



