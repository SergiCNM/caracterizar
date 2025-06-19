import os
import numpy as np
from datetime import datetime

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from modules.ui_wafer import Ui_WaferWindow
from modules.ui_modules import Ui_ModulesWindow
from modules.ui_plot import Ui_PlotWindow
from modules.plots import *


from functools import partial
from functions import *
from config.defs import *


class Wafer(QMainWindow):
    def __init__(self, wafer_parameters):
        QMainWindow.__init__(self)
        # wafer parameters, array with 15 parameters
        self.wafer_error = False
        self.waferwindow = ""
        self.wafer_parameters = wafer_parameters
        try:
            if len(wafer_parameters)>=13:
                self.wafer_name = wafer_parameters["wafer_name"]
                self.wafer_size_inch = wafer_parameters["wafer_size"]
                self.wafer_size_mm = 0
                self.thickness = 0
                self.set_wafer_size()
                self.xsize = float(wafer_parameters["xsize"])
                self.ysize = float(wafer_parameters["ysize"])

                # xmax & ymax optionals
                if "xmax" in wafer_parameters:
                    self.xmax = wafer_parameters["xmax"]
                else:
                    self.xmax = 0

                if "ymax" in wafer_parameters:
                    self.ymax = wafer_parameters["ymax"]
                else:
                    self.ymax = 0

                #self.ymax = 0
                self.nchips = int(wafer_parameters["nchips"])
                self.nmodules = int(wafer_parameters["nmodules"])
                self.origin_chip = wafer_parameters["origin_chip"]
                self.home_chip = wafer_parameters["home_chip"]
                self.flat_orientation = int(wafer_parameters["flat_orientation"])
                self.wafer_positions = wafer_parameters["wafer_positions"]
                self.wafer_modules = wafer_parameters["wafer_modules"]
                if "wafer_modules_name" in wafer_parameters:
                    self.wafer_modules_name = wafer_parameters["wafer_modules_name"]
                else:
                    self.wafer_modules_name = self.wafer_modules
                self.real_origin_chip = wafer_parameters["real_origin_chip"]
                self.navigation_options = wafer_parameters["navigation_options"]
            else:
                self.wafer_parameters = ""
                self.wafer_error = True
                retval = messageBox(self,"Problem with ppg parameters","Wafer file not initialized","error")

        except:
            self.wafer_parameters = ""
            self.wafer_error = True
            retval = messageBox(self,"Problem initializing class Wafer","Wafer file not initialized","error")

    def set_wafer_size(self):
        self.wafer_size_mm, self.thickness = calc_wafer_size(float(self.wafer_size_inch))

    def check_wafer_parameters(self):
        check_wafer_parameters = True
        # check wafer_positions & nchips
        if len(self.wafer_positions)!=int(self.nchips):
            check_wafer_parameters = False
            print("Error checking number of chips (" + str(self.nchips) + ") <> wafer_positions size ( " + str(len(self.wafer_positions)) + ")")
        # check wafer_size
        if self.wafer_size_mm == 0 or self.thickness == 0:
            check_wafer_parameters = False
            print("Error checking wafer_size_mm and wafer thickness...")
        # check xsize and ysize
        wafer_size_um = float(self.wafer_size_mm*1000)
        if wafer_size_um<self.xsize or wafer_size_um<self.ysize:
            check_wafer_parameters = False
            print("Error checking xsize & ysize...")
        # check home chip (is possible home chip not in wafer_position to measure)
        # if self.home_chip not in self.wafer_positions:
        #     check_wafer_parameters = False
        #     print("Error checking home chip...")
        # check origin chip 
        if self.origin_chip not in self.wafer_positions:
            check_wafer_parameters = False
            print("Error checking origin chip...")
        # check flat orientation
        flat_orientation_array = [0,90,180,270]
        if self.flat_orientation not in flat_orientation_array:
            check_wafer_parameters = False
            print("Error checking flat orientation...")
        # set xmax & ymax
        if check_wafer_parameters:
            xmax_detected = 0
            ymax_detected = 0
            elementos_x_detected = []
            elementos_y_detected = []
            for elemento in self.wafer_positions:
                elemento_array = elemento.split()
                if len(elemento_array)!=2:
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
                    for elemento_buscar in self.wafer_positions:
                        elemento_buscar_array = elemento_buscar.split()
                        if elemento_buscar_array[0] == elemento_x:
                            num_elemento_y += 1 # cambiamos el eje porque buscamos sumatorio en vertical
                        if elemento_buscar_array[1] == elemento_y:
                            num_elemento_x += 1 # cambiamos el eje porque buscamos sumatorio en horizontal

                    if num_elemento_x>xmax_detected:
                        xmax_detected = num_elemento_x
                    if num_elemento_y>ymax_detected:
                        ymax_detected = num_elemento_y

            # if xmax or ymax not initialized then equal to detected
            if self.xmax==0:
                self.xmax = xmax_detected
            if self.ymax==0:
                self.ymax = ymax_detected

            if xmax_detected!=self.xmax and ymax_detected!=self.ymax:
                check_wafer_parameters = False
                print("Error checking xmax (" + str(xmax_detected) + ") & ymax (" + str(ymax_detected) + ")...")

        # check navigation options
        if len(self.navigation_options)!=3:
            check_wafer_parameters = False
            print("Error checking navigation options, not all parameters passed!")
        else:
            # verify parameters
            starting_location = self.navigation_options[0]
            if not starting_location in ["UPPER-LEFT","UPPER-RIGHT","BOTTOM-LEFT","BOTTOM-RIGHT"]:
                check_wafer_parameters = False
                print("Error checking navigation options (starting location). " + starting_location + " not allowed value!")
            else :
                direction_movement = self.navigation_options[1]
                if not direction_movement in ["BI-DIRECTIONAL","UNI-DIRECTIONAL"]:
                    check_wafer_parameters = False
                    print("Error checking navigation options (directional movement). " + direction_movement + " not allowed value!")
                else :
                    move_by = self.navigation_options[2]
                    if not move_by in ["ROW","COLUMN"]:
                        check_wafer_parameters = False
                        print("Error checking navigation options (move by). " + move_by + " not allowed value!")

        # verifiy wafer_position according to navigation_options


        return check_wafer_parameters

    def calculate_real_coordinate(self, from_coordinate):
        to_coordinate=self.real_origin_chip
        from_array = from_coordinate.split()
        to_array = to_coordinate.split()
        X_from = int(from_array[0])
        Y_from = int(from_array[1])
        X_to = int(to_array[0])
        Y_to = int(to_array[1])
        movement_X = (X_to+X_from) # change sign axis X
        movement_Y = (Y_from+Y_to) # same sign axis Y
        # adjust flat orientation
        if self.flat_orientation!=0:
            if self.flat_orientation==180:
                movement_X = movement_X*-1
                movement_Y = movement_Y*-1
            else:
                if self.flat_orientation==90:
                    movement_X, movement_Y = movement_Y, movement_X*-1
                else:
                    if self.flat_orientation==270:
                        movement_X, movement_Y = movement_Y*-1, movement_X


        return str(movement_X) + " " + str(movement_Y)

    def calculate_prober_movement(self,from_coordinate,to_coordinate,coordinates=True):
        # return X & Y movement
        # get coordinates X & Y
        if coordinates:
            from_array = from_coordinate.split()
            to_array = to_coordinate.split()
            X_from = int(from_array[0])
            Y_from = int(from_array[1])
            X_to = int(to_array[0])
            Y_to = int(to_array[1])
            # calculate movement in um & change signs
            movement_X = (X_to-X_from)*self.xsize # change sign axis X
            movement_Y = (Y_from-Y_to)*self.ysize # same sign axis Y
        else:
            movement_X = from_coordinate
            movement_Y = to_coordinate

        # adjust flat orientation
        if self.flat_orientation!=0:
            if self.flat_orientation==180:
                movement_X = movement_X*-1
                movement_Y = movement_Y*-1
            else:
                if self.flat_orientation==90:
                    movement_X, movement_Y = movement_Y, movement_X*-1
                else:
                    if self.flat_orientation==270:
                        movement_X, movement_Y = movement_Y*-1, movement_X


        return [movement_X,movement_Y]

    def calculate_init_prober_movement(self):
        if self.home_chip!=self.origin_chip:
            return self.calculate_prober_movement(self.home_chip,self.origin_chip)
        return [0,0]

    def calculate_process_percentage(self,die,module, init_chip, end_chip):
        # nchips = self.nchips
        # nmodules = self.nmodules
        # total = nchips * nmodules
        # calc = int(die)*int(module)/int(total) * 100
        # percentage = "{:.2f}".format(calc)
        # return float(percentage)
        nmodules = int(self.nmodules)
        total_chips = int(end_chip) - int(init_chip) + 1
        total = total_chips * nmodules

        # Ajustar die al rango actual (ej: si init_chip=12, die=12 → offset = 0)
        die_offset = int(die) - int(init_chip)
        current = die_offset * nmodules + (int(module) - 1)

        percentage = (current + 1) / total * 100
        return round(percentage, 2)

    def calculate_finish_time(self,date_init,die,module, init_chip, end_chip):
        # date_now = datetime.now()
        # difference = date_now-date_init
        # nchips = self.nchips
        # nmodules = self.nmodules
        # total = nchips * nmodules
        # total_seconds = difference * int(total) /(((int(die)-1) * int(nmodules)) + int(module))
        # finish_time = date_init + total_seconds
        # return finish_time.strftime('%Y-%m-%d %H:%M:%S')
        date_now = datetime.now()
        time_elapsed = date_now - date_init

        nmodules = int(self.nmodules)
        total_chips = int(end_chip) - int(init_chip) + 1
        total = total_chips * nmodules

        # Ajustar die al rango actual
        die_offset = int(die) - init_chip
        current_index = die_offset * nmodules + (int(module) - 1)

        if current_index <= 0:
            return "Calculating..."

        avg_time_per_step = time_elapsed / (current_index + 1)
        total_duration = avg_time_per_step * total
        estimated_end = date_init + total_duration

        return estimated_end.strftime('%Y-%m-%d %H:%M:%S')

    def create_wafer_window(self,enable):
        self.waferwindow = WaferWindow(self.wafer_parameters,enable)
        return self.waferwindow

    def is_home(self,x,y):
        # pass x,y position
        if self.real_origin_chip!="" and self.home_chip!="":
            real_origin_chipX , real_origin_chipY = self.real_origin_chip.split()
            home_chipX , home_chipY = self.home_chip.split()
            if int(x)*-1 - int(float(real_origin_chipX)) == int(float(home_chipX)) and int(y)*-1 - int(float(real_origin_chipY)) == int(float(home_chipY)):
                return True
        return False

    def is_origin(self,x,y):
        # pass x,y position
        if self.real_origin_chip!="":
            real_origin_chipX , real_origin_chipY = self.real_origin_chip.split()
            origin_chipX , origin_chipY = self.origin_chip.split()
            if int(x)*-1 - int(float(real_origin_chipX)) == int(float(origin_chipX)) and int(y)*-1 - int(float(real_origin_chipY)) == int(float(origin_chipY)):
                return True
        return False

    def is_in(self,x,y):
        # (x-a)² + (y-b)² = R²
        # miramos si los 4 puntos estan dentro 
        is_in = True
        R = float(self.wafer_size_mm)/2
        xstep = float(self.xsize)/1000
        ystep = float(self.ysize)/1000
        a1 = int(abs(x))*xstep
        b1 = int(abs(y))*ystep
        a = { 1:a1, 2:a1+xstep, 3:a1, 4:a1+xstep}
        b = { 1:b1, 2:b1, 3:b1+ystep, 4:b1+ystep}
        for i in range(1,5):
            if pow(R-a[i],2)+pow(R-b[i],2)>pow(R,2):
                # is out
                is_in = False
                break

        return is_in

    def is_to_measure(self,x,y):
        is_to_measure = False
        if len(self.wafer_positions)>0:
            if self.real_origin_chip!="":
                real_origin_chipX , real_origin_chipY = self.real_origin_chip.split()
                realX = -int(x) - int(real_origin_chipX)
                realY = -int(y) - int(real_origin_chipY)
                realpos = str(realX) + " " + str(realY)
                if realpos in self.wafer_positions:
                    is_to_measure = True
        return is_to_measure

    def save_wafermap(self):

        dir_wafermaps = os.getcwd() + base_dir + wafermaps_dir + "/"
        nameFile, _ = QFileDialog.getSaveFileName(self, 'Save wafermap', dir_wafermaps,"Wafermaps (*.py)")
        # and then you need to adjust wafer_parameters
        texto = 'global wafer_parameters\n\
\n\
\n\
# Configuration wafer parameters\n\
wafer_name = "' + self.wafer_name + '"\n\
wafer_size = ' + str(self.wafer_size_inch) + '\n\
xsize = ' + str(self.xsize) + '\n\
ysize = ' + str(self.ysize) + '\n\
nchips = ' + str(self.nchips) + '\n\
nmodules = ' + str(self.nmodules) + '\n\
\n\
real_origin_chip = "' + str(self.real_origin_chip) + '"\n\
origin_chip = "' + str(self.origin_chip) + '" # normaly start with 0,0\n\
home_chip = "' + str(self.home_chip) + '" # home (0um , 0um) could be different to origin (first die to measure)\n\
flat_orientation = ' + str(self.flat_orientation) + ' # flat orientation: 0, 90, 180 or 270\n\
\n\
# navigation options\n\
navigation_options = ' + str(self.navigation_options) + '\n\
\n\
# wafer positions\n\
wafer_positions = ' + str(self.wafer_positions) + '\n\
# distances from chip origin\n\
wafer_modules = ' + str(self.wafer_modules) + '\n\
# modules name\n\
wafer_modules_name = ' + str(self.wafer_modules_name) + '\n\
\n\
# wafer parameters\n\
wafer_parameters = {\n\
\n\
"wafer_name": wafer_name,\n\
"wafer_size": wafer_size,\n\
"xsize": xsize,\n\
"ysize": ysize,\n\
"nchips": nchips,\n\
"nmodules": nmodules,\n\
"origin_chip": origin_chip,\n\
"home_chip": home_chip,\n\
"flat_orientation": flat_orientation,\n\
"wafer_positions": wafer_positions,\n\
"wafer_modules": wafer_modules,\n\
"wafer_modules_name": wafer_modules_name,\n\
"real_origin_chip": real_origin_chip,\n\
"navigation_options": navigation_options\n\
\n\
}'

        if nameFile!="":
            # create texto
            with open(nameFile, 'w') as f:
                f.write(texto)
            retval = messageBox(self,"Save wafermap","Wafermap file saved!","info")



class ModulesWindow(QMainWindow):
    def __init__(self, WaferWindow, enable):
        QMainWindow.__init__(self)
        self.ui = Ui_ModulesWindow()
        self.ui.setupUi(self)
        global widgets
        self.max_modules = 40  # max modules in wafer, if changed then change also in ui_modules.py
        widgets = self.ui
        widgets.txtNumberModules.setText(str(WaferWindow.widgets.txtNumberModules.value()))
        WaferWindow.wafer_nmodules = WaferWindow.widgets.txtNumberModules.value()
        #self.wafer = wafer
        #self.wafer_nmodules = wafer_nmodules
        #self.wafer_modules = wafer_modules
        i = 1
        for modul in WaferWindow.wafer_modules:
            modul_array = modul.split()
            if len(modul_array)==2:
                name_widget = "txtX" + str(i)
                self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).setValue(float(modul_array[0]))
                name_widget = "txtY" + str(i)
                self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).setValue(float(modul_array[1]))
                name_widget = "txtN" + str(i)
                if WaferWindow.wafer_modules_name:
                    self.ui.centralwidget.findChild(QLineEdit, name_widget).setText(WaferWindow.wafer_modules_name[i-1])
                i = i + 1
            else:
                print("Error getting modules")
                break
        for i in range(1, int(WaferWindow.wafer_nmodules)):
            name_widget = "txtX" + str(i)
            self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).setEnabled(True)
            name_widget = "txtY" + str(i)
            self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).setEnabled(True)
            name_widget = "txtN" + str(i)
            self.ui.centralwidget.findChild(QLineEdit, name_widget).setEnabled(True)
        for i in range(int(WaferWindow.wafer_nmodules)+1,self.max_modules + 1):
            name_widget = "txtX" + str(i)
            self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).setEnabled(False)
            self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).setValue(0)
            name_widget = "txtY" + str(i)
            self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).setEnabled(False)
            self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).setValue(0)
            name_widget = "txtN" + str(i)
            self.ui.centralwidget.findChild(QLineEdit, name_widget).setEnabled(False)
            self.ui.centralwidget.findChild(QLineEdit, name_widget).setText("Module_" + str(i))

        widgets.btnSaveModules.clicked.connect(partial(self.SaveModules,WaferWindow))

    def SaveModules(self, WaferWindow):
        wafer_modules = []
        wafer_modules_name = []
        for i in range (1,int(WaferWindow.wafer_nmodules)+1):
            name_widget = "txtX" + str(i)
            X = self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).value()
            name_widget = "txtY" + str(i)
            Y = self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).value()
            coord = str(X) + " " + str(Y)
            wafer_modules.append(coord)
            name_widget = "txtN" + str(i)
            name = self.ui.centralwidget.findChild(QLineEdit, name_widget).text()
            if name=="":
                name = "Module_" + str(i)
            wafer_modules_name.append(name)
        WaferWindow.wafer_modules = wafer_modules
        WaferWindow.wafer_modules_name = wafer_modules_name
        self.close()




class WaferWindow(QMainWindow):
    def __init__(self, wafer_parameters, enable):
        #super().__init__()
        QMainWindow.__init__(self)
        global set_home, set_origin

        set_home = False
        set_origin = False

        self.ui = Ui_WaferWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui
        self.widgets = widgets
        self.moduleswindow = ""

        wafer = Wafer(wafer_parameters)
        self.wafer = wafer
        self.wafer_parameters = wafer_parameters
        self.wafer_modules = wafer.wafer_modules
        # create wafer modules name if not exists
        self.wafer_modules_name = wafer.wafer_modules_name
        self.wafer_nmodules = wafer.nmodules
        self.view_modules = wafer.nmodules # see last module (default)
        self.max_size = 860 # MAX_SIZE w/h BUTTONS
        self.max_window_size = 1100 # MAX WINDOW SIZE w/h

        # create empty meas_result
        # array [die][module] with dict content status, message, contact_height, variables & plot_parameters
        self.meas_result = self.create_meas_result(self.wafer.nchips, self.wafer.nmodules)

        # add buttons to gridLayout and get numx buttons & numy buttons
        self.numx, self.numy = self.add_die_buttons(wafer, enable)

        # set values into textBoxes
        widgets.txtWaferName.setText(wafer.wafer_name)
        widgets.txtXSize.setValue(wafer.xsize)
        widgets.txtYSize.setValue(wafer.ysize)
        widgets.txtNumberDies.setValue(wafer.nchips)
        widgets.txtNumberModules.setValue(wafer.nmodules)
        #widgets.txtXmax.setValue(wafer.xmax)
        #widgets.txtYmax.setValue(wafer.ymax)
        widgets.txtHomeChip.setText(wafer.home_chip)
        widgets.txtOriginChip.setText(wafer.real_origin_chip)

        widgets.cmbWaferSize.clear()
        widgets.cmbWaferSize.addItem("Wafer size")
        wafer_sizes = ["1","2","3","4","5","6","8","12"]
        widgets.cmbWaferSize.addItems(wafer_sizes)
        widgets.cmbWaferSize.setCurrentIndex(wafer_sizes.index(str(int(wafer.wafer_size_inch)))+1)
        widgets.cmbWaferSize.currentIndexChanged.connect(self.load_wafersize)

        widgets.cmbWaferOrientation.clear()
        widgets.cmbWaferOrientation.addItem("Wafer flat")
        wafer_orientations = ["0","90","180","270"]
        widgets.cmbWaferOrientation.addItems(wafer_orientations)
        widgets.cmbWaferOrientation.setCurrentIndex(wafer_orientations.index(str(int(wafer.flat_orientation)))+1)
        widgets.cmbWaferOrientation.currentIndexChanged.connect(self.load_waferorientation)

        widgets.txtNumberModules.valueChanged.connect(self.values_changed)
        widgets.txtNumberDies.valueChanged.connect(self.values_changed)
        widgets.txtXSize.valueChanged.connect(self.values_changed)
        widgets.txtYSize.valueChanged.connect(self.values_changed)
        widgets.txtHomeChip.textChanged.connect(self.values_changed)
        widgets.txtOriginChip.textChanged.connect(self.values_changed)

        if self.wafer.nmodules==1:
            self.menuBar().setVisible(False)
        else:
            menu = self.menuBar().addMenu("Modules")
            self.actions = []
            for i in range(1,self.wafer.nmodules+1):
                self.actions.append("")
            for nmodule in range(1,self.wafer.nmodules+1):
                self.actions[nmodule-1] = QAction("View module "+str(nmodule),self)
                self.actions[nmodule-1].setCheckable(True)
                self.actions[nmodule-1].triggered.connect(partial(self.viewModulesChange,nmodule))
                if nmodule==self.wafer.nmodules:
                    self.actions[nmodule-1].setChecked(True)
                menu.addAction(self.actions[nmodule-1])

        #status_array = ["IDLE","SET ORIGIN","SET HOME","IN","OUT","MEAS"]
        self._status = "IDLE"
        self.statusBar().showMessage(self._status)

        starting_location_array = ["UPPER-LEFT","UPPER-RIGHT","BOTTOM-LEFT","BOTTOM-RIGHT"]
        widgets.cmbStartingLocation.addItems(starting_location_array)
        widgets.cmbStartingLocation.setCurrentIndex(starting_location_array.index(wafer.navigation_options[0]))
        widgets.cmbStartingLocation.currentIndexChanged.connect(self.values_changed)

        directional_movement_array = ["BI-DIRECTIONAL","UNI-DIRECTIONAL"]
        widgets.cmbDirectionalMovement.addItems(directional_movement_array)
        widgets.cmbDirectionalMovement.setCurrentIndex(directional_movement_array.index(wafer.navigation_options[1]))
        widgets.cmbDirectionalMovement.currentIndexChanged.connect(self.values_changed)

        move_by_array = ["ROW","COLUMN"]
        widgets.cmbMoveBy.addItems(move_by_array)
        widgets.cmbMoveBy.setCurrentIndex(move_by_array.index(wafer.navigation_options[2]))
        widgets.cmbMoveBy.currentIndexChanged.connect(self.values_changed)

        widgets.btnDraw.clicked.connect(self.DrawWafer)
        widgets.btnSave.clicked.connect(self.SaveWafer)
        widgets.btnPrint.clicked.connect(self.PrintWafer)
        widgets.btnModules.clicked.connect(self.ModulesWafer)

        widgets.btnHomePosition.clicked.connect(self.actionsButtons)
        widgets.btnOriginPosition.clicked.connect(self.actionsButtons)
        widgets.btnIN.clicked.connect(self.actionsButtons)
        widgets.btnOUT.clicked.connect(self.actionsButtons)
        widgets.btnIDLE.clicked.connect(self.actionsButtons)
        widgets.btnMEAS.clicked.connect(self.actionsButtons)
        widgets.btnMEAS_SUCCESS.clicked.connect(self.actionsButtons)
        widgets.btnMEAS_WARNING.clicked.connect(self.actionsButtons)
        widgets.btnMEAS_ERROR.clicked.connect(self.actionsButtons)


        widgets.btnMarkAll.clicked.connect(self.MarkAll)
        widgets.btnUnmarkAll.clicked.connect(self.UnmarkAll)
        windowTitle = "Wafer window"
        if wafer.wafer_name!="":
            windowTitle = windowTitle + " - " + wafer.wafer_name



        self.setWindowTitle(windowTitle)
        #·self.setMinimumHeight(self.max_size)
        self.setMinimumHeight(860)
        self.setMinimumWidth(self.max_window_size)
        #self.setMaximumHeight(self.max_window_size)
        self.setMaximumHeight(960)
        self.setMaximumWidth(self.max_window_size)
        self.enabled_widgets(enable)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self,value):
        self._status = value
        self.statusBar().showMessage(value)

    @status.deleter
    def status(self):
        del self._status

    def values_changed(self):
        self.wafer.nmodules = self.widgets.txtNumberModules.value()
        self.wafer.nchips = self.widgets.txtNumberDies.value()
        if len(self.wafer.wafer_modules)<=int(self.wafer.nmodules):
            for i in range (len(self.wafer.wafer_modules),self.wafer.nmodules):
                self.wafer.wafer_modules.append('0.000000 0.000000')
        else:
            for i in range (self.wafer.nmodules,len(self.wafer.wafer_modules)):
                del self.wafer.wafer_modules[i]
        self.wafer.xsize = self.widgets.txtXSize.value()
        self.wafer.ysize = self.widgets.txtYSize.value()
        self.wafer.home_chip = self.widgets.txtHomeChip.text()
        self.wafer.real_origin_chip = self.widgets.txtOriginChip.text()
        self.wafer.navigation_options = [self.widgets.cmbStartingLocation.currentText(),self.widgets.cmbDirectionalMovement.currentText(),self.widgets.cmbMoveBy.currentText()]

    def create_meas_result(self, totalDies, totalModules):
        meas_result = []
        modulesList = []
        # first create module list
        for module in range(0,totalModules):
            modulesList.append(module)
        for die in range(0, totalDies):
            meas_result.append([die])
            for module in range(0, totalModules):
                meas_result[die].append([modulesList[module]])
            # meas_result[die].append(modulesList)
            for module in range(0, totalModules):
                # print(str(die) + " " + " " + str(totalDies) + str(module) + " " + str(totalModules))
                meas_result[die][module] = {"status" : "meas", "message" : "", "contact_height" : "", "variables" : "", "plot_parameters" : ""}

        return meas_result

    def viewModulesChange(self,nmodule):
        # unchecked all

        for actionModule in range (0,self.wafer.nmodules):
            self.actions[actionModule].setChecked(False)
        # check the selected module view
        self.actions[nmodule-1].setChecked(True)
        self.view_modules = nmodule
        # print module view in buttons to measure
        for i in range (0,self.wafer_parameters["nchips"]):
            x , y = self.wafer_parameters["wafer_positions"][i].split()
            x2, y2 = change_coord_to_origin(-int(x),-int(y),self.wafer_parameters["real_origin_chip"]).split()
            btn = self.centralWidget().findChild(QPushButton,get_btnName(x2,y2))
            meas_array = ["meas_success","meas_warning","meas_error"]
            if self.meas_result[i][nmodule-1]["status"] in meas_array:
                btn.btnType = self.meas_result[i][nmodule-1]["status"]
                btn.message = self.meas_result[i][nmodule-1]["message"]
            else:
                btn.btnType = "meas"
            QApplication.processEvents()


    def closeEvent(self, event):

        if self.moduleswindow!="":
            self.moduleswindow.close()


    def MarkAll(self):
        for i in self.centralWidget().findChildren(QWaferButton):
            if i._btnType == "in":
                i.btnType = "meas"
        self.total_meas()

    def UnmarkAll(self):
        for i in self.centralWidget().findChildren(QWaferButton):
            if i._btnType == "meas":
                x = i.x * -1
                y = i.y * -1
                if not i.origin:
                    if i.waferwindow.wafer.is_in(x,y):
                        i.btnType = "in"
                    else:
                        i.btnType = "out"

        self.total_meas()

    def total_meas(self):
        # get measured chips

        total_meas = 0
        total_in = 0
        total_out = 0
        total_meas_success = 0
        total_meas_warning = 0
        total_meas_error = 0

        for i in self.centralWidget().findChildren(QWaferButton):
            if i._btnType == "meas":
                total_meas += 1
            if i._btnType == "meas_success":
                total_meas_success += 1
                total_meas += 1
            if i._btnType == "in":
                total_in += 1
            if i._btnType == "out":
                total_out += 1
            if i._btnType == "meas_warning":
                total_meas_warning += 1
                total_meas += 1
            if i._btnType == "meas_error":
                total_meas_error += 1
                total_meas += 1
        self.widgets.txtNumberDies.setValue(total_meas)
        self.widgets.btnIN.setText("IN\n" + str(total_in))
        self.widgets.btnOUT.setText("OUT\n" + str(total_out))
        self.widgets.btnMEAS.setText("MEAS\n" + str(total_meas))
        self.widgets.btnMEAS_SUCCESS.setText("SUCCESS\n" + str(total_meas_success))
        self.widgets.btnMEAS_WARNING.setText("WARNING\n" + str(total_meas_warning))
        self.widgets.btnMEAS_ERROR.setText("ERROR\n" + str(total_meas_error))

        return {"meas" : total_meas, "in" : total_in, "out" : total_out, "meas_success" : total_meas_success, "meas_warning" : total_meas_warning, "meas_error" : total_meas_error}

    def actionsButtons(self):
        global set_origin, set_home
        btn = self.sender()
        btnName = btn.objectName()
        set_origin = set_home = False


        if btnName == "btnOriginPosition":

            previous_origin = self.widgets.txtOriginChip.text()
            retval = messageBox(self,"Set Origin Position","Are you sure to SET ORIGIN position?","question")
            if retval == QMessageBox.Yes:
                self.status = "SET ORIGIN"
                # first reset previous home
                if previous_origin!="":
                    previous_origin_x, previous_origin_y = previous_origin.split()
                    for i in range(self.ui.gridLayout.count()):
                        name_button = "btn_" + previous_origin_x + "_" + previous_origin_y
                        if self.ui.gridLayout.itemAt(i).widget().btnName == name_button:
                            coord_text = "(" + previous_origin_x + "," + previous_origin_y + ")"
                            #self.ui.gridLayout.itemAt(i).widget().setText(coord_text)
                            self.ui.gridLayout.itemAt(i).widget().origin = False
                            QApplication.processEvents()
                            break
                self.widgets.txtOriginChip.setText("")
                retval = messageBox(self,"Set Origin Position","Click in new Origin chip","info")
                set_origin = True

        else:
            if btnName == "btnHomePosition":
                if self.widgets.txtOriginChip.text()!="":
                    self.status = "SET HOME"
                    previous_home = self.widgets.txtHomeChip.text()
                    origin = self.widgets.txtOriginChip.text()
                    # first reset previous home
                    if previous_home!="":
                        previous_home_x, previous_home_y = previous_home.split()
                        origin_x, origin_y = origin.split()
                        real_home_x = int(origin_x) + int(previous_home_x)
                        real_home_y = int(origin_y) + int(previous_home_y)
                        name_button = "btn_" + str(real_home_x) + "_" + str(real_home_y)
                        for i in range(self.ui.gridLayout.count()):
                            if self.ui.gridLayout.itemAt(i).widget().btnName == name_button:
                                self.ui.gridLayout.itemAt(i).widget().home = False
                                QApplication.processEvents()
                                break
                else:
                    retval = messageBox(self,"Setting home problem","Please, select first the Origin chip!","warning")

            else:
                self.status = btnName.replace("btn","")



    def enabled_widgets(self,enable):
        # LineEdit, spinbox
        self.widgets.txtWaferName.setEnabled(enable)
        self.widgets.txtXSize.setEnabled(enable)
        self.widgets.txtYSize.setEnabled(enable)
        self.widgets.txtNumberDies.setEnabled(enable)
        self.widgets.txtNumberModules.setEnabled(enable)
        #self.widgets.txtXmax.setEnabled(enable)
        #self.widgets.txtYmax.setEnabled(enable)
        # Combos
        self.widgets.cmbWaferSize.setEnabled(enable)
        self.widgets.cmbWaferOrientation.setEnabled(enable)
        self.widgets.cmbStartingLocation.setEnabled(enable)
        self.widgets.cmbDirectionalMovement.setEnabled(enable)
        self.widgets.cmbMoveBy.setEnabled(enable)
        # Buttons
        self.widgets.btnHomePosition.setEnabled(enable)
        self.widgets.btnOriginPosition.setEnabled(enable)
        self.widgets.btnDraw.setEnabled(enable)
        self.widgets.btnSave.setEnabled(enable)
        self.widgets.btnPrint.setEnabled(True) # print always enable
        self.widgets.btnModules.setEnabled(enable)
        self.widgets.btnIDLE.setEnabled(enable)
        self.widgets.btnIN.setEnabled(enable)
        self.widgets.btnOUT.setEnabled(enable)
        self.widgets.btnMEAS.setEnabled(enable)
        self.widgets.btnMEAS_SUCCESS.setEnabled(enable)
        self.widgets.btnMEAS_WARNING.setEnabled(enable)
        self.widgets.btnMEAS_ERROR.setEnabled(enable)
        self.widgets.btnMarkAll.setEnabled(enable)
        self.widgets.btnUnmarkAll.setEnabled(enable)

    def ModulesWafer(self):
        if self.widgets.txtNumberModules.value()>0:
            self.moduleswindow = ModulesWindow(self, True)
            self.moduleswindow.show()
        else:
            pass

    def PrintWafer(self):
        pixmap = QPixmap(self.size()*2)
        pixmap.setDevicePixelRatio(2)
        self.render(pixmap)
        name = self.widgets.txtWaferName.text()
        if name!="":
            imagename = "wafer_" + name + ".png"
            pixmap.save(imagename, "PNG", -1)
            retval = messageBox(self,"Print wafermap","Wafermap printed to " + imagename +" !","info")
        else:
            retval = messageBox(self,"Print wafermap","Please, fill the wafer name to print image!","warning")

    def DrawWafer(self):
        widgets = self.ui
        wafer_size = widgets.cmbWaferSize.currentText()
        if widgets.cmbWaferSize.currentIndex()>0:
            flat_orientation = widgets.cmbWaferOrientation.currentText()
            if widgets.cmbWaferOrientation.currentIndex()>0:
                try:
                    wafer_name = widgets.txtWaferName.text()
                    wafer_xsize = float(widgets.txtXSize.text().replace(",","."))
                    wafer_ysize = float(widgets.txtYSize.text().replace(",","."))
                    #wafer_xmax = 1
                    #wafer_ymax = 1
                    wafer_nchips = 0
                    wafer_nmodules = 1
                    # wafer_real_origin_chip = widgets.txtOriginChip.text()
                    wafer_origin_chip = "0 0"
                    # wafer_home_chip = widgets.txtHomeChip.text()
                    wafer_real_origin_chip = ""
                    wafer_home_chip = ""

                    if wafer_name!="":
                        if wafer_xsize>0 and wafer_ysize>0:
                            origin_chip = wafer_origin_chip
                            home_chip = wafer_home_chip
                            real_origin_chip = wafer_real_origin_chip
                            wafer_positions = []
                            wafer_modules = ["0 0"]
                            wafer_navigation_options = ["UPPER-LEFT","BI-DIRECTIONAL","ROW"]
                            wafer_parameters = {
                                "wafer_name": wafer_name,
                                "wafer_size": wafer_size,
                                "xsize": wafer_xsize,
                                "ysize": wafer_ysize,
                                "nchips": wafer_nchips,
                                "nmodules": wafer_nmodules,
                                "origin_chip": origin_chip,
                                "home_chip": home_chip,
                                "flat_orientation": flat_orientation,
                                "wafer_positions": wafer_positions,
                                "wafer_modules": wafer_modules,
                                "real_origin_chip": real_origin_chip,
                                "navigation_options": wafer_navigation_options

                                }
                            self.close()
                            wafer = Wafer(wafer_parameters)
                            self.waferwindow = wafer.create_wafer_window(True)
                            self.waferwindow.show()
                            self.waferwindow.total_meas()
                        else:
                            retval = messageBox(self,"Problem with die dimensions","Please, insert a number in XSize & YSize","warning")
                    else:
                        retval = messageBox(self,"Problem with wafer name","Please, type a wafer name","warning")
                except Exception as e:
                    retval = messageBox(self,"Some problem with variables",str(e),"critical")



    def SaveWafer(self):
        self.total_meas()
        # first construct wafer_parameters
        wafer_name = self.widgets.txtWaferName.text()
        wafer_size = self.widgets.cmbWaferSize.currentText()
        xsize = self.widgets.txtXSize.value()
        ysize = self.widgets.txtYSize.value()
        #xmax = self.widgets.txtXmax.value()
        #ymax = self.widgets.txtYmax.value()
        nchips = self.widgets.txtNumberDies.value()
        nmodules = self.widgets.txtNumberModules.value()
        flat_orientation = self.widgets.cmbWaferOrientation.currentText()

        origin_chip = "0 0"
        real_origin_chip = self.widgets.txtOriginChip.text()
        home_chip = self.widgets.txtHomeChip.text()
        if real_origin_chip=="":
            retval = messageBox(self,"Problem with Origin","Please, mark your origin first!","warning")
            return
        if home_chip=="":
            retval = messageBox(self,"Problem with Home","Please, mark your home first!","warning")
            return
        navigation_options = [self.widgets.cmbStartingLocation.currentText(),self.widgets.cmbDirectionalMovement.currentText(),self.widgets.cmbMoveBy.currentText()]
        starting_location = navigation_options[0].split("-")
        stepx = 1
        stepy = 1
        if starting_location[0]=="UPPER":
            yini = 0
            yfin = self.numy-1
        else:
            yini = self.numy-1
            yfin = 0
            stepy = -1
        if starting_location[1]=="LEFT":
            xini = 0
            xfin = self.numx-1
        else:
            xini = self.numx-1
            xfin = 0
            stepx = -1
        change_direction = False
        if navigation_options[1]=="BI-DIRECTIONAL":
            change_direction = True
        wafer_positions = []

        try:
            if navigation_options[2]=="ROW":
                for y in range (yini,yfin+stepy,stepy):
                    count_found = 0
                    for x in range(xini,xfin+stepx,stepx):
                        # coordenadas negativas
                        btn = self.centralWidget().findChild(QPushButton,get_btnName(x,y))
                        if btn.btnType == "meas":
                            if len(wafer_positions)==0:
                                # check origin
                                if real_origin_chip != str(-x)+" "+str(-y):
                                    retval = messageBox(self,"Problem with Origin","Please, check your origin in base to navigation options. Origin correct: ("+str(-x)+" "+str(-y)+")!","error")
                                    return

                            wafer_positions.append(change_coord_to_origin(-x,-y,real_origin_chip))
                            count_found+=1

                    if change_direction and count_found>0: # only change direction if first chip meas found
                        xini, xfin = xfin, xini
                        stepx = stepx * -1

            else:
                # COLUMN
                for x in range (xini,xfin+stepx,stepx):
                    count_found = 0
                    for y in range(yini,yfin+stepy,stepy):
                        # coordenadas negativas
                        btn = self.centralWidget().findChild(QPushButton,get_btnName(x,y))
                        if btn.btnType == "meas":
                            if len(wafer_positions)==0:
                                # check origin
                                if real_origin_chip != str(-x)+" "+str(-y):
                                    retval = messageBox(self,"Problem with Origin","Please, check your origin in base to navigation options. Origin correct: ("+str(-x)+" "+str(-y)+")!","error")
                                    return

                            wafer_positions.append(change_coord_to_origin(-x,-y,real_origin_chip))
                            count_found+=1

                    if change_direction and count_found>0: # only change direction if first chip meas found
                        yini, yfin = yfin, yini
                        stepy = stepy * -1

        except Exception as e:
            retval = messageBox(self,"Some problem getting wafer_positions",str(e),"critical")
            return

        if len(wafer_positions)==0:
            retval = messageBox(self,"Problem with wafer positions","Please mark at least one chip to measure","critical")
            return

        wafer_modules = self.wafer_modules
        wafer_modules_name = self.wafer_modules_name

        wafer_parameters = {

            "wafer_name": wafer_name,
            "wafer_size": wafer_size,
            "xsize": xsize,
            "ysize": ysize,
            "nchips": nchips,
            "nmodules": nmodules,
            "origin_chip": origin_chip,
            "home_chip": home_chip,
            "flat_orientation": flat_orientation,
            "wafer_positions": wafer_positions,
            "wafer_modules": wafer_modules,
            "wafer_modules_name": wafer_modules_name,
            "real_origin_chip": real_origin_chip,
            "navigation_options": navigation_options

        }

        #wafer_parameters = [wafer_name, wafer_size, xsize, ysize, nchips, nmodules, origin_chip, home_chip, flat_orientation, wafer_positions, wafer_modules, real_origin_chip, navigation_options]
        # and assign to self.wafer_parameteres = wafer_parameters
        # get and object
        wafer_save = Wafer(wafer_parameters)
        print("Save wafer ppg file!")
        print(wafer_save.wafer_parameters)
        # call function
        wafer_save.save_wafermap()

    def load_wafersize(self):

        wafersize_selected = self.widgets.cmbWaferSize.currentText()
        self.wafer.wafer_size_inch = wafersize_selected

    def load_waferorientation(self):

        waferorientation_selected = self.widgets.cmbWaferOrientation.currentText()
        self.wafer.flat_orientation = waferorientation_selected


    def add_die_buttons(self, wafer, enable):
        # die out wafer => color white
        # die in wafer => color yellow
        # die in wafer (to measure) => color blue light
        # die in wafer (measure ok) => color green
        # die in wafer (measure with problems) => color orange
        # die in wafer (measure ko) => color red

        x = y = xmax = ymax = 0
        name = ""
        ratio = float(wafer.wafer_size_mm*1000 / self.max_size)

        xstep = wafer.xsize/(ratio)
        ystep = wafer.ysize/(ratio)

        #num_xsteps = self.max_size/xstep
        #num_ysteps = self.max_size/ystep


        while ymax<self.max_size+ystep:
            while xmax<self.max_size+xstep:

                name = ""
                btnType = "out"
                if wafer.is_home(x,y):
                    name = "H"
                if wafer.is_origin(x,y):
                    name = "O"
                    btnType = "meas"
                if wafer.is_in(x,y):
                    btnType = "in"
                if wafer.is_to_measure(x,y): # not only in in, set in wafer_position
                    btnType = "meas"

                b = QWaferButton(self, name, btnType, xstep, ystep, -x, -y, enable)
                b.clicked.connect(CallButton(self,btnType,-x,-y,name,b))

                if name=="H":
                    b.home = True
                if name=="O":
                    b.origin = True

                self.ui.gridLayout.addWidget(b,y,x)
                xmax = xmax + xstep
                x = x + 1
            numx = x
            ymax = ymax + ystep
            y = y + 1
            xmax = 0
            x = 0
        numy = y

        return [numx,numy]

class CallButton:
    def __init__(self, waferwindow, btnType, x, y,name, b):
        global set_home, set_origin
        # state button: die out wafer, die in wafer, die in (measure), die in (measured ok), die in (measured ko)
        # die out wafer => color white
        # die in wafer => color yellow
        # die in wafer (to measure) => color blue light
        # die in wafer (measure ok) => color green
        # die in wafer (measure with problems) => color orange
        # die in wafer (measure ko) => color red
        self.COLORS_DIES = {
            "out" : "#FFFFFF",
            "in" : "#FFFF99",
            "meas" : "#33CCFF",
            "meas_success" : "#66CC99",
            "meas_error" : "#FF3300",
            "meas_warning" : "#FFCC33"
        }
        self.name = name
        self.btnType = btnType
        #self.x = x * -1
        #self.y = y * -1
        self.waferwindow = waferwindow
        self.x = x
        self.y = y
        self.b = b
    def __call__(self):
        global set_home, set_origin
        status = self.waferwindow._status
        coord_text = str(self.x)+" "+str(self.y)
        coord_text_x, coord_text_y = coord_text.split()
        #  contruct possible home coord
        if self.waferwindow.widgets.txtOriginChip.text()!="":
            origin_coord_text = self.waferwindow.widgets.txtOriginChip.text()
            origin_coord_text_x, origin_coord_text_y = origin_coord_text.split()
            home_coord_text_x = int(coord_text_x) - int(origin_coord_text_x)
            home_coord_text_y = int(coord_text_y) - int(origin_coord_text_y)
            home_coord = str(home_coord_text_x) + " " + str(home_coord_text_y)

        previous_btnType = self.b.btnType
        #print("previous btn Type: " + previous_btnType)
        if status != "IDLE":
            if status == "SET HOME":
                if self.waferwindow.widgets.txtHomeChip.text()!="":
                    # borramos el home btn y lo dejamos como estaba el btnType
                    for i in self.waferwindow.centralWidget().findChildren(QWaferButton):
                        if i.text() == "H":
                            i.setText("")
                self.b.home = True
                print("Home")
                self.waferwindow.widgets.txtHomeChip.setText(home_coord)
                self.waferwindow.status = "IDLE"
                #self.waferwindow.widgets.cmbStatus.setCurrentText("IDLE")
                self.waferwindow.total_meas()
                QApplication.processEvents()
            else:
                if status == "SET ORIGIN":
                    print("Origin")
                    self.b.origin = True
                    self.b.btnType = "meas"
                    self.waferwindow.widgets.txtOriginChip.setText(coord_text)
                    # clear home position
                    self.waferwindow.widgets.txtHomeChip.setText("")
                    for i in self.waferwindow.centralWidget().findChildren(QWaferButton):
                        if i.text() == "H":
                            #i.setText(i.coord_text)
                            i.setText("")

                    self.waferwindow.status = "IDLE"
                    #self.waferwindow.widgets.cmbStatus.setCurrentText("IDLE")
                    self.waferwindow.total_meas()
                    QApplication.processEvents()
                else:
                    meas_array = ["MEAS_SUCCESS", "MEAS_WARNING" ,"MEAS_ERROR"]
                    # case "IN, "OUT, "MEAS", "MEAS_SUCCESS", "MEAS_WARNING" & "MEAS_ERROR"
                    if status=="IN" or status =="OUT" or status == "MEAS" or (previous_btnType =="meas" and (status in meas_array)):
                        self.b.btnType = status.lower()
                    else:
                        print("Please, make meas chip first previous to apply status (Success, Warning or Error)!")
        else:
            # click button active (meas) => view variables & plot
            if self.waferwindow.widgets.txtOriginChip.text()!="":
                real_coord = str(self.x - int(origin_coord_text_x)) + " " + str(self.y - int(origin_coord_text_y))
                die = int(self.waferwindow.wafer_parameters["wafer_positions"].index(real_coord))
                module = int(self.waferwindow.view_modules)-1
                variables = self.waferwindow.meas_result[die][module]["variables"]["params"]
                if variables!="":
                    print("=> Variables for die: " + str(die+1) + " & module " + str(module+1) + ":")
                    returnText = ""
                    for i in range (0,len(variables)):
                        for nombre , valor in variables[i].items():
                            if nombre=="name":
                                if returnText=="":
                                    returnText = valor + " = "
                                else:
                                    returnText += ", " + valor + " = "
                            else:
                                returnText += str(valor)

                    print(returnText)
                # view graph
                plot_parameters = self.waferwindow.meas_result[die][module]["plot_parameters"]

                if plot_parameters!="":
                    self.plotwindow = PlotWindow(plot_parameters,True)
                    self.plotwindow.show()







class QWaferButton(QPushButton):

    def __init__(self, waferwindow, name, btnType, xstep,ystep,x,y, enable):
        super().__init__()

        self.COLORS_DIES = {
            "out" : "#FFFFFF",
            "in" : "#FFFF99",
            "meas" : "#33CCFF",
            "meas_success" : "#66CC99",
            "meas_error" : "#FF3300",
            "meas_warning" : "#FFCC33"
        }
        self.setFixedSize(QSize(xstep,ystep))
        self.waferwindow = waferwindow
        self.xstep = xstep
        self.ystep = ystep
        self.x = x
        self.y = y
        self.coord_text = "("+str(self.x)+","+str(self.y)+")"
        # Control variables
        self._home = False
        self._origin = False
        self._btnType = btnType
        self._message = ""
        self._enable = enable
        self.setEnabled(enable)

        if name=="H":
            self._home = True
        if name=="O":
            self._origin = True
        btnName = "btn_"+str(x)+"_"+str(y)
        if name!="":
            self.setText(name)

        self.setStyleSheet("font-size: 8pt; text-align: center; border: 1px solid #DDDDDD; background-color: %s;" % self.COLORS_DIES[self.btnType])
        self.btnName = btnName
        self.setObjectName(self.btnName)
        self.setToolTip(self.coord_text)

    # def total_meas(self):
    #     # get measured chips
    #     total_meas = 0
    #     for i in self.waferwindow.centralWidget().findChildren(QWaferButton):
    #         if i._btnType == "meas":
    #             total_meas += 1
    #     self.waferwindow.widgets.txtNumberDies.setValue(total_meas)

    def unset_home(self):
        for i in self.waferwindow.centralWidget().findChildren(QWaferButton):
            if i.text() == "H":
                #i.setText(self.coord_text)
                i.setText("")

    @property
    def home(self):
        return self._home

    @home.setter
    def home(self,value):
        self._home = value
        if value:
            self.setText("H")
        else:
            self.setText("")

    @home.deleter
    def home(self):
        del self._home

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self,value):
        self._origin = value
        if value:
            self._origin = value
            self.setText("O")
            # origin always to measure
            self.setStyleSheet("font-size: 8pt; text-align: center; border: 1px solid #DDDDDD; background-color: %s;" % self.COLORS_DIES["meas"])
        else:
            self.setText("")

    @origin.deleter
    def origin(self):
        del self._origin

    @property
    def btnType(self):
        return self._btnType

    @btnType.setter
    def btnType(self,value):
        states =["in","out","meas","meas_success","meas_warning","meas_error"]
        self._btnType = value
        if value in states:
            #self.setStyleSheet("font-size: 8pt; text-align: center; border: 1px solid #DDDDDD; background-color: qlineargradient(x1:0, x2:1, stop: 0.24 red, stop: 0.49 blue, stop: 0.74 red, stop: 0.98 blue)")
            self.setStyleSheet("font-size: 8pt; text-align: center; border: 1px solid #DDDDDD; background-color: %s;" % self.COLORS_DIES[value])
            self.waferwindow.total_meas()
        if value!="meas_warning" or value!="meas_error":
            self.setToolTip(self.coord_text)
        if "meas" in value:
            self.setEnabled(True)

    @btnType.deleter
    def btnType(self):
        del self._btnType


    @property
    def message(self):
        return self._message

    @message.setter
    def message(self,value):
        self._message = value
        # warning message put set tooltip to message
        if self._btnType == "meas_warning":
            if value !="":
                self.setToolTip("Warning: " + self._message)
            else:
                self.setToolTip("No warning message found!")
        elif self._btnType == "meas_error":
            if value !="":
                self.setToolTip("Error: " + self._message)
            else:
                self.setToolTip("No error message found!")
        else:
            self.setToolTip(self.coord_text)


    @message.deleter
    def message(self):
        del self._message
