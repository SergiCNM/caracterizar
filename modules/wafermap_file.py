# ----------------------------------------------
# CLASS WafermapFile to read a wafermap file (could be from old format (ppg) or new format(.py)
# ----------------------------------------------
import os
import datetime
import numpy as np

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from config.functions import *
from functions import *  # messageBox


class WafermapFile():
    def __init__(self, path_to_file):
        self.error = False
        self.error_message = ""
        self.path_to_file = path_to_file
        self.filename = os.path.basename(self.path_to_file)
        self.mode_types = ["py", "ppg"]
        self.mode_type = self.filename.split(".")[-1]
        # wafer size mm & thickness
        self.wafer_size_inch = 0
        self.wafer_size_mm = 0
        self.thickness = 0

        self.number_lines = 0
        self.wafer_parameters = {}  # init dict wafer parameters
        # init initial movement (for ppg files) for get the origin chip
        self.movement_x = 0
        self.movement_y = 0
        # get movement in ppg file to adjust wafer_positions
        self.wafer_movements = dict()
        if os.path.exists(path_to_file):
            # read lines first
            self.lines = list()
            self.wafer_parameters["wafer_positions"] = list()  # init list wafer_positions
            self.wafer_parameters["wafer_modules"] = list()  # init list wafer_modules
            with open(path_to_file) as file_in:
                origin_found = False
                num_movement = 0
                blank_lines = 0
                for line in file_in:
                    line = line.strip()
                    if line != "":
                        self.lines.append(line.replace("\n", ""))
                        # case ppg: get positions & origin_chip
                        if "lappend positions" in line:
                            # append positions
                            line = line.replace("lappend positions ", "")
                            line = line.replace('" "', ',')
                            line = line.replace('"', '')
                            line_array = line.split(",")
                            for lines in line_array:
                                self.wafer_parameters["wafer_positions"].append(lines)

                        if "set numchips" in line:
                            self.wafer_parameters["nchips"] = line.replace("set numchips ", "")

                        if "set nummodulos" in line:
                            self.wafer_parameters["nmodules"] = line.replace("set nummodulos ", "")

                        if "switch $current_pos" in line:
                            num_movement = len(self.lines) + blank_lines  # get the line number for get the movement

                        if len(self.lines) > num_movement > 0:
                            if not "wafer_parameters" in line and ' {' in line and not "ESPERA" in line:
                                # is ppg then get movements
                                movement_string = line.replace(" {", "")
                                movements_list = movement_string.split(" - ")

                                for movement in movements_list:
                                    self.wafer_movements[movement] = {}
                                    self.wafer_movements[movement]["x"] = 0
                                    self.wafer_movements[movement]["y"] = 0

                        if "prober pimove" in line:
                            move_x, move_y = line.replace("prober pimove ", "").split(" ")
                            if "0" in self.wafer_movements and not origin_found:
                                origin_found = True

                                # get the first movement (origin)
                                self.movement_x, self.movement_y = move_x, move_y
                                self.wafer_movements["0"]["x"] = self.movement_x
                                self.wafer_movements["0"]["y"] = self.movement_y

                            for movement in self.wafer_movements:
                                if movement != 0 and int(self.wafer_movements[movement]["x"]) == 0 and int(
                                        self.wafer_movements[movement]["y"]) == 0:
                                    self.wafer_movements[movement]["x"], self.wafer_movements[movement][
                                        "y"] = move_x, move_y

                    else:
                        blank_lines += 1

                self.number_lines = len(self.lines)

            # first check py & ppg file before execute
            if self.number_lines == 0:
                self.error_message = "File: " + path_to_file + " is empty!"
                self.error = True
            else:
                check_file = self.check_file()
                if not check_file[0]:
                    self.error = True
                    self.error_message = check_file[1]

            if self.mode_type == "py" and self.filename.split("_")[-1] == "wafermap.py":
                # execute py file
                with open(self.path_to_file, "r") as rnf:
                    try:
                        exec(rnf.read())
                        self.wafer_parameters = wafer_parameters
                        self.wafer_size_inch = float(self.wafer_parameters["wafer_size"])
                        self.set_wafer_size()
                        if not "xmax" in self.wafer_parameters or not "ymax" in self.wafer_parameters:
                            # get xmax & ymax from wafer_positions
                            self.wafer_parameters["xmax"], self.wafer_parameters["ymax"] = self.get_xmax_ymax()

                    except:
                        self.error = True
                        self.error_message = "Problem executing file: Problem exists while exec file's content: " + path_to_file

            elif self.mode_type == "ppg":

                # check modules number
                if int(self.wafer_parameters["nmodules"]) != len(self.wafer_parameters["wafer_modules"]):
                    self.error = True
                    self.error_message = "Problem with modules number: Different number detected in ppg file!" + \
                                         str(self.wafer_parameters["nmodules"]) + \
                                         "-" + str(len(self.wafer_parameters["wafer_modules"]))

            else:
                self.error = True
                self.error_message = "File mode type not found!"

        else:
            # retval = messageBox(self,"Error loading file","File: " + path_to_file + " doesn't exists!","error")
            self.error_message = "File: " + path_to_file + " doesn't exists!"
            self.error = True

    def set_wafer_size(self):
        self.wafer_size_mm, self.thickness = calc_wafer_size(self.wafer_size_inch)

    def get_xmax_ymax(self):
        xmax_detected = 0
        ymax_detected = 0
        elementos_x_detected = []
        elementos_y_detected = []
        for elemento in self.wafer_parameters["wafer_positions"]:

            elemento_array = elemento.split()
            if len(elemento_array) != 2:
                check_wafer_parameters = False
                break
            # init variables
            elemento_x = elemento_array[0]
            elemento_y = elemento_array[1]
            buscar_x = False
            buscar_y = False
            num_elemento_x = 0
            num_elemento_y = 0
            if elemento_x not in elementos_x_detected:
                elementos_x_detected = np.append(elementos_x_detected, elemento_x)
                buscar_x = True
            if elemento_y not in elementos_y_detected:
                elementos_y_detected = np.append(elementos_y_detected, elemento_y)
                buscar_y = True
            if buscar_x and buscar_y:
                for elemento_buscar in self.wafer_parameters["wafer_positions"]:
                    elemento_buscar_array = elemento_buscar.split()
                    if elemento_buscar_array[0] == elemento_x:
                        num_elemento_y += 1  # cambiamos el eje porque buscamos sumatorio en vertical
                    if elemento_buscar_array[1] == elemento_y:
                        num_elemento_x += 1  # cambiamos el eje porque buscamos sumatorio en horizontal

                if num_elemento_x > xmax_detected:
                    xmax_detected = num_elemento_x
                if num_elemento_y > ymax_detected:
                    ymax_detected = num_elemento_y

        return [xmax_detected, ymax_detected]

    def info(self):

        return "------------------------------------------\n" \
               "  INFO FILE:      " + "\t" + self.filename + "\n" \
                                                             "------------------------------------------\n" \
                                                             "  - Name:         " + "\t" + str(
            self.wafer_parameters["wafer_name"]) + "\n" \
                                                   "  - Size:         " + "\t" + str(
            self.wafer_parameters["wafer_size"]) + "\n" \
                                                   "  - Size (mm):    " + "\t" + str(self.wafer_size_mm) + "\n" \
                                                                                                           "  - Thickness:    " + "\t" + str(
            self.thickness) + "\n" \
                              "  - Xsize:        " + "\t" + str(self.wafer_parameters["xsize"]) + "\n" \
                                                                                                  "  - Ysize:        " + "\t" + str(
            self.wafer_parameters["ysize"]) + "\n" \
                                              "  - Nchips:       " + "\t" + str(self.wafer_parameters["nchips"]) + "\n" \
                                                                                                                   "  - Nmodules:     " + "\t" + str(
            self.wafer_parameters["nmodules"]) + "\n" \
                                                 "  - Xmax:         " + "\t" + str(self.wafer_parameters["xmax"]) + "\n" \
                                                                                                                    "  - Ymax:         " + "\t" + str(
            self.wafer_parameters["ymax"]) + "\n" \
                                             "  - Origin:       " + "\t" + str(
            self.wafer_parameters["origin_chip"]) + "\n" \
                                                    "  - Home:         " + "\t" + str(
            self.wafer_parameters["home_chip"]) + "\n" \
                                                  "  - Real origin:  " + "\t" + str(
            self.wafer_parameters["real_origin_chip"]) + "\n" \
                                                         "  - Orientation:  " + "\t" + str(
            self.wafer_parameters["flat_orientation"]) + "\n" \
                                                         "  - Positions:    " + "\t" + str(
            self.wafer_parameters["wafer_positions"]) + "\n" \
                                                        "  - Modules:      " + "\t" + str(
            self.wafer_parameters["wafer_modules"]) + "\n" \
                                                      "  - Nav options:  " + "\t" + str(
            self.wafer_parameters["navigation_options"]) + "\n" \
                                                           "------------------------------------------\n"

    def check_file(self):
        # Verifications for wafermap file
        if self.mode_type in self.mode_types:
            if self.mode_type == "ppg":
                try:
                    # 1) check first line
                    # 4.000000 2790.000000 1950.000000 11 12 104.000000
                    # wafer_size xsize ysize xmax ymax nchips
                    first_line_information = self.lines[0].replace("# ", "").split(" ")
                    if len(first_line_information) == 6:
                        self.wafer_parameters["wafer_name"] = self.filename.replace(".ppg", "")
                        self.wafer_parameters["wafer_size"] = first_line_information[0]
                        self.wafer_parameters["xsize"] = first_line_information[1]
                        self.wafer_parameters["ysize"] = first_line_information[2]
                        self.wafer_parameters["xmax"] = first_line_information[3]
                        self.wafer_parameters["ymax"] = first_line_information[4]

                        self.wafer_size_inch = float(self.wafer_parameters["wafer_size"])
                        self.set_wafer_size()

                        if float(self.wafer_parameters["nchips"]) != float(first_line_information[5]):
                            return [False, "Different information getted for nchips!"]
                        if float(self.wafer_parameters["nchips"]) != float(
                                len(self.wafer_parameters["wafer_positions"])):
                            return [False, "Different information getted for number of chips & positions!"]

                        self.wafer_parameters["origin_chip"] = "0 0"  # always 0 0 ?
                        # get origin chip
                        chips_x = int(float(self.movement_x) / float(self.wafer_parameters["xsize"]))
                        chips_y = int(float(self.movement_y) / float(self.wafer_parameters["ysize"]))
                        self.wafer_parameters["home_chip"] = str(chips_x * -1) + " " + str(
                            chips_y)  # x axis negative on right side
                        # real origin chip in this case (ppg) center on wafer (wafer_size => get mm, check xmax & ymax)
                        self.wafer_parameters["real_origin_chip"] = self.get_real_origin_chip()
                        self.wafer_parameters["flat_orientation"] = "0"  # always 0 ?
                        if int(self.wafer_parameters["nmodules"]) == 1:
                            self.wafer_parameters["wafer_modules"].append("0.000000 0.000000")  # only one module
                        else:
                            # get nmodules & wafer_modules
                            nmodules_num = 1002
                            wafer_modules = list()
                            wafer_modules.append("0.000000 0.000000")
                            while True:
                                if str(nmodules_num) in self.wafer_movements:
                                    wafer_modules.append(self.wafer_movements[str(nmodules_num)]["x"] + " " +
                                                         self.wafer_movements[str(nmodules_num)]["y"])
                                    nmodules_num += 1
                                else:
                                    nmodules_num = nmodules_num - 1002
                                    break
                            self.wafer_parameters["wafer_modules"] = wafer_modules

                        # setting navigations option (always the same in ppg? check navigations options in wafer_positions)
                        self.wafer_parameters["navigation_options"] = ["UPPER-LEFT", "BI-DIRECTIONAL", "ROW"]

                        if float(self.wafer_parameters["nchips"]) != len(self.wafer_parameters["wafer_positions"]):
                            return [False, "Chips number (" + str(
                                self.wafer_parameters["nchips"]) + ") not equal to number of wafer positions (" + int(
                                self.wafer_parameters["wafer_positions"]) + ")!"]
                        if int(self.wafer_parameters["nmodules"]) != len(self.wafer_parameters["wafer_modules"]):
                            return [False, "Modules number (" + str(
                                self.wafer_parameters["nmodules"]) + ") not equal to number of wafer modules (" + int(
                                self.wafer_parameters["wafer_modules"]) + ")!"]

                    else:
                        return [False, "Bad information in first line of ppg file!"]
                except:
                    return [False, "Problem parsing ppg file!"]

            if self.mode_type == "py":
                verify_parameters = ["global wafer_parameters", "wafer_name =", "wafer_size =", "xsize =", "ysize =",
                                     "nchips =", "real_origin_chip =", "origin_chip =", "home_chip =",
                                     "flat_orientation =", "navigation_options =", "wafer_positions =",
                                     "wafer_modules ="]
                founded = 0
                for line in self.lines:
                    for param in verify_parameters:
                        if param in line:
                            founded += 1

                if founded < len(verify_parameters):
                    return [False, "Not present at least one param definition for wafer_parameters! "]



        else:
            return [False, "Mode type '" + str(self.mode_type) + "' not available!"]

        return [True, ""]

    # get real origin chip (ppg files) from origin chip, home chip, wafer_size, xsize, ysize, xmax, ymax
    def get_real_origin_chip(self):
        # change wafer_positions definition in base to movements
        # get central chip
        x_max = 0
        x_min = 0
        y_max = 0
        y_min = 0
        for position in self.wafer_parameters["wafer_positions"]:
            x_pos, y_pos = map(int, position.split())
            if x_pos > x_max:
                x_max = x_pos
            if x_pos < x_min:
                x_min = x_pos
            if y_pos > y_max:
                y_max = y_pos
            if y_pos < y_min:
                y_min = y_pos
        dif_x = abs(x_max - x_min)
        dif_y = abs(y_max - y_min)

        chip_central_x = x_max - dif_x / 2
        chip_central_y = y_max - dif_y / 2
        # assign real chip central in wafer_positions (first position)
        chip_central_positions_x, chip_central_positions_y = map(int,
                                                                 self.wafer_parameters["wafer_positions"][0].split())

        # first search X near to central chip x
        for position in self.wafer_parameters["wafer_positions"]:
            x_pos, y_pos = map(int, position.split())
            if abs(x_pos - int(chip_central_x)) < abs(chip_central_positions_x - int(chip_central_x)):
                chip_central_positions_x = x_pos

        # the search Y with fixes X
        for position in self.wafer_parameters["wafer_positions"]:
            x_pos, y_pos = map(int, position.split())
            if x_pos == chip_central_positions_x:
                if abs(y_pos - int(chip_central_y)) < abs(chip_central_positions_y - int(chip_central_y)):
                    chip_central_positions_y = y_pos

        # now we know the offset
        # get the middle position for all wafer
        wafer_size_um = self.wafer_size_mm * 1000
        num_chips_center_x = -1 * round(float(wafer_size_um) / (2 * float(self.wafer_parameters["xsize"])))
        num_chips_center_y = -1 * round(float(wafer_size_um) / (2 * float(self.wafer_parameters["ysize"])))

        real_origin_chip_x = num_chips_center_x - chip_central_positions_x
        real_origin_chip_y = num_chips_center_y - chip_central_positions_y

        return str(real_origin_chip_x) + " " + str(real_origin_chip_y)

    def get_heatmap_values_old(self, data_values):
        # return numpy array 2D to use in heatmap seaborn
        # pass data_values: dictionary with wafer_positions & value. Ex:
        # {'0 0': 592.58027418, '-3 0': 593.775609049, '-6 0': 598.320966887, ....}
        # 0) set np array 2D with zeros. Calc the number of chips in X & Y

        xsize = float(self.wafer_parameters["xsize"])
        ysize = float(self.wafer_parameters["ysize"])
        num_chips_X = float(self.wafer_size_mm) * 1000 / xsize
        num_chips_Y = float(self.wafer_size_mm) * 1000 / ysize
        # set 2D array with zeros
        separation_Y = 2  # create extra separation chips Y
        get_heatmap_values = np.zeros((int(num_chips_Y + separation_Y), int(num_chips_X)))
        # 1) We use the wafermaf class to get wafer_positions, real_origin_chip
        wafer_positions = self.wafer_parameters["wafer_positions"]

        real_origin_chip = self.wafer_parameters["real_origin_chip"]
        real_origin_chip_x, real_origin_chip_y = real_origin_chip.split()

        num_pos = 0
        for pos in wafer_positions:
            posx, posy = pos.split()
            wafer_position = wafer_positions[num_pos]
            medida = data_values[wafer_position]
            wafer_position_x, wafer_position_y = wafer_position.split()

            # real wafer position is the wafer_position + real_origin_chip position
            real_wafer_position_x = int(wafer_position_x) + int(real_origin_chip_x)
            real_wafer_position_y = int(wafer_position_y) + int(real_origin_chip_y)

            # for seaborn is positive
            real_wafer_position_x_sns = int(real_wafer_position_x) * -1
            real_wafer_position_y_sns = int(real_wafer_position_y) * -1

            # set the value for array position (inverted)
            get_heatmap_values[real_wafer_position_y_sns][real_wafer_position_x_sns] = medida
            num_pos += 1

        return get_heatmap_values

    def get_heatmap_values(self, data_values):
        # return numpy array 2D to use in heatmap seaborn
        # pass data_values: dictionary with wafer_positions & value. Ex:
        # {'0 0': 592.58027418, '-3 0': 593.775609049, '-6 0': 598.320966887, ....}
        # 0) set np array 2D with zeros. Calc the number of chips in X & Y

        xsize = float(self.wafer_parameters["xsize"])
        ysize = float(self.wafer_parameters["ysize"])
        num_chips_X = float(self.wafer_size_mm) * 1000 / xsize
        num_chips_Y = float(self.wafer_size_mm) * 1000 / ysize
        # set 2D array with zeros
        separation_Y = 2  # create extra separation chips Y
        get_heatmap_values = np.empty((int(num_chips_Y + separation_Y), int(num_chips_X)))
        get_heatmap_values.fill(9E99)
        # 1) We use the wafermaf class to get wafer_positions, real_origin_chip
        wafer_positions = self.wafer_parameters["wafer_positions"]

        real_origin_chip = self.wafer_parameters["real_origin_chip"]
        real_origin_chip_x, real_origin_chip_y = real_origin_chip.split()

        num_pos = 0
        medidas = list()
        for pos in wafer_positions:
            posx, posy = pos.split()
            wafer_position = wafer_positions[num_pos]
            medida = data_values[wafer_position]
            wafer_position_x, wafer_position_y = wafer_position.split()

            # real wafer position is the wafer_position + real_origin_chip position
            real_wafer_position_x = int(wafer_position_x) + int(real_origin_chip_x)
            real_wafer_position_y = int(wafer_position_y) + int(real_origin_chip_y)

            # for seaborn is positive
            real_wafer_position_x_sns = int(real_wafer_position_x) * -1
            real_wafer_position_y_sns = int(real_wafer_position_y) * -1

            # set the value for array position (inverted)
            get_heatmap_values[real_wafer_position_y_sns][real_wafer_position_x_sns] = medida
            medidas.append(medida)
            num_pos += 1

        min_value = min(medidas)
        max_value = max(medidas)

        if max_value < 0:
            max_value_replace = max_value - max_value * 10 / 100
        else:
            max_value_replace = max_value + max_value * 10 / 100
        if min_value < 0:
            min_value_replace = min_value + min_value * 90 / 100
        else:
            min_value_replace = min_value - min_value * 90 / 100

        # print(str(max_value))
        print(str(min_value))
        # Replace values 9E99 for max_value or min_value (depends cmap colors)
        # get_heatmap_values = np.where(get_heatmap_values==9E99,max_value,get_heatmap_values)
        get_heatmap_values = np.where(get_heatmap_values == 9E99, min_value_replace, get_heatmap_values)

        return get_heatmap_values
