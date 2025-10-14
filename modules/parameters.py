from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
import os
import toml


class ParametersWindow(QWidget):
    def __init__(self, filename=""):
        # QMainWindow.__init__(self)
        super().__init__()
        title = ""
        min_width = 350
        width = min_width
        layout = QVBoxLayout()
        layout.setObjectName("verticalLayout")
        tabs = QTabWidget()
        tabs.setObjectName("tabs")
        self.path_file = filename
        self.toml_info = None
        self.toml_parameters = None
        self.toml_units = None
        self.toml_options = None
        self.toml_help = None
        self.error = False
        self.error_message = ""
        # read toml information
        if os.path.exists(filename):
            self.toml_info = toml.load(filename)
            if not "parameters" in self.toml_info:
                self.error = True
                self.error_message = "Not parameters found!"
            else:
                self.toml_parameters = self.toml_info["parameters"]
                if "units" in self.toml_info:
                    self.toml_units = self.toml_info["units"]
                if "options" in self.toml_info:
                    self.toml_options = self.toml_info["options"]
                if "help" in self.toml_info:
                    self.toml_help = self.toml_info["help"]

        if not self.error:
            # capture title app
            if "title" in self.toml_info:
                title = self.toml_info["title"]
            if "width" in self.toml_info:
                width = int(self.toml_info["width"])
                if width < min_width:
                    width = min_width
            self.layoutSubGroup = dict()

            for elem in self.toml_info:
                if elem != "units" and elem != "options" and elem != "help" and isinstance(self.toml_info[elem], dict):
                    if elem != "WIDTH":
                        tabs.addTab(self.field_to_layout(elem), elem.upper())

            layout.addWidget(tabs)
            button = QPushButton("Save configuration")
            button.clicked.connect(self.save_configuration)
            button.setObjectName("btnSave")
            layout.addWidget(button)

            self._layout = layout
            self.setLayout(self._layout)
            # self.setCentralWidget(button)

        self.setFixedWidth(width)
        # self.resize(400,500)
        self.setWindowTitle(title)
        if self.error:
            raise Exception(self.error_message)

    def field_to_layout(self, var):
        # create layout
        groupTab = QWidget()
        groupTab.setObjectName("groupTab_" + var)
        layoutGroup = QVBoxLayout()
        layoutGroup.setObjectName("verticalLayout_" + var)

        self.layoutSubGroup[var] = QGridLayout()
        self.layoutSubGroup[var].setObjectName("gridLayout_" + var)
        count = 0
        for elem in self.toml_info[var]:
            # add label
            wg = QLabel(elem)
            if elem in self.toml_help:
                wg.setToolTip(self.toml_help[elem])
            self.layoutSubGroup[var].addWidget(wg, count, 0)

            # add widgets
            if isinstance(self.toml_info[var][elem], bool):
                wg = QCheckBox()
                wg.setObjectName(elem)
                wg.setChecked(self.toml_info[var][elem])
                self.layoutSubGroup[var].addWidget(wg, count, 1)
                unit = ""
                if elem in self.toml_units:
                    unit = self.toml_units[elem]
                wg = QLabel(unit)
                self.layoutSubGroup[var].addWidget(wg, count, 2)
            elif isinstance(self.toml_info[var][elem], float) or self.toml_info[var][elem] == 0:
                wg = QDoubleSpinBox()
                wg.setObjectName(elem)
                wg.setMaximum(9999999)
                wg.setMinimum(-9999999)
                wg.setDecimals(4)
                wg.setValue(self.toml_info[var][elem])
                self.layoutSubGroup[var].addWidget(wg, count, 1)
                unit = ""
                if elem in self.toml_units:
                    unit = self.toml_units[elem]
                wg = QLabel(unit)
                self.layoutSubGroup[var].addWidget(wg, count, 2)
            elif isinstance(self.toml_info[var][elem], int):
                wg = QSpinBox()
                wg.setObjectName(elem)
                wg.setMaximum(9999999)
                wg.setMinimum(-9999999)
                wg.setValue(self.toml_info[var][elem])
                self.layoutSubGroup[var].addWidget(wg, count, 1)
                unit = ""
                if elem in self.toml_units:
                    unit = self.toml_units[elem]
                wg = QLabel(unit)
                self.layoutSubGroup[var].addWidget(wg, count, 2)
            elif isinstance(self.toml_info[var][elem], str):
                if elem in self.toml_options:
                    # create combobox
                    wg = QComboBox()
                    wg.setObjectName(elem)
                    options = self.toml_options[elem].split(",")
                    wg.addItems(options)
                    wg.setCurrentText(self.toml_info[var][elem])
                    self.layoutSubGroup[var].addWidget(wg, count, 1)
                else:
                    wg = QLineEdit(elem)
                    wg.setObjectName(elem)
                    wg.setText(self.toml_info[var][elem])
                    self.layoutSubGroup[var].addWidget(wg, count, 1)
                unit = ""
                if elem in self.toml_units:
                    unit = self.toml_units[elem]
                wg = QLabel(unit)
                self.layoutSubGroup[var].addWidget(wg, count, 2)
            count += 1
        layoutGroup.addLayout(self.layoutSubGroup[var])
        groupTab.setLayout(layoutGroup)
        return groupTab

    def save_configuration(self):
        for elem in self.toml_info:
            if elem != "units" and elem != "options" and elem != "help" and isinstance(self.toml_info[elem], dict):
                section = elem
                for i in reversed(range(self.layoutSubGroup[elem].count())):
                    if self.layoutSubGroup[elem].itemAt(i).widget().objectName() != "":
                        subSection = self.layoutSubGroup[elem].itemAt(i).widget().objectName()
                        if isinstance(self.layoutSubGroup[elem].itemAt(i).widget(), QComboBox):
                            self.toml_info[section][subSection] = self.layoutSubGroup[elem].itemAt(
                                i).widget().currentText()
                        if isinstance(self.layoutSubGroup[elem].itemAt(i).widget(), QCheckBox):
                            self.toml_info[section][subSection] = self.layoutSubGroup[elem].itemAt(
                                i).widget().isChecked()
                        if isinstance(self.layoutSubGroup[elem].itemAt(i).widget(), QLineEdit):
                            self.toml_info[section][subSection] = self.layoutSubGroup[elem].itemAt(i).widget().text()
                        if isinstance(self.layoutSubGroup[elem].itemAt(i).widget(), QSpinBox) or \
                                isinstance(self.layoutSubGroup[elem].itemAt(i).widget(), QDoubleSpinBox):
                            self.toml_info[section][subSection] = self.layoutSubGroup[elem].itemAt(i).widget().value()
        # save config
        toml_file = open(self.path_file, "w", encoding="utf-8")
        toml.dump(self.toml_info, toml_file)
        toml_file.close()


# class DeviceParametersWindow(QWidget):
#     """
#     Ventana de configuración para instrumentos o probers (instruments.toml / probers.toml).
#     Permite editar los parámetros del dispositivo seleccionado.
#     """
#     def __init__(self, toml_path, device_name):
#         super().__init__()
#         self.toml_path = toml_path
#         self.device_name = device_name
#         self.setWindowTitle(f"Parameters: {device_name}")
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)
#
#         # Cargar configuración completa del fichero TOML
#         import toml
#         if not os.path.exists(toml_path):
#             raise FileNotFoundError(f"{toml_path} not found.")
#         self.toml_data = toml.load(toml_path)
#
#         if device_name not in self.toml_data:
#             raise KeyError(f"Device {device_name} not found in {toml_path}")
#
#         self.device_data = self.toml_data[device_name]
#         self.fields = {}
#
#         form = QFormLayout()
#         for key, value in self.device_data.items():
#             widget = None
#
#             if isinstance(value, bool):
#                 widget = QCheckBox()
#                 widget.setChecked(value)
#             elif isinstance(value, int):
#                 widget = QSpinBox()
#                 widget.setMaximum(9999999)
#                 widget.setMinimum(-9999999)
#                 widget.setValue(value)
#             elif isinstance(value, float):
#                 widget = QDoubleSpinBox()
#                 widget.setMaximum(9999999)
#                 widget.setMinimum(-9999999)
#                 widget.setDecimals(3)
#                 widget.setValue(value)
#             else:
#                 display_value = (
#                     str(value)
#                     .replace("\r", "\\r")
#                     .replace("\n", "\\n")
#                 )
#                 widget = QLineEdit(display_value)
#
#             form.addRow(QLabel(key), widget)
#             self.fields[key] = widget
#
#         self.layout.addLayout(form)
#
#         # Botón guardar
#         save_button = QPushButton("Save configuration")
#         save_button.clicked.connect(self.save_configuration)
#         self.layout.addWidget(save_button)
#
#         self.setMinimumWidth(400)
#
#     def save_configuration(self):
#         """Guardar cambios en el fichero TOML."""
#         for key, widget in self.fields.items():
#             if isinstance(widget, QCheckBox):
#                 self.device_data[key] = widget.isChecked()
#             elif isinstance(widget, QSpinBox) or isinstance(widget, QDoubleSpinBox):
#                 self.device_data[key] = widget.value()
#             elif isinstance(widget, QLineEdit):
#                 text = widget.text()
#
#                 # Convertir secuencias visibles "\n" o "\r" a caracteres reales
#                 text = (
#                     text.replace("\\r", "\r")
#                     .replace("\\n", "\n")
#                 )
#
#                 # Intentar convertir a número si aplica
#                 if text.isdigit():
#                     self.device_data[key] = int(text)
#                 else:
#                     try:
#                         self.device_data[key] = float(text)
#                     except ValueError:
#                         self.device_data[key] = text
#
#         # Sobrescribir el bloque correspondiente en el TOML
#         self.toml_data[self.device_name] = self.device_data
#         with open(self.toml_path, "w", encoding="utf-8") as f:
#             import toml
#             toml.dump(self.toml_data, f)
#
#         QMessageBox.information(self, "Saved", f"Configuration saved for {self.device_name}")


class DeviceParametersWindow(QWidget):
    def __init__(self, toml_path, device_name):
        super().__init__()
        self.toml_path = toml_path
        self.device_name = device_name
        self.setWindowTitle(f"Parameters: {device_name}")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        import toml
        if not os.path.exists(toml_path):
            raise FileNotFoundError(f"{toml_path} not found.")
        self.toml_data = toml.load(toml_path)

        # Buscar sección principal y posibles subbloques
        if device_name not in self.toml_data:
            raise KeyError(f"Device {device_name} not found in {toml_path}")

        self.device_data = self.toml_data[device_name]
        self.fields = {}

        tabs = QTabWidget()
        tabs.addTab(self._build_form(self.device_data, device_name), "Main")

        # Buscar subbloques como [device_name.xxx]
        # prefix = device_name + "."
        # for key in self.toml_data.keys():
        #     if key.startswith(prefix):
        #         subname = key.split(".")[1]
        #         subdata = self.toml_data[key]
        #         tabs.addTab(self._build_form(subdata, subname), subname)
        # Buscar subbloques dentro del diccionario principal (anidados)
        for subname, subdata in self.device_data.items():
            if isinstance(subdata, dict):
                tabs.addTab(self._build_form(subdata, subname), subname)
        self.layout.addWidget(tabs)

        # Botón guardar
        save_button = QPushButton("Save configuration")
        save_button.clicked.connect(self.save_configuration)
        self.layout.addWidget(save_button)
        self.setMinimumWidth(450)

    def _build_form(self, section_data, section_name):
        """Crea un formulario (tab) para un bloque de configuración"""
        form = QFormLayout()
        container = QWidget()
        container.setLayout(form)

        if section_name not in self.fields:
            self.fields[section_name] = {}

        for key, value in section_data.items():
            # ⚠️ Ignorar subdiccionarios (que ya tendrán su pestaña)
            if isinstance(value, dict):
                continue
            if isinstance(value, bool):
                widget = QCheckBox()
                widget.setChecked(value)
            elif isinstance(value, int):
                widget = QSpinBox()
                widget.setMaximum(9999999)
                widget.setMinimum(-9999999)
                widget.setValue(value)
            elif isinstance(value, float):
                widget = QDoubleSpinBox()
                widget.setMaximum(9999999)
                widget.setMinimum(-9999999)
                widget.setDecimals(3)
                widget.setValue(value)
            else:
                # Mostrar secuencias de escape visibles
                display_value = (
                    str(value)
                    .replace("\r", "\\r")
                    .replace("\n", "\\n")
                )
                widget = QLineEdit(display_value)

            form.addRow(QLabel(key), widget)
            self.fields[section_name][key] = widget

        return container

    def save_configuration(self):
        """Guardar cambios en el fichero TOML."""
        for section_name, section_fields in self.fields.items():
            # Referencia al bloque correcto dentro del diccionario principal
            if section_name == self.device_name:
                target_dict = self.toml_data[self.device_name]
            else:
                # Asegurar que el subdiccionario existe dentro del principal
                if section_name not in self.toml_data[self.device_name]:
                    self.toml_data[self.device_name][section_name] = {}
                target_dict = self.toml_data[self.device_name][section_name]

            # Actualizar valores
            for key, widget in section_fields.items():
                if isinstance(widget, QCheckBox):
                    val = widget.isChecked()
                elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                    val = widget.value()
                elif isinstance(widget, QLineEdit):
                    val = widget.text().replace("\\r", "\r").replace("\\n", "\n")
                    if val.isdigit():
                        val = int(val)
                    else:
                        try:
                            val = float(val)
                        except ValueError:
                            pass
                else:
                    val = widget.text()

                target_dict[key] = val

        import toml
        with open(self.toml_path, "w", encoding="utf-8") as f:
            toml.dump(self.toml_data, f)

        QMessageBox.information(self, "Saved", f"Configuration saved for {self.device_name}")

