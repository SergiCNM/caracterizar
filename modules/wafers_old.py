import os
import numpy as np
from datetime import datetime
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from modules.ui_wafer import Ui_WaferWindow
from modules.ui_modules import Ui_ModulesWindow

from functools import partial
from config.functions import *
from config.defs import *

class Wafer(QMainWindow):
    def __init__(self,wafer_parameters):
        QMainWindow.__init__(self)
        # wafer parameters, array with 15 parameters
        self.wafer_error = False
        self.waferwindow = ""
        self.wafer_parameters = wafer_parameters
        try:
            if len(wafer_parameters)==15:
                self.wafer_name = wafer_parameters[0]
                self.wafer_size_inch = wafer_parameters[1]
                self.wafer_size_mm = 0
                self.thickness = 0
                self.set_wafer_size()
                self.xsize = wafer_parameters[2]
                self.ysize = wafer_parameters[3]
                self.xmax = wafer_parameters[4]
                self.ymax = wafer_parameters[5]
                self.nchips = wafer_parameters[6]
                self.nmodules = wafer_parameters[7]
                self.origin_chip = wafer_parameters[8]
                self.home_chip = wafer_parameters[9]
                self.flat_orientation = wafer_parameters[10]
                self.wafer_positions = wafer_parameters[11]
                self.wafer_modules = wafer_parameters[12]
                self.real_origin_chip = wafer_parameters[13]
                self.navigation_options = wafer_parameters[14]
            else:
                self.wafer_parameters = ""
                self.wafer_error = True
                retval = messageBox(self,"Problem with ppg parameters","Wafer file not initialized","error")

        except:
            self.wafer_parameters = ""
            self.wafer_error = True
            retval = messageBox(self,"Problem initializing class Wafer","Wafer file not initialized","error")

    def set_wafer_size(self):
        if int(self.wafer_size_inch)==1:
            self.wafer_size_mm = 25
            self.thickness = 1
        if int(self.wafer_size_inch)==2:
            self.wafer_size_mm = 51
            self.thickness = 275
        if int(self.wafer_size_inch)==3:
            self.wafer_size_mm = 76
            self.thickness = 375
        if int(self.wafer_size_inch)==4:
            self.wafer_size_mm = 100
            self.thickness = 525
        if int(self.wafer_size_inch)==5: # 4.9 inch
            self.wafer_size_mm = 125
            self.thickness = 625
        if int(self.wafer_size_inch)==6: # 5.9 inch
            self.wafer_size_mm = 150
            self.thickness = 675
        if int(self.wafer_size_inch)==8: # 7.9 inch
            self.wafer_size_mm = 200
            self.thickness = 725
        if int(self.wafer_size_inch)==12: # 11.8 inch
            self.wafer_size_mm = 300 
            self.thickness = 775
                
        

    def check_wafer_parameters(self):
        check_wafer_parameters = True
        # check wafer_positions & nchips
        if self.wafer_positions.size!=int(self.nchips):
            check_wafer_parameters = False
            print("Error checking number of chips (" + str(self.nchips) + ") <> wafer_positions size ( " + str(self.wafer_positions.size) + ")")
        # check wafer_size
        if self.wafer_size_mm==0 or self.thickness==0:
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
        # check xmax & ymax
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

            if xmax_detected!=self.xmax and ymax_detected!=self.ymax:
                check_wafer_parameters = False
                print("Error checking xmax (" + str(xmax_detected) + ") & ymax (" + str(ymax_detected) + ")...")

        # check navigation options
        if self.navigation_options.len()!=3:
            check_wafer_parameters = False
            print("Error checking navigation options, not all parameters passed!")
        else:
            # verify parameters
            starting_location = self.navigation_options[0]
            if not starting_location in ["UP-LEFT","UP-RIGHT","BOTTOM-LEFT","BOTTOM-RIGHT"]:
                check_wafer_parameters = False
                print("Error checking navigation options (starting location). " + starting_location + " not allowed value!")   
            else :
                direction_movement = self.navigation_options[1]
                if not direction_movement in ["BI","UNI"]:
                    check_wafer_parameters = False
                    print("Error checking navigation options (directional movement). " + direction_movement + " not allowed value!")   
                else :
                    move_by = self.navigation_options[2]
                    if not move_by in ["ROW","COLUMN"]:
                        check_wafer_parameters = False
                        print("Error checking navigation options (move by). " + move_by + " not allowed value!")   
        
        # verifiy wafer_position according to navigation_options
        

        return check_wafer_parameters

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
                    movement_X = movement_X*-1
                else:
                    if self.flat_orientation==270:
                        movement_Y = movement_Y*-1
        
        return [movement_X,movement_Y]

    def calculate_init_prober_movement(self):
        if self.home_chip!=self.origin_chip:
            return self.calculate_prober_movement(self.home_chip,self.origin_chip)
        return [0,0]

    def calculate_process_percentage(self,die,module):
        nchips = self.nchips
        nmodules = self.nmodules
        total = nchips * nmodules
        calc = int(die)*int(module)/int(total) * 100
        percentage = "{:.2f}".format(calc)
        return float(percentage)

    def calculate_finish_time(self,date_init,die,module):
        date_now = datetime.now()
        difference = date_now-date_init
        nchips = self.nchips
        nmodules = self.nmodules
        total = nchips * nmodules
        total_seconds = difference * int(total) /(((int(die)-1) * int(nmodules)) + int(module))
        finish_time = date_init + total_seconds
        return finish_time.strftime('%Y-%m-%d %H:%M:%S')

    def create_wafer_window(self,enable):
        self.waferwindow = WaferWindow(self.wafer_parameters,enable)
        return self.waferwindow

    def is_home(self,x,y):
        # pass x,y position
        real_origin_chipX , real_origin_chipY = self.real_origin_chip.split()
        home_chipX , home_chipY = self.home_chip.split()
        if int(x)*-1 - int(real_origin_chipX) == int(home_chipX) and int(y)*-1 - int(real_origin_chipY) == int(home_chipY):
            return True
        return False

    def is_origin(self,x,y):
        # pass x,y position
        real_origin_chipX , real_origin_chipY = self.real_origin_chip.split()
        origin_chipX , origin_chipY = self.origin_chip.split()
        if int(x)*-1 - int(real_origin_chipX) == int(origin_chipX) and int(y)*-1 - int(real_origin_chipY) == int(origin_chipY):
            return True
        return False

    def is_in(self,x,y):
        # (x-a)² + (y-b)² = R²
        # miramos si los 4 puntos estan dentro 
        is_in = True
        R = self.wafer_size_mm/2
        xstep = self.xsize/1000
        ystep = self.ysize/1000
        a1 = int(x)*xstep
        b1 = int(y)*ystep
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
        real_origin_chipX , real_origin_chipY = self.real_origin_chip.split()
        realX = -int(x) - int(real_origin_chipX)
        realY = -int(y) - int(real_origin_chipY)
        realpos = str(realX) + " " + str(realY)
        if realpos in self.wafer_positions:
            is_to_measure = True
        return is_to_measure

    def save_wafermap(self):
        
        # here we create a dialog to put the name of the wafermap.py
        # dialog.setNameFilter("Wafermaps (*.py)")
        dir_wafermaps = os.getcwd() + base_dir + wafermaps_dir + "/"
        nameFile, _ = QFileDialog.getSaveFileName(self, 'Save wafermap', dir_wafermaps,"Wafermaps (*.py)")
        # and then you need to adjust wafer_parameters
        print(self.waferwindow)
        self.waferwindow = self.create_wafer_window(False) # just to create waferwindow object and get data
        self.wafer_name = self.waferwindow.widgets.txtWaferName.text()

        texto = 'global wafer_parameters\n\
\n\
\n\
# Configuration wafer parameters\n\
wafer_name = "' + self.wafer_name + '"\n\
wafer_size = 4.000000\n\
xsize = 2790.000000\n\
ysize = 1950.000000\n\
xmax = 6\n\
ymax = 1\n\
nchips = 6\n\
nmodules = 2\n\
\n\
real_origin_chip = "-10 -4"\n\
origin_chip = "0 0" # normaly start with 0,0\n\
home_chip = "-6 -12" # home (0um , 0um) could be different to origin (first die to measure)\n\
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270\n\
\n\
# wafer positions\n\
wafer_positions = []\n\
wafer_positions = np.append(wafer_positions,["0 0","-3 0","-6 0","-9 0","-12 0", "-15 0"])\n\
# distances from chip origin\n\
wafer_modules = ["0.00 0.00", "1000.00 1000.00"]\n\
navigation_options = []\n\
\n\
# wafer parameters (array with 14 parameters)\n\
wafer_parameters = [wafer_name, wafer_size, xsize, ysize, xmax, ymax, nchips, nmodules, origin_chip, home_chip, flat_orientation, wafer_positions, wafer_modules, real_origin_chip, navigation_options]\n'
        if nameFile!="":
            # create texto
            with open(nameFile, 'w') as f:
                f.write(texto)
            retval = messageBox(self,"Save wafermap","Wafermap file saved!","info") 
            
        



class ModulesWindow(QMainWindow):
    def __init__(self, WaferWindow, enable):
        #super().__init__()
        QMainWindow.__init__(self)
        self.ui = Ui_ModulesWindow()
        self.ui.setupUi(self)
        global widgets

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
                i = i + 1
            else:
                print("Error getting modules")
                break
        for i in range(1, int(WaferWindow.wafer_nmodules)):
            name_widget = "txtX" + str(i)
            self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).setEnabled(True)
            name_widget = "txtY" + str(i)
            self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).setEnabled(True)
        for i in range(int(WaferWindow.wafer_nmodules)+1,11):
            name_widget = "txtX" + str(i)
            self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).setEnabled(False)
            self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).setValue(0)
            name_widget = "txtY" + str(i)
            self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).setEnabled(False)
            self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).setValue(0)

        widgets.btnSaveModules.clicked.connect(partial(self.SaveModules,WaferWindow))

    def SaveModules(self, WaferWindow):
        wafer_modules = []
        for i in range (1,int(WaferWindow.wafer_nmodules)+1):
            name_widget = "txtX" + str(i)
            X = self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).value()
            name_widget = "txtY" + str(i)
            Y = self.ui.centralwidget.findChild(QDoubleSpinBox,name_widget).value()
            coord = str(X) + " " + str(Y)
            wafer_modules.append(coord)
        WaferWindow.wafer_modules = wafer_modules
        self.close()
        
        
    
    def GetModules(self):
        pass

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
        
        self.wafer_parameters = wafer_parameters
        self.wafer_nmodules = wafer.nmodules
        self.wafer_modules = wafer.wafer_modules
        self.max_size = 1000 # MAX_SIZE w/h BUTTONS
        self.max_window_size = 1000 # MAX WINDOW SIZE w/h
        self.add_die_buttons(wafer, enable)
        # set values into textBoxes
        widgets.txtWaferName.setText(wafer.wafer_name)
        
        widgets.txtXSize.setValue(wafer.xsize)
        widgets.txtYSize.setValue(wafer.ysize)
        widgets.txtNumberDies.setValue(wafer.nchips)
        widgets.txtNumberModules.setValue(wafer.nmodules)
        widgets.txtXmax.setValue(wafer.xmax)
        widgets.txtYmax.setValue(wafer.ymax)
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

        self.status_array = ["IDLE","SET ORIGIN","SET HOME","IN","OUT","MEAS"]
        self._status = "IDLE"
        widgets.cmbStatus.setEnabled(False)
        widgets.cmbStatus.addItems(self.status_array)


        widgets.btnDraw.clicked.connect(self.DrawWafer)
        widgets.btnSave.clicked.connect(self.SaveWafer)
        widgets.btnModules.clicked.connect(self.ModulesWafer)
        widgets.btnHomePosition.clicked.connect(self.actionsButtons)
        widgets.btnOriginPosition.clicked.connect(self.actionsButtons)
        widgets.btnIN.clicked.connect(self.actionsButtons)
        widgets.btnOUT.clicked.connect(self.actionsButtons)
        widgets.btnIDLE.clicked.connect(self.actionsButtons)
        widgets.btnMEAS.clicked.connect(self.actionsButtons)

        windowTitle = "Wafer window"
        if wafer.wafer_name!="":
            windowTitle = windowTitle + " - " + wafer.wafer_name
        
        

        self.setWindowTitle(windowTitle)
        self.setMinimumHeight(self.max_size)
        self.setMinimumWidth(self.max_size)
        self.setMaximumHeight(self.max_window_size)
        self.setMaximumWidth(self.max_window_size)
        self.enabled_widgets(enable)

        
    def total_meas(self):
        # get measured chips
        total_meas = 0
        for i in self.centralWidget().findChildren(QWaferButton):
            if i._btnType == "meas":
                total_meas += 1
        self.widgets.txtNumberDies.setValue(total_meas)

    def actionsButtons(self):
        global set_origin, set_home
        btn = self.sender()
        btnName = btn.objectName()
        set_origin = set_home = False
        if btnName == "btnIDLE":
            self._status = "IDLE"
            
            
        if btnName == "btnOriginPosition":
            
            previous_origin = self.widgets.txtOriginChip.text()
            retval = messageBox(self,"Set Origin Position","Are you sure to SET ORIGIN position?","question")
            if retval == QMessageBox.Yes: 
                self._status = "SET ORIGIN"
                #self.widgets.cmbStatus.setCurrentText(self.status_array[1])
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

        if btnName == "btnHomePosition":
            if self.widgets.txtOriginChip.text()!="":
                self._status = "SET HOME"
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

        if btnName == "btnIN":
            self._status = "IN"
            
            
        if btnName == "btnOUT":
            self._status = "OUT"
            #self.widgets.cmbStatus.setCurrentText(self.status_array[4])
            
        if btnName == "btnMEAS":
            self._status = "MEAS"
            #self.widgets.cmbStatus.setCurrentText(self.status_array[5])
            
        self.widgets.cmbStatus.setCurrentText(self._status)
    
    def enabled_widgets(self,enable):
        self.widgets.txtWaferName.setEnabled(enable)
        self.widgets.txtXSize.setEnabled(enable)
        self.widgets.txtYSize.setEnabled(enable)
        self.widgets.txtNumberDies.setEnabled(enable)
        self.widgets.txtNumberModules.setEnabled(enable)
        self.widgets.txtXmax.setEnabled(enable)
        self.widgets.txtYmax.setEnabled(enable)
        self.widgets.btnDraw.setEnabled(enable)
        self.widgets.btnSave.setEnabled(enable)
        self.widgets.btnModules.setEnabled(enable)
        self.widgets.cmbWaferSize.setEnabled(enable)
        self.widgets.cmbWaferOrientation.setEnabled(enable)
        self.widgets.btnHomePosition.setEnabled(enable)
        self.widgets.btnOriginPosition.setEnabled(enable)

        
            


    def ModulesWafer(self):
        if self.widgets.txtNumberModules.value()>0:
            self.moduleswindow = ModulesWindow(self,True)
            self.moduleswindow.show()
        else:
            pass
        
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
                    wafer_xmax = int(widgets.txtXmax.text())
                    wafer_ymax = int(widgets.txtYmax.text())
                    wafer_nchips = int(widgets.txtNumberDies.text())
                    wafer_nmodules = int(widgets.txtNumberModules.value())
                    wafer_real_origin_chip = widgets.txtOriginChip.text()
                    wafer_origin_chip = "0 0"
                    wafer_home_chip = widgets.txtHomeChip.text()

                    if wafer_name!="":
                        if wafer_xsize>0 and wafer_ysize>0:
                            if wafer_xmax>0 and wafer_ymax>0:
                                if wafer_nchips>0 and wafer_nmodules>0:
                                    print("ok")
                                    origin_chip = wafer_origin_chip
                                    home_chip = wafer_home_chip
                                    real_origin_chip = wafer_real_origin_chip
                                    wafer_positions = []
                                    wafer_modules = "0 0"
                                    wafer_navigation_options = ["UP-LEFT","BI","ROW"]
                                    wafer_parameters = [wafer_name, wafer_size, wafer_xsize, wafer_ysize, wafer_xmax, wafer_ymax, wafer_nchips, wafer_nmodules, origin_chip, home_chip, flat_orientation, wafer_positions, wafer_modules, real_origin_chip, wafer_navigation_options]
                                    self.close()
                                    wafer = Wafer(wafer_parameters)
                                    self.waferwindow = wafer.create_wafer_window(True)
                                    self.waferwindow.show()
                                    self.waferwindow.total_meas()
                                    
                                else:
                                    retval = messageBox(self,"Problem with wafer Number dies & modules","Please, insert a number in Number of Dies & Modules (>0)","warning") 
                            else:
                                retval = messageBox(self,"Problem with wafer Xmax & Ymax","Please, insert a number in Xmax & Ymax (>0)","warning") 
                        else:
                            retval = messageBox(self,"Problem with die dimensions","Please, insert a number in XSize & YSize","warning")     
                    else:
                        retval = messageBox(self,"Problem with wafer name","Please, type a wafer name","warning") 
                except Exception as e:
                    retval = messageBox(self,"Some problem with variables",str(e),"critical") 

        

    def SaveWafer(self):
        # first construct wafer_parameters
        wafer_name = self.widgets.txtWaferName.text()
        wafer_size = self.widgets.cmbWaferSize.currentText()
        xsize = self.widgets.txtXSize.value()
        ysize = self.widgets.txtYSize.value()
        xmax = self.widgets.txtXmax.value()
        ymax = self.widgets.txtYmax.value()
        nchips = self.widgets.txtNumberDies.value()
        nmodules = self.widgets.txtNumberModules.value()
        flat_orientation = self.widgets.cmbWaferOrientation.currentText()

        origin_chip = "0 0"
        real_origin_chip = self.widgets.txtOriginChip.text()
        home_chip = self.widgets.txtHomeChip.text()

        wafer_positions = []
        wafer_modules = []
        navigation_options = []

        wafer_parameters = [wafer_name, wafer_size, xsize, ysize, xmax, ymax, nchips, nmodules, origin_chip, home_chip, flat_orientation, wafer_positions, wafer_modules, real_origin_chip, navigation_options]
        # and assign to self.wafer_parameteres = wafer_parameters
        # get and object
        wafer = Wafer(self.wafer_parameters)
        # call function
        wafer.save_wafermap()

    def load_wafersize(self):
        global widgets
        wafersize_selected = widgets.cmbWaferSize.currentText()
        print(wafersize_selected)

    def load_waferorientation(self):
        global widgets
        waferorientation_selected = widgets.cmbWaferOrientation.currentText()
        print(waferorientation_selected)


    def add_die_buttons(self, wafer, enable):
        # die out wafer => color white
        # die in wafer => color yellow
        # die in wafer (to measure) => color blue light
        # die in wafer (measure ok) => color green
        # die in wafer (measure with problems) => color orange
        # die in wafer (measure ko) => color red
        
        x = y = xmax = ymax = 0
        name = ""
        ratio = wafer.wafer_size_mm*1000 / self.max_size
        
        xstep = wafer.xsize/(ratio)
        ystep = wafer.ysize/(ratio)

        num_xsteps = self.max_size/xstep
        num_ysteps = self.max_size/ystep


        while ymax<self.max_size+ystep:
            while xmax<self.max_size+xstep:
            
                name =""
                if wafer.is_home(x,y):
                    name = "H"
                if wafer.is_origin(x,y):
                    name = "O"
                btnType = "out"
                if wafer.is_in(x,y):
                    btnType = "in"
                
                if wafer.is_to_measure(x,y): # not only in in
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
            ymax = ymax + ystep
            y = y + 1
            xmax = 0
            x = 0

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
        print("previous btn Type: " + previous_btnType)
        if status != "IDLE":
            if status == "SET HOME":
                if self.waferwindow.widgets.txtHomeChip.text()!="":
                    # borramos el home btn y lo dejamos como estaba el btnType
                    pass
                self.b.home = True
                print("Home")
                self.waferwindow.widgets.txtHomeChip.setText(home_coord)
                self.waferwindow._status = "IDLE"
                self.waferwindow.widgets.cmbStatus.setCurrentText("IDLE")
                    
            if status == "SET ORIGIN":
                print("Origin")
                self.b.origin = True
                self.waferwindow.widgets.txtOriginChip.setText(coord_text)
                # clear home position
                self.waferwindow.widgets.txtHomeChip.setText("")
                for i in self.waferwindow.centralWidget().findChildren(QWaferButton):
                    if i.text() == "H":
                        i.setText(i.coord_text)

                self.waferwindow._status = "IDLE"
                self.waferwindow.widgets.cmbStatus.setCurrentText("IDLE")
            if status == "IN":
                self.b.btnType = "in"
            if status == "OUT":
                self.b.btnType = "out"
            if status == "MEAS":
                self.b.btnType = "meas"

        print("color selected: " + str(self.btnType) + "; xmax,ymax: " + str(self.x) + "," + str(self.y))
        print("status : " + self.waferwindow.widgets.cmbStatus.currentText())




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
        self._enable = enable
        self.setEnabled(enable)
        
        if name=="H":
            self._home = True
        if name=="O":
            self._origin = True
        btnName = "btn_"+str(x)+"_"+str(y)
        if name=="":
            self.setText(self.coord_text)
        else:
            # Home & Origin
            self.setText(name)
        self.setStyleSheet("font-size: 8pt; text-align: center; border: 1px solid #DDDDDD; background-color: %s;" % self.COLORS_DIES[self.btnType])
        self.btnName = btnName
        self.setObjectName(self.btnName)
        self.setToolTip(self.coord_text)

    def total_meas(self):
        # get measured chips
        total_meas = 0
        for i in self.waferwindow.centralWidget().findChildren(QWaferButton):
            if i._btnType == "meas":
                total_meas += 1
        self.waferwindow.widgets.txtNumberDies.setValue(total_meas)
        
    def unset_home(self):
        for i in self.waferwindow.centralWidget().findChildren(QWaferButton):
            if i.text() == "H":
                i.setText(self.coord_text)

    @property
    def home(self):
        return self._home

    @home.setter
    def home(self,value):
        self._home = value
        if value:
            self.setText("H")
            print ("set home")
        else:
            # self.unset_home()
            self.setText(self.coord_text)
            print ("unset home")


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
            print ("set origin")
        else:

            self.setText(self.coord_text)
            print ("unset origin")

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
            self.setStyleSheet("font-size: 8pt; text-align: center; border: 1px solid #DDDDDD; background-color: %s;" % self.COLORS_DIES[value])
            self.waferwindow.total_meas()


    @btnType.deleter
    def btnType(self):
        del self._btnType
