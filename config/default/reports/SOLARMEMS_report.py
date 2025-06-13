# SOLARMEMS report
import os
import sys
import importlib 
# FOR testing

if 'config.default.reports' in sys.modules:
 	del sys.modules['config.default.reports']

if 'config.default.reports.SOLARMEMS' in sys.modules:
	del sys.modules['config.default.reports.SOLARMEMS']

from config.default.reports import SOLARMEMS

import datetime

# report options
options = {"wafermap" : True, "results" : True, "sensor" : True,
    "sensor_data" : False, "sensor_image" : True,  "sensor_plot" : False,
	"dark_folder" : 'dark', "light_folder" : 'light',
	"image_folder" : 'photos', "plot_folder" : "plots", "compressed" : 50}


exists_result_file = False
file_results = ""
get_report = False

dirName = QFileDialog.getExistingDirectory(self, "Select folder", results_dir,  QFileDialog.ShowDirsOnly)
if dirName != "":
	file_results = dirName + "/" + dirName.split("/")[-1] + ".txt"
	if os.path.exists(file_results):
		exists_result_file = True

if exists_result_file:
	get_report = True
else:
	if file_results!="":
		retval = messageBox(self, "Result file error", "Result file: " + file_results + " doesn't exists in this path!","info")

if get_report:
	widgets.txtResultReport.setPlainText("Creating report SOLARMEMS")
	SOLARMEMS = SOLARMEMS(widgets, options, file_results)
	if not SOLARMEMS.error:
		today = datetime.datetime.now()
		date1 = str(today)[0:19].replace(":","-")
		namefile_pdf = date1 +  '__' + SOLARMEMS.filename.replace(".txt","") + '.pdf'
		SOLARMEMS.filename_pdf = namefile_pdf
		SOLARMEMS.print_report()
		# save in root folder
		head, tail = os.path.split(dirName)
		SOLARMEMS.output(head + "/" + namefile_pdf)
		retval = messageBox(self, "PDF report info:", "Report created in: " + head + "/" + namefile_pdf,"info")
	else:
		retval = messageBox(self, "Error creating PDF", SOLARMEMS.errorMessage,"error")

