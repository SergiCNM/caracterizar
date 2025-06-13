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
            self.layoutSubGroup = dict()

            for elem in self.toml_info:
                if elem != "units" and elem != "options" and elem != "help" and isinstance(self.toml_info[elem], dict):
                    tabs.addTab(self.field_to_layout(elem), elem.upper())

            layout.addWidget(tabs)
            button = QPushButton("Save configuration")
            button.clicked.connect(self.save_configuration)
            button.setObjectName("btnSave")
            layout.addWidget(button)

            self._layout = layout
            self.setLayout(self._layout)
            # self.setCentralWidget(button)

        self.setFixedWidth(300)
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
