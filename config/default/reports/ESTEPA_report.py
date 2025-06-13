# Generate estepa file from result file
import os
import io, sys
import importlib 


# FOR testing


if 'config.default.reports.RESULT_FILE' in sys.modules:
	del sys.modules['config.default.reports.RESULT_FILE']

if 'modules.result_file' in sys.modules:
	del sys.modules['modules.result_file']

from modules.result_file import ResultFile


options = {"separator": "\t", "header": False}

exists_result_file = False
fileName = ""
filters = "Text files (*.dat *.txt)"
selected_filter = "Text files (*.dat *.txt)"
widgets.txtResultReport.setPlainText("")
try:
	path_fileName = QFileDialog.getOpenFileName(self, "Select Result file", results_dir,  filters, selected_filter)[0]
	if path_fileName!="":
		file_results = os.path.basename(path_fileName)
		file_extension = os.path.splitext(file_results)[1]
		path_abs = path_fileName.replace(file_results, "")
		result_file = ResultFile(path_fileName)
		if not result_file.error:
			widgets.txtResultReport.setPlainText("Creating report RESULT FILE")
			save_filename = file_results.replace(file_extension, "") + "_estepa.dat"
			# create estepa file
			result_file.create_estepa_file(path_abs, save_filename)
			widgets.txtResultReport.appendHtml(result_file.info().replace("\n", "<br />"))
			widgets.txtResultReport.appendHtml("Finish report: ESTEPA file generated!")
			messageBox(self, "Result file success", "All files have been generated in this path ("+path_abs+")!", "info")
		else:
			widgets.txtResultReport.setPlainText("Problems loading result file: " + result_file.error_message)
	
except Exception as e:
	print("Error: " + str(e))

		


