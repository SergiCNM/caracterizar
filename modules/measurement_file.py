# ----------------------------------------------
# CLASS MeasurementFile to create a measure file
# ----------------------------------------------

import os
import numpy as np
from datetime import datetime, date

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt


from functools import partial
from config.functions import *
from config.defs import *
from functions import * # messageBox


class MeasurementFile():
    section_levels = {
        "GLOBAL": 0,
        "WAFER": 0,
        "DIE": 1,
        "MODULE": 2,
        "MODTEST": 3,
        "PARMS": 4,
        "DATA": 4,
    }
    def __init__(self, parameters, filename=""):
        # create a measurement file for Caracterizar process (filename without .dat)
        # getting parameters
        if "process_name" in parameters and "lot_name" in parameters and \
          "wafer_name" in parameters and "mask_name" in parameters and \
          "operator_name" in parameters and "filename_test" in parameters and \
          "date" in parameters and "time" in parameters and "waferinfo" in parameters:
            self.process_name = parameters["process_name"].strip()
            self.lot_name = parameters["lot_name"].strip()
            self.wafer_name = parameters["wafer_name"].strip()
            self.mask_name = parameters["mask_name"].strip()
            self.operator_name = parameters["operator_name"]
            self.filename_test = parameters["filename_test"]
            self.date = parameters["date"]
            self.time = parameters["time"]
            if self.date == "" and self.time == "":
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                self.date = dt_string.split()[0]
                self.time = dt_string.split()[1]

            self.waferinfo = parameters["waferinfo"]

            # set filename_dat
            if filename=="":
                filename = self.process_name + "_" + self.date.replace("/","") + "_" + self.time.replace(":","")
            filename_dat = filename + ".dat"
            self.filename = filename_dat

            self.created = True
            self.error_message = ""
            self.numtabs = 0
            # create file if not exists
            if self.process_name == "":
                self.created = False
                self.error_message = "Process name empty!"
        else:
            self.created = False
            self.error_message = "Parameters not valid!"


    def MeasurementHeaderFile(self, overwrite=False):
        MeasurementHeaderFile = False

        date_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        date = date_time.split()[0]
        time = date_time.split()[1]
        if self.process_name == "":
            self.error_message = "Process name empty!"
        else:
            # make header for process name
            self.created = True
            if os.path.exists(self.filename) and not overwrite:
                self.created = False
                # check if exists file
                self.error_message = "Warning: File exists!"

            if self.created:
                break_line = "\n"
                f = open(self.filename, "w")
                seq = ["<BEG GLOBAL>" + break_line]
                seq.append("\tProcess[s]\t" + self.process_name + break_line)
                seq.append("\tLot[s]\t" + self.lot_name + break_line)
                seq.append("\tWafer[s]\t" + self.wafer_name + break_line)
                seq.append("\tMask[s]\t" + self.mask_name + break_line)
                seq.append("\tOperator[s]\t" + self.operator_name + break_line)
                seq.append("\tDate[s]\t" + date + break_line)
                seq.append("\tTime[s]\t" + time + break_line)
                seq.append("\tWaferInfo[s]\t" + self.waferinfo + break_line)
                # seq.append("WaferInfo[s]\tU=UM|S=101600|X=7500|Y=7500|F=0|XO=6|YO=13|IX=0|IY=0|SA=0|WC=ONDIE|CX=0|CY=0|"+"\n")
                seq.append("<END GLOBAL>" + break_line)
                f.writelines(seq)
                f.close()
                MeasurementHeaderFile = True

        return MeasurementHeaderFile


    def MeasurementSectionFile(self, section, tag, modtest=0, die_position='0 0', module_position='0 0'):
        section_name = ""

        if section == "WAFER":
            section_name = self.wafer_name
        elif section == "DIE":
            section_name = die_position
        elif section == "MODULE":
            section_name = module_position
        elif section == "MODTEST":
            section_name = self.filename_test.replace(".py", "")
            if modtest > 0:
                section_name = section_name + " " + str(modtest)

        break_line = "\n"

        # Obtener nivel fijo según sección, +1 si es BEG para data y parms?
        base_indent = self.section_levels.get(section, 0)
        indent = base_indent

        # Para DATA y PARMS se escribe con un nivel adicional
        # if section in ["DATA", "PARMS"]:
        #     indent = base_indent

        # Para etiquetas END, mantenemos misma indentación que BEG
        # (podrías agregar lógica si necesitas distinta indentación en END)

        f = open(self.filename, "a")

        if section not in ["PARMS", "DATA"]:
            txt = (indent * "\t") + f"<{tag}>\t{section} ({section_name})"
        else:
            txt = (indent * "\t") + f"<{tag} {section}>"

        f.write(txt + break_line)
        f.close()

    def MeasurementVariablesFile(self, variables):
        break_line = "\n"
        params = variables.get("params", [])
        if params:
            self.MeasurementSectionFile(section="PARMS", tag="BEG")
            f = open(self.filename, "a")
            indent = (self.section_levels["PARMS"] + 1) * "\t"
            for param in params:
                txt = indent + f"{param['name']}\t{param['value']}"
                f.write(txt + break_line)
            f.close()
            self.MeasurementSectionFile(section="PARMS", tag="END")

        datas = variables.get("data", [])
        if datas:
            self.MeasurementSectionFile(section="DATA", tag="BEG")

            headers = []
            values = []
            for data in datas:
                headers.append(f"{data['name']}({data['units']})")
                values.append(data["values"])

            f = open(self.filename, "a")
            indent = (self.section_levels["DATA"] + 1) * "\t"

            # Cabecera
            f.write(indent + '\t'.join(headers) + break_line)

            # Datos
            for i in range(len(values[0])):
                row = [str(values[j][i]) for j in range(len(headers))]
                f.write(indent + '\t'.join(row) + break_line)

            f.close()
            self.MeasurementSectionFile(section="DATA", tag="END")

    def MeasurementSectionFile2(self, section, tag, modtest=0, die_position='0 0', module_position='0 0'):
        # tag: BEG or END
        section_name = ""

        if section == "WAFER":
            section_name = self.wafer_name
        if section == "DIE":
            # get coord
            #section_name = MainWindow.waferwindow.wafer_parameters["wafer_positions"][int(MainWindow.ui.dieActual.text())-1]
            section_name = die_position
        if section == "MODULE":
            # get coord
            # section_name = MainWindow.waferwindow.wafer_parameters["wafer_modules"][int(MainWindow.ui.moduleActual.text())-1]
            section_name = module_position
        if section == "MODTEST":
            # get testname
            section_name = self.filename_test.replace(".py","")
            if modtest>0:
                section_name = section_name + " " + str(modtest)

        break_line = "\n"
        if tag=="BEG" and section!="WAFER":
            self.numtabs += 1
        if tag=="END" and section!="MODTEST":
            self.numtabs -= 1
        f = open(self.filename, "a")
        if section != "PARMS" and section != "DATA":
            # modified space "> " by tab ">\t" 12/12/2022
            txt = (self.numtabs * "\t") + "<" + tag + ">\t" + section + " (" + section_name + ")"
        else:
            txt = (self.numtabs * "\t") + "<" + tag + " " + section + ">"
        f.write(txt + break_line)
        f.close()
        if tag=="END" and section=="DIE":
            self.numtabs -= 1


    def MeasurementVariablesFile2(self,variables):
        # "variables" : {
        #	"params" : [{"name" : "CMAX", "value" : 420.056E-12},{"name" : "CMIN", "value" : 210.057E-12}],
        #   "data" : [{"name" : "V", "values" : [0,1,2,3,4,5], "units" : "V"},{"name": "C", "values" : [210.057E-12, 215.24E-12, 310.85E-12, 360.45E-12, 400, 420.56E-12], "units": "F"}]
        # }

        break_line = "\n"
        params = variables["params"]
        if len(params)>0:
            # txt = (self.numtabs * "\t") + "<BEG PARMS>" + break_line
            self.MeasurementSectionFile(section="PARMS", tag="BEG")
            f = open(self.filename, "a")
            for param in params:
                txt = (self.numtabs * "\t") + "\t" + str(param["name"]) + "\t" + str(param["value"])
                f.write(txt + break_line)
            f.close()
            self.numtabs +=1
            self.MeasurementSectionFile(section="PARMS", tag="END")



        datas = variables["data"]
        if len(datas)>0:
            self.numtabs -=1
            self.MeasurementSectionFile(section="DATA", tag="BEG")
            # header
            headers = []
            values = []
            f = open(self.filename, "a")
            for data in datas:
                # get header
                headers.append(str(data["name"]) + "(" + str(data["units"]) + ")")
                values.append(data["values"])

            headers_text = '\t'.join(headers) + break_line
            f.write(headers_text)

            for i in range (0,len(values[0])):
                txtprint = ""
                for j in range (0,len(headers)):
                    if txtprint=="":
                        txtprint = (self.numtabs * "\t") + "\t" + str(values[j][i])
                    else:
                        txtprint = txtprint + "\t" + str(values[j][i])
                f.write(txtprint + break_line)
            f.close()
            self.MeasurementSectionFile(section="DATA", tag="END")