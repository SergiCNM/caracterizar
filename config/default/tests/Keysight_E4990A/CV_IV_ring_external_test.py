# -------------------------------------------------------
# Test CV_IV_ring_external in Keysight E4990A and two Keithleys
# -------------------------------------------------------
# This test is used to measure CV curves using two external voltage sources
# - Two Keithleys apply the same voltage steps (pad and ring)
# - Keysight E4990A measures capacitance at each voltage step
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

from config.default.instruments import Keysight_E4990A
from config.default.instruments import Keithley_2470
from config.default.instruments import Keithley_2410
from config.default.devices import *
from config.default.tests.common import save_results_to_file, build_results_folder, get_plot_parameters
from config.functions import *
import toml

global test_status, measurement_status
global dieActual, moduleActual
global CV_IV_ring_external_parameters
global base_dir, tests_dir, results_dir, username, cartographic_measurement


def load_CV_IV_ring_external_parameters():
    """
    Load parameters from toml file or default
    :return: None
    """
    global CV_IV_ring_external_parameters

    # default values
    CV_IV_ring_external_parameters = {
        "START": 0.0,
        "STOP": 40.0,
        "STEP": 1.0,
        "FREQ": "100",
        "OSC": 500,
        "APERTURE": "5",
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
    filename_config = os.getcwd() + base_dir + tests_dir + '/Keysight_E4990A/CV_IV_ring_external.toml'
    file_exists = os.path.exists(filename_config)
    if file_exists:
        toml_info = toml.load(filename_config)
        CV_IV_ring_external_parameters = toml_info["parameters"]
        if "output" in toml_info:
            CV_IV_ring_external_parameters["output"] = toml_info["output"]
        if "plot" in toml_info:
            CV_IV_ring_external_parameters["plot"] = toml_info["plot"]


def config_E4990A_for_spot_measurement(keysightE4990A, CV_IV_ring_external_parameters):
    """
    Configure E4990A for spot capacitance measurement at fixed frequency
    Without applying DC bias (external voltage sources will be used)
    Configure in continuous mode to read single points
    :param keysightE4990A: E4990A instrument instance
    :param CV_IV_ring_external_parameters: parameters dictionary
    :return: True if successful
    """
    try:
        # Configure display and parameters
        if CV_IV_ring_external_parameters["GRAPH2"] != "NONE":
            keysightE4990A.instrument.write(':DISP:WIND1:SPL D1_2')
            keysightE4990A.instrument.write(f':CALC1:PAR2:DEF {CV_IV_ring_external_parameters["GRAPH2"]}')
        else:
            keysightE4990A.instrument.write(':DISP:WIND1:SPL D1')
        keysightE4990A.instrument.write(f':CALC1:PAR1:DEF {CV_IV_ring_external_parameters["GRAPH1"]}')

        # Configure AC signal
        keysightE4990A.instrument.write(f':SOUR1:VOLT:LEV {CV_IV_ring_external_parameters["OSC"] * 1e-3}')

        # Set frequency to fixed value (convert kHz to Hz) - CW mode
        freq_hz = float(CV_IV_ring_external_parameters["FREQ"]) * 1e3
        keysightE4990A.instrument.write(f':SENS1:FREQ:CW {freq_hz}')

        # Set sweep type to point (single measurement at fixed frequency)
        keysightE4990A.instrument.write(':SENS1:SWE:POIN 1')  # Single point
        keysightE4990A.instrument.write(':INIT1:CONT OFF')  # Single shot mode

        # Configure measurement settings
        keysightE4990A.instrument.write(f':SENS1:APER {CV_IV_ring_external_parameters["APERTURE"]}')
        keysightE4990A.instrument.write(f':SENS1:AVER:COUN {CV_IV_ring_external_parameters["AVERAGE_POINTS"]}')
        keysightE4990A.instrument.write(f':SENS1:AVER:STAT {1 if CV_IV_ring_external_parameters["POINT_AVERAGE"] else 0}')
        keysightE4990A.instrument.write(f':CALC1:AVER:COUN {CV_IV_ring_external_parameters["AVERAGE_SWEEPS"]}')
        keysightE4990A.instrument.write(f':CALC1:AVER:STAT {1 if CV_IV_ring_external_parameters["SWEEP_AVERAGE"] else 0}')

        # Set bias to 0V and keep it off (external sources will control DC voltage)
        keysightE4990A.instrument.write(':SOUR:BIAS:VOLT 0')
        keysightE4990A.instrument.write(':SOUR:BIAS:STAT OFF')

        # Trigger settings
        keysightE4990A.instrument.write(':TRIG:SOUR BUS')
        keysightE4990A.instrument.write(':INIT:CONT ON')

        return True
    except Exception as ex:
        print(f"Error configuring E4990A: {ex}")
        return False


def measure_single_capacitance(keysightE4990A, CV_IV_ring_external_parameters):
    """
    Measure single capacitance value at current voltage (set by external sources)
    Read results from E4990A
    :param keysightE4990A: E4990A instrument instance
    :param CV_IV_ring_external_parameters: parameters dictionary
    :return: capacitance, conductance, elapsed_time
    """
    try:
        t0 = time.time()

        # Trigger single measurement
        keysightE4990A.instrument.write(':TRIG:SING')
        keysightE4990A.instrument.write('*WAI')

        # Read capacitance (PAR1)
        keysightE4990A.instrument.write(':CALC1:PAR1:SEL')
        keysightE4990A.instrument.write(':FORM:DATA ASC')
        keysightE4990A.instrument.write(':FORM:REAL:ASC:LENG 12')
        r1 = keysightE4990A.instrument.query(':CALC1:SEL:DATA:FDAT?')
        ra1 = np.fromstring(r1, sep=',')

        # Read conductance (PAR2)
        if CV_IV_ring_external_parameters["GRAPH2"] != "NONE":
            keysightE4990A.instrument.write(':CALC1:PAR2:SEL')
            keysightE4990A.instrument.write(':FORM:DATA ASC')
            keysightE4990A.instrument.write(':FORM:REAL:ASC:LENG 12')
            r2 = keysightE4990A.instrument.query(':CALC1:SEL:DATA:FDAT?')
            ra2 = np.fromstring(r2, sep=',')
            conductance = ra2[0] if len(ra2) > 0 else 0.0
        else:
            conductance = 0.0

        capacitance = ra1[0] if len(ra1) > 0 else None
        elapsed = time.time() - t0

        return capacitance, conductance, elapsed

    except Exception as ex:
        print("Error measuring capacitance:", ex)
        return None, None, None


def measure_CV_IV_ring_external(main, source_pad, source_ring, keysightE4990A, CV_IV_ring_external_parameters):
    """
    Measure CV curve using two external voltage sources (Keithleys)
    Both SMUs apply the same voltage simultaneously
    :param main: main program instance
    :param source_pad: Keithley instrument instance for pad
    :param source_ring: Keithley instrument instance for ring
    :param keysightE4990A: Keysight E4990A instrument instance
    :param CV_IV_ring_external_parameters: parameters dictionary
    :return: voltage, current_pad, current_ring, capacitance, conductance lists
    """
    voltage_list = []
    current_pad_list = []
    current_ring_list = []
    capacitance_list = []
    conductance_list = []
    print("measuring Keysight_E4990A CV_IV_ring_external...")

    # Generate voltage steps
    start_v = CV_IV_ring_external_parameters["START"]
    stop_v = CV_IV_ring_external_parameters["STOP"]
    step_v = CV_IV_ring_external_parameters["STEP"]

    if start_v > stop_v:
        step_v = -abs(step_v)
    else:
        step_v = abs(step_v)

    num_points = int(abs((stop_v - start_v) / step_v)) + 1
    voltage_steps = np.linspace(start_v, stop_v, num_points)

    # Configure Pad SMU
    if source_pad.driver_name == "Keithley_2470":
        compliance = float(CV_IV_ring_external_parameters["COMPLIANCE"] * 1E-3)
        source_pad.instrument.write(f":SENS:CURR:RANGE {str(compliance)}")
    
    # Configure Ring SMU
    if source_ring.driver_name == "Keithley_2470":
        compliance = float(CV_IV_ring_external_parameters["COMPLIANCE"] * 1E-3)
        source_ring.instrument.write(f":SENS:CURR:RANGE {str(compliance)}")

    if source_pad.config_IV(CV_IV_ring_external_parameters) and source_ring.config_IV(CV_IV_ring_external_parameters):
        source_pad.set_voltage(start_v)
        source_ring.set_voltage(start_v)
        source_pad.output("ON")
        source_ring.output("ON")
    else:
        print("Error configuring source SMU instruments")
        return [], [], [], [], []

    # Light control
    if CV_IV_ring_external_parameters["LIGHT"]:
        main.init_prober()
        if main.prober != "":
            main.prober.light("1")
            time.sleep(CV_IV_ring_external_parameters["LIGHT_TIME"])
            main.prober.light("0")

    # Wait time before starting
    if CV_IV_ring_external_parameters["WAIT_TIME"] > 0:
        time.sleep(CV_IV_ring_external_parameters["WAIT_TIME"])

    # Measure at each voltage step
    for voltage in voltage_steps:
        try:
            # Set voltage on both Keithleys
            print("Setting voltage to:", voltage)
            source_pad.set_voltage(voltage)
            source_ring.set_voltage(voltage)

            # Wait for voltage to settle
            if CV_IV_ring_external_parameters["SETTLE_TIME"] > 0:
                time.sleep(CV_IV_ring_external_parameters["SETTLE_TIME"])

            # Measure current
            current_pad = source_pad.measure_current_once()
            current_ring = source_ring.measure_current_once()

            # Measure capacitance with E4990A
            capacitance, conductance, t_meas = measure_single_capacitance(
                keysightE4990A, CV_IV_ring_external_parameters
            )
            print("measured capacitance: ", capacitance)
            if t_meas is not None:
                print(f"tmeas: {t_meas * 1000:.1f} ms")
            
            if capacitance is not None and current_pad is not None and current_ring is not None:
                voltage_list.append(voltage)
                current_pad_list.append(current_pad)
                current_ring_list.append(current_ring)
                capacitance_list.append(capacitance)
                conductance_list.append(conductance)
            else:
                print(f"Error measuring at voltage {voltage}V")

        except Exception as ex:
            print(f"Error at voltage {voltage}V: {ex}")

    # Turn off outputs
    source_pad.output("OFF")
    source_ring.output("OFF")

    # Hysteresis
    if CV_IV_ring_external_parameters["HYSTERESIS"]:
        if CV_IV_ring_external_parameters["HYSTERESIS_TIME"] > 0:
            time.sleep(CV_IV_ring_external_parameters["HYSTERESIS_TIME"])

        voltage_steps_reverse = voltage_steps[::-1]

        source_pad.output("ON")
        source_ring.output("ON")
        for voltage in voltage_steps_reverse:
            try:
                source_pad.set_voltage(voltage)
                source_ring.set_voltage(voltage)
                if CV_IV_ring_external_parameters["SETTLE_TIME"] > 0:
                    time.sleep(CV_IV_ring_external_parameters["SETTLE_TIME"])

                current_pad = source_pad.measure_current_once()
                current_ring = source_ring.measure_current_once()

                capacitance, conductance, _ = measure_single_capacitance(
                    keysightE4990A, CV_IV_ring_external_parameters
                )

                if capacitance is not None and current_pad is not None and current_ring is not None:
                    voltage_list.append(voltage)
                    current_pad_list.append(current_pad)
                    current_ring_list.append(current_ring)
                    capacitance_list.append(capacitance)
                    conductance_list.append(conductance)

            except Exception as ex:
                print(f"Error at voltage {voltage}V (hysteresis): {ex}")

        source_pad.output("OFF")
        source_ring.output("OFF")

    return voltage_list, current_pad_list, current_ring_list, capacitance_list, conductance_list


def make_compensation(main, keysightE4990A, CV_IV_ring_external_parameters):
    """
    Make OPEN and SHORT compensation
    :param main: main program instance
    :param keysightE4990A: E4990A instrument instance
    :param CV_IV_ring_external_parameters: parameters dictionary
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
    if CV_IV_ring_external_parameters["COMPENSATION_OPEN"]:
        keysightE4990A.zero_open("ON")
    else:
        keysightE4990A.zero_open("OFF")
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
    if CV_IV_ring_external_parameters["COMPENSATION_SHORT"]:
        keysightE4990A.zero_short("ON")
    else:
        keysightE4990A.zero_short("OFF")
    time.sleep(1)
    return True


def make_full_compensation(main, keysightE4990A, CV_IV_ring_external_parameters):
    """
    Make full compensation if not already done
    :param main: main program instance
    :param keysightE4990A: E4990A instrument instance
    :param CV_IV_ring_external_parameters: parameters dictionary
    :return: None
    """
    if not CV_IV_ring_external_parameters["COMPENSATION_DONE"]:
        main.updateTextDescription("<br />Making compensation...<br />")
        if not make_compensation(main, keysightE4990A, CV_IV_ring_external_parameters):
            main.updateTextDescription("Compensation failed! Aborting test...<br />", "ERROR")
            test_status.status = "ABORTED"
        else:
            CV_IV_ring_external_parameters["COMPENSATION_DONE"] = True
            filename_config = os.getcwd() + base_dir + tests_dir + '/Keysight_E4990A/CV_IV_ring_external.toml'
            file_exists = os.path.exists(filename_config)
            if file_exists:
                toml_info = toml.load(filename_config)
                toml_info["parameters"] = CV_IV_ring_external_parameters
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
    load_CV_IV_ring_external_parameters()
    instr_name = CV_IV_ring_external_parameters.get("SOURCE_INSTRUMENT", "Keithley_2470")

    if instr_name == "Keithley_2410":
        source_pad = Keithley_2410(instruments["Keithley_2410"])
        source_pad.driver_name = "Keithley_2410"
        source_ring = Keithley_2410(instruments["Keithley_2410ring"])
        source_ring.driver_name = "Keithley_2410"
    else:
        source_pad = Keithley_2470(instruments["Keithley_2470"])
        source_pad.driver_name = "Keithley_2470"
        source_ring = Keithley_2470(instruments["Keithley_2470ring"])
        source_ring.driver_name = "Keithley_2470"

    keysightE4990A = Keysight_E4990A(instruments["Keysight_E4990A"])

    # Extract frequencies
    freqs = CV_IV_ring_external_parameters["FREQ"].replace(" ", "").split(",")
    freqs = [float(f) for f in freqs if f]

    if cartographic_measurement:
        if str(dieActual) == "1" and str(moduleActual) == "1":
            retval = message_user(
                main,
                "Init instruments for CV_IV_ring_external (Keysight E4990A)!",
                "Please, configure instruments for initialization",
                "yes_cancel",
            )
            if retval == QMessageBox.Yes:
                test_status.status = "STARTED"
                make_full_compensation(main, keysightE4990A, CV_IV_ring_external_parameters)
            else:
                test_status.status = "ABORTED"

        if test_status.status == "STARTED":
            for freq in freqs:
                CV_IV_ring_external_parameters["FREQ"] = str(freq)

                if config_E4990A_for_spot_measurement(keysightE4990A, CV_IV_ring_external_parameters):
                    voltage, current_pad, current_ring, capacitance, conductance = measure_CV_IV_ring_external(
                        main, source_pad, source_ring, keysightE4990A, CV_IV_ring_external_parameters
                    )

                    if len(voltage) > 0:
                        meas_status = "meas_success"
                        meas_message = f"Measured {len(voltage)} points"
                    else:
                        meas_status = "meas_error"
                        meas_message = "No measurements obtained"

                    # Numpy and save
                    voltage = np.array(voltage)
                    current_pad = np.array(current_pad)
                    current_ring = np.array(current_ring)
                    capacitance = np.array(capacitance)
                    conductance = np.array(conductance)

                    plot_config = CV_IV_ring_external_parameters.get("plot", {}).copy()
                    plot_config["NAME"] = f"Plot CV_IV_ring_external Keysight E4990A {freq}kHz (Die {dieActual} Module {moduleActual})"
                    plot_config["TITLE"] = f"CV_IV_ring_external Keysight E4990A {freq}kHz (Die {dieActual} Module {moduleActual})"

                    results_data_dict = {"V": voltage.tolist(), "C": (capacitance * 1e12).tolist(), "G": (conductance * 1e9).tolist()}
                    plot_parameters = get_plot_parameters(results_data_dict, ["V", "C", "G"], plot_config)

                    main.waferwindow.meas_result[int(dieActual) - 1][int(moduleActual) - 1] = {
                        "status": meas_status,
                        "message": meas_message,
                        "contact_height": "",
                        "variables": {
                            "params": [],
                            "data": [
                                {"name": "V", "values": voltage.tolist(), "units": "V"},
                                {"name": "I_pad", "values": current_pad.tolist(), "units": "A"},
                                {"name": "I_ring", "values": current_ring.tolist(), "units": "A"},
                                {"name": "C", "values": (capacitance * 1e12).tolist(), "units": "pF"},
                                {"name": "G", "values": (conductance * 1e9).tolist(), "units": "nS"},
                            ],
                        },
                        "plot_parameters": plot_parameters,
                    }

                    if plot_config.get("SHOW_PLOT", True):
                        emit_plot(plot_parameters)

                    results_data = list(zip(voltage, current_pad, current_ring, capacitance, conductance))
                    variables_list = ["V", "I_pad", "I_ring", "C", "G"]
                    output_params = CV_IV_ring_external_parameters.get("output", {"separator": "comma", "prefix": f"CV_IV_ring_external_E4990A_{freq}kHz", "suffix": ""})
                    
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
                    meas_message = "Error configuring Keysight E4990A"

    else:
        # Single mode
        make_full_compensation(main, keysightE4990A, CV_IV_ring_external_parameters)

        for freq in freqs:
            CV_IV_ring_external_parameters["FREQ"] = str(freq)

            if config_E4990A_for_spot_measurement(keysightE4990A, CV_IV_ring_external_parameters):
                voltage, current_pad, current_ring, capacitance, conductance = measure_CV_IV_ring_external(
                    main, source_pad, source_ring, keysightE4990A, CV_IV_ring_external_parameters
                )

                if len(voltage) > 0:
                    voltage = np.array(voltage)
                    current_pad = np.array(current_pad)
                    current_ring = np.array(current_ring)
                    capacitance = np.array(capacitance)
                    conductance = np.array(conductance)

                    plot_config = CV_IV_ring_external_parameters.get("plot", {}).copy()
                    plot_config["TITLE"] = f"CV_IV_ring_external Keysight E4990A Measurement at {freq}kHz"

                    results_data_dict = {"V": voltage.tolist(), "C": (capacitance * 1e12).tolist(), "G": (conductance * 1e9).tolist()}
                    plot_parameters = get_plot_parameters(results_data_dict, ["V", "C", "G"], plot_config)

                    if plot_config.get("SHOW_PLOT", True):
                        emit_plot(plot_parameters)

                    dieActual = 1
                    moduleActual = 1
                    
                    results_data = list(zip(voltage, current_pad, current_ring, capacitance, conductance))
                    variables_list = ["V", "I_pad", "I_ring", "C", "G"]
                    output_params = CV_IV_ring_external_parameters.get("output", {"separator": "comma", "prefix": f"CV_IV_ring_external_E4990A_{freq}kHz", "suffix": "single"})
                    
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

    # Stop and close
    source_pad.stop()
    source_pad.close()
    source_ring.stop()
    source_ring.close()
    keysightE4990A.stop()

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
