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
from config.default.instruments import Keithley_2410
from config.default.devices import *
from config.default.tests.common import save_results_to_file, build_results_folder, get_plot_parameters
from config.functions import *
import toml

global test_status, measurement_status
global dieActual, moduleActual
global CV_IV_external_parameters
global base_dir, tests_dir, results_dir, username, cartographic_measurement


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
        "SOURCE_INSTRUMENT": "Keithley_2470",
        "GRAPH1": "CP",
        "GRAPH2": "G",
    }
    # load from external toml file in tests_dir (if exists, if not default values)
    filename_config = os.getcwd() + base_dir + tests_dir + '/HP_4192A/CV_IV_external.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        CV_IV_external_parameters = toml_info["parameters"]
        if "output" in toml_info:
            CV_IV_external_parameters["output"] = toml_info["output"]
        if "plot" in toml_info:
            CV_IV_external_parameters["plot"] = toml_info["plot"]


def config_HP4192A_for_spot_measurement(hp4192A, CV_IV_external_parameters):
    """
    Configure HP 4192A for spot capacitance measurement at fixed frequency.
    The DC bias is assumed to be provided by an external voltage source,
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


def measure_CV_IV_external(main, source_smu, hp4192A, CV_IV_external_parameters):
    """
    Measure CV curve using external voltage source
    :param main: main program instance
    :param source_smu: Keithley instrument instance
    :param hp4192A: HP_4192A instrument instance
    :param CV_IV_external_parameters: parameters dictionary
    :return: voltage, capacitance, conductance lists
    """
    voltage_list = []
    current_list = []
    capacitance_list = []
    conductance_list = []

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

    # Configure source SMU for voltage source mode
    if source_smu.driver_name == "Keithley_2470":
        compliance = float(CV_IV_external_parameters["COMPLIANCE"] * 1E-3)
        source_smu.instrument.write(f":SENS:CURR:RANGE {str(compliance)}")

    if source_smu.config_IV(CV_IV_external_parameters):
        source_smu.set_voltage(start_v)
        source_smu.output("ON")
    else:
        print("Error configuring source SMU")
        return [], [], [], []

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
            # Set voltage on source SMU
            source_smu.set_voltage(voltage)

            # Wait for voltage to settle
            if CV_IV_external_parameters["SETTLE_TIME"] > 0:
                time.sleep(CV_IV_external_parameters["SETTLE_TIME"])

            # Measure current with source SMU
            current = source_smu.measure_current_once()

            # Measure capacitance with HP_4192A
            capacitance, conductance, t_meas = measure_single_capacitance(
                hp4192A, CV_IV_external_parameters
            )
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

    # Turn off source SMU output
    source_smu.output("OFF")

    # Hysteresis measurement (reverse direction)
    if CV_IV_external_parameters["HYSTERESIS"]:
        if CV_IV_external_parameters["HYSTERESIS_TIME"] > 0:
            time.sleep(CV_IV_external_parameters["HYSTERESIS_TIME"])

        # Reverse voltage steps
        voltage_steps_reverse = voltage_steps[::-1]

        source_smu.output("ON")
        for voltage in voltage_steps_reverse:
            try:
                source_smu.set_voltage(voltage)
                if CV_IV_external_parameters["SETTLE_TIME"] > 0:
                    time.sleep(CV_IV_external_parameters["SETTLE_TIME"])

                # Measure current with source SMU
                current = source_smu.measure_current_once()

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

        source_smu.output("OFF")

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
    load_CV_IV_external_parameters()
    instr_name = CV_IV_external_parameters.get("SOURCE_INSTRUMENT", "Keithley_2470")
    
    if instr_name == "Keithley_2410":
        source_smu = Keithley_2410(instruments["Keithley_2410"])
        source_smu.driver_name = "Keithley_2410"
    else:
        source_smu = Keithley_2470(instruments["Keithley_2470"])
        source_smu.driver_name = "Keithley_2470"

    hp4192A = HP_4192A(instruments["HP_4192A"])

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
                CV_IV_external_parameters["FREQ"] = str(freq)

                # Configure HP_4192A for spot measurement
                if config_HP4192A_for_spot_measurement(hp4192A, CV_IV_external_parameters):
                    # Measure CV curve
                    voltage, current, capacitance, conductance = measure_CV_IV_external(
                        main, source_smu, hp4192A, CV_IV_external_parameters
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
                    plot_config = CV_IV_external_parameters.get("plot", {}).copy()
                    base_title = plot_config.get("TITLE", "CV Measurement")
                    plot_config["NAME"] = f"Plot CV_IV_external HP_4192A {freq}kHz (Die {dieActual} Module {moduleActual})"
                    plot_config["TITLE"] = f"{base_title} {freq}kHz (Die {dieActual} Module {moduleActual})"

                    results_data_dict = {"V": voltage.tolist(), "I": current.tolist(), "C": (capacitance * 1e12).tolist(), "G": (conductance * 1e9).tolist()}
                    plot_parameters = get_plot_parameters(results_data_dict, ["V", "I", "C", "G"], plot_config)

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
                        "plot_parameters": plot_parameters
                    }

                    if plot_config.get("SHOW_PLOT", True):
                        emit_plot(plot_parameters)

                    # Save to file
                    results_data = list(zip(voltage, current, capacitance, conductance))
                    variables_list = ["V", "I", "C", "G"]
                    output_params = CV_IV_external_parameters.get("output", {"separator": "comma", "prefix": f"CV_IV_external_HP_4192A_{freq}kHz", "suffix": ""})
                    
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
                else:
                    meas_status = "meas_error"
                    meas_message = "Error configuring HP_4192A"

    else:
        # Single measurement mode
        # Make compensation
        make_full_compensation(main, hp4192A, CV_IV_external_parameters)

        # Measure for each frequency
        for freq in freqs:
            CV_IV_external_parameters["FREQ"] = str(freq)

            if config_HP4192A_for_spot_measurement(hp4192A, CV_IV_external_parameters):
                voltage, current, capacitance, conductance = measure_CV_IV_external(
                    main, source_smu, hp4192A, CV_IV_external_parameters
                )

                if len(voltage) > 0:
                    voltage = np.array(voltage)
                    current = np.array(current)
                    capacitance = np.array(capacitance)
                    conductance = np.array(conductance)

                    plot_config = CV_IV_external_parameters.get("plot", {}).copy()
                    base_title = plot_config.get("TITLE", "CV Measurement")
                    plot_config["NAME"] = f"Plot CV_IV_external HP_4192A {freq}kHz"
                    plot_config["TITLE"] = f"{base_title} {freq}kHz"

                    results_data_dict = {"V": voltage.tolist(), "I": current.tolist(), "C": (capacitance * 1e12).tolist(), "G": (conductance * 1e9).tolist()}
                    plot_parameters = get_plot_parameters(results_data_dict, ["V", "I", "C", "G"], plot_config)

                    dieActual = 1
                    moduleActual = 1

                    if plot_config.get("SHOW_PLOT", True):
                        emit_plot(plot_parameters)

                    # Save to file
                    dieActual = 1
                    moduleActual = 1
                    
                    results_data = list(zip(voltage, current, capacitance, conductance))
                    variables_list = ["V", "I", "C", "G"]
                    output_params = CV_IV_external_parameters.get("output", {"separator": "comma", "prefix": f"CV_IV_external_HP_4192A_{freq}kHz", "suffix": "single"})
                    
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

    # Stop and close instruments
    source_smu.stop()
    source_smu.close()
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



