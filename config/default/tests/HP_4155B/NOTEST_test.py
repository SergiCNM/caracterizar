# Test in HP 4155B instrument
global test_status, measurement_status
global dieActual, moduleActual

# print("Testing die "+str(dieActual)+ " & module " + str(moduleActual))
if cartographic_measurement:
    meas_status = "meas_success"
    self.waferwindow.meas_result[int(dieActual)-1][int(moduleActual)-1] = {
        "status" : meas_status,
        "message" : "",
        "contact_height" : "", 
        "variables" : {
    		"params" : [{"name" : "CMAX", "value" : 420.056E-12},{"name" : "CMIN", "value" : 210.057E-12}],
       		"data" : [{"name" : "V", "values" : [0,1,2,3,4,5], "units" : "V"},{"name": "C", "values" : [210.057E-12, 215.24E-12, 310.85E-12, 360.45E-12, 400, 420.56E-12], "units": "F"}]
     	},
        #"variables" : [{"name" : "cmax(pF)", "value" : 420.056},{"name" : "cmin(pF)", "value" : 210.057}],
        "plot_parameters" : {
        	"name" : "Plot die " + dieActual + " & module " + moduleActual,
            "x" : [0,1,2,3,4,5],
            "y" : [210.057, 215.24, 310.85, 360.45, 400, 420.56],
            "y2" : [],
            #"y2" : [3500.057, 2050.24, 2800.85, 3200.45, 3900, 4200.56],

            "titles" : {
            	"title" : "C-V Measurement",
                "left" : "Capacitance",
                "bottom" : "Voltage",
                "right" : "Conductance"
            },
            "units" : {
            	"left" : "pF",
                "bottom" : "V",
                "right" : "s"
            },
            "showgrid" : {"x" : False, "y" : False},
            "legend" : True
            #"foreground" : "#CCCCCC"

        }

    }

else:
    print("No test...")		
