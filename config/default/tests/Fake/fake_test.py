# Test for fake instrument
import time
import sys
global test_status, measurement_status
global dieActual, moduleActual, cartographic_measurement



print("Making test for fake instrument")
time.sleep(2)
if __name__ == "__main__":
    try:
        if cartographic_measurement:
            # fake cartographic measurement
            params = [{"name" : "CMAX", "value" : 420.056E-12},{"name" : "CMIN", "value" : 210.057E-12}]
            voltage = [0, 1, 2, 3, 4, 5]
            capacitance = [0, 1, 2, 3, 4, 5]
            conductance = [0, 1, 2, 3, 4, 5]

            meas_status = "meas_success"
            # save results
            main.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1] = {
                "status": meas_status,
                "message": "",
                "contact_height": "",
                "variables": {
                    "params": params,
                    "data": [{"name": "V", "values": voltage, "units": "V"},
                             {"name": "C", "values": capacitance, "units": "fF"},
                             {"name": "G", "values": conductance, "units": "nS"}]
                },
                "plot_parameters": {
                    "name": "Plot CV Die " + str(dieActual) + " Module " + str(moduleActual),
                    "x": voltage,
                    "y1": capacitance,
                    "y2": conductance,

                    "titles": {
                        "title": "C-V Measurement Die " + str(dieActual) + " Module " + str(moduleActual),
                        "left": "Capacitance",
                        "bottom": "Voltage",
                        "right": "Conductance"
                    },
                    "units": {
                        "left": "fF",
                        "bottom": "V",
                        "right": "nS"
                    },
                    "showgrid": {"x": True, "y": True},
                    "legend": False

                }

            }
            plot_parameters = main.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1]["plot_parameters"]
            emit_plot(plot_parameters)
        else:
            dieActual = 1
            moduleActual = 1
            # plot
            params = []
            voltage = [0, 1, 2, 3, 4, 5]
            capacitance = [0, 1, 2, 3, 4, 5]
            conductance = [0, 1, 2, 3, 4, 5]
            meas_status = "meas_success"
            # save results
            plot_parameters = {
                "name": "Plot CV Die " + str(dieActual) + " Module " + str(moduleActual),
                "x": voltage,
                "y1": capacitance,
                "y2": conductance,

                "titles": {
                    "title": "C-V Measurement" + str(dieActual) + " Module " + str(moduleActual),
                    "left": "Capacitance",
                    "bottom": "Voltage",
                    "right": "Conductance"
                },
                "units": {
                    "left": "fF",
                    "bottom": "V",
                    "right": "nS"
                },
                "showgrid": {"x": True, "y": True},
                "legend": False

            }
            emit_plot(plot_parameters)

    except:
        message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<","").replace(">","") + " occurred. " + str(sys.exc_info()[1])
        main.updateTextDescription(message,"ERROR")
        # retval = messageBox(main,"ERROR",message,"critical")
        message_user(main, "ERROR", message, "ok_error")
        #print("ERROR: " + "Oops! " + str(sys.exc_info()[0]) + " occurred. " + str(sys.exc_info()[1]))

