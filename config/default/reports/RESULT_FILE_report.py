# Generate measurement files from result file
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
		print(result_file.data)
		if not result_file.error:
			widgets.txtResultReport.setPlainText("Creating report RESULT FILE")
			# save all files with same 
			count_dies = 0
			for die in result_file.dies:
				count_dies += 1
				count_modules = 0
				for module in result_file.modules:
					count_modules += 1
					# create file measurement
					save_filename = file_results.replace(file_extension, "") + "_" + str(count_dies) + "_" + str(count_modules) + ".txt"
					f = open(path_abs + save_filename,'w')
					header = ""
					listas = list() # create list of list
					for k in result_file.data[die][module]:
						listas.append(result_file.data[die][module][k])
						# print header
						header += str(k) + "#"
					if options["header"]:
						header = header[:-1].replace("#", options["separator"]) + "\n"
						f.write(header)
					if len(listas) > 0:
						for i in range(len(listas[0])):
							line = ""
							for j in range(len(listas)):
								line += listas[j][i] + "#"
							line = line[:-1].replace("#", options["separator"]) + "\n"
							f.write(line)
					f.close()
		
			widgets.txtResultReport.appendHtml(result_file.info().replace("\n", "<br />"))
			widgets.txtResultReport.appendHtml("Finish report RESULT FILE")
			messageBox(self, "Result file success", "All files have been generated in this path ("+path_abs+")!", "info")
		else:
			widgets.txtResultReport.setPlainText("Problems loading result file: " + result_file.error_message)
	
except Exception as e:
	print("Error: " + str(e))

		


