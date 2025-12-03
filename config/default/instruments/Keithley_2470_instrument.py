# KEITHLEY 2470 instrument driver
import pyvisa
import time
import numpy as np


class Keithley_2470:
    function_values = ["VOLT", "CURR", "RES"]
    terminal_values = ["SOUR", "SENSE"]
    output_values = ["ON", "OFF"]
    unit_values = ["OHM", "WATT", "VOLT", "AMP"]
    route_values = ["REAR", "FRONT"]
    lim_values = ["VLIM", "ILIM"]

    def __init__(self, parameters):
        """
		Init driver
		:param parameters:  configuration parameters
		:return None
		"""
        rm = pyvisa.ResourceManager()
        inst = rm.open_resource(parameters["address"])
        self.instrument = inst
        self.address = parameters["address"]
        self.read_termination(parameters["read_termination"])
        self.write_termination(parameters["write_termination"])

        self.bufferName = "defbuffer1"
        if "bufferName" in parameters:
            if parameters["bufferName"] in ["defbuffer1", "devbuffer2"]:
                self.bufferName = parameters["bufferName"]
            else:
                print("Buffer name not correct (defbuffer1 or devbuffer2), set to defbuffer1")
                self.bufferName = 'defbuffer1'
        if "timeout" in parameters:
            self.timeout(int(parameters["timeout"]))
        # The delay between measurement points; default is 0 for no delay or you can set a
        # specific delay value from 50 µs to 10,000 s
        self.delay = 0
        if "delay" in parameters:
            if 50E-6 <= float(parameters["delay"]) <= 10000:
                self.delay = float(parameters["delay"])
            else:
                print("Delay not correct (50 us to 10000 s), set to 0")
                self.delay = 0
        # The number of times to run the sweep; default is 1:
        # Infinite loop: 0, Finite loop: 1 to 268435455
        self.count = 1
        if "count" in parameters:
            if 0 <= int(parameters["count"]) <= 268435455:
                self.count = int(parameters["count"])
            else:
                print("Count not correct (0 to 268435455), set to 1")
                self.count = 1
        self.rangeType = "BEST"
        if "rangeType" in parameters:
            if parameters["rangeType"] in ["AUTO", "BEST", "FIXed"]:
                self.rangeType = parameters["rangeType"]
            else:
                print("Range type not correct (AUTO, BEST or FIXed), set to BEST")
                self.rangeType = "BEST"
        # Fail abort: ON or OFF
        self.failAbort = "OFF"
        if "failAbort" in parameters:
            if parameters["failAbort"] in ["ON", "OFF"]:
                self.failAbort = parameters["failAbort"]
            else:
                print("Fail abort not correct (ON or OFF), set to OFF")
                self.failAbort = "OFF"
        # Dual parameter
        self.dual = "OFF"
        if "dual" in parameters:
            if parameters["dual"] in ["ON", "OFF"]:
                self.dual = parameters["dual"]
            else:
                print("Dual parameter not correct (ON or OFF), set to OFF")
                self.dual = "OFF"
        self.parameters = parameters

    def reset(self):
        """
		Reset function
		:return: None
		"""

        self.instrument.write('*RST')

    def read_termination(self, read_termination):
        """
		Read termination function
		:param read_termination: termination on read
		:return:
		"""

        self.instrument.read_termination = read_termination

    def write_termination(self, write_termination):
        """
		Write termination function
		:param write_termination: termination on write
		:return: none
		"""
        self.instrument.write_termination = write_termination

    def timeout(self, timeout):
        """
		Set timeout
		:param timeout: time in ms
		:return: None
		"""
        self.instrument.timeout = timeout

    def idn(self):
        """
		Send IDN function
		:return: IDN information
		"""
        return self.instrument.query('*IDN?')

    def srq(self):
        """
		SRQ function
		:return: None
		"""
        return self.instrument.query('*STB?')

    def wait(self):
        """
		Wait function
		:return: None
		"""
        self.instrument.write('*WAI')

    def output(self, state):
        """
		Put OUTPUT ON or OFF
		:return: None
		"""
        if state == 1:
            state = "ON"
        if state == 0:
            state = "OFF"
        if state.lower() == "on" or state.lower() == "off":
            cmd = ":OUTP " + state.upper()
            self.instrument.write(cmd)
        else:
            raise ValueError("OUTPUT state not possible (ON or OFF)")

    def set_compliance(self, lim, value):
        """
		Set compliance
		:param function: VOLT or CURR
		:param value: value of compliance
		:return:
		"""
        if lim in self.lim_values:
            function = "VOLT" if lim == "ILIM" else "CURR"
            self.instrument.write(f":SOUR:{function}:{lim} {str(value)}")
        else:
            raise ValueError("Function not possible (VOLT or CURR)")

    def set_lin_sweep(self, function, start, stop, points):
        """
		Make a linear sweep
		Before setting up the sweep, set up the instrument for the test you will run.
		Typical settings you can set for a sweep include:
        • Source function
        • Measure function
        • Current or voltage limit
        • Source readback
        • Voltage protection limits
        • 2-wire or 4-wire sense mode
        • Front or rear terminal selection
		:param function: VOLT or CURR
		:param start: start value Current: -1.05 A to 1.05 A, Voltage: -1100 V to 1100 V
		:param stop: end value Current: -1.05 A to 1.05 A, Voltage: -1100 V to 1100 V
		:param points: The number of source-measure points between the start and stop values. Points = [(Stop - Start) / Step] + 1
		:return: data
		"""
        if function in self.function_values:
            # Set up a linear sweep from 0 V to 5 V in 51 steps
            cmd = f':SOUR:SWE:{function}:LIN {start}, {stop}, {points}, {self.delay}, {self.count}, {self.rangeType}, {self.failAbort}, {self.dual}, "{self.bufferName}"'
            self.instrument.write(cmd)
        else:
            raise ValueError("Function not possible (VOLT or CURR)")

    def set_list_sweep(self, function, startIndex):
        if function in self.function_values:
            cmd = f":SOUR:SWE:{function}:LIST {startIndex}, {self.delay}, {self.count}, {self.failAbort}"
            self.instrument.write(cmd)
        else:
            raise ValueError("Value error: Function not correct!")

    def source_delay(self, function, delay):
        # This command contains the source delay.
        # The delay in seconds (0 to 10 ks)
        # If you send this command without the <function> parameter, it sets the delay for all functions.
        if function in self.function_values or function == "":
            if not (0 <= delay <= 10000):
                raise ValueError("Value error: Delay not correct (0 to 10000 s)!")
            if function == "":
                # send
                self.instrument.write(f":SOUR:DEL {delay}")
            else:
                self.instrument.write(f":SOUR:{function}:DEL {delay}")
        else:
            raise ValueError("Value error: Function not correct!")

    def sense_count(self, count):
        # This command sets the number of measurements to make when a measurement is requested
        # count: The number of measurements (1 to 300,000 or buffer capacity)
        self.instrument.write(f":COUN {count}")

    def set_list(self, function, lista):
        if function in self.function_values:
            lista_values = ", ".join(str(valor) for valor in lista)
            cmd = f":SOUR:LIST:{function} {lista_values}"
            self.instrument.write(cmd)
        else:
            raise ValueError("Value error: Function not correct!")

    def set_mode_2wire(self):
        self.instrument.write(":SENS:CURR:RSEN OFF")

    def set_mode_4wire(self):
        self.instrument.write(":SENS:CURR:RSEN ON")

    def start(self):
        cmd = "INIT"
        self.instrument.write(cmd)
        cmd = "*WAI"
        self.instrument.write(cmd)
        time.sleep(0.5)


    def stop(self):
        """
		Stop de measurement
		:return: None
		"""
        self.output("OFF")

    def dataready(self):
        """
		Check data ready
		:return: None
		"""
        opc = self.instrument.query("*OPC?")
        while not int(opc) & 1:
            opc = self.instrument.query("*OPC?")
            time.sleep(0.1)

    def integration_time(self, time_us):
        """
		Change integration time
		:param type: Type integration time
		:return: None
		"""
        cmd = ":SENS:CURR:APER " + time_us
        self.instrument.write(cmd)

    def clear_buffer(self):
        """
		Clear instrument buffer
		:return: None
		"""
        self.instrument.write(":TRAC:CLE")

    def config_buffer(self, steps):
        """
		Configure buffer with steps number
		:param steps: number of steps
		:return: None
		"""
        self.instrument.write(":TRAC:FEED:CONT NEXT")
        self.instrument.write(":TRAC:POIN {0}".format(steps))

    def read_buffer(self, startIndex, endIndex, bufferElements="READ"):
        """
		Read buffer
		:param startIndex startIndex
		:param endIndex endIndex
		:return: data
		"""
        cmd = f":TRAC:DATA? {startIndex}, {endIndex}, \"{self.buffer_name}\", {bufferElements}"
        data = self.instrument.query(cmd)
        return data.split(",")

    def get_buffer_end(self):
        """
        Read buffer end
        :param bufferName name of the buffer
        :return end
        """
        cmd = f":TRAC:ACT:END?"
        data = self.instrument.query(cmd)

        return data

    def set_measurement_unit(self, function, unit):
        if function in self.function_values:
            if unit in self.unit_values:
                self.instrument.write(f':SENS:{function}:UNIT {unit}')
            else:
                raise ValueError("Value error: Unit not correct (OHM,WATT, AMP or VOLT)")
        else:
            raise ValueError("Value error: Function not correct!")

    def set_function(self, terminal, function):
        if terminal in self.terminal_values:
            if function in self.function_values:
                cmd = ":" + terminal + ":FUNC " + function
                self.instrument.write(cmd)
            else:
                raise ValueError("Value error: Function not correct!")
        else:
            raise ValueError("Value error: Route terminal not correct!")

    def set_range(self, terminal, function, value="ON"):
        if terminal in self.terminal_values:
            if function in self.function_values:
                if value in ["ON", "OFF"]:
                    cmd = ":" + terminal + ":" + function + ":RANG:AUTO " + value
                else:
                    # number
                    cmd = ":" + terminal + ":" + function + ":RANG " + str(value)
                self.instrument.write(cmd)
            else:
                raise ValueError("Value error: Function not correct!")
        else:
            raise ValueError("Value error: Route terminal not correct!")

    def config_IV(self, IV_parameters, sens4wire=False):
        # Stop = IV_parameters["STOP"]
        # Start = IV_parameters["START"]
        # Step = IV_parameters["STEP"]
        # Points = [(Stop - Start) / Step] + 1
        if sens4wire:
            self.set_mode_4wire()
        else:
            self.set_mode_2wire()
        self.set_measurement_unit("CURR", "AMP")
        self.set_route_term(IV_parameters["ROUTE_TERM"])
        # compliance value in mA or mV
        self.set_compliance("ILIM", float(IV_parameters["COMPLIANCE"]) * 1E-3)
        if IV_parameters["RANGE"] == "AUTO":
            self.set_range("SOUR", "VOLT", "ON")
        else:
            self.set_range("SOUR", "VOLT", IV_parameters["RANGE"])

        if IV_parameters["COUNT"]:
            self.sense_count(IV_parameters["COUNT"])
        if IV_parameters["SOURCE_DELAY"]:
            self.source_delay("", IV_parameters["SOURCE_DELAY"])

        return True

    def config_IV4(self, IV_parameters):
        self.set_measurement_unit("CURR", "OHM")
        self.set_mode_4wire()
        self.set_route_term(IV_parameters["ROUTE_TERM"])
        # compliance value in mA or mV
        self.set_compliance("ILIM", float(IV_parameters["COMPLIANCE"]) * 1E-3)
        if IV_parameters["RANGE"] == "AUTO":
            self.set_range("SOUR", "VOLT", "ON")
        else:
            self.set_range("SOUR", "VOLT", IV_parameters["RANGE"])
        return True

    def config_IV_temp(self, IV_parameters):
        if IV_parameters["FOUR_TERMINAL"]:
            self.set_mode_4wire()
        else:
            self.set_mode_2wire()
        self.set_route_term(IV_parameters["ROUTE_TERM"])
        if IV_parameters["MEAS_SOURCE"] == "VOLT":
            if IV_parameters["VOLT_RANGE"] == "AUTO":
                self.set_range("SOUR", IV_parameters["MEAS_SOURCE"], "ON")
            else:
                self.set_range("SOUR", IV_parameters["MEAS_SOURCE"], IV_parameters["VOLT_RANGE"])
            self.set_compliance("ILIM", float(IV_parameters["COMPLIANCE"]) * 1E-3)
        if IV_parameters["MEAS_SOURCE"] == "CURR":
            if IV_parameters["CURR_RANGE"] == "AUTO":
                self.set_range("SOUR", IV_parameters["MEAS_SOURCE"], "ON")
            else:
                self.set_range("SOUR", IV_parameters["MEAS_SOURCE"], IV_parameters["CURR_RANGE"])
            self.set_compliance("VLIM", float(IV_parameters["COMPLIANCE"]) * 1E-3)

        return True

    def set_voltage(self, voltage):
        cmd = f":SOUR:VOLT {voltage}"
        self.instrument.write(cmd)

    def get_error_count(self):
        return self.instrument.query(":SYST:ERR:COUN?")

    def get_error(self):
        """
        Get error
        """
        return self.instrument.query(":SYST:ERR:NEXT?")

    def clear(self):
        """
        This command removes all events from the event log, including entries in the front-panel event log
        """
        self.instrument.write(":SYST:CLE")

    def beep(self, frequency=500, duration=1):
        if (20 <= frequency <= 8000) and (0.01 <= duration <= 100):
            cmd = ":SYST:BEEP " + str(frequency) + ", " + str(duration)
            self.instrument.write(cmd)
        else:
            raise ValueError("Value error: Frequency or duration not correct!")

    def set_route_term(self, route):
        if route in self.route_values:
            self.instrument.write(":ROUTE:TERM " + route)
        else:
            raise ValueError("Value error: Route value not correct (REAR or FRONT)!")

    def measure_list_IV(self, IV_parameters):
        """
        Measure IV list mode
        :param IV_parameters:☺
        :return:  current, voltage list
        """
        self.clear_buffer()
        source = self.get_source_list(IV_parameters)
        self.set_list(IV_parameters["MEAS_SOURCE"], source)  # Not used?
        self.set_list_sweep(IV_parameters["MEAS_SOURCE"], 1)
        self.start()
        lastIndex_buffer = self.get_buffer_end()
        sense = self.read_buffer(1, lastIndex_buffer)
        source = source[0:len(sense)]
        self.reset()
        return source, sense

    def measure_temp(self, IV_parameters):
        """
        Measure temp
        :param IV_parameters:
        :return:  current, voltage list
        """
        self.clear_buffer()
        if IV_parameters["MEAS_SWEEP"]:
            print("measurement sweep")
            source = self.get_source_list(IV_parameters)
            print(source)
            self.set_list(IV_parameters["MEAS_SOURCE"], source)
            self.set_list_sweep(IV_parameters["MEAS_SOURCE"], 1)
            self.start()

            lastIndex_buffer = self.get_buffer_end()
            sens = self.read_buffer(1, lastIndex_buffer)
            source = source[0:(int(lastIndex_buffer))]
        else:
            print("spot measurement")
            # spot measurements
            Start = IV_parameters["START"]
            Meas_source = IV_parameters["MEAS_SOURCE"]
            source = []
            sens = []
            for i in range(0,10):
                source.append(Start)
            print(f"Source: {source}")
            print(f"set volt/curr spot to {Start}")
            cmd = f":SOURC:{Meas_source} {Start}"
            self.instrument.write(cmd)
            time.sleep(3)
            print("Count")
            cmd = f":COUN 10"
            # self.instrument.write(cmd)
            print("Start measurement")
            self.output("ON")
            time.sleep(3)
            # get measurements
            lastIndex_buffer = self.get_buffer_end()

            if int(lastIndex_buffer) >= 1:
                sens = self.read_buffer(1, lastIndex_buffer)
                source = source[0:(int(lastIndex_buffer))]
            self.output("OFF")
        print(f"last index buffer: {lastIndex_buffer}")
        self.reset()
        print(source, sens)
        return source, sens

    def get_source_list(self, IV_parameters):
        Stop = IV_parameters["STOP"]
        Start = IV_parameters["START"]
        Step = IV_parameters["STEP"]
        # Points = (Stop - Start) / Step
        source_values = np.arange(Start, Stop + Step, Step)
        source_values = np.round(source_values, decimals=6)

        return source_values.tolist()

    def close(self):
        """
		Close instrument
		@return: None
		"""
        self.instrument.close()
