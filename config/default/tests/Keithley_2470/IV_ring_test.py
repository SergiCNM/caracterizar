# Test IV_ring in two Keithley 2470 instruments
import os.path
from config.default.instruments import Keithley_2470
from config.default.devices import *
from config.default.tests.common import save_results_to_file, build_results_folder, get_plot_parameters
from config.functions import *
from PySide6.QtWidgets import QMessageBox
import toml, time
import numpy as np

global test_status, measurement_status
global dieActual, moduleActual, init_chip
global IV_ring_parameters
global base_dir, tests_dir, results_dir, username, cartographic_measurement


def load_IV_ring_parameters():
    """
    Load parameters from toml file or default
    :return: None
    """
    global IV_ring_parameters

    # default values (same as IV_test)
    IV_ring_parameters = {
        "START": 1,
        "STOP": -1,
        "STEP": 0.1,
        "COMPLIANCE": 0.1,
        "HYSTERESIS": False,
        "WAIT_TIME": 0,
        "LIGHT": False,
        "LIGHT_TIME": 1,
        "RANGE": "AUTO",
        "ROUTE_TERM": "REAR",
        "MEAS_SOURCE": "VOLT",
        "MEAS_SENSE": "CURR",
        "SOURCE_DELAY": 1.0,
        "COUNTS": 3,
        "RES_MIN": 100.0,
        "RES_MAX": 120.0
    }
    # load from external toml file in tests_dir (if exists, if not default values)
    filename_config = os.getcwd() + base_dir + tests_dir + '/Keithley_2470/IV_ring.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        IV_ring_parameters = toml_info["parameters"]
        if "output" in toml_info:
            IV_ring_parameters["output"] = toml_info["output"]
        if "plot" in toml_info:
            IV_ring_parameters["plot"] = toml_info["plot"]

def save_file(main, voltage, current_pad, current_ring, resistance_pad, resistance_ring, namefile):
    """
    Save file using common.save_results_to_file
    """
    global dieActual, moduleActual, username
    
    results_data = list(zip(voltage, current_pad, current_ring, resistance_pad, resistance_ring))
    variables_list = ["V", "I_pad", "I_ring", "R_pad", "R_ring"]
    output_params = IV_ring_parameters.get("output", {"separator": "comma", "prefix": "IV_ring", "suffix": ""})
    
    save_results_to_file(
        results_data=results_data,
        variables_list=variables_list,
        test_parameters=output_params,
        die=dieActual,
        module=moduleActual,
        folder_func=lambda: build_results_folder(
            username=username,
            process=main.ui.txtProcess.text(),
            lot=main.ui.txtLot.text(),
            wafer=main.ui.txtWafer.text()
        )
    )

def measure_IV_ring(k2470_pad, k2470_ring, IV_ring_parameters, main):
    voltage_list = []
    current_pad_list = []
    current_ring_list = []
    resistance_pad = []
    resistance_ring = []

    start = IV_ring_parameters["START"]
    stop = IV_ring_parameters["STOP"]
    step = abs(IV_ring_parameters["STEP"])
    delay = IV_ring_parameters.get("SOURCE_DELAY", 0.1)

    if start > stop:
        step = -step

    npts = int(abs((stop - start) / step)) + 1
    voltages = np.linspace(start, stop, npts)

    # Enable outputs
    k2470_pad.set_voltage(start)
    k2470_ring.set_voltage(start)
    k2470_pad.output("ON")
    k2470_ring.output("ON")

    # Optional wait time before sweep
    if IV_ring_parameters["WAIT_TIME"] > 0:
        time.sleep(IV_ring_parameters["WAIT_TIME"])

    # light time wait
    if IV_ring_parameters["LIGHT"]:
        # prober is not initialized when you select single measurement
        main.init_prober()
        if main.prober != "":
            main.prober.light("1")
            time.sleep(IV_ring_parameters["LIGHT_TIME"])
            main.prober.light("0")

    for V in voltages:
        try:
            # Apply same voltage to both SMUs
            k2470_pad.set_voltage(V)
            k2470_ring.set_voltage(V)

            time.sleep(delay)

            # Measure currents
            I_pad = float(k2470_pad.measure_current_once())
            I_ring = float(k2470_ring.measure_current_once())

            voltage_list.append(V)
            current_pad_list.append(I_pad)
            current_ring_list.append(I_ring)

            # Resistance (avoid division by zero)
            resistance_pad.append(V / I_pad if I_pad != 0 else 0.0)
            resistance_ring.append(V / I_ring if I_ring != 0 else 0.0)


        except Exception as ex:
            print(f"Error at V={V}: {ex}")
            break

    # Disable outputs
    k2470_pad.output("OFF")
    k2470_ring.output("OFF")

    return (
        voltage_list,
        current_pad_list,
        current_ring_list,
        resistance_pad,
        resistance_ring,
    )

# Removed local get_plot_parameters


if __name__ == "__main__":
    try:
        # init IV_ring_parameters
        load_IV_ring_parameters()
        instruments = load_toml_config("instruments.toml")
        k2470_pad = Keithley_2470(instruments["Keithley_2470"])
        k2470_ring = Keithley_2470(instruments["Keithley_2470ring"])
        
        if cartographic_measurement:
            if str(dieActual)==str(init_chip) and str(moduleActual) == "1":
                retval = message_user(main, "Init instruments for IV ring!",
                                      "Please, configure instruments for initialization",
                                      "yes_cancel")
                if retval == QMessageBox.Yes:
                    if not (k2470_pad.config_IV(IV_ring_parameters) and
                            k2470_ring.config_IV(IV_ring_parameters)):
                        raise RuntimeError("Error configuring Keithley 2470 instruments")
                    test_status.status = "STARTED"
                else:
                    test_status.status = "ABORTED"


            if test_status.status == "STARTED":
                # measure IV_ring
                time.sleep(1)
                voltage, current_pad, current_ring, resistance_pad, resistance_ring = \
                    measure_IV_ring(k2470_pad, k2470_ring, IV_ring_parameters, main)

                # error in measurement if error counts >0
                meas_status = "meas_error"
                message = "Some error in measurement!"
                voltage_end = float(voltage[len(voltage) - 1])
                current_pad_end = float(current_pad[len(current_pad)-1])
                current_ring_end = float(current_ring[len(current_ring)-1])
                
                # Check if both measurements reached stop voltage (within a small tolerance)
                if abs(float(IV_ring_parameters["STOP"]) - voltage_end) < 1e-6:
                    meas_status = "meas_success" # if reach the stop voltage
                    message = f"Current pad at {voltage_end} V : {current_pad_end} A, Current ring: {current_ring_end} A"
                else:
                    if k2470_pad.get_error_count() == 0 and k2470_ring.get_error_count() == 0:
                        meas_status = "meas_warning"  # if not reach the stop voltage
                        message = f"Current pad at {voltage_end} V : {current_pad_end} A, Current ring: {current_ring_end} A"
                
                # get average of resistance for pad and ring, strip first and last 2 points
                if len(resistance_pad) > 4:
                    resistance_pad_avg = sum(resistance_pad[2:-2]) / (len(resistance_pad) - 4)
                else:
                    resistance_pad_avg = sum(resistance_pad) / len(resistance_pad) if len(resistance_pad) > 0 else 0
                
                if len(resistance_ring) > 4:
                    resistance_ring_avg = sum(resistance_ring[2:-2]) / (len(resistance_ring) - 4)
                else:
                    resistance_ring_avg = sum(resistance_ring) / len(resistance_ring) if len(resistance_ring) > 0 else 0

                # Check both resistances against limits
                if meas_status == "meas_success":
                    pad_out_of_range = resistance_pad_avg < IV_ring_parameters["RES_MIN"] or resistance_pad_avg > IV_ring_parameters["RES_MAX"]
                    ring_out_of_range = resistance_ring_avg < IV_ring_parameters["RES_MIN"] or resistance_ring_avg > IV_ring_parameters["RES_MAX"]
                    
                    if pad_out_of_range or ring_out_of_range:
                        meas_status = "meas_warning"
                        pad_msg = f"R_pad_avg ({resistance_pad_avg:.4e} Ohms)" if pad_out_of_range else ""
                        ring_msg = f"R_ring_avg ({resistance_ring_avg:.4e} Ohms)" if ring_out_of_range else ""
                        if pad_msg and ring_msg:
                            message = f"{pad_msg} and {ring_msg} out of limits"
                        elif pad_msg:
                            message = f"{pad_msg} out of limits"
                        else:
                            message = f"{ring_msg} out of limits"

                # show results resistance average in description
                main.updateTextDescription(f"R_pad_avg: {resistance_pad_avg:.4e} Ohm, R_ring_avg: {resistance_ring_avg:.4e} Ohm", "RESULT")
                # get plot parameters (only currents, no resistance)
                results_data_dict = {"V": voltage, "I_pad": current_pad, "I_ring": current_ring}
                plot_parameters = get_plot_parameters(results_data_dict, ["V", "I_pad", "I_ring"], IV_ring_parameters.get("plot", {}))
                # save results
                main.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1] = {
                    "status": meas_status,
                    "message": message,
                    "contact_height": "",
                    "variables": [{
                        "params": [{"name" : "pass", "value" : str(meas_status)}, 
                                  {"name" : "R_pad_avg", "value" : str(resistance_pad_avg)},
                                  {"name" : "R_ring_avg", "value" : str(resistance_ring_avg)}],
                        "data": [{"name": "V", "values": voltage, "units": "V"},
                                 {"name": "I_pad", "values": current_pad, "units": "A"},
                                 {"name": "I_ring", "values": current_ring, "units": "A"},
                                 {"name": "R_pad", "values": resistance_pad, "units": "Ohm"},
                                 {"name": "R_ring", "values": resistance_ring, "units": "Ohm"}
                                 ]
                    }],
                    "plot_parameters": plot_parameters

                }

                namefile = f"IV_ring_{main.ui.txtLot.text()}_W" + f"{int(main.ui.txtWafer.text()):02d}_{str(dieActual)}_{str(moduleActual)}"
                save_file(main, voltage, current_pad, current_ring, resistance_pad, resistance_ring, namefile)
        else:
            # single measure
            if k2470_pad.config_IV(IV_ring_parameters) and k2470_ring.config_IV(IV_ring_parameters):
                time.sleep(1)
                voltage, current_pad, current_ring, resistance_pad, resistance_ring = \
                    measure_IV_ring(k2470_pad, k2470_ring, IV_ring_parameters, main)
                # get average of resistance for pad and ring, strip first and last 2 points
                if len(resistance_pad) > 4:
                    resistance_pad_avg = sum(resistance_pad[2:-2]) / (len(resistance_pad) - 4)
                else:
                    resistance_pad_avg = sum(resistance_pad) / len(resistance_pad) if len(resistance_pad) > 0 else 0
                
                if len(resistance_ring) > 4:
                    resistance_ring_avg = sum(resistance_ring[2:-2]) / (len(resistance_ring) - 4)
                else:
                    resistance_ring_avg = sum(resistance_ring) / len(resistance_ring) if len(resistance_ring) > 0 else 0

                # show results resistance average in description
                main.updateTextDescription(f"R_pad_avg: {resistance_pad_avg:.4e} Ohm, R_ring_avg: {resistance_ring_avg:.4e} Ohm", "RESULT")
                # main.updateTextDescription(txt_result)
                results_data_dict = {"V": voltage, "I_pad": current_pad, "I_ring": current_ring}
                plot_parameters = get_plot_parameters(results_data_dict, ["V", "I_pad", "I_ring"], IV_ring_parameters.get("plot", {}))
                # Single measurement, view plot
                if IV_ring_parameters.get("plot", {}).get("SHOW_PLOT", True):
                    emit_plot(plot_parameters)
                # Save file in results
                namefile = f"IV_ring_{main.ui.txtLot.text()}_W{int(main.ui.txtWafer.text()):02d}_single"
                save_file(main, voltage, current_pad, current_ring, resistance_pad, resistance_ring, namefile)

        # stop process, close instruments
        k2470_pad.stop()
        k2470_pad.close()
        k2470_ring.stop()
        k2470_ring.close()

    except:
        message = "ERROR: Oops! " + str(sys.exc_info()[0]).replace("<","").replace(">","") + " occurred. " + str(sys.exc_info()[1])
        main.updateTextDescription(message,"ERROR")
        message_user(main, "ERROR", message, "ok_error")



