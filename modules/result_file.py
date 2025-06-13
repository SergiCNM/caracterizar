# ----------------------------------------------
# CLASS ResultFile to read a measure file (could be from old format or metrics format)
# ----------------------------------------------
import datetime
import re
from functions import *  # messageBox


class ResultFile:
    """
    Class to read a measure file (could be from old format or metrics format)
    """
    def __init__(self, path_to_file, excluded_parameters=None):
        self.error = False
        self.error_message = ""
        self.path_to_file = path_to_file
        self.filename = os.path.basename(self.path_to_file)
        self.mode_types = ["metrics", "old"]
        self.mode_type = ""
        self.number_lines = 0
        self.process = ""
        self.lot = ""
        self.wafer = ""
        self.mask = ""
        self.operator = ""
        # set temperature & humidity default
        self.temperature = 0
        self.humidity = 0
        self.date = ""
        self.time = ""
        self.waferinfo = ""
        self.params = {}
        self.data = {}
        self.dies = []
        self.modules = []
        self.params_list = []
        if excluded_parameters is None:
            self.excluded_parameters = []
        else:
            self.excluded_parameters = excluded_parameters
        if os.path.exists(path_to_file):
            self.lines = []
            with open(path_to_file) as file_in:
                for line in file_in:
                    if line != "":
                        self.lines.append(line.replace("\n", ""))
                self.number_lines = len(self.lines)
            if self.number_lines == 0:
                # retval = messageBox(self,"Error loading file","File: " + path_to_file + " is empty!","error")
                self.error_message = "File: " + path_to_file + " is empty!"
                self.error = True
            else:
                check_file = self.check_file()
                if not check_file[0]:
                    # retval = messageBox(self,"Error checking file",check_file[1],"error")
                    self.error = True
                    self.error_message = f"ERROR checking file: {check_file[1]}"
                # get params & data info
                get_variables = self.get_variables()
                if not get_variables[0]:
                    self.error = True
                    self.error_message = "Problem getting params or data! " + get_variables[1]

        else:
            # retval = messageBox(self,"Error loading file","File: " + path_to_file + " doesn't exists!","error")
            self.error_message = "File: " + path_to_file + " doesn't exists!"
            self.error = True

    def info(self):
        """
        Return info text
        :return: text with info
        """
        info_text = "------------------------------------------\n" \
            "  INFO FILE: " + "\t" + self.filename + "\n" \
            "------------------------------------------\n" \
            "  - Process:    " + "\t" + self.process + "\n" \
            "  - Lot:        " + "\t" + self.lot + "\n" \
            "  - Wafer:      " + "\t" + self.wafer + "\n" \
            "  - Mask:       " + "\t" + self.mask + "\n" \
            "  - Operator:   " + "\t" + self.operator + "\n"

        if self.temperature != 0 and self.humidity != 0:
            info_text += "  - Temperature:" + "\t" + str(self.temperature) + "\n" \
                "  - Humidity:   " + "\t" + str(self.humidity) + "\n" \

        info_text += "  - Date:       " + "\t" + self.date + "\n" \
            "  - Time:       " + "\t" + self.time + "\n" \
            "  - WaferInfo:  " + "\t" + self.waferinfo + "\n" \
            "  - Chips:      " + "\t" + str(len(self.dies)) + "\n" \
            "  - Modules:    " + "\t" + str(len(self.modules)) + "\n" \
            "------------------------------------------\n"
        return info_text

    def check_file(self):
        """
        Check file to get mode type (metrics or old), and get header info
        :return: [True,""] if ok, [False,"Error message"] if error
        """
        if self.lines[0] == "<BEG GLOBAL>":
            self.mode_type = "metrics"
        elif "No=" in self.lines[2] and "Nv=" in self.lines[3]:
            self.mode_type = "old"

        # Verifications for result file
        if self.mode_type in self.mode_types:
            if self.mode_type == "metrics":
                # 1) check begin and end
                if not "<BEG GLOBAL>" in self.lines[0] and (
                        not "<END>\tWAFER" in self.lines[self.number_lines - 1].upper() or not "<END>\tWAFER" in
                                                                                               self.lines[
                                                                                                   self.number_lines - 2].upper()):
                    return [False, "Problem in BEGIN or END tags"]
                # 2) check globals
                header_file = self.check_header_file()
                if not header_file[0]:
                    return [False, header_file[1]]
            if self.mode_type == "old":
                if self.lines[0] != '""':
                    self.process = self.lines[0].replace('"', '')  # run-wafer
                    self.lot = self.process.split("-")[0]  # run
                    self.wafer = self.process.split("-")[1]  # wafer
                else:
                    # get process, lot & wafer from name if empty information
                    s = [str(s) for s in re.findall(r'-?\d+\.?\d*', self.filename)]
                    if len(s) >= 2:  # first 2 contains run & wafer!!
                        s = s[0:2]
                        self.process = ''.join(s)
                        self.lot = s[0]
                        self.wafer = s[1].replace("-", "").replace(".", "")
                        self.process = self.lot + "-" + self.wafer

                # file modification timestamp of a file
                m_time = os.path.getmtime(self.path_to_file)
                # file creation timestamp of a file
                # c_time = os.path.getctime(self.path_to_file)
                # convert timestamp into DateTime object
                dt_m = datetime.datetime.fromtimestamp(m_time)
                dt_ms = dt_m.strftime("%d/%m/%Y %H:%M:%S")
                self.date = dt_ms.split(" ")[0]
                self.time = dt_ms.split(" ")[1]
        else:
            return [False, "Mode type '" + str(self.mode_type) + "' not available!"]

        return [True, ""]

    def check_header_file(self):
        """
        Check header file metrics (process, lot, wafer, operator, date, time)
        :return:  [True,""] if ok, [False,"Error message"] if error
        """
        # Check header file metrics (process, lot, wafer, operator, date, time)
        line_number = 0
        header_variables = ["Process", "Lot", "Wafer", "Mask", "Operator", "Date", "Time", "WaferInfo"]
        line = self.lines[line_number].strip("\t")
        if not "<BEG GLOBAL>" in line:
            return [False, "Not BEG GLOBAL tag founded!"]
        for header_var in header_variables:
            line_number += 1
            line = self.lines[line_number].strip("\t")  # delete tab begin & end
            if not header_var in line:
                return [False, "Not " + header_var + " info founded!"]
            else:
                line = line.replace("\t", " ")
                line = line.replace(header_var + "[s]", "")
                line = line.strip()
                # check operator (temperature & humidity)
                if header_var.lower() == "operator":
                    operator_list = line.lower().strip().split(" ")
                    if len(operator_list) == 3:
                        cmd = "self.operator='" + operator_list[0] + "'"
                        exec(cmd)
                        cmd = "self.temperature='" + operator_list[1] + "'"
                        exec(cmd)
                        cmd = "self.humidity='" + operator_list[2] + "'"
                        exec(cmd)
                    else:
                        cmd = "self." + header_var.lower() + "='" + line + "'"
                        exec(cmd)
                else:
                    cmd = "self." + header_var.lower() + "='" + line + "'"
                    exec(cmd)


        line_number += 1
        line = self.lines[line_number].strip("\t")
        if not "<END GLOBAL>" in line:
            return [False, "Not END GLOBAL tag founded!"]
        return [True, ""]

    def get_variables(self):
        """
        Get variables (params & data) from file and save to self.params & self.data
        :return: [True,""] if ok, [False,"Error message"] if error
        """
        try:
            self.params = {}
            self.data = {}
            die = ""
            module = ""
            module_principal = ""
            line_number = 0
            beg_modules = 0
            variables_list = []
            if self.mode_type == "metrics":
                # get variables from metrics format file
                while line_number < self.number_lines - 1:
                    # for line_number in range(0,self.number_lines-1):
                    line = self.lines[line_number]
                    line = line.replace("\t", " ").strip()
                    if "<BEG> DIE " in line.upper():
                        die = line[10:].replace("(", "").replace(")", "").strip()
                        self.params[die] = {}
                        self.data[die] = {}
                        self.dies.append(die)
                    if "<BEG> MODULE " in line.upper():
                        beg_modules += 1 # control de número de modules dentro de modules
                        # prevenir module dentro de module
                        if module == "":
                            # module = line[13:].replace("(", "").replace(")", "").strip()
                            module = line[13:].strip()
                            module_principal = module
                            self.params[die][module] = {}
                            self.data[die][module] = {}
                            if not module in self.modules:
                                self.modules.append(module)
                        # code added 26/11/2024
                        else:
                            # submodule
                            module = module_principal + " " + line[13:].strip()
                            self.params[die][module] = {}
                            self.data[die][module] = {}
                            if not module in self.modules:
                                self.modules.append(module)
                    if "<END> DIE " in line.upper():
                        die = ""
                    if "<END> MODULE " in line.upper():
                        if beg_modules == 1:
                            module = ""
                            module_principal = ""
                            beg_modules = 0
                        else:
                            beg_modules -= 1
                    if "<BEG PARMS>" in line:
                        # always inside a module
                        if module != "":
                            # not save params if previous <BEG>	Algorithm
                            if "<BEG> Algorithm" in self.lines[line_number - 1].replace("\t", " "):
                                while not "<END PARMS>" in self.lines[line_number]:
                                    line_number += 1
                                line_number -= 1
                            else:
                                line_number += 1
                                if module not in self.params[die]:
                                    self.params[die][module] = {}
                                while not "<END PARMS>" in self.lines[line_number]:
                                    line = self.lines[line_number].strip("\t")  # out tab at beggining & end
                                    param = line.split("\t")[0]
                                    value = line.split("\t")[1].strip()
                                    line_number += 1
                                    if param not in self.excluded_parameters:
                                        if isinstance(value, float):
                                            self.params[die][module][param] = float(value)
                                        else:
                                            self.params[die][module][param] = str(value)
                                        if param not in self.params_list:
                                            self.params_list.append(param)
                    if "<BEG DATA>" in line:
                        line_number += 1
                        self.data[die][module] = {}
                        firstline = True
                        while not "<END DATA>" in self.lines[line_number]:
                            # first line with variable names
                            line = self.lines[line_number].strip("\t")  # out tab at beggining & end
                            if firstline:
                                variables_list = line.split("\t")
                                # create vars into data
                                for var in variables_list:
                                    self.data[die][module][var] = []
                                firstline = False
                            else:
                                # get data for each line
                                data_list = line.split("\t")
                                num = 0
                                # assign into var list
                                for var in variables_list:
                                    self.data[die][module][var].append(data_list[num])
                                    num += 1
                            line_number += 1
                    line_number += 1
                return [True, ""]
            if self.mode_type == "old":
                # get variables from metrics format file (no data)
                # number_dies = 0
                number_parameters = 0
                numero_linea = 0
                for line_number in range(0, self.number_lines):
                    line = self.lines[line_number]
                    if "No=" in line:
                        number_dies = int(line.replace('"', '').replace('No=', ''))
                        if number_dies <= 0:
                            return False
                    if "Nv=" in line:
                        number_parameters = int(line.replace('"', '').replace('Nv=', '')) - 2
                        if number_parameters <= 0:
                            return False
                    if '"" "COLUMN" "ROW"' in line:
                        # get parameters
                        self.params_list = line.replace('"" "COLUMN" "ROW" ', '').replace('"', '').split()
                        if len(self.params_list) != number_parameters:
                            return False
                        else:
                            numero_linea = line_number
                for line_number in range(numero_linea + 1, self.number_lines):
                    line = self.lines[line_number]
                    if line != "":
                        # while not empty
                        datos = line.replace('" " ', '').split(" ")
                        column = datos[0]
                        row = datos[1]
                        die = column + " " + row
                        module = "0 0"  # only one module is 0 0
                        if not die in self.dies:
                            self.dies.append(die)
                        if not module in self.modules:
                            self.modules.append(module)
                        # init dicts
                        self.params[die] = {}
                        self.data[die] = {}
                        self.params[die][module] = {}
                        self.data[die][module] = {}
                        # add all params
                        i = 2
                        for param in self.params_list:
                            self.params[die][module][param] = float(datos[i])
                            i += 1

                    else:
                        break
                return [True, ""]
        except Exception as e:
            return [False, "Exception : " + str(e)]

    def param_to_list(self, name_param):
        """
        Get a list with all values of a parameter
        :param name_param: Name of parameter
        :return: list with all values of a parameter
        """
        list_return = []
        if name_param in self.params_list:
            for die in self.dies:
                for module in self.modules:
                    if name_param in self.params[die][module]:
                        list_return.append(self.params[die][module][name_param])
        return list_return

    def get_params(self, name_params):
        """
        Get all parameters values
        :param name_params: Name of parameters
        :return: Dict with all parameters values
        """
        # get param + medida for get the statistics to print in QPlainText
        get_params = dict()
        for die in self.dies:
            for module in self.modules:
                for param in self.params_list:
                    if param in name_params:
                        if self.params[die][module] and param in self.params[die][module]:
                            medida = self.params[die][module][param].strip()  # get medida value
                            if not param in get_params:
                                get_params[param] = dict()  # create dict to store medida value
                                get_params[param]["medida"] = list()
                            get_params[param]["medida"].append(medida)  # append value medida to list

        return get_params

    def get_data_values(self, name_param):
        """
        Get all data values
        :param name_param: Name of parameter
        :return: Dict with all data values
        """
        # get data values chip + medida for printing in QPlainText
        get_data_values = dict()
        for die in self.dies:
            for module in self.modules:
                for param in self.params_list:
                    if param == name_param:
                        medida = self.params[die][module][param]  # get medida value
                        if not die in get_data_values:
                            get_data_values[die] = dict()
                            get_data_values[die] = medida

        return get_data_values

    def get_parameters(self):
        """
        Get all parameters
        :return: parameters dict
        """
        # return dict with all parameteres
        parameters = {
            "process_name": self.process,
            "lot_name": self.lot,
            "wafer_name": self.wafer,
            "mask_name": self.mask,
            "operator_name": self.operator,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "filename_test": "",
            "date": self.date,
            "time": self.time
        }
        return parameters

    def create_data_files(self, folder, prefix="CV_", show_die=True, show_module=True,
                          show_header=False, sep=" ", wafer="", text_die=False, text_module=False):
        """
        Create data files
        :param folder: folder to save files
        :param prefix: prefix for file name
        :param show_die: show die in file name
        :param show_module: show module in file name
        :param show_header: show header in file
        :param sep: separator
        :param wafer: wafer name
        :param text_die: Put text in die name (not number) if True
        :param text_module: Put text in module name (not number) if True
        :return: None
        """
        die_count = 0
        if wafer == "":
            wafer = self.wafer
        for die in self.dies:
            die_count += 1
            module_count = 0
            for module in self.modules:
                module_count += 1
                name_file = prefix + self.lot + "-" + wafer
                if show_die:
                    name_file += "_" + str(die_count) if not text_die else "_" + die
                if show_module:
                    name_file += "_" + str(module_count) if not text_module else "_" + module.replace("\\", "_")
                name_file += ".txt"
                key_list = self.data[die][module].keys()
                listas = list()
                for key in key_list:
                    listas.append(self.data[die][module][key])
                lista_combinada = list(zip(*listas))
                file_with_info = False
                with open(folder + "/" + name_file, 'w') as archivo:
                    if show_header:
                        linea = sep.join(str(key) for key in key_list)
                        if linea != "":
                            archivo.write(linea + '\n')
                            file_with_info = True
                    # Itera sobre la lista combinada y escribe cada tupla en una línea
                    for lista in lista_combinada:
                        linea = sep.join(str(valor) for valor in lista) # Convierte la tupla en una cadena
                        if linea != "":
                            archivo.write(linea + '\n')
                            file_with_info = True
                if not file_with_info:
                    os.remove(folder + "/" + name_file)

    def create_estepa_file(self, path, filename):
        """
        Create estepa file
        :param path: path to save file
        :param filename: name of file
        :return: None
        """
        no = len(self.dies)
        nv = len(self.params_list) + 2
        header = '""' + "\n" + "\n"
        header += '"No=' + str(no) + '"' + "\n"
        header += '"Nv=' + str(nv) + '"' + "\n" + "\n"
        header += '"" "COLUMN" "ROW" '
        for param in self.params_list:
            header += '"' + param + '" '
        header += "\n"
        f = open(path + filename, 'w')
        f.write(header)
        get_medidas = self.get_params(self.params_list)
        counter = 0
        for die in self.dies:
            line = '" "' + str(die.split(",")[0]) + " " + str(die.split(",")[1]) + " "
            for param in self.params_list:
                line += str(get_medidas[param]["medida"][counter]) + " "
            counter += 1
            line += "\n"
            f.write(line)
        f.close()