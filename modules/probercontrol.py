from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QMessageBox, QGridLayout, QSpinBox, QDoubleSpinBox
)
from PySide6.QtCore import Qt

class ProberControl(QWidget):
    def __init__(self, main_context, prober_name):
        super().__init__()
        self.main = main_context
        self.setWindowTitle(f"Prober Control - {prober_name}")

        layout = QVBoxLayout()

        # --- MOVIMIENTO XY ---
        layout.addWidget(QLabel("<b>Movement XY</b>"))
        grid_xy = QGridLayout()
        self.cmbRefXY = QComboBox()
        self.cmbRefXY.addItems(["Zero", "Home", "Relative", "Center", "User", "Z", "H", "R", "C"])
        self.txtX = QDoubleSpinBox();
        self.txtX.setRange(-100000, 100000);
        self.txtX.setDecimals(4)
        self.txtY = QDoubleSpinBox();
        self.txtY.setRange(-100000, 100000);
        self.txtY.setDecimals(4)
        btnGoXY = QPushButton("Go XY")
        btnGoXY.clicked.connect(self.move_xy)
        grid_xy.addWidget(QLabel("Reference:"), 0, 0)
        grid_xy.addWidget(self.cmbRefXY, 0, 1)
        grid_xy.addWidget(QLabel("X:"), 1, 0)
        grid_xy.addWidget(self.txtX, 1, 1)
        grid_xy.addWidget(QLabel("Y:"), 2, 0)
        grid_xy.addWidget(self.txtY, 2, 1)
        grid_xy.addWidget(btnGoXY, 1, 2, 2, 1)
        layout.addLayout(grid_xy)

        # --- MOVIMIENTO Z ---
        layout.addWidget(QLabel("<b>Movement Z</b>"))
        grid_z = QGridLayout()
        self.cmbRefZ = QComboBox()
        self.cmbRefZ.addItems(["Zero", "Contact", "Separation", "Relative"])
        self.txtZ = QDoubleSpinBox();
        self.txtZ.setRange(-10000, 10000);
        self.txtZ.setDecimals(4)
        btnGoZ = QPushButton("Go Z")
        btnGoZ.clicked.connect(self.move_z)
        grid_z.addWidget(QLabel("Reference:"), 0, 0)
        grid_z.addWidget(self.cmbRefZ, 0, 1)
        grid_z.addWidget(QLabel("Z:"), 1, 0)
        grid_z.addWidget(self.txtZ, 1, 1)
        grid_z.addWidget(btnGoZ, 1, 2)
        layout.addLayout(grid_z)

        # --- POSICIÓN / HOME / CONTACTO ---
        layout.addWidget(QLabel("<b>Quick Moves</b>"))

        # 🔸 Nuevo combo para referencia de posición (Zero, Home, Current, Center)
        ref_layout = QHBoxLayout()
        ref_layout.addWidget(QLabel("Reference (Get Position):"))
        self.cmbRefGetPos = QComboBox()
        self.cmbRefGetPos.addItems(["Zero", "Home", "Current", "Center"])
        self.cmbRefGetPos.setCurrentText("Current")
        ref_layout.addWidget(self.cmbRefGetPos)
        layout.addLayout(ref_layout)

        move_buttons = QHBoxLayout()
        for label, func in [
            ("Home", self.move_home),
            ("Center", self.move_center),
            ("Contact", self.move_contact),
            ("Separation", self.move_separation),
            ("Get Position", self.get_position)
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(func)
            move_buttons.addWidget(btn)
        layout.addLayout(move_buttons)

        # --- VACUUM ---
        layout.addWidget(QLabel("<b>Vacuum Control</b>"))
        vac_layout = QHBoxLayout()
        self.cmbVacuumRef = QComboBox()
        self.cmbVacuumRef.addItems(["Wafer", "AuxRight", "AuxRight2", "AuxLeft", "AuxLeft2"])
        btnVacOn = QPushButton("Vacuum ON")
        btnVacOff = QPushButton("Vacuum OFF")
        btnVacOn.clicked.connect(lambda: self.set_vacuum(1))
        btnVacOff.clicked.connect(lambda: self.set_vacuum(0))
        vac_layout.addWidget(self.cmbVacuumRef)
        vac_layout.addWidget(btnVacOn)
        vac_layout.addWidget(btnVacOff)
        layout.addLayout(vac_layout)

        # --- LUZ ---
        layout.addWidget(QLabel("<b>Light Control</b>"))
        light_layout = QHBoxLayout()
        btnLightOn = QPushButton("Light ON")
        btnLightOff = QPushButton("Light OFF")
        btnLightOn.clicked.connect(lambda: self.light(1))
        btnLightOff.clicked.connect(lambda: self.light(0))
        light_layout.addWidget(btnLightOn)
        light_layout.addWidget(btnLightOff)
        layout.addLayout(light_layout)

        # --- TEMPERATURA CHUCK ---
        layout.addWidget(QLabel("<b>Chuck Temperature</b>"))
        temp_layout = QHBoxLayout()
        self.txtTemp = QDoubleSpinBox()
        self.txtTemp.setRange(-50, 300)
        self.txtTemp.setDecimals(1)
        btnGetTemp = QPushButton("Get Temp")
        btnSetTemp = QPushButton("Set Temp")
        btnGetTemp.clicked.connect(self.get_temp)
        btnSetTemp.clicked.connect(self.set_temp)
        temp_layout.addWidget(self.txtTemp)
        temp_layout.addWidget(btnGetTemp)
        temp_layout.addWidget(btnSetTemp)
        layout.addLayout(temp_layout)

        # --- Mostrar posición actual ---
        self.lblPos = QLabel("Position: -")
        layout.addWidget(self.lblPos)

        self.setLayout(layout)
        self.setFixedWidth(450)

    # -----------------------------
    # Métodos conectados
    # -----------------------------
    def move_xy(self):
        ref = self.cmbRefXY.currentText()
        x = self.txtX.value()
        y = self.txtY.value()
        try:
            self.main.prober.move_chuck_xy(ref, x, y)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error moving XY:\n{e}")

    def move_z(self):
        ref = self.cmbRefZ.currentText()
        z = self.txtZ.value()
        try:
            self.main.prober.move_chuck_z(ref, z)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error moving Z:\n{e}")

    def move_home(self): self._call("move_home")
    def move_center(self): self._call("move_center")
    def move_contact(self): self._call("move_contact")
    def move_separation(self): self._call("move_separation")

    def get_position(self):
        try:
            reference = self.cmbRefGetPos.currentText()
            xy = self.main.prober.get_chuck_xy(reference)
            z = self.main.prober.get_chuck_z(reference)
            self.lblPos.setText(f"Position ({reference}): XY={xy}, Z={z}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error getting position ({reference}):\n{e}")

    def get_temp(self):
        try:
            temp = self.main.prober.get_chuck_temp()
            self.txtTemp.setValue(float(temp))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error reading temperature:\n{e}")

    def set_temp(self):
        try:
            temp = self.txtTemp.value()
            self.main.prober.set_chuck_temp(temp)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error setting temperature:\n{e}")

    def light(self, mode):
        try:
            self.main.prober.light(mode)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error controlling light:\n{e}")

    def set_vacuum(self, mode):
        ref = self.cmbVacuumRef.currentText()
        try:
            status = self.main.prober.get_vacuum_status(ref)
            self.main.prober.set_vacuum(mode)
            QMessageBox.information(
                self,
                "Vacuum",
                f"Vacuum {ref} set to {'ON' if mode else 'OFF'} (previous status: {status})"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error controlling vacuum:\n{e}")

    def _call(self, method):
        try:
            getattr(self.main.prober, method)()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error calling {method}:\n{e}")
