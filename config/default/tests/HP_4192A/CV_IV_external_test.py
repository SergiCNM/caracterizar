# -------------------------------------------------------
# Test CV_IV_external in HP 4192A and Keithley 2470 instruments
# -------------------------------------------------------
# This test is used to measure CV curves using an external voltage source
# - Keithley 2470 applies voltage steps
# - HP 4192A measures capacitance at each voltage step
# It can be used in cartographic mode or single measurement mode
# In cartographic mode, the test is performed in each die and module of the wafer
# In single measurement mode, the test is performed in a single device
# The test can be configured to:
#   - make OPEN and SHORT compensation before the measurement
#   - make hysteresis measurement
#   - use light during the measurement
#   - use different frequencies for the measurement
# The results are saved in a text file and plotted in the main window
# The results are also saved in the meas_result variable of the waferwindow object
# The configuration is saved in a toml file
# -------------------------------------------------------

import os.path
import numpy as np
import time
from PySide6.QtWidgets import QMessageBox

from config.default.instruments import HP_4192A
from config.default.instruments import Keithley_2470
from config.default.devices import *
from config.functions import *
import toml

global test_status, measurement_status
global dieActual, moduleActual
global CV_IV_external_parameters
global base_dir, tests_dir, cartographic_measurement


def load_CV_IV_external_parameters():
    """
    Load parameters from toml file or default
    :return: None
    """
    global CV_IV_external_parameters

    # default values (similar to Keysight_E4990A CV_IV_external but adapted for HP_4192A)
    CV_IV_external_parameters = {
        "START": 0.0,
        "STOP": 40.0,
        "STEP": 1.0,
        "FREQ": "100",
        "OSC": 500,
        "APERTURE": "3",
        "POINT_AVERAGE": False,
        "AVERAGE_POINTS": 8,
        "SWEEP_AVERAGE": False,
        "AVERAGE_SWEEPS": 8,
        "HYSTERESIS": False,
        "HYSTERESIS_TIME": 0,
        "WAIT_TIME": 0.5,
        "SETTLE_TIME": 0.1,
        "LIGHT": False,
        "LIGHT_TIME": 1,
        "COMPLIANCE": 0.01,
        "RANGE": "AUTO",
        "ROUTE_TERM": "REAR",
        "COMPENSATION_OPEN": False,
        "COMPENSATION_SHORT": False,
        "COMPENSATION_DONE": False,
        "GRAPH1": "CP",
        "GRAPH2": "G",
    }
    # load from external toml file in tests_dir (if exists, if not default values)
    filename_config = os.getcwd() + base_dir + tests_dir + '/HP_4192A/CV_IV_external.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        CV_IV_external_parameters = toml_info["parameters"]


def config_HP4192A_for_spot_measurement(hp4192A, CV_IV_external_parameters):
    """
    Configure HP 4192A for spot capacitance measurement at fixed frequency.
    The DC bias is assumed to be provided by an external voltage source (Keithley 2470),
    so the internal sweep of the HP 4192A is not used.
    :param hp4192A: HP_4192A instrument instance
    :param CV_IV_external_parameters: parameters dictionary
    :return: True if successful
    """
    try:
        # Build a minimal CV_parameters dict reusing the existing driver interface
        freq_khz = float(str(CV_IV_external_parameters["FREQ"]).replace(" ", "").split(",")[0])
        cv_params = {
            "START": 0.0,
            "STOP": 0.0,
            "STEP": 0.1,
            "OSC": float(CV_IV_external_parameters["OSC"]),
            "FREQ": freq_khz,
            "CIRCUIT_MODE": "Parallel",
            "AVERAGE": CV_IV_external_parameters.get("POINT_AVERAGE", False),
        }

        # Configure the instrument using its existing CV configuration method
        # Even though START/STOP/STEP define an internal sweep, we will only
        # trigger single measurements at the currently applied external bias.
        if not hp4192A.config_CV_spot(cv_params):
            return False

        return True
    except Exception as ex:
        print(f"Error configuring HP_4192A: {ex}")
        return False


def measure_single_capacitance(hp4192A, CV_IV_external_parameters):
    """
    Measure single capacitance value at current voltage (set by external source)
    Using HP_4192A single measurement command.
    :param hp4192A: HP_4192A instrument instance
    :param CV_IV_external_parameters: parameters dictionary (kept for compatibility)
    :return: capacitance, conductance
    """
    try:
        start_time = time.time()

        # Trigger single measurement and read response
        hp4192A.single()
        lectura = hp4192A.read()
        lectura_array = lectura.split(",")
        print("lectura_array:", lectura_array)

        # Expected format similar to CV_test: "Cxxx,...", "R/Gxxx,...", "Vxxx..."
        capacitance_value = lectura_array[0][4:]
        conductance_value = lectura_array[1][4:]

        capacitance = float(capacitance_value)
        conductance = float(conductance_value)

        elapsed = time.time() - start_time

        return capacitance, conductance, elapsed

    except Exception as ex:
        print(f"Error measuring capacitance (HP_4192A): {ex}")
        return None, None, None


def measure_CV_IV_external(main, k2470, hp4192A, CV_IV_external_parameters):
    """
    Measure CV curve using external voltage source (Keithley 2470)
    :param main: main program instance
    :param k2470: Keithley 2470 instrument instance
    :param hp4192A: HP_4192A instrument instance
    :param CV_IV_external_parameters: parameters dictionary
    :return: voltage, capacitance, conductance lists
    """
    voltage_list = []
    current_list = []
    capacitance_list = []
    conductance_list = []
    print("measuring CV_IV_external with HP_4192A...")

    # Generate voltage steps
    start_v = CV_IV_external_parameters["START"]
    stop_v = CV_IV_external_parameters["STOP"]
    step_v = CV_IV_external_parameters["STEP"]

    if start_v > stop_v:
        step_v = -abs(step_v)
    else:
        step_v = abs(step_v)

    num_points = int(abs((stop_v - start_v) / step_v)) + 1
    voltage_steps = np.linspace(start_v, stop_v, num_points)

    # Configure Keithley 2470 for voltage source mode
    compliance = float(CV_IV_external_parameters["COMPLIANCE"] * 1E-3)
    print("set compliance:", str(compliance))
    k2470.instrument.write(f":SENS:CURR:RANGE {str(compliance)}")

    # Configure Keithley 2470 for voltage source mode
    if k2470.config_IV(CV_IV_external_parameters):
        k2470.set_voltage(start_v)
        k2470.output("ON")
    else:
        print("Error configuring Keithley 2470")
        return [], [], []

    # Light control
    if CV_IV_external_parameters["LIGHT"]:
        main.init_prober()
        if main.prober != "":
            main.prober.light("1")
            time.sleep(CV_IV_external_parameters["LIGHT_TIME"])
            main.prober.light("0")

    # Wait time before starting
    if CV_IV_external_parameters["WAIT_TIME"] > 0:
        time.sleep(CV_IV_external_parameters["WAIT_TIME"])

    # Measure at each voltage step
    for voltage in voltage_steps:
        try:
            # Set voltage on Keithley 2470
            print("Setting voltage to:", voltage)
            k2470.set_voltage(voltage)

            # Wait for voltage to settle
            if CV_IV_external_parameters["SETTLE_TIME"] > 0:
                time.sleep(CV_IV_external_parameters["SETTLE_TIME"])

            # Measure current with Keithley 2470
            current = k2470.measure_current_once()

            # Measure capacitance with HP_4192A
            capacitance, conductance, t_meas = measure_single_capacitance(
                hp4192A, CV_IV_external_parameters
            )
            print("measured capacitance: ", capacitance)
            if t_meas is not None:
                print(f"tmeas: {t_meas * 1000:.1f} ms")
            if capacitance is not None and current is not None:
                voltage_list.append(voltage)
                current_list.append(current)
                capacitance_list.append(capacitance)
                conductance_list.append(conductance)
            else:
                print(f"Error measuring at voltage {voltage}V")

        except Exception as ex:
            print(f"Error at voltage {voltage}V: {ex}")

    # Turn off Keithley output
    k2470.output("OFF")

    # Hysteresis measurement (reverse direction)
    if CV_IV_external_parameters["HYSTERESIS"]:
        if CV_IV_external_parameters["HYSTERESIS_TIME"] > 0:
            time.sleep(CV_IV_external_parameters["HYSTERESIS_TIME"])

        # Reverse voltage steps
        voltage_steps_reverse = voltage_steps[::-1]

        k2470.output("ON")
        for voltage in voltage_steps_reverse:
            try:
                k2470.set_voltage(voltage)
                if CV_IV_external_parameters["SETTLE_TIME"] > 0:
                    time.sleep(CV_IV_external_parameters["SETTLE_TIME"])

                # Measure current with Keithley 2470
                current = k2470.measure_current_once()

                capacitance, conductance, _ = measure_single_capacitance(
                    hp4192A, CV_IV_external_parameters
                )

                if capacitance is not None and current is not None:
                    voltage_list.append(voltage)
                    current_list.append(current)
                    capacitance_list.append(capacitance)
                    conductance_list.append(conductance)

            except Exception as ex:
                print(f"Error at voltage {voltage}V (hysteresis): {ex}")

        k2470.output("OFF")

    return voltage_list, current_list, capacitance_list, conductance_list


def make_compensation(main, hp4192A, CV_IV_external_parameters):
    """
    Make OPEN and SHORT compensation
    :param main: main program instance
    :param hp4192A: HP_4192A instrument instance
    :param CV_IV_external_parameters: parameters dictionary
    :return: True if successful
    """
    retval = message_user(
        main,
        "Compensation",
        "Please, make OPEN compensation: remove the device from the fixture and press OK",
        "ok_cancel",
    )
    if retval != QMessageBox.Ok:
        return False
    main.updateTextDescription("Making OPEN compensation...<br />")
    if CV_IV_external_parameters["COMPENSATION_OPEN"]:
        hp4192A.zero_open("ON")
    else:
        hp4192A.zero_open("OFF")
    time.sleep(1)
    retval = message_user(
        main,
        "Compensation",
        "Please, make SHORT compensation: short the fixture and press OK",
        "ok_cancel",
    )
    if retval != QMessageBox.Ok:
        return False
    main.updateTextDescription("Making SHORT compensation...<br />")
    if CV_IV_external_parameters["COMPENSATION_SHORT"]:
        hp4192A.zero_short("ON")
    else:
        hp4192A.zero_short("OFF")
    time.sleep(1)
    return True


def make_full_compensation(main, hp4192A, CV_IV_external_parameters):
    """
    Make full compensation if not already done
    :param main: main program instance
    :param hp4192A: HP_4192A instrument instance
    :param CV_IV_external_parameters: parameters dictionary
    :return: None
    """
    if not CV_IV_external_parameters["COMPENSATION_DONE"]:
        main.updateTextDescription("<br />Making compensation...<br />")
        if not make_compensation(main, hp4192A, CV_IV_external_parameters):
            main.updateTextDescription("Compensation failed! Aborting test...<br />", "ERROR")
            test_status.status = "ABORTED"
        else:
            # Modify toml file to indicate that compensation is done
            CV_IV_external_parameters["COMPENSATION_DONE"] = True
            filename_config = os.getcwd() + base_dir + tests_dir + '/HP_4192A/CV_IV_external.toml'
            file_exists = os.path.exists(filename_config)
            if file_exists:
                toml_info = toml.load(filename_config)
                toml_info["parameters"] = CV_IV_external_parameters
                with open(filename_config, 'w', encoding='utf-8') as tomlfile:
                    toml.dump(toml_info, tomlfile)
            main.updateTextDescription("Compensation done!<br />")
            retval = message_user(
                main,
                "Compensation done!",
                "Please, configure instruments for measurement, make CONTACT and press YES to continue",
                "yes_cancel",
            )


try:
    # Initialize instruments
    k2470 = Keithley_2470(instruments["Keithley_2470"])
    hp4192A = HP_4192A(instruments["HP_4192A"])

    # Load parameters
    load_CV_IV_external_parameters()

    # Extract frequencies (comma-separated list)
    freqs = CV_IV_external_parameters["FREQ"].replace(" ", "").split(",")
    freqs = [float(f) for f in freqs if f]

    if cartographic_measurement:
        if str(dieActual) == "1" and str(moduleActual) == "1":
            retval = message_user(
                main,
                "Init instruments for CV_IV_external (HP_4192A)!",
                "Please, configure instruments for initialization",
                "yes_cancel",
            )
            if retval == QMessageBox.Yes:
                test_status.status = "STARTED"
                # Make compensation
                make_full_compensation(main, hp4192A, CV_IV_external_parameters)
            else:
                test_status.status = "ABORTED"

        if test_status.status == "STARTED":
            # Measure for each frequency
            for freq in freqs:
                load_CV_IV_external_parameters()  # Reload parameters
                CV_IV_external_parameters["FREQ"] = str(freq)

                # Configure HP_4192A for spot measurement
                if config_HP4192A_for_spot_measurement(hp4192A, CV_IV_external_parameters):
                    # Measure CV curve
                    voltage, current, capacitance, conductance = measure_CV_IV_external(
                        main, k2470, hp4192A, CV_IV_external_parameters
                    )

                    if len(voltage) > 0:
                        meas_status = "meas_success"
                        meas_message = f"Measured {len(voltage)} points"
                    else:
                        meas_status = "meas_error"
                        meas_message = "No measurements obtained"

                    # Convert to numpy arrays for easier manipulation
                    voltage = np.array(voltage)
                    current = np.array(current)
                    capacitance = np.array(capacitance)
                    conductance = np.array(conductance)

                    # Save results
                    main.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1] = {
                        "status": meas_status,
                        "message": meas_message,
                        "contact_height": "",
                        "variables": {
                            "params": [],
                            "data": [
                                {"name": "V", "values": voltage.tolist(), "units": "V"},
                                {"name": "I", "values": current.tolist(), "units": "A"},
                                {"name": "C", "values": (capacitance * 1e12).tolist(), "units": "pF"},
                                {"name": "G", "values": (conductance * 1e9).tolist(), "units": "nS"},
                            ],
                        },
                        "plot_parameters": {
                            "name": f"Plot CV_IV_external HP_4192A {freq}kHz (Die {dieActual} Module {moduleActual})",
                            "x": voltage.tolist(),
                            "y1": (capacitance * 1e12).tolist(),
                            "y2": (conductance * 1e9).tolist(),
                            "titles": {
                                "title": f"CV_IV_external HP_4192A {freq}kHz (Die {dieActual} Module {moduleActual})",
                                "left": "Capacitance",
                                "bottom": "Voltage",
                                "right": "Conductance",
                            },
                            "units": {
                                "left": "pF",
                                "bottom": "V",
                                "right": "nS",
                            },
                            "showgrid": {"x": True, "y": True},
                            "legend": False,
                        },
                    }

                    plot_parameters = main.waferwindow.meas_result[int(dieActual) - 1][
                        int(moduleActual) - 1
                    ]["plot_parameters"]
                    emit_plot(plot_parameters)

                    # Save to file
                    namefile = (
                        main.getDirs("results")
                        + f"/CV_IV_external_HP_4192A_{freq}kHz_{main.ui.txtProcess.text()}_{dieActual}_{moduleActual}.txt"
                    )
                    main.save_lists_to_txt(
                        namefile=namefile,
                        var_list=[voltage, current, capacitance, conductance],
                        headers=["V", "I", "C", "G"],
                        separation=",",
                    )
                else:
                    meas_status = "meas_error"
                    meas_message = "Error configuring HP_4192A"

    else:
        # Single measurement mode
        # Make compensation
        make_full_compensation(main, hp4192A, CV_IV_external_parameters)

        # Measure for each frequency
        for freq in freqs:
            load_CV_IV_external_parameters()
            CV_IV_external_parameters["FREQ"] = str(freq)

            if config_HP4192A_for_spot_measurement(hp4192A, CV_IV_external_parameters):
                voltage, current, capacitance, conductance = measure_CV_IV_external(
                    main, k2470, hp4192A, CV_IV_external_parameters
                )

                if len(voltage) > 0:
                    voltage = np.array(voltage)
                    current = np.array(current)
                    capacitance = np.array(capacitance)
                    conductance = np.array(conductance)

                    plot_parameters = {
                        "name": f"Plot CV_IV_external HP_4192A {freq}kHz",
                        "x": voltage.tolist(),
                        "y1": (capacitance * 1e12).tolist(),
                        "y2": (conductance * 1e9).tolist(),
                        "titles": {
                            "title": f"CV_IV_external HP_4192A Measurement at {freq}kHz",
                            "left": "Capacitance",
                            "bottom": "Voltage",
                            "right": "Conductance",
                        },
                        "units": {
                            "left": "pF",
                            "bottom": "V",
                            "right": "nS",
                        },
                        "showgrid": {"x": True, "y": True},
                        "legend": True,
                    }

                    emit_plot(plot_parameters)

                    # Save to file
                    dieActual = 1
                    moduleActual = 1
                    namefile = (
                        main.getDirs("results")
                        + f"/CV_IV_external_HP_4192A_{freq}kHz_{main.ui.txtProcess.text()}_single.txt"
                    )
                    main.save_lists_to_txt(
                        namefile=namefile,
                        var_list=[voltage, current, capacitance, conductance],
                        headers=["V", "I", "C", "G"],
                        separation=",",
                    )

    # Stop and close instruments
    k2470.stop()
    k2470.close()
    hp4192A.stop()
    hp4192A.close()

except:
    import sys

    message = (
        "ERROR: Oops! "
        + str(sys.exc_info()[0]).replace("<", "").replace(">", "")
        + " occurred. "
        + str(sys.exc_info()[1])
    )
    main.updateTextDescription(message, "ERROR")
    message_user(main, "ERROR", message, "ok_error")



