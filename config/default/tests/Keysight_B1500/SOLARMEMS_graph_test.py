# SOLARMEM test

import os.path
import sys
import statistics

global test_status, measurement_status
global dieActual, moduleActual, posx, posy

global Voltage, bad_devices, good_devices

meas_status = "meas_success"
message = ""
Voltage = [0,1,2,3]

I1_dark = [0,1,2,3]
I2_dark = [0,2,2,3]
I3_dark = [1,3,4,5]
I4_dark = [-1,4,5,8]

I1_light = [1,2,3,4]
I2_light = [1,2,3,4]
I3_light = [1,2,3,4]
I4_light = [1,2,3,4]

params = []

plot_parameters =  [{
        "name" : "Plot IV dark",
        "x" : Voltage,
        "y1" : I1_dark,
        "y2" : I2_dark,
		"y3" : I3_dark,
		"y4" : I4_dark,
        "titles" : {
            "title" : "I-V Measurement dark",
            "left" : "Sensor current",
            "bottom" : "Voltage"
        },
        "units" : {
            "left" : "A",
            "bottom" : "V",
            "right" : "A"
        },
        "showgrid" : {"x" : False, "y" : False},
        "legend" : True,
        "multiaxis" : False

    },{
        "name" : "Plot IV light",
        "x" : Voltage,
        "y1" : I1_light,
        "y2" : I2_light,
		"y3" : I3_light,
		"y4" : I4_light,
        "titles" : {
            "title" : "I-V Measurement light",
            "left" : "Sensor current",
            "bottom" : "Voltage"
        },
        "units" : {
            "left" : "A",
            "bottom" : "V",
            "right" : "A"
        },
        "showgrid" : {"x" : False, "y" : False},
        "legend" : True,
        "multiaxis" : False

    }]



try:
	# show 2 graphs
	num_graphs = 2
	for i in range(0,num_graphs):
		self.plotwindow[i] = ""
		self.show_plotwindow(plot_parameters[i],i)


except:
    message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<","").replace(">","") + " occurred. " + str(sys.exc_info()[1])
    self.updateTextDescription(message,"ERROR")
    retval = messageBox(self,"ERROR",message,"critical")

