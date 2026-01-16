import pyvisa
import time


class Keithley_2410:
    """
    Driver Keithley 2410
    API compatible con el uso actual del Keithley 2470
    (IV ring test, IV sweep punto a punto)
    """

    def __init__(self, parameters):
        rm = pyvisa.ResourceManager()
        self.instrument = rm.open_resource(parameters["address"])

        self.instrument.read_termination = parameters.get("read_termination", "\n")
        self.instrument.write_termination = parameters.get("write_termination", "\n")
        self.instrument.timeout = int(parameters.get("timeout", 5000))

        self.source_delay = parameters.get("source_delay", 0.0)

        self.reset()
        self._basic_config()

    # --------------------------------------------------
    # Basic instrument control
    # --------------------------------------------------

    def reset(self):
        self.instrument.write("*RST")
        time.sleep(0.5)

    def idn(self):
        return self.instrument.query("*IDN?")

    def output(self, state):
        if state in ["ON", 1, True]:
            self.instrument.write(":OUTP ON")
        elif state in ["OFF", 0, False]:
            self.instrument.write(":OUTP OFF")
        else:
            raise ValueError("OUTPUT must be ON or OFF")

    # --------------------------------------------------
    # Configuration
    # --------------------------------------------------

    def _basic_config(self):
        """
        Configuración estándar para IV
        """
        # Source Voltage, Measure Current
        self.instrument.write(":SOUR:FUNC VOLT")
        self.instrument.write(":SENS:FUNC 'CURR'")

        # Autorange ON
        self.instrument.write(":SOUR:VOLT:RANG:AUTO ON")
        self.instrument.write(":SENS:CURR:RANG:AUTO ON")

        # 2-wire by default
        self.set_mode_2wire()

        # Formato de lectura: solo valores
        self.instrument.write(":FORM:ELEM CURR")

    def set_mode_4wire(self):
        self.instrument.write(":SYST:RSEN ON")

    def set_mode_2wire(self):
        self.instrument.write(":SYST:RSEN OFF")

    # --------------------------------------------------
    # Compliance
    # --------------------------------------------------

    def set_compliance_current(self, value):
        """
        Compliance de corriente (cuando se fuentea voltaje)
        """
        self.instrument.write(f":SENS:CURR:PROT {value}")

    def set_compliance_voltage(self, value):
        """
        Compliance de voltaje (cuando se fuentea corriente)
        """
        self.instrument.write(f":SENS:VOLT:PROT {value}")

    # --------------------------------------------------
    # Source functions
    # --------------------------------------------------

    def set_voltage(self, value):
        self.instrument.write(f":SOUR:VOLT {value}")
        if self.source_delay > 0:
            time.sleep(self.source_delay)

    def set_current(self, value):
        self.instrument.write(":SOUR:FUNC CURR")
        self.instrument.write(f":SOUR:CURR {value}")
        if self.source_delay > 0:
            time.sleep(self.source_delay)

    # --------------------------------------------------
    # Measurement
    # --------------------------------------------------

    def measure_current_once(self):
        """
        Devuelve corriente en amperios (float)
        """
        value = self.instrument.query(":MEAS:CURR?")
        return float(value.strip().split(",")[0])

    def measure_voltage_once(self):
        """
        Devuelve voltaje en voltios (float)
        """
        value = self.instrument.query(":MEAS:VOLT?")
        return float(value.strip().split(",")[0])

    # --------------------------------------------------
    # Cleanup
    # --------------------------------------------------

    def close(self):
        try:
            self.output("OFF")
        except Exception:
            pass
        self.instrument.close()
