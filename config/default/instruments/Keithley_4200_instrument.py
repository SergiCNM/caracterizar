# Keithley 4200 instrument driver
import pyvisa
from pyvisa.constants import EventType, EventMechanism
from pyvisa.errors import VisaIOError


import time
import numpy as np

class Keithley_4200:
	SMU_SOURCE_FUNCTION = {
		'VAR1': 1,
		'VAR2': 2,
		'CONST': 3,
		"VAR1'": 4,
	}
	SMU_SOURCE_TYPE = {
		'VOLTAGE': 1,
		'CURRENT': 2,
		'COMMON': 3
	}
	CHANNEL_NUMBERS = [1, 2, 3, 4]

	cvu_model = '4210'  # Default model, can be changed if needed

	def __init__(self,parameters):
		print(f"Parameters: {parameters}")
		rm = pyvisa.ResourceManager()
		inst = rm.open_resource(parameters["address"])
		self.instrument = inst
		self.address = parameters["address"]
		self.read_termination(parameters["read_termination"])
		self.write_termination(parameters["write_termination"])
		if "timeout" in parameters:
			self.timeout(int(parameters["timeout"]))
		if "term_chars" in parameters:
			self.termination_chars(int(parameters["term_chars"]))

	def reset(self):
		self.instrument.write('*RST')

	def read_termination(self,read_termination):
		self.instrument.read_termination = read_termination

	def write_termination(self,write_termination):
		self.instrument.write_termination = write_termination

	def timeout(self,timeout):
		self.instrument.timeout = timeout

	def termination_chars(self,term_chars):
		self.instrument.term_chars = term_chars

	def idn(self):
		return self.instrument.query('*IDN?')


	def wait(self):
		self.instrument.write('*WAI')

	def srq(self):
		self.instrument.write('SR1')

	# Selects the channel definition page
	def select_channel_page(self):
		self.instrument.write('DE')

	# select the source setup page
	def select_setup_page(self):
		self.instrument.write('SS')

	# select the measurement setup page
	def select_measurement_page(self):
		self.instrument.write('SM')

	# select the measurement control page
	def select_measurement_control_page(self):
		self.instrument.write('MD')

	# select the display mode
	def select_display_mode(self, mode):
		# 		Display modes:
		# ▪ Graphics display mode: 1
		# ▪ List display mode: 2
		# Example: "DM1" to select display mode 1
		# Valid modes: 1 to 2
		if mode not in [1, 2]:
			raise ValueError(f"Invalid display mode: {mode}. Valid modes are 1 to 4.")
		cmd = f'DM{mode}'
		self.instrument.write(cmd)

	# set delay time for measurements
	def set_delay(self, delay):
		# Delay time in seconds: 0 to  6.553
		# Example: "DELAY 0.1" for 100 ms
		if not (0 <= delay <=  6.553):
			raise ValueError("Delay must be between 0 and 6553 seconds.")
		cmd = f'DT {delay}'
		self.instrument.write(cmd)

	# set hold time for measurements
	def set_hold_time(self, hold_time):
		# Hold time in seconds: 0 to  655.3
		# Example: "HOLD 0.1" for 100 ms
		if not (0 <= hold_time <=  655.3):
			raise ValueError("Hold time must be between 0 and 6553 seconds.")
		cmd = f'HT {hold_time}'
		self.instrument.write(cmd)

	# sets the time between sample measurements.
	def set_sample_time(self, sample_time):
		# 		IN AA.AA
		# AA.AA Interval in seconds: 0.01 to 10
		# Example: "IN 0.1" for 100 ms
		# Details:
		# For time domain measurements, you can set the time between sample measurements. After
		# a sample measurement is made, the next measurement starts after the time interval expires.
		# For constant bias measurements, this is the time between readings.
		if not (0.01 <= sample_time <= 10):
			raise ValueError("Sample time must be between 0.01 and 10 seconds.")
		cmd = f'IN {sample_time}'
		self.instrument.write(cmd)

	# configure SMU channel
	def config_channel(self, channel_number, var_voltage_name, var_current_name, source_type, source_function):
		# Example: "CH1, 'VS', 'IS', 1, 3"+term  # configure channel 1 with voltage source 'VS', current source 'IS', source type VOLT (1) and function SWEEP (3)
		var_voltage_name = f"'{var_voltage_name}'"
		var_current_name = f"'{var_current_name}'"
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		if source_type not in self.SMU_SOURCE_TYPE:
			raise ValueError(f"Invalid source type: {source_type}. Valid types are {list(self.SMU_SOURCE_TYPE.keys())}.")
		if source_function not in self.SMU_SOURCE_FUNCTION:
			raise ValueError(f"Invalid source function: {source_function}. Valid functions are {list(self.SMU_SOURCE_FUNCTION.keys())}.")
		if source_type == 'COMMON' and source_function != 'CONST':
			raise ValueError("Source type 'COMMON' can only be used with source function 'CONST'.")
		cmd = f'"CH{channel_number}, {var_voltage_name}, {var_current_name}, {source_function}, {source_type}"'
		self.instrument.write(cmd)

	def config_channel_off(self, channel_number):
		# Example: "CH1 OFF" to turn off channel 1
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		cmd = f'CH{channel_number}'
		self.instrument.write(cmd)

	def config_channel_voltimeter(self, channel_number, channel_voltage_name):
		# Example: "VM1, 'VM1'" to configure channel 1 as voltimeter with variable name 'VM1'
		channel_voltage_name = f"'{channel_voltage_name}'"
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		cmd = f'VM{channel_number}, {channel_voltage_name}'
		self.instrument.write(cmd)

	def config_channel_voltage_source(self, channel_number, channel_voltage_name, source_function='VAR1'):
		# Example: "VS1, 'VS1' 1" to configure channel 1 as voltage source with variable name 'VS1' and source function 'VAR1'
		channel_voltage_name = f"'{channel_voltage_name}'"
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		if source_function not in self.SMU_SOURCE_FUNCTION:
			raise ValueError(f"Invalid source function: {source_function}. Valid functions are {list(self.SMU_SOURCE_FUNCTION.keys())}.")
		cmd = f'VS{channel_number}, {channel_voltage_name}, {self.SMU_SOURCE_FUNCTION[source_function]}'
		self.instrument.write(cmd)

	# set offset value or VAR1'
	def set_offset(self, channel_number, offset_value):
		# Example: "FS 0.1, 1" to set offset for channel 1 to 0.1 V
		# Offset value: -210 to +210
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		if not (-210 <= offset_value <= 210):
			raise ValueError("Offset value must be between -210 and +210.")
		sign = "+"
		if offset_value < 0:
			sign = "-"
		offset_value = abs(offset_value)  # Ensure offset is positive for command
		cmd = f'FS {sign}{offset_value},{channel_number}'
		self.instrument.write(cmd)

	# set ratio value for VAR1'
	def set_ratio(self, channel_number, ratio_value):
		# Example: "FR 0.1, 1" to set ratio for channel 1 to 0.1
		# Ratio value: -10 to +10
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		if not (-10 <= ratio_value <= 10):
			raise ValueError("Ratio value must be between -10 and +10.")
		sign = "+"
		if ratio_value < 0:
			sign = "-"
		ratio_value = abs(ratio_value)  # Ensure ratio is positive for command
		cmd = f'RT {sign}{ratio_value},{channel_number}'
		self.instrument.write(cmd)

	# set source to output a fixed voltage level for channels that are configured to be voltage source only.
	def set_fixed_voltage(self, channel_number, voltage_value):
		# Example: "FS 0.1, 1" to set fixed voltage for channel 1 to 0.1 V
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		if not (-210 <= voltage_value <= 210):
			raise ValueError("Voltage value must be between -210 and +210.")
		sign = "+"
		if voltage_value < 0:
			sign = "-"
		voltage_value = abs(voltage_value)
		cmd = f'SC{channel_number}, {sign}{voltage_value}'
		self.instrument.write(cmd)

	# enables or disables automatic standby
	def set_auto_standby(self, channel_number, enable=True):
		# When automatic standby is enabled, the SMU automatically goes into standby when the test
		# completes. When disabled, the output stays on when the test completes
		# Example: "ST1 1" to enable auto standby
		if enable:
			self.instrument.write(f'ST{channel_number} 1')
		else:
			self.instrument.write(f'ST{channel_number} 0')

	# configure the SMU to output a fixed (constant) voltage or current level.
	def set_fixed_level(self, channel_number, level_value, compliance_value, mode='VC'):
		# AAB, ±CCC.CCCC, ±DDD.DDDD
		# AA Source mode:
		# ▪ Voltage: VC
		# ▪ Current: IC
		# B SMU channel number: 1 to 9
		# CCC.CCCC
		# Output value:
		# ▪ Voltage source: -210.00 to +210.00
		# ▪ Current source, 4200-SMU or 4201-SMU: -0.1050 to +0.1050
		# ▪ Current source, 4210-SMU or 4211-SMU: -1.0500 to +1.0500
		# DDD.DDDD
		# Compliance value:
		# ▪ Voltage source: -210.00 to +210.00
		# ▪ Current source, 4200-SMU or 4201-SMU: -0.1050 to +0.1050
		# ▪ Current source, 4210-SMU or 4211-SMU: -1.0500 to +1.0500
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")

		if mode not in ['VC', 'IC']:
			raise ValueError(f"Invalid mode: {mode}. Valid modes are 'VC' for voltage source and 'IC' for current source.")
		if mode == 'VC':
			if not (-210 <= level_value <= 210):
				raise ValueError("Voltage level must be between -210 and +210.")
			if not (-210 <= compliance_value <= 210):
				raise ValueError("Voltage compliance must be between -210 and +210.")
		elif mode == 'IC':
			if not (-0.1050 <= level_value <= 0.1050):
				raise ValueError("Current level must be between -0.1050 and +0.1050")
			if not (-0.1050 <= level_value <= 0.1050):
				raise ValueError("Current compliance must be between -1.0500 and +1.0500.")
		sign = "+"
		sign_compliance = "+"
		if level_value < 0:
			sign = "-"
		if compliance_value < 0:
			sign_compliance = "-"
		level_value = abs(level_value)
		compliance_value = abs(compliance_value)
		cmd = f'{mode}{channel_number}, {sign}{level_value}, {sign_compliance}{compliance_value}'
		self.instrument.write(cmd)

	#  set up a list sweep
	def set_list_sweep(self, channel_number, list_values, compliance_value, source_mode='VL', master_mode=False):
		# 		AAB, C, ±DDD.DDDD, ±EE.EEEE, ... ±EE.EEEE
		# AA The source mode:
		# ▪ Voltage source (SMU or VS1...VS9): VL
		# ▪ Current source (SMU only): IL
		# B Channel number: 1 to 9
		# C Master or subordinate mode:
		# ▪ Subordinate mode: 0
		# ▪ Master mode: 1
		# DDD.DDDD Compliance value:
		# ▪ Voltage source: -210.00 to +210.00
		# ▪ Current source, 4200-SMU or 4201-SMU: -0.1050 to +0.1050
		# ▪ Current source, 4210-SMU or 4211-SMU: -1.0500 to +1.0500
		# EE.EEEE List values:
		# ▪ Voltage source: -210.00 to +210.00
		# ▪ Current source, 4200-SMU or 4201-SMU: -0.1050 to +0.1050
		# ▪ Current source, 4210-SMU or 4211-SMU: -1.0500 to +1.0500
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		if source_mode not in ['VL', 'IL']:
			raise ValueError(f"Invalid source mode: {source_mode}. Valid modes are 'VL' for voltage source and 'IL' for current source.")
		if master_mode not in [True, False]:
			raise ValueError("Master mode must be a boolean value (True or False).")

		if source_mode == 'VL':
			if not (0 <= compliance_value <= 210):
				raise ValueError("Compliance value must be between 0 and 210.")
			if not all(-210 <= value <= 210 for value in list_values):
				raise ValueError("All list values must be between -210 and +210.")
		elif source_mode == 'IL':
			if not (-0.1050 <= compliance_value <= 0.1050):
				raise ValueError("Compliance value must be between -0.1050 and +0.1050.")
			if not all(-0.1050 <= value <= 0.1050 for value in list_values):
				raise ValueError("All list values must be between -0.1050 and +0.1050.")
		sign_list = ["+" if value >= 0 else "-" for value in list_values]
		list_values = [abs(value) for value in list_values]
		list_values_str = ', '.join([f"{sign}{value}" for sign, value in zip(sign_list, list_values)])
		sign_compliance = "+"
		if compliance_value < 0:
			sign_compliance = "-"
		compliance_value = abs(compliance_value)
		cmd = f'{source_mode}{channel_number}, {int(master_mode)}, {sign_compliance}{compliance_value}, {list_values_str}'
		self.instrument.write(cmd)

	# set up the VAR2 step sweep.
	def set_var2_step_sweep(self, source_mode, start_value, step_value, num_steps, compliance_value, var2_source_stepper_index=1):
		# 		AA ±BBB.BBBB, ±CCC.CCCC, DD, ±EEE.EEEE
		# AA ±BBB.BBBB, ±CCC.CCCC, DD, ±EEE.EEEE, FF
		# AA The source mode:
		# ▪ VP: Voltage source (SMU or VS1...VS8)
		# ▪ IP: Current source (SMU only)
		# BBB.BBBB Start value:
		# ▪ Voltage source: -210.00 to +210.00
		# ▪ Current source, 4200-SMU or 4201-SMU: -0.1050 to +0.1050
		# ▪ Current source, 4210-SMU or 4211-SMU: -1.0500 to +1.0500
		# CCC.CCCC Step value:
		# ▪ Voltage source: -210.00 to +210.00
		# ▪ Current source, 4200-SMU or 4201-SMU: -0.1050 to +0.1050
		# ▪ Current source, 4210-SMU or 4211-SMU: -1.0500 to +1.0500
		# DD Number of steps: 1 to 32
		# EEE.EEEE Compliance value (see Details):
		# ▪ Voltage source: -210.00 to +210.00
		# ▪ Current source, 4200-SMU or 4201-SMU: -0.1050 to +0.1050
		# ▪ Current source, 4210-SMU or 4211-SMU: -1.0500 to +1.0500
		# FF VAR2 source stepper index: 1 to 4 (see Details)

		# 		Example
		# VP 5, 5, 3, 0.01
		# This command string sets up a VAR2 voltage sweep with start = 5 V, step = 5 V, number of steps = 3, and
		# compliance = 10 mA. This command string performs the steps shown in the figure in the Details. These
		# are the same steps that are shown synchronized with sweeps in VR and IR: VAR1 setup (on page 5-19).
		if var2_source_stepper_index not in [1, 2, 3, 4]:
			raise ValueError(f"Invalid VAR2 source stepper index: {var2_source_stepper_index}. Valid indices are 1 to 4.")
		if source_mode not in ['VP', 'IP']:
			raise ValueError(f"Invalid source mode: {source_mode}. Valid modes are 'VP' for voltage source and 'IP' for current source.")
		if source_mode == 'VP':
			if not (-210 <= start_value <= 210):
				raise ValueError("Start value must be between -210 and +210.")
			if not (-210 <= step_value <= 210):
				raise ValueError("Step value must be between -210 and +210.")
			if not (-210 <= compliance_value <= 210):
				raise ValueError("Compliance value must be between -210 and +210.")
		elif source_mode == 'IP':
			if not (-0.1050 <= start_value <= 0.1050):
				raise ValueError("Start value must be between -0.1050 and +0.1050.")
			if not (-0.1050 <= step_value <= 0.1050):
				raise ValueError("Step value must be between -0.1050 and +0.1050.")
			if not (-0.1050 <= compliance_value <= 0.1050):
				raise ValueError("Compliance value must be between -0.1050 and +0.1050.")
		if not (1 <= num_steps <= 32):
			raise ValueError("Number of steps must be between 1 and 32.")
		sign_start = "+" if start_value >= 0 else "-"
		sign_step = "+" if step_value >= 0 else "-"
		sign_compliance = "+" if compliance_value >= 0 else "-"
		start_value = abs(start_value)
		step_value = abs(step_value)
		compliance_value = abs(compliance_value)
		cmd = f'{source_mode} {sign_start}{start_value}, {sign_step}{step_value}, {num_steps}, {sign_compliance}{compliance_value}, {var2_source_stepper_index}'
		self.instrument.write(cmd)

	# set up the VAR1 source function
	def set_var1_source_function(self, source_mode, sweep_type, start_value, stop_value, step_value=None, compliance_value=None):
		# 		AAB, ±CCC.CCCC, ±DDD.DDDD, ±EEE.EEEE, ±FFF.FFFF
		# AA The source mode:
		# ▪ VR: Voltage source (SMU or VS1...VS9)
		# ▪ IR: Current source (SMU only)
		# B The sweep type:
		# ▪ 1: Linear sweep
		# ▪ 2: Log10 sweep
		# ▪ 3: Log25 sweep
		# ▪ 4: Log50 sweep
		# CCC.CCCC Start value:
		# ▪ Voltage source: -210.00 to +210.00
		# ▪ Current source, 4200-SMU or 4201-SMU: -0.1050 to +0.1050
		# ▪ Current source, 4210-SMU or 4211-SMU: -1.0500 to +1.0500
		# DDD.DDDD Stop value:
		# ▪ Voltage source: -210.00 to +210.00
		# ▪ Current source, 4200-SMU or 4201-SMU: -0.1050 to +0.1050
		# ▪ Current source, 4210-SMU or 4211-SMU: -1.0500 to +1.0500
		# EEE.EEEE Step value (linear sweep only):
		# ▪ Voltage source: -210.00 to +210.00
		# ▪ Current source, 4200-SMU or 4201-SMU: -0.1050 to +0.1050
		# ▪ Current source, 4210-SMU or 4211-SMU: -1.0500 to +1.0500
		# For a log sweep, do not set a step value (steps are determined by the setting for B)
		# FFF.FFFF Compliance value (also see Details):
		# ▪ Voltage source: -210.00 to +210.00
		# ▪ Current source, 4200-SMU or 4201-SMU: -0.1050 to +0.1050
		# ▪ Current source, 4210-SMU or 4211-SMU: -1.0500 to +1.0500
		# For a log sweep, do not set a compliance value

		# 		When setting the step value, be aware that the maximum number of points for VAR1
		# is 1024:
		# Number of points = (int)(Abs((Stop Value - Start Value) / Step Value) + 1.5)
		if source_mode not in ['VR', 'IR']:
			raise ValueError(f"Invalid source mode: {source_mode}. Valid modes are 'VR' for voltage source and 'IR' for current source.")
		if sweep_type not in [1, 2, 3, 4]:
			raise ValueError(f"Invalid sweep type: {sweep_type}. Valid types are 1 for linear, 2 for log10, 3 for log25, and 4 for log50.")
		if source_mode == 'VR':
			if not (-210 <= start_value <= 210):
				raise ValueError("Start value must be between -210 and +210.")
			if not (-210 <= stop_value <= 210):
				raise ValueError("Stop value must be between -210 and +210.")
			if sweep_type == 1:
				if not (-210 <= step_value <= 210):
					raise ValueError("Step value must be between -210 and +210 for linear sweep.")
				if compliance_value is not None and not (-210 <= compliance_value <= 210):
					raise ValueError("Compliance value must be between -210 and +210 for voltage source.")
			elif sweep_type in [2, 3, 4]:
				if step_value is not None:
					raise ValueError("Step value must be None for log sweeps.")
				if compliance_value is not None:
					raise ValueError("Compliance value must be None for log sweeps.")
		elif source_mode == 'IR':
			if not (-0.1050 <= start_value <= 0.1050):
				raise ValueError("Start value must be between -0.1050 and +0.1050.")
			if not (-0.1050 <= stop_value <= 0.1050):
				raise ValueError("Stop value must be between -0.1050 and +0.1050.")
			if sweep_type == 1:
				if not (-0.1050 <= step_value <= 0.1050):
					raise ValueError("Step value must be between -0.1050 and +0.1050 for linear sweep.")
				if compliance_value is not None and not (-1.0500 <= compliance_value <= 1.0500):
					raise ValueError("Compliance value must be between -1.0500 and +1.0500 for current source.")
			elif sweep_type in [2, 3, 4]:
				if step_value is not None:
					raise ValueError("Step value must be None for log sweeps.")
				if compliance_value is not None:
					raise ValueError("Compliance value must be None for log sweeps.")


		num_points = int(abs((stop_value - start_value) / step_value) + 1.5) if sweep_type == 1 else None
		if num_points is not None and num_points > 1024:
			raise ValueError("Number of points exceeds maximum limit of 1024 for VAR1 sweeps.")

		sign_start = "+" if start_value >= 0 else "-"
		sign_stop = "+" if stop_value >= 0 else "-"
		start_value = abs(start_value)
		stop_value = abs(stop_value)
		if sweep_type == 1:
			sign_step = "+" if step_value >= 0 else "-"
			step_value = abs(step_value)
			if compliance_value is not None:
				sign_compliance = "+" if compliance_value >= 0 else "-"
				compliance_value = abs(compliance_value)
				cmd = f'{source_mode} {sweep_type}, {sign_start}{start_value}, {sign_stop}{stop_value}, {sign_step}{step_value}, {sign_compliance}{compliance_value}'
			else:
				cmd = f'{source_mode} {sweep_type}, {sign_start}{start_value}, {sign_stop}{stop_value}, {sign_step}{step_value}'
		else:
			if compliance_value is not None:
				sign_compliance = "+" if compliance_value >= 0 else "-"
				compliance_value = abs(compliance_value)
				cmd = f'{source_mode} {sweep_type}, {sign_start}{start_value}, {sign_stop}{stop_value}, {sign_compliance}{compliance_value}'
			else:
				cmd = f'{source_mode} {sweep_type}, {sign_start}{start_value}, {sign_stop}{stop_value}'
		self.instrument.write(cmd)

	# enables voltage and current functions to be measured when the 4200A-SCS is in list
	# display mode.
	def enable_list_display_mode(self, channel_list=[]):
		# Example: "LI 'V1', 'I1', 'VS1'" # to enable list display mode for channel 1 with voltage variable 'V1', current variable 'I1', and voltage source 'VS1'
		if not channel_list:
			raise ValueError("Channel list cannot be empty. Provide at least one channel variable.")
		for channel in channel_list:
			if not isinstance(channel, str):
				raise ValueError(f"Invalid channel variable: {channel}. Channel variables must be strings.")
		cmd = 'LI ' + ', '.join([f"'{channel}'" for channel in channel_list])
		self.instrument.write(cmd)

	# sets the number of readings that can be made for time domain measurements
	def set_time_domain_readings(self, num_readings):
		# 		NR AAAA
		# AAAA Number of measurements to make:
		# ▪ 4200A command set: 1 to 4096
		# ▪ 4145 Emulation command set: 1 to 1024
		if not (1 <= num_readings <= 4096):
			raise ValueError("Number of readings must be between 1 and 4096.")
		cmd = f'NR {num_readings}'
		self.instrument.write(cmd)

	# delays the start of a test sequence for time domain measurements
	def set_time_domain_delay(self, delay):
		# 		WT AAA.AA
		# AAA.AA Wait time in seconds: 0 to 100
		if not (0 <= delay <= 100):
			raise ValueError("Wait time must be between 0 and 100 seconds.")
		cmd = f'WT {delay}'
		self.instrument.write(cmd)

	# configures the X-axis of the graph to plot an electrical parameter
	def config_graph_x_axis(self, channel_name, scale_type, min_value, max_value):
		# 		XN 'AAAAAA', B, ±CCCC.CCC, ±DDDD.DDD
		# AAAAAA The SMU channel name for the X-axis; up to 6 characters long; must be one of the
		# SMU channel names that you specify on the channel definition (DE) page
		# B X-axis scale type
		# ▪ Linear scale: 1
		# ▪ Log scale: 2
		# CCCC.CCC X-axis minimum value
		# ▪ Volts: ±9999
		# ▪ Amperes: ±999
		# DDDD.DDD X-axis maximum value
		# ▪ Volts: ±9999
		# ▪ Amperes: ±999

		# Example
		# XN 'V1', 1, -5, 5
		# This command string:
		# ▪ Specifies that values from SMU channel V1 are to be plotted on the X-axis.
		# ▪ Sets up the X-axis to be scaled linearly between −5 V and +5 V

		if not isinstance(channel_name, str) or len(channel_name) > 6:
			raise ValueError(f"Invalid channel name: {channel_name}. Channel name must be a string up to 6 characters long.")
		if scale_type not in [1, 2]:
			raise ValueError(f"Invalid scale type: {scale_type}. Valid types are 1 for linear and 2 for log scale.")
		if scale_type == 1:
			if not (-9999 <= min_value <= 9999):
				raise ValueError("X-axis minimum value must be between -9999 and +9999 for linear scale.")
			if not (-9999 <= max_value <= 9999):
				raise ValueError("X-axis maximum value must be between -9999 and +9999 for linear scale.")
		elif scale_type == 2:
			if not (-999 <= min_value <= 999):
				raise ValueError("X-axis minimum value must be between -999 and +999 for log scale.")
			if not (-999 <= max_value <= 999):
				raise ValueError("X-axis maximum value must be between -999 and +999 for log scale.")
		sign_min = "+" if min_value >= 0 else "-"
		sign_max = "+" if max_value >= 0 else "-"
		min_value = abs(min_value)
		max_value = abs(max_value)
		cmd = f'XN \'{channel_name}\', {scale_type}, {sign_min}{min_value}, {sign_max}{max_value}'
		self.instrument.write(cmd)

	# configures the X-axis of the graph to plot time domain values in seconds.
	def config_graph_x_axis_time(self, min_value, max_value):
		# 		XT AAAA.AA, BBBB.BB
		# AAAA.AA X-axis minimum time value (in seconds): 0.01 to 9999
		# BBBB.BB X-axis maximum time value (in seconds): 0.01 to 9999

		# Example
		# XT 0, 10
		# This command string:
		# ▪ Specifies that time domain values are to be plotted on the X-axis.
		# ▪ Sets up the X-axis to be scaled between 0 s and 10 s

		if not (0.01 <= min_value <= 9999):
			raise ValueError("X-axis minimum time value must be between 0.01 and 9999 seconds.")
		if not (0.01 <= max_value <= 9999):
			raise ValueError("X-axis maximum time value must be between 0.01 and 9999 seconds.")
		sign_min = "+" if min_value >= 0 else "-"
		sign_max = "+" if max_value >= 0 else "-"
		min_value = abs(min_value)
		max_value = abs(max_value)
		cmd = f'XT {sign_min}{min_value}, {sign_max}{max_value}'
		self.instrument.write(cmd)

	#  configures the Y1-axis of the graph.
	# Usage
	# YA 'AAAAAA', B, ±CCCC.CCC, ±DDDD.DDD
	# AAAAAA The SMU channel name for the Y1-axis, up to 6 characters; must be one of the
	# SMU channel names that you specify on the channel definition (DE) page
	# B Y1-axis scale type:
	# ▪ Linear scale: 1
	# ▪ Log scale: 2
	# ▪ Log scale absolute value: 3
	# CCCC.CCC Y1-axis minimum value:
	# ▪ Volts: ±9999
	# ▪ Amps: ±999
	# DDDD.DDD Y1-axis maximum value:
	# ▪ Volts: ±9999
	# ▪ Amps: ±999
	# Example
	# YA 'I1', 1, -5E-9, 5E-9
	# This command string:
	# ▪ Specifies that values from SMU channel I1 are to be plotted on the Y1-axis.
	# ▪ Sets up the Y1-axis to be scaled linearly between −5 nA and +5 nA.

	def config_graph_y1_axis(self, channel_name, scale_type, min_value, max_value):
		if not isinstance(channel_name, str) or len(channel_name) > 6:
			raise ValueError(f"Invalid channel name: {channel_name}. Channel name must be a string up to 6 characters long.")
		if scale_type not in [1, 2, 3]:
			raise ValueError(f"Invalid scale type: {scale_type}. Valid types are 1 for linear, 2 for log scale, and 3 for log scale absolute value.")
		if scale_type == 1:
			if not (-9999 <= min_value <= 9999):
				raise ValueError("Y1-axis minimum value must be between -9999 and +9999 for linear scale.")
			if not (-9999 <= max_value <= 9999):
				raise ValueError("Y1-axis maximum value must be between -9999 and +9999 for linear scale.")
		elif scale_type in [2, 3]:
			if not (-999 <= min_value <= 999):
				raise ValueError("Y1-axis minimum value must be between -999 and +999 for log scales.")
			if not (-999 <= max_value <= 999):
				raise ValueError("Y1-axis maximum value must be between -999 and +999 for log scales.")
		sign_min = "+" if min_value >= 0 else "-"
		sign_max = "+" if max_value >= 0 else "-"
		min_value = abs(min_value)
		max_value = abs(max_value)
		cmd = f'YA \'{channel_name}\', {scale_type}, {sign_min}{min_value}, {sign_max}{max_value}'
		self.instrument.write(cmd)

	# configures the Y2-axis of the graph.
	# Usage
	# YB 'AAAAAA', B, ±CCCC.CCC, ±DDDD.DDD
	# AAAAAA The SMU channel name for the Y2-axis, up to 6 characters; must be one of the
	# SMU channel names that you specify on the channel definition (DE) page
	# B Y2 axis scale type:
	# ▪ Linear scale: 1
	# ▪ Log scale: 2
	# ▪ Log scale absolute value: 3
	# CCCC.CCC Y2-axis minimum value
	# ▪ Volts: ±9999
	# ▪ Amperes: ±999
	# DDDD.DDD Y2-axis maximum value
	# ▪ Volts: ±9999
	# ▪ Amperes: ±999
	# Example
	# YB 'I2', 2, 100E-9, 1E-3
	# The command string:
	# ▪ Specifies that values from SMU channel I2 are to be plotted on the Y2-axis.
	# ▪ Sets up the Y2-axis to be scaled logarithmically between 100 nA and 1 mA.

	def config_graph_y2_axis(self, channel_name, scale_type, min_value, max_value):
		if not isinstance(channel_name, str) or len(channel_name) > 6:
			raise ValueError(f"Invalid channel name: {channel_name}. Channel name must be a string up to 6 characters long.")
		if scale_type not in [1, 2, 3]:
			raise ValueError(f"Invalid scale type: {scale_type}. Valid types are 1 for linear, 2 for log scale, and 3 for log scale absolute value.")
		if scale_type == 1:
			if not (-9999 <= min_value <= 9999):
				raise ValueError("Y2-axis minimum value must be between -9999 and +9999 for linear scale.")
			if not (-9999 <= max_value <= 9999):
				raise ValueError("Y2-axis maximum value must be between -9999 and +9999 for linear scale.")
		elif scale_type in [2, 3]:
			if not (-999 <= min_value <= 999):
				raise ValueError("Y2-axis minimum value must be between -999 and +999 for log scales.")
			if not (-999 <= max_value <= 999):
				raise ValueError("Y2-axis maximum value must be between -999 and +999 for log scales.")
		sign_min = "+" if min_value >= 0 else "-"
		sign_max = "+" if max_value >= 0 else "-"
		min_value = abs(min_value)
		max_value = abs(max_value)
		cmd = f'YB \'{channel_name}\', {scale_type}, {sign_min}{min_value}, {sign_max}{max_value}'
		self.instrument.write(cmd)


	# controls measurements
	# Usage
	# MEA
	# A Measurement action:
	# ▪ Run a single trigger test and store readings in a cleared buffer: 1
	# ▪ Run a repeat trigger test and store readings in a cleared buffer: 2
	# ▪ Run a single trigger test and append readings to the buffer: 3
	# ▪ Abort the test: 4
	# Details
	# The ME1 or ME2 command triggers the start of the test and makes the programmed number
	# of measurements. The measured readings are stored in the buffer. Note that the buffer is
	# cleared before readings are stored.
	# The ME3 command also triggers the test but does not clear the buffer before storing the
	# measured readings. The readings are appended to the readings already stored in the buffer.
	# The buffer can hold up to 4096 readings.
	# The ME4 command aborts the test.
	# Example
	# ME1
	# This command string triggers the start of the test and stores the readings in the cleared buffer
	def control_measurements(self, action):
		# Example: "MEA 1" to run a single trigger test and store readings in a cleared buffer
		if action not in [1, 2, 3, 4]:
			raise ValueError(f"Invalid measurement action: {action}. Valid actions are 1 for single trigger, 2 for repeat trigger, 3 for append to buffer, and 4 for abort.")
		cmd = f'ME{action}'

	# acquires (loads) the saved data file or program file
	# Usage
	# GT 'A BBBBBB'
	# A File type:
	# ▪ Program file: P
	# ▪ Data/program file: D
	# BBBBB Name of file (up to 6 characters)
	# Details
	# The file type and file name must be separated by a space.
	# For a program file, this command launches the program. For a data file, it opens the files.
	# When the saved program file is recalled, the instrument returns to the settings stored in that
	# file.
	# The save (SV) command string is used to save instrument settings or to store data acquired
	# in a test.
	# Example
	# GT 'P Setup1'
	# This command string gets the program file named Setup1.

	def acquire_file(self, file_type, file_name):
		# Example: "GT 'P Setup1'" to get the program file named Setup1
		if file_type not in ['P', 'D']:
			raise ValueError(f"Invalid file type: {file_type}. Valid types are 'P' for program file and 'D' for data/program file.")
		if not isinstance(file_name, str) or len(file_name) > 6:
			raise ValueError(f"Invalid file name: {file_name}. File name must be a string up to 6 characters long.")
		cmd = f'GT \'{file_type} {file_name}\''
		self.instrument.write(cmd)

	# saves a program file or data file.
	# Usage
	# SV 'A BBBBBB'
	# SV 'A BBBBBB CCCCCCCC'
	# A File type:
	# ▪ Program file: P
	# ▪ Data file: D
	# BBBBB Name of file (up to 6 characters)
	# CCCCCCCC Comment (up to 8 characters)
	# Details
	# You must separate the file name and the comment from each other by a space.
	# When saving a program file, the present instrument settings are stored in a file at the
	# directory path:
	# C:\s4200\sys\KXCI
	# You specify the name for the file.
	# The get command string is used to acquire the saved file.
	# Example
	# SV 'P Setup1'
	# This command string saves the command sequence as a program file named Setup1
	def save_file(self, file_type, file_name, comment=None):
		# Example: "SV 'P Setup1'" to save the program file named Setup1
		if file_type not in ['P', 'D']:
			raise ValueError(f"Invalid file type: {file_type}. Valid types are 'P' for program file and 'D' for data file.")
		if not isinstance(file_name, str) or len(file_name) > 6:
			raise ValueError(f"Invalid file name: {file_name}. File name must be a string up to 6 characters long.")
		if comment is not None and (not isinstance(comment, str) or len(comment) > 8):
			raise ValueError(f"Invalid comment: {comment}. Comment must be a string up to 8 characters long.")
		cmd = f'SV \'{file_type} {file_name}\''
		if comment:
			cmd += f' \'{comment}\''
		self.instrument.write(cmd)

	# MP
	# This command maps channel n to a given VS, SMU, or VM function.
	# Usage
	# MP A, BBBC
	# A The channel to be mapped: A value between 1 and the number of channels in the
	# system (9 maximum)
	# BBB SMU, VS, or VM
	# C The number of the SMU, VS, or VM
	# Details
	# If BBB and C are not included in the command, the function defaults to SMU<A>, where <A>
	# is the number of the channel to be mapped.
	# Example
	# MP 3, VM5
	# This command string maps channel 3 to VM5.
	def map_channel(self, channel_number, function):
		# Example: "MP 3, VM5" to map channel 3 to VM5
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		if not isinstance(function, str) or len(function) < 2:
			raise ValueError(f"Invalid function: {function}. Function must be a string with at least 2 characters.")
		cmd = f'MP {channel_number}, {function}'
		self.instrument.write(cmd)

	# SR
	# This command sets a fixed source range on channel n.
	# Usage
	# SR A, B
	# A The channel to be controlled: A value between 1 and the number of channels in the
	# system (9 maximum)
	# B Range:
	# ▪ Auto: 0
	# ▪ Best fixed range (determined by maximum sweep parameters): 2
	# ▪ Fixed range: > 0 to 1.0
	# Details
	# The default setting is autorange for backward compatibility. If you specify a range that is
	# below the bias or sweep parameters that follow, the range is adjusted to accommodate the
	# sweep.
	# Example
	# SR 1, 2
	# This command string selects best fixed range on channel 1.
	def set_source_range(self, channel_number, range_value):
		# Example: "SR 1, 2" to select best fixed range on channel 1
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		if range_value not in [0, 2] and (not isinstance(range_value, (int, float)) or range_value <= 0):
			raise ValueError(f"Invalid range value: {range_value}. Valid values are 0 for auto, 2 for best fixed range, or a positive number for fixed range.")
		cmd = f'SR {channel_number}, {range_value}'
		self.instrument.write(cmd)

	# DI
	# This command sets up a SMU channel as a current source.
	# Usage
	# DIB
	# DIB, CC, ±DDD.DDDD, ±EEE.EEEE
	# B SMU channel: 1 to 9
	# CC Current source range:
	# ▪ Autorange: 0
	# ▪ 1 nA range (only with a preamplifier): 1
	# ▪ 10 nA range (only with a preamplifier): 2
	# ▪ 100 nA range: 3
	# ▪ 1 μA range: 4
	# ▪ 10 μA range: 5
	# ▪ 100 μA range: 6
	# ▪ 1 mA range: 7
	# ▪ 10 mA range: 8
	# ▪ 100 mA range: 9
	# ▪ 1 A range (only with a 4210-SMU or 4211-SMU): 10
	# ▪ 1 pA range (only with a preamplifier): 11
	# ▪ 10 pA range (only with a preamplifier): 12
	# ▪ 100 pA range (only with a preamplifier): 13
	# DDD.DDDD Output value (amperes):
	# ▪ 4200-SMU or 4201-SMU: −0.1050 to +0.1050
	# ▪ 4210-SMU or 4211-SMU: −1.0500 to +1.0500
	# EEE.EEEE Compliance value (voltage): −210.00 to 210.00
	# Details
	# For every channel that is configured as a SMU, you must select the source mode (voltage or
	# current), source output range, output value, and compliance value.
	# To select the voltage source mode, see DV (on page 5-33).
	# If you send DIB with no other parameters, the output of the specified channel is disabled.
	# Example
	# DI1, 1, 10, 1, 20
	# This command string configures SMU1 to source 1 nA on the 1 A source range and sets voltage
	# compliance to 20 V.
	def set_smu_current_source(self, channel_number, range_value, output_value, compliance_value):
		# Example: "DI1, 1, 10, 1, 20" to configure SMU1 to source 1 nA on the 1 A source range and set voltage compliance to 20 V
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		if range_value not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]:
			raise ValueError(f"Invalid range value: {range_value}. Valid ranges are from 0 (autorange) to 13 (100 pA range with preamplifier).")
		if not isinstance(output_value, (int, float)):
			raise ValueError(f"Invalid output value: {output_value}. Output value must be a number.")
		if not (-1.0500 <= output_value <= 1.0500):
			raise ValueError("Output value must be between -1.0500 and +1.0500 for current sources.")
		if not (-210.00 <= compliance_value <= 210.00):
			raise ValueError("Compliance value must be between -210.00 and +210.00.")
		sign_output = "+" if output_value >= 0 else "-"
		sign_compliance = "+" if compliance_value >= 0 else "-"
		output_value = abs(output_value)
		compliance_value = abs(compliance_value)
		cmd = f'DI{channel_number}, {range_value}, {sign_output}{output_value}, {sign_compliance}{compliance_value}'
		self.instrument.write(cmd)

	# DS
	# This command specifies the channel number and the voltage output value for each voltage source.
	# Usage
	# DSA, ±BBB.BBBB
	# A n, for voltage source VSn; range 1 to 9
	# BBB.BBBB Output voltage value: -200.00 to +200.00
	# Details
	# KXCI allows up to nine source-measure units to function solely as voltage sources. You can
	# use any channel for any voltage-source function between VS1 and VS9. For example, in a
	# system containing four SMUs, you can use SMU2 as VS5.
	# The assigned n value for a voltage source (VSn) or voltmeter (VMn) depends on how
	# instruments are mapped in KCon.
	# Example
	# DS1, 20
	# This command string sets VS1 to output 20 V
	def set_voltage_source(self, channel_number, output_value):
		# Example: "DS1, 20" to set VS1 to output 20 V
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		if not isinstance(output_value, (int, float)):
			raise ValueError(f"Invalid output value: {output_value}. Output value must be a number.")
		if not (-200.00 <= output_value <= 200.00):
			raise ValueError("Output voltage value must be between -200.00 and +200.00.")
		sign_output = "+" if output_value >= 0 else "-"
		output_value = abs(output_value)
		cmd = f'DS{channel_number}, {sign_output}{output_value}'
		self.instrument.write(cmd)

	# DV
	# This command sets up a SMU channel as a voltage source.
	# Usage
	# DVB
	# DVB, CC, ±DDD.DDDD, ±EEE.EEEE
	# B SMU channel: 1 to 9
	# CC Voltage source range:
	# ▪ Autorange: 0
	# ▪ 20 V range: 1
	# ▪ 200 V range: 2 or 3
	# ▪ 200 mV range: 4 (only with a preamplifier)
	# ▪ 2 V range: 5 (only with a preamplifier)
	# DDD.DDDD Output value (voltage): −210.00 to +210.00
	# EEE.EEEE Current compliance value (amperes):
	# ▪ 4200-SMU or 4201-SMU: −0.1050 to +0.1050
	# ▪ 4210-SMU or 4211-SMU: −1.0500 to +1.0500
	# Details
	# For every channel that is configured as a SMU, you must select the source mode (voltage or
	# current), source output range, output value, and compliance value.
	# To select the current source mode, see DI (on page 5-32).
	# If you specify a compliance current that is below the minimum allowable value, KXCI sets it
	# to the minimum allowable value.
	# If you send DVB with no other parameters, the output of the specified channel is disabled.
	# Example
	# DV1, 1, 10, 10E-3
	# This command string configures SMU1 to source 10 V on the 20 V source range and sets current
	# compliance to 10 mA.
	def set_smu_voltage_source(self, channel_number, range_value, output_value, compliance_value):
		# Example: "DV1, 1, 10, 10E-3" to configure SMU1 to source 10 V on the 20 V source range and set current compliance to 10 mA
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		if range_value not in [0, 1, 2, 3, 4, 5]:
			raise ValueError(f"Invalid range value: {range_value}. Valid ranges are from 0 (autorange) to 5 (2 V range with preamplifier).")
		if not isinstance(output_value, (int, float)):
			raise ValueError(f"Invalid output value: {output_value}. Output value must be a number.")
		if not (-210.00 <= output_value <= 210.00):
			raise ValueError("Output voltage value must be between -210.00 and +210.00.")
		if not (-0.1050 <= compliance_value <= 0.1050):
			raise ValueError("Compliance value must be between -0.1050 and +0.1050 for 4200-SMU or 4201-SMU; -1.0500 and +1.0500 for 4210-SMU or 4211-SMU.")
		sign_output = "+" if output_value >= 0 else "-"
		sign_compliance = "+" if compliance_value >= 0 else "-"
		output_value = abs(output_value)
		compliance_value = abs(compliance_value)
		cmd = f'DV{channel_number}, {range_value}, {sign_output}{output_value}, {sign_compliance}{compliance_value}'
		self.instrument.write(cmd)

	# TI
	# This command triggers a current measurement.
	# Usage
	# TI AABB
	# BB Measure channel for current measurements:
	# ▪ SMU1: 1
	# ▪ SMU2: 2
	# ▪ SMU3: 3
	# ▪ SMU4: 4
	# ▪ SMU5: 5
	# ▪ SMU6: 6
	# ▪ SMU7: 7
	# ▪ SMU8: 8
	# Details
	# After sending the command string to trigger a measurement and addressing the 4200A-SCS
	# to talk, the output data string is sent to the computer in the following format:
	# X Y Z ±N.NNNN E±NN
	# Where:
	# • X: The status of the data (where X = N for a normal reading)
	# • Y: The measure channel (Y = A through F)
	# • Z: The measure mode (Z = V or I)
	# • ±N.NNNN E±NN is the reading (mantissa and exponent)
	# • When channels are mapped to different functions (VM or VS), KXCI tries to trigger
	# measurements on the specified channels. However, if the mapped function for a channel
	# does not match the requested measurement, KXCI reports an error. For example, if the
	# mapped function for a channel is VS2, but the requested measurement is TI2, KXCI
	# reports an error, because a VS cannot measure current.
	def trigger_current_measurement(self, channel_number):
		# Example: "TI 1" to trigger a current measurement on SMU1
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		cmd = f'TI {channel_number}'
		self.instrument.write(cmd)

	# TV
	# This command triggers a voltage measurement.
	# Usage
	# TV BB
	# BB Measure channel for voltage measurements:
	# ▪ SMU1: 1
	# ▪ SMU2: 2
	# ▪ SMU3: 3
	# ▪ SMU4: 4
	# ▪ VM1: 5
	# ▪ VM2: 6
	# ▪ SMU5: 7
	# ▪ SMU6: 8
	# ▪ SMU7: 9
	# ▪ SMU8: 10
	# ▪ VM3: 11
	# ▪ VM4: 12
	# ▪ VM5: 13
	# ▪ VM6: 14
	# ▪ VM7: 15
	# ▪ VM8: 16
	# Details
	# You can use a SMU to measure voltage either directly (as mapped SMU1 to SMU9) or as a
	# mapped voltmeter (VM1 to VM9), so the SMU is specified in the trigger command string by a
	# unique identifier. For example, a physical SMU that has been mapped as SMU5 (using
	# KCon) is specified by the unique identifier 7.
	# After sending the command string to trigger a measurement and addressing the 4200A-SCS
	# to talk, the output data string is sent to the computer in the following format:
	# X Y Z ±N.NNNN E±NN
	# Where:
	# • X: The status of the data (where X = N for a normal reading)
	# • Y: The measure channel (Y = A through F)
	# • Z: The measure mode (Z = V or I)
	# • ±N.NNNN E±NN is the reading (mantissa and exponent)
	# When channels are mapped to different functions (VM or VS), KXCI tries to trigger
	# measurements on the specified channels. However, if the mapped function for a channel
	# does not match the requested measurement, KXCI reports an error. For example, if the
	# mapped function for a channel is VS2, but the requested measurement is TI2, KXCI reports
	# an error, because a VS cannot measure current.
	def trigger_voltage_measurement(self, channel_number):
		# Example: "TV 1" to trigger a voltage measurement on SMU1
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		cmd = f'TV {channel_number}'
		self.instrument.write(cmd)

	# AC
	# This command autocalibrates a SMU channel.
	# Usage
	# AC A
	# A SMU number (1 to 9)
	# Details
	# SMU only.
	# When this command is sent, the selected SMU channel is calibrated automatically. The busy
	# bit in the status register is set so that you can detect when autocalibration is finished. The
	# 4200A-SCS will not respond to any commands while autocalibration is executing.
	# Example
	# AC 1
	# This command string performs autocalibration on SMU channel number 1.
	def autocalibrate_smu(self, channel_number):
		# Example: "AC 1" to perform autocalibration on SMU channel number 1
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		cmd = f'AC {channel_number}'
		self.instrument.write(cmd)

	# BC
	# This command clears all readings from the buffer.
	# Usage
	# BC
	# Details
	# SMU only.
	# The GPIB data buffer can hold up to 4096 readings.
	# This command string clears all readings from the buffer. It also clears bit B0 (Data Ready) of
	# the status byte.
	def clear_buffer(self):
		# Example: "BC" to clear all readings from the buffer
		cmd = 'BC'
		self.instrument.write(cmd)

	# DO
	# This command returns the timestamp data that was acquired with the voltage or current measurement,
	# or both.
	# Usage
	# DO 'AAAAAA'
	# DO 'AAAAAAB'
	# AAAAAA User-specified name of the channel that made the measurement, up to
	# 6 characters; cannot be changed through the CH or VS commands
	# B T: Return timestamp data
	# S: Return the SMU status
	# Details
	# SMU only.
	# After making measurements, use this command string to request the readings. After the
	# 4200A-SCS is addressed to talk, the readings are sent.
	# Output data is sent to the computer in the format ±N.NNNN E±NN.
	# Output data of 0 indicates this point is not measured yet.
	# When you run a voltage sweep without measure commands, you can use DO to retrieve the
	# voltage measurement. However, you cannot use DO to retrieve the current measurement
	# from a voltage sweep. To retrieve the current measurement, use LI, XN, YA, YB, or DV.
	# Example
	# DO 'CH1'
	# This command string requests the reading string for SMU channel 1.
	def get_measurement_data(self, channel_name, include_timestamp=False, include_status=False):
		# Example: "DO 'CH1'" to request the reading string for SMU channel 1
		if not isinstance(channel_name, str) or len(channel_name) > 6:
			raise ValueError(f"Invalid channel name: {channel_name}. Channel name must be a string up to 6 characters long.")
		cmd = f'DO \'{channel_name}\''
		if include_timestamp:
			cmd += ' T'
		if include_status:
			cmd += ' S'
		self.instrument.write(cmd)

	# EC
	# This command sets the condition to exit the test if compliance is reached.
	# Usage
	# EC A
	# A Action on compliance:
	# ▪ Off (do not exit if compliance is reached): 0
	# ▪ On (exit if compliance is reached): 1
	# Details
	# SMU only.
	# Example
	# EC 1
	# This command enables exit on compliance.
	def set_exit_on_compliance(self, action):
		# Example: "EC 1" to enable exit on compliance
		if action not in [0, 1]:
			raise ValueError(f"Invalid action: {action}. Valid actions are 0 for off (do not exit) and 1 for on (exit if compliance is reached).")
		cmd = f'EC {action}'
		self.instrument.write(cmd)

	# EM
	# This command switches between 4145 Emulation and 4200A command sets.
	# Usage
	# EM A,B
	# A Mode:
	# ▪ 4145 Emulation: 0
	# ▪ 4200A: 1
	# B Which sessions:
	# ▪ This session only: 0
	# ▪ This and all subsequent sessions (writes to KCon file): 1
	# Details
	# SMU only.
	# Example
	# EM 0,1
	# This selects the 4145 Emulation command set permanently.
	def set_emulation_mode(self, mode, session_type):
		# Example: "EM 0,1" to select the 4145 Emulation command set permanently
		if mode not in [0, 1]:
			raise ValueError(f"Invalid mode: {mode}. Valid modes are 0 for 4145 Emulation and 1 for 4200A command set.")
		if session_type not in [0, 1]:
			raise ValueError(f"Invalid session type: {session_type}. Valid types are 0 for this session only and 1 for this and all subsequent sessions.")
		cmd = f'EM {mode},{session_type}'
		self.instrument.write(cmd)

	# IT
	# This command sets the integration time of a SMU.
	# Usage
	# ITA
	# IT4, X, Y, Z
	# A Integration time:
	# ▪ Short (0.1 PLC): 1
	# ▪ Medium (1.0 PLC): 2
	# ▪ Long (10 PLC): 3
	# ▪ Custom (4200A command set only): 4
	# X Delay factor for custom setting: 0.0 to 100
	# Y Filter factor for custom setting: 0.0 to 100
	# Z A/D converter integration time in number of PLCs for custom setting: 0.01 to 10.0
	# Details
	# SMU only.
	# The integration time is the time to convert a measurement. In general, a short integration
	# time provides the fastest measurement speed at the expense of noise. Conversely, a long
	# integration time provides stable readings at the expense of speed. Integration time is based
	# on power line cycles (PLC). Assuming 60 Hz line power, the integration time for a 1 PLC
	# setting is 16.67 ms (1/60).
	# The preconfigured integration time settings are equivalent to the Fast, Normal, and Quiet
	# settings available in Clarius:
	# • Short: Equivalent to the Clarius Fast setting. Optimizes the SMU for speed at the
	# expense of noise performance. It is a good choice for measurements where noise and
	# settling time are not concerns.
	# • Normal: Equivalent to the Clarius Medium setting. The default and most commonly used
	# setting. It provides a good combination of speed and low noise and is the best setting for
	# most cases.
	# • Long: Equivalent to the Clarius Quiet setting. Optimizes the SMU for low-noise
	# measurements at the expense of speed. If speed is not a critical consideration, it is a
	# good choice when you need the lowest noise and most accurate measurements.
	# The custom setting combines delay factor, filter factor, and A/D integration time, which is
	# comparable to the individual Clarius Delay Factor, Filter Factor, and A/D converter
	# integration time settings.
	# Example 1
	# IT2
	# This command string sets the integration time to 1.0 PLC.
	# Example 2
	# IT4,2.5,0.6,1.3
	# This command string sets the delay factor to 2.5, the filter factor to 0.6, and the A/D converter integration time
	# to 1.3 PLCs.
	def set_integration_time(self, mode, delay_factor=None, filter_factor=None, ad_integration_time=None):
		# Example: "IT2" to set the integration time to 1.0 PLC
		if mode not in [1, 2, 3, 4]:
			raise ValueError(f"Invalid mode: {mode}. Valid modes are 1 for short (0.1 PLC), 2 for medium (1.0 PLC), 3 for long (10 PLC), and 4 for custom.")
		if mode == 4:
			if delay_factor is None or filter_factor is None or ad_integration_time is None:
				raise ValueError("For custom integration time (mode 4), delay factor, filter factor, and A/D integration time must be provided.")
			if not (0.0 <= delay_factor <= 100):
				raise ValueError("Delay factor must be between 0.0 and 100.")
			if not (0.0 <= filter_factor <= 100):
				raise ValueError("Filter factor must be between 0.0 and 100.")
			if not (0.01 <= ad_integration_time <= 10.0):
				raise ValueError("A/D integration time must be between 0.01 and 10.0 PLCs.")
			cmd = f'IT{mode}, {delay_factor}, {filter_factor}, {ad_integration_time}'
		else:
			cmd = f'IT{mode}'
		self.instrument.write(cmd)

	# RD
	# This command requests real-time readings.
	# Usage
	# RD 'AAAAAA', N
	# RD 'AAAAAAB', N
	# AAAAAA User-specified name of the channel that made the measurement, up to 6 characters
	# B T: Return timestamp data
	# S: Return the SMU status
	# N Index of the point to retrieve; valid range from 1 to the total number of readings
	# Details
	# SMU only.
	# While making measurements, use this command string to request the real-time reading. This
	# can be used in a loop while measuring.
	# Output data is sent to the computer in the format ±N.NNNN E±NN.
	# Output data of 0 indicates this point is not measured yet.
	# For an example that demonstrates how to use this command, refer to Program 4: VAR1
	# sweep with real-time data retrieval (on page 5-46).
	# Example
	# RD 'Volt', 1
	# This command string requests the first reading for a SMU channel that is named Volt.

	def request_real_time_reading(self, channel_name, index, include_timestamp=False, include_status=False):
		# Example: "RD 'Volt', 1" to request the first reading for a SMU channel that is named Volt
		if not isinstance(channel_name, str) or len(channel_name) > 6:
			raise ValueError(f"Invalid channel name: {channel_name}. Channel name must be a string up to 6 characters long.")
		if not isinstance(index, int) or index < 1:
			raise ValueError(f"Invalid index: {index}. Index must be a positive integer starting from 1.")
		cmd = f'RD \'{channel_name}\', {index}'
		if include_timestamp:
			cmd += ' T'
		if include_status:
			cmd += ' S'
		self.instrument.write(cmd)

	# RG
	# This command sets the lowest current range of the SMU to be used when measuring.
	# Usage
	# RG A,B
	# A SMU number (1 to 9)
	# B The lowest autoranged range in amps:
	# ▪ 4200-SMU or 4201-SMU without a preamplifier: -100e-9 to 100e-3
	# ▪ 4200-SMU or 4201-SMU with a preamplifier: -1e-12 to 100e-3
	# ▪ 4210-SMU or 4211-SMUwithout a preamplifier: -100e-9 to 1
	# ▪ 4210-SMU or 4211-SMU with a preamplifier: -1e-12 to 1
	# Details
	# SMU only.
	# The default autoranged ranges are 100 nA without a preamplifier and 1 nA with
	# a preamplifier.
	# Example
	# RG 2, 10E-12
	# This command string sets the lowest range of SMU2 with a preamplifier to 10 pA.

	def set_lowest_current_range(self, channel_number, lowest_range):
		# Example: "RG 2, 10E-12" to set the lowest range of SMU2 with a preamplifier to 10 pA
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		if not isinstance(lowest_range, (int, float)):
			raise ValueError(f"Invalid lowest range: {lowest_range}. Lowest range must be a number.")
		if not (-1e-12 <= lowest_range <= 100e-3):
			raise ValueError("Lowest range must be between -1e-12 and +100e-3 for 4200-SMU or 4201-SMU with a preamplifier.")
		sign_lowest = "+" if lowest_range >= 0 else "-"
		lowest_range = abs(lowest_range)
		cmd = f'RG {channel_number}, {sign_lowest}{lowest_range}'
		self.instrument.write(cmd)

	# RI
	# This command instructs a SMU to go to a specified current range immediately without waiting until the
	# initiation of a test.
	# Usage
	# RI channel, range, compliance
	# channel SMU number (1 to 9)
	# range Range value (amperes):
	# ▪ 4200-SMU or 4201-SMU without a preamplifier: 100e-9 to 100e-3
	# ▪ 4200-SMU or 4201-SMU with a preamplifier: 1e-12 to 100e-3
	# compliance Current compliance value (amperes):
	# ▪ 4200-SMU or 4201-SMU: −0.1050 to +0.1050
	# ▪ 4210-SMU or 4211-SMU: −1.0500 to +1.0500
	# Details
	# SMU only.
	# Example
	# RI 1, 1E-3, 1E-3
	# This command string instructs SMU1 to go to the 1 mA range and set compliance to 1 mA.
	def set_immediate_current_range(self, channel_number, range_value, compliance_value):
		# Example: "RI 1, 1E-3, 1E-3" to instruct SMU1 to go to the 1 mA range and set compliance to 1 mA
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		if not isinstance(range_value, (int, float)):
			raise ValueError(f"Invalid range value: {range_value}. Range value must be a number.")
		if not (-100e-9 <= range_value <= 100e-3):
			raise ValueError("Range value must be between -100e-9 and +100e-3 for 4200-SMU or 4201-SMU without a preamplifier; -1e-12 and +100e-3 with a preamplifier.")
		if not (-0.1050 <= compliance_value <= 0.1050):
			raise ValueError("Compliance value must be between -0.1050 and +0.1050 for 4200-SMU or 4201-SMU; -1.0500 and +1.0500 for 4210-SMU or 4211-SMU.")
		sign_range = "+" if range_value >= 0 else "-"
		sign_compliance = "+" if compliance_value >= 0 else "-"
		range_value = abs(range_value)
		compliance_value = abs(compliance_value)
		cmd = f'RI {channel_number}, {sign_range}{range_value}, {sign_compliance}{compliance_value}'
		self.instrument.write(cmd)

	# RS
	# This command sets the measurement resolution for all channels of a SMU.
	# Usage
	# RS A
	# A Resolution, in number of digits:
	# ▪ 4200A command set: 3 to 7
	# ▪ 4145 Emulation command set: 3 to 5
	# Details
	# SMU only.
	# Example
	# RS 7
	# This command string provides full SMU resolution when the 4200A command set is selected.
	def set_measurement_resolution(self, resolution):
		# Example: "RS 7" to provide full SMU resolution when the 4200A command set is selected
		if not isinstance(resolution, int) or resolution < 3 or (self.instrument.emulation_mode == '4145' and resolution > 5) or (self.instrument.emulation_mode == '4200' and resolution > 7):
			raise ValueError(f"Invalid resolution: {resolution}. Valid resolutions are 3 to 5 for 4145 Emulation and 3 to 7 for 4200A command set.")
		cmd = f'RS {resolution}'
		self.instrument.write(cmd)


	# RV
	# This command instructs a SMU to go to a specified voltage range immediately without waiting until the
	# initiation of a test.
	# Usage
	# RV channel, range, compliance
	# channel SMU number (1 to 9)
	# range Range value (voltage): −210.00 to +210.00
	# compliance Voltage compliance value (voltage): −210.00 to +210.00
	# Details
	# SMU only.
	# The range is set to the range that is closest to the entered value. For example, if you set
	# range to 10, the 20 V range is selected.
	# Example
	# RV 1, 2, 1
	# This command string instructs SMU1 to go to the 2 V range and to set compliance to 1 V.
	def set_immediate_voltage_range(self, channel_number, range_value, compliance_value):
		# Example: "RV 1, 2, 1" to instruct SMU1 to go to the 2 V range and to set compliance to 1 V
		if channel_number not in self.CHANNEL_NUMBERS:
			raise ValueError(f"Invalid channel number: {channel_number}. Valid channels are {self.CHANNEL_NUMBERS}.")
		if not isinstance(range_value, (int, float)):
			raise ValueError(f"Invalid range value: {range_value}. Range value must be a number.")
		if not (-210.00 <= range_value <= 210.00):
			raise ValueError("Range value must be between -210.00 and +210.00.")
		if not (-210.00 <= compliance_value <= 210.00):
			raise ValueError("Compliance value must be between -210.00 and +210.00.")
		sign_range = "+" if range_value >= 0 else "-"
		sign_compliance = "+" if compliance_value >= 0 else "-"
		range_value = abs(range_value)
		compliance_value = abs(compliance_value)
		cmd = f'RV {channel_number}, {sign_range}{range_value}, {sign_compliance}{compliance_value}'
		self.instrument.write(cmd)

	# -----------------
	# KXCI CVU commands
	# -----------------

	# :CVU:CABLE:COMP:LOAD
	# This command performs load compensation and collects the load compensation cable data for
	# the CVU.
	# Usage
	# :CVU:CABLE:COMP:LOAD length, load
	# length The length of the cable:
	# ▪ 0: ≤ 0.5 m
	# ▪ 1.5: >0.5 m to < 2.5 m
	# ▪ 3.0: ≥ 2.5 m to 5 m
	# ▪ 4.0: Custom
	# ▪ 5.0: CVIV 2W
	# ▪ 6.0: CVIV 4W black 0.75 m cable
	# ▪ 7.0: CVIV 4W blue 0.61 m cable
	# load The load value
	# Details
	# If you use the custom setting, run :CVU:CABLE:COMP:MEASCUSTOM before sending the
	# :CVU:CABLE:COMP:LOAD command.
	# Custom cable compensation supports only one set of cable constants for a CVU. For
	# example, if you run custom cable compensation for CVU2 and CVU1, the constants for
	# CVU2 are lost.
	# To enable or disable load compensation, send :CVU:CORRECT.
	# For additional information on cable compensation, refer to “Connection compensation” in the
	# Model 4200A-SCS Capacitance-Voltage Unit (CVU) User’s Manual.
	def cable_compensation_load(self, length, load):
		# Example: ":CVU:CABLE:COMP:LOAD 1.5, 100" to perform load compensation with a cable length of 1.5 m and a load value of 100
		if length not in [0, 1.5, 3.0, 4.0, 5.0, 6.0, 7.0]:
			raise ValueError(f"Invalid cable length: {length}. Valid lengths are 0 (≤ 0.5 m), 1.5 (>0.5 m to < 2.5 m), 3.0 (≥ 2.5 m to 5 m), 4.0 (Custom), 5.0 (CVIV 2W), 6.0 (CVIV 4W black 0.75 m cable), and 7.0 (CVIV 4W blue 0.61 m cable).")
		if not isinstance(load, (int, float)):
			raise ValueError(f"Invalid load value: {load}. Load value must be a number.")
		cmd = f':CVU:CABLE:COMP:LOAD {length}, {load}'
		self.instrument.write(cmd)

	# :CVU:CABLE:COMP:MEASCUSTOM
	# This command performs custom cable-length compensation and collects the compensation cable data
	# for the CVU.
	# Usage
	# :CVU:CABLE:COMP:MEASCUSTOM
	# Details
	# If you are using the custom parameter for the open, short, or load commands, send
	# the :CVU:CABLE:COMP:MEASCUSTOM command before sending those commands.
	# For additional information on cable compensation, refer to “Connection compensation” in the
	# Model 4200A-SCS Capacitance-Voltage Unit (CVU) User’s Manual.
	# Also see
	# :CVU:CABLE:COMP:LOAD (on page 6-4)
	# :CVU:CABLE:COMP:OPEN (on page 6-5)
	# :CVU:CABLE:COMP:SHORT (on page 6-6)
	def cable_compensation_measure_custom(self):
		# Example: ":CVU:CABLE:COMP:MEASCUSTOM" to perform custom cable-length compensation
		cmd = ':CVU:CABLE:COMP:MEASCUSTOM'
		self.instrument.write(cmd)

	# :CVU:CABLE:COMP:OPEN
	# This command performs open compensation and collects the open compensation cable data for the
	# CVU.
	# Usage
	# :CVU:CABLE:COMP:OPEN length
	# length The length of the cable:
	# ▪ 0: ≤ 0.5 m
	# ▪ 1.5: >0.5 m to < 2.5 m
	# ▪ 3.0: ≥ 2.5 m to 5 m
	# ▪ 4.0: Custom
	# ▪ 5.0: CVIV 2W
	# ▪ 6.0: CVIV 4W black 0.75 m cable
	# ▪ 7.0: CVIV 4W blue 0.61 m cable
	# Details
	# If you use the custom setting, send the :CVU:CABLE:COMP:MEASCUSTOM command before
	# sending the :CVU:CABLE:COMP:OPEN command.
	# Custom cable compensation supports only one set of cable constants for a CVU. For
	# example, if you run custom cable compensation for CVU2 and CVU1, the constants for
	# CVU2 are lost.
	# To enable or disable load compensation, send the CVU:CORRECT command.
	# For additional information on cable compensation, refer to “Connection compensation” in the
	# Model 4200A-SCS Capacitance-Voltage Unit (CVU) User’s Manual.
	def cable_compensation_open(self, length):
		# Example: ":CVU:CABLE:COMP:OPEN 1.5" to perform open compensation with a cable length of 1.5 m
		if length not in [0, 1.5, 3.0, 4.0, 5.0, 6.0, 7.0]:
			raise ValueError(f"Invalid cable length: {length}. Valid lengths are 0 (≤ 0.5 m), 1.5 (>0.5 m to < 2.5 m), 3.0 (≥ 2.5 m to 5 m), 4.0 (Custom), 5.0 (CVIV 2W), 6.0 (CVIV 4W black 0.75 m cable), and 7.0 (CVIV 4W blue 0.61 m cable).")
		cmd = f':CVU:CABLE:COMP:OPEN {length}'
		self.instrument.write(cmd)

	# :CVU:CABLE:COMP:SHORT
	# This command performs short compensation and collects the short compensation cable data for
	# the CVU.
	# Usage
	# :CVU:CABLE:COMP:SHORT length
	# length The length of the cable:
	# ▪ 0: ≤ 0.5 m
	# ▪ 1.5: >0.5 m to < 2.5 m
	# ▪ 3.0: ≥ 2.5 m to 5 m
	# ▪ 4.0: Custom
	# ▪ 5.0: CVIV 2W
	# ▪ 6.0: CVIV 4W black 0.75 m cable
	# ▪ 7.0: CVIV 4W blue 0.61 m cable
	# Details
	# If you use the custom parameter, send the :CVU:CABLE:COMP:MEASCUSTOM command
	# before sending the :CVU:CABLE:COMP:SHORT command.
	# Custom cable compensation supports only one set of cable constants for a CVU. For
	# example, if you run custom cable compensation for CVU2 and CVU1, the constants for
	# CVU2 are lost.
	# To enable or disable load compensation, send the CVU:CORRECT command.
	# For additional information on cable compensation, refer to “Connection compensation” in the
	# Model 4200A-SCS Capacitance-Voltage Unit (CVU) User’s Manual.
	def cable_compensation_short(self, length):
		# Example: ":CVU:CABLE:COMP:SHORT 1.5" to perform short compensation with a cable length of 1.5 m
		if length not in [0, 1.5, 3.0, 4.0, 5.0, 6.0, 7.0]:
			raise ValueError(f"Invalid cable length: {length}. Valid lengths are 0 (≤ 0.5 m), 1.5 (>0.5 m to < 2.5 m), 3.0 (≥ 2.5 m to 5 m), 4.0 (Custom), 5.0 (CVIV 2W), 6.0 (CVIV 4W black 0.75 m cable), and 7.0 (CVIV 4W blue 0.61 m cable).")
		cmd = f':CVU:CABLE:COMP:SHORT {length}'
		self.instrument.write(cmd)

	# :CVU:MEASZ?
	# This command triggers and returns a single Z measurement using the present CVU settings.
	# Usage
	# :CVU:MEASZ?
	# Details
	# When the command is complete, the single reading is available
	def get_cvu_measurement(self):
		# Example: ":CVU:MEASZ?" to trigger and return a single Z measurement using the present CVU settings
		cmd = ':CVU:MEASZ?'
		self.instrument.write(cmd)
		response = self.instrument.read()  # Assuming the instrument has a read method to get the response
		return response  # Return the measurement data received from the instrument

	# :CVU:BIAS:DCV:SAMPLE
	# This command configures the CVU card to bias a DC voltage and sample n Z measurements.
	# Usage
	# :CVU:BIAS:DCV:SAMPLE biasv, samples
	# biasv Voltage to source when sampling Z-measurements: −30 to +30
	# samples The number of Z-measurements the CVU makes for the test operation: 1 to 4096
	# Details
	# Configures the CVU to bias a DC voltage and sample n Z measurements for the CVU card.
	# The other parameters are set by their respective commands.
	def configure_cvu_bias_and_sample(self, bias_voltage, samples):
		# Example: ":CVU:BIAS:DCV:SAMPLE 5, 10" to configure the CVU to bias a DC voltage of 5 V and sample 10 Z measurements
		if not (-30 <= bias_voltage <= 30):
			raise ValueError(f"Invalid bias voltage: {bias_voltage}. Bias voltage must be between -30 and +30 V.")
		if not (1 <= samples <= 4096):
			raise ValueError(f"Invalid number of samples: {samples}. Number of samples must be between 1 and 4096.")
		cmd = f':CVU:BIAS:DCV:SAMPLE {bias_voltage}, {samples}'

	# :CVU:DATA:FREQ?
	# This command queries the frequency measurement of the CVU when a test is complete.
	# Usage
	# :CVU:DATA:FREQ?
	def get_cvu_frequency_data(self):
		# Example: ":CVU:DATA:FREQ?" to query the frequency measurement of the CVU when a test is complete
		cmd = ':CVU:DATA:FREQ?'
		self.instrument.write(cmd)
		response = self.instrument.read()
		return response

	# :CVU:DATA:STATUS?
	# This command queries the status of the CVU when a test is complete.
	# Usage
	# :CVU:DATA:STATUS?
	def get_cvu_status_data(self):
		# Example: ":CVU:DATA:STATUS?" to query the status of the CVU when a test is complete
		cmd = ':CVU:DATA:STATUS?'
		self.instrument.write(cmd)
		response = self.instrument.read()
		return response

	# :CVU:DATA:TSTAMP?
	# This command queries the timestamp of the measurements of the CVU when a test is complete.
	# Usage
	# :CVU:DATA:TSTAMP?
	def get_cvu_timestamp_data(self):
		# Example: ":CVU:DATA:TSTAMP?" to query the timestamp of the measurements of the CVU when a test is complete
		cmd = ':CVU:DATA:TSTAMP?'
		self.instrument.write(cmd)
		response = self.instrument.read()
		return response

	# :CVU:DATA:VOLT?
	# This command queries the voltage measurement of the CVU when a test is complete.
	# Usage
	# :CVU:DATA:VOLT?
	def get_cvu_voltage_data(self):
		# Example: ":CVU:DATA:VOLT?" to query the voltage measurement of the CVU when a test is complete
		cmd = ':CVU:DATA:VOLT?'
		self.instrument.write(cmd)
		response = self.instrument.read()
		return response

	# :CVU:DATA:Z?
	# This command queries the Z measurement of the CVU when a test is complete.
	# Usage
	# :CVU:DATA:Z?
	# Details
	# Z measurements are returned as semicolon delimiter pairs. Each reading is then delimited
	# with commas.
	def get_cvu_z_data(self):
		# Example: ":CVU:DATA:Z?" to query the Z measurement of the CVU when a test is complete
		cmd = ':CVU:DATA:Z?'
		self.instrument.write(cmd)
		response = self.instrument.read()
		return response  # Return the Z measurement data received from the instrument

	# :CVU:DELAY:STEP
	# This command sets the hold time for the CVU test on the selected card for the :CVU:SWEEP:FREQ and
	# :CVU:SWEEP:DCV operations.
	# Usage
	# :CVU:DELAY:STEP stepd
	# stepd Hold time to apply the presoak value in seconds: 0 to 999
	# Details
	# The presoak value is set by the :CVU:SOAK:DCV command
	def set_cvu_delay_step(self, step_delay):
		# Example: ":CVU:DELAY:STEP 5" to set the hold time for the CVU test on the selected card to 5 seconds
		if not (0 <= step_delay <= 999):
			raise ValueError(f"Invalid step delay: {step_delay}. Step delay must be between 0 and 999 seconds.")
		cmd = f':CVU:DELAY:STEP {step_delay}'
		self.instrument.write(cmd)

	# :CVU:DELAY:SWEEP
	# This command sets the sweep delay for the CVU test on the selected card.
	# Usage
	# :CVU:DELAY:SWEEP sweepd
	# sweepd Delay in seconds: 0 to 999
	# Details
	# This command is used in sweeping mode for all sweep types except
	# :CVU:BIAS:DCV:SAMPLE.
	def set_cvu_delay_sweep(self, sweep_delay):
		# Example: ":CVU:DELAY:SWEEP 10" to set the sweep delay for the CVU test on the selected card to 10 seconds
		if not (0 <= sweep_delay <= 999):
			raise ValueError(f"Invalid sweep delay: {sweep_delay}. Sweep delay must be between 0 and 999 seconds.")
		cmd = f':CVU:DELAY:SWEEP {sweep_delay}'
		self.instrument.write(cmd)

	# :CVU:FSTEPSIZE
	# This command configures the frequency step size for the selected 4215-CVU card.
	# Usage
	# :CVU:FSTEPSIZE fstep
	# fstep The frequency size for the sweep (1e3 to 10e6); see Details
	# Details
	# The resolution of fstep is 1 kHz.
	# The lower and upper bounds shown are the maximum range. They are also limited based on
	# the start and stop values set for the sweep.
	# Set fstep to 0 if you are using the 4210-CVU.
	def set_cvu_frequency_step_size(self, fstep):
		# Example: ":CVU:FSTEPSIZE 1e4" to configure the frequency step size for the selected 4215-CVU card to 10 kHz
		if not (1e3 <= fstep <= 10e6):
			raise ValueError(f"Invalid frequency step size: {fstep}. Frequency step size must be between 1e3 and 10e6 Hz.")
		cmd = f':CVU:FSTEPSIZE {fstep}'
		self.instrument.write(cmd)

	# :CVU:SAMPLE:HOLDT
	# This command sets the hold time for a sampling mode test on the selected card.
	# Usage
	# :CVU:SAMPLE:HOLDT holdt
	# holdt Hold time in seconds: 0 to 999
	# Details
	# This command is only used when executing the :CVU:BIAS:DCV:SAMPLE command.
	def set_cvu_sample_hold_time(self, hold_time):
		# Example: ":CVU:SAMPLE:HOLDT 5" to set the hold time for a sampling mode test on the selected card to 5 seconds
		if not (0 <= hold_time <= 999):
			raise ValueError(f"Invalid hold time: {hold_time}. Hold time must be between 0 and 999 seconds.")
		cmd = f':CVU:SAMPLE:HOLDT {hold_time}'
		self.instrument.write(cmd)

	# :CVU:SAMPLE:INTERVAL
	# This command sets the delay between samples for the selected card.
	# Usage
	# :CVU:SAMPLE:INTERVAL interval
	# interval Delay in seconds: 0 to 999
	# Details
	# This command is only used when executing the :CVU:BIAS:DCV:SAMPLE command.
	def set_cvu_sample_interval(self, interval):
		# Example: ":CVU:SAMPLE:INTERVAL 2" to set the delay between samples for the selected card to 2 seconds
		if not (0 <= interval <= 999):
			raise ValueError(f"Invalid interval: {interval}. Interval must be between 0 and 999 seconds.")
		cmd = f':CVU:SAMPLE:INTERVAL {interval}'
		self.instrument.write(cmd)

	# :CVU:SOAK:DCV
	# This command sets the presoak DC voltage for all sweeps for the selected CVU card.
	# Usage
	# :CVU:SOAK:DCV voltage
	# voltage The voltage to bias before test sequence begins: −30 to +30
	def set_cvu_soak_voltage(self, voltage):
		# Example: ":CVU:SOAK:DCV 5" to set the presoak DC voltage for all sweeps for the selected CVU card to 5 V
		if not (-30 <= voltage <= 30):
			raise ValueError(f"Invalid soak voltage: {voltage}. Soak voltage must be between -30 and +30 V.")
		cmd = f':CVU:SOAK:DCV {voltage}'
		self.instrument.write(cmd)

	# :CVU:STANDBY
	# This command configures the selected CVU card to disable DC bias at the end of a test or to leave the
	# DC bias active.
	# Usage
	# :CVU:STANDBY state
	# state The state of the CVU card at the end of the test:
	# ▪ Disable the DC voltage output: 1
	# ▪ Leave the DC bias active: 0
	def set_cvu_standby_state(self, state):
		# Example: ":CVU:STANDBY 1" to disable the DC voltage output at the end of the test
		if state not in [0, 1]:
			raise ValueError(f"Invalid state: {state}. Valid states are 0 to leave the DC bias active and 1 to disable the DC voltage output.")
		cmd = f':CVU:STANDBY {state}'
		self.instrument.write(cmd)

	# :CVU:STEP:FREQ
	# This command configures the selected CVU card to step frequency and sample Z measurements.
	# Usage
	# :CVU:STEP:FREQ fstart, fstop
	# fstart The frequency that is used for capturing the initial sample in the sweep
	# fstop The frequency that is used for capturing the final sample in the sweep
	# Details
	# Only the start frequency and stop frequency are set by this command for the step order. The
	# other parameters are set by their respective commands.
	# Values are coerced to one of the 37 discrete frequencies for the 4210-CVU.
	# To perform a linear sweep using the 4215-CVU, use the :CVU:FSTEPSIZE command
	def configure_cvu_step_frequency(self, fstart, fstop):
		# Example: ":CVU:STEP:FREQ 1e3, 10e6" to configure the selected CVU card to step frequency from 1 kHz to 10 MHz
		if not (1e3 <= fstart <= 10e6):
			raise ValueError(f"Invalid start frequency: {fstart}. Start frequency must be between 1e3 and 10e6 Hz.")
		if not (1e3 <= fstop <= 10e6):
			raise ValueError(f"Invalid stop frequency: {fstop}. Stop frequency must be between 1e3 and 10e6 Hz.")
		cmd = f':CVU:STEP:FREQ {fstart}, {fstop}'
		self.instrument.write(cmd)

	# :CVU:SWEEP:ACV
	# This command configures the selected CVU card to sweep AC voltage and sample Z measurements.
	# Usage
	# :CVU:SWEEP:ACV acvstart, acvstop, acvstep
	# acvstart Start AC voltage, in volts:
	# ▪ 4210-CVU: 0.01 to 0.1
	# ▪ 4215-CVU: 0.01 to 1.0
	# acvstop Stop AC voltage, in volts:
	# ▪ 4210-CVU: 0.01 to 0.1
	# ▪ 4215-CVU: 0.01 to 1.0
	# acvstep The AC voltage step size
	# Details
	# The other parameters (such as DC voltage level and frequency) are set by their
	# respective commands.

	def configure_cvu_sweep_ac_voltage(self, acvstart, acvstop, acvstep):
		# Example: ":CVU:SWEEP:ACV 0.01, 0.1, 0.01" to configure the selected CVU card to sweep AC voltage from 0.01 V to 0.1 V with a step size of 0.01 V
		if not (0.01 <= acvstart <= (0.1 if self.cvu_model == '4210' else 1.0)):
			raise ValueError(f"Invalid start AC voltage: {acvstart}. Start AC voltage must be between 0.01 and {0.1 if self.cvu_model == '4210' else 1.0} V.")
		if not (0.01 <= acvstop <= (0.1 if self.cvu_model == '4210' else 1.0)):
			raise ValueError(f"Invalid stop AC voltage: {acvstop}. Stop AC voltage must be between 0.01 and {0.1 if self.cvu_model == '4210' else 1.0} V.")
		if not (acvstep > 0):
			raise ValueError(f"Invalid AC voltage step size: {acvstep}. AC voltage step size must be greater than 0.")
		cmd = f':CVU:SWEEP:ACV {acvstart}, {acvstop}, {acvstep}'
		self.instrument.write(cmd)

	# :CVU:SWEEP:DCV
	# This command configures the selected CVU card to sweep DC voltage and sample Z measurements.
	# Usage
	# :CVU:SWEEP:DCV dcvstart, dcvstop, dcvstep
	# dcvstart Start voltage, in volts: −30 to +30
	# dcvstop Stop voltage, in volts: −30 to +30
	# dcvstep Voltage step size
	# Details
	# The other parameters (AC voltage level, frequency, and so on) are set by their
	# respective commands
	# Example
	# :CVU:MODEL 2
	# :CVU:SPEED 2
	# :CVU:ACZ:RANGE 0
	# :CVU:FREQ 1E6
	# :CVU:SWEEP:DCV 5, -5, -0.2
	# :CVU:DELAY:SWEEP 0.1 – sweep delay
	# :CVU:TEST:RUN
	# Set the measurement model to Cp-GP.
	# Set the measurement speed to quiet.
	# Set the AC measurement range to autorange.
	# Set the frequency for the AC source to 1E6.
	# Set sweep to start at 5 V, stop at −5 V, and step in −0.2 V increments.
	# Set the sweep delay to 0.1 s.
	# Run the test.
	def configure_cvu_sweep_dc_voltage(self, dcvstart, dcvstop, dcvstep):
		# Example: ":CVU:SWEEP:DCV 5, -5, -0.2" to configure the selected CVU card to sweep DC voltage from 5 V to -5 V with a step size of -0.2 V
		if not (-30 <= dcvstart <= 30):
			raise ValueError(f"Invalid start DC voltage: {dcvstart}. Start DC voltage must be between -30 and +30 V.")
		if not (-30 <= dcvstop <= 30):
			raise ValueError(f"Invalid stop DC voltage: {dcvstop}. Stop DC voltage must be between -30 and +30 V.")
		if not (dcvstep != 0):
			raise ValueError(f"Invalid DC voltage step size: {dcvstep}. DC voltage step size must not be zero.")
		cmd = f':CVU:SWEEP:DCV {dcvstart}, {dcvstop}, {dcvstep}'
		self.instrument.write(cmd)

	# :CVU:SWEEP:FREQ
	# This command configures the selected CVU card to sweep frequency and sample Z measurements.
	# Usage
	# :CVU:SWEEP:FREQ fstart, fstop
	# :CVU:SWEEP:FREQ fstart, fstop, order
	# fstart The frequency that is used for capturing the initial sample in the sweep
	# fstop The frequency that is used for capturing the final sample in the sweep
	# order Determines whether the test biases DC voltage and sweeps frequency or steps
	# voltage and sweeps frequency:
	# ▪ 1: The voltage bias is the voltage set by the :CVU:DCV command (default)
	# ▪ 2: The voltage steps based on the vstart, vstop, vstep parameters set by
	# the :CVU:SWEEP:DCV command.
	# Details
	# This command sets the start frequency, stop frequency, and sweep order. The other
	# parameters are set by their respective commands.
	# Values are coerced to one of the 37 discrete frequencies for the 4210-CVU.
	# To perform a linear sweep using the 4215-CVU, use the :CVU:FSTEPSIZE command.

	def configure_cvu_sweep_frequency(self, fstart, fstop, order=1):
		# Example: ":CVU:SWEEP:FREQ 1e3, 10e6, 1" to configure the selected CVU card to sweep frequency from 1 kHz to 10 MHz with order 1
		if not (1e3 <= fstart <= 10e6):
			raise ValueError(f"Invalid start frequency: {fstart}. Start frequency must be between 1e3 and 10e6 Hz.")
		if not (1e3 <= fstop <= 10e6):
			raise ValueError(f"Invalid stop frequency: {fstop}. Stop frequency must be between 1e3 and 10e6 Hz.")
		if order not in [1, 2]:
			raise ValueError(f"Invalid order: {order}. Order must be either 1 (voltage bias) or 2 (voltage steps).")
		cmd = f':CVU:SWEEP:FREQ {fstart}, {fstop}, {order}'
		self.instrument.write(cmd)

	# :CVU:SWEEP:LISTDCV
	# This command configures the selected CVU card to sweep arbitrary DC voltage points and sample
	# Z measurements.
	# Usage
	# :CVU:SWEEP:LISTDCV pt1, pt2, pt3 ... ptn
	# pt1, pt2, pt3 … ptn Sweep points: 1 to 4096
	# Details
	# Only starting voltage sweep points are set with this command.
	# The other parameters (AC voltage level, frequency, and so on) are set by their
	# respective commands.
	def configure_cvu_sweep_list_dc_voltage(self, *points):
		# Example: ":CVU:SWEEP:LISTDCV 0, 1, 2, 3" to configure the selected CVU card to sweep arbitrary DC voltage points 0 V, 1 V, 2 V, and 3 V
		if len(points) < 1 or len(points) > 4096:
			raise ValueError(f"Invalid number of points: {len(points)}. Number of points must be between 1 and 4096.")
		for point in points:
			if not isinstance(point, (int, float)):
				raise ValueError(f"Invalid point value: {point}. Point values must be numbers.")
		points_str = ', '.join(map(str, points))
		cmd = f':CVU:SWEEP:LISTDCV {points_str}'
		self.instrument.write(cmd)

	# :CVU:TEST:ABORT
	# This command stops a running KXCI CVU test.
	# Usage
	# :CVU:TEST:ABORT
	# Details
	# This command terminates all ongoing processes and returns the 4200A-SCS to the idle
	# state. Data that results from the ongoing processes may be corrupt.
	# This command is not appropriate to stop a CVU KXCI test running from a remote UTM. For
	# more information, refer to Calling KULT user libraries remotely (on page 4-6).
	# This command is not valid in user mode.
	def abort_cvu_test(self):
		# Example: ":CVU:TEST:ABORT" to stop a running KXCI CVU test
		cmd = ':CVU:TEST:ABORT'
		self.instrument.write(cmd)

	# :CVU:TEST:RUN
	# This command starts a CVU test on the specified card.
	# Usage
	# :CVU:TEST:RUN
	# Details
	# Use the serial poll byte to determine when not busy or data ready.
	def run_cvu_test(self):
		# Example: ":CVU:TEST:RUN" to start a CVU test on the specified card
		cmd = ':CVU:TEST:RUN'
		self.instrument.write(cmd)
		# Optionally, you can wait for the instrument to be ready or not busy
		# This can be done using a serial poll or other methods depending on the instrument's capabilities

	# :CVU:ACV
	# This command sets the AC drive level for specified CVU card.
	# Usage
	# :CVU:ACV aclevel
	# aclevel AC voltage level (default 0.03):
	# ▪ 4210-CVU: 0.01 to 0.1
	# ▪ 4215-CVU: 0.01 to 1
	# Details
	# If the instrument is in user mode, this takes immediate effect.
	# If the instrument is in system mode, the value is buffered for use in all sweeps except the AC
	# voltage sweep. The voltage level for the AC voltage sweep is set using the
	# :CVU:SWEEP:ACV command.
	def set_cvu_ac_voltage(self, aclevel):
		# Example: ":CVU:ACV 0.05" to set the AC drive level for the specified CVU card to 0.05 V
		if self.cvu_model == '4210':
			if not (0.01 <= aclevel <= 0.1):
				raise ValueError(f"Invalid AC voltage level for 4210-CVU: {aclevel}. Must be between 0.01 and 0.1 V.")
		elif self.cvu_model == '4215':
			if not (0.01 <= aclevel <= 1.0):
				raise ValueError(f"Invalid AC voltage level for 4215-CVU: {aclevel}. Must be between 0.01 and 1.0 V.")
		else:
			raise ValueError("Unsupported CVU model.")
		cmd = f':CVU:ACV {aclevel}'

	# :CVU:ACZ:RANGE
	# This command sets the AC measurement range for the specified CVU card.
	# Usage
	# :CVU:ACZ:RANGE range
	# range Range in amps:
	# ▪ Auto: 0
	# ▪ 1 μA: 1e-6
	# ▪ 30 μA: 30e-6
	# ▪ 1 mA: 1e-3 (default)
	def set_cvu_ac_measurement_range(self, range_value):
		# Example: ":CVU:ACZ:RANGE 1e-6" to set the AC measurement range for the specified CVU card to 1 μA
		if range_value not in [0, 1e-6, 30e-6, 1e-3]:
			raise ValueError(f"Invalid AC measurement range: {range_value}. Valid ranges are Auto (0), 1 μA (1e-6), 30 μA (30e-6), and 1 mA (1e-3).")
		cmd = f':CVU:ACZ:RANGE {range_value}'
		self.instrument.write(cmd)

	# :CVU:CHANNEL
	# This command selects the CVU card on which subsequent CVU commands will act.
	# Usage
	# :CVU:CHANNEL chan
	# chan CVU card on which KXCI CVU commands act (default 1)
	# Details
	# The majority of systems only have one CVU card. You can use this command to configure
	# multiple cards
	def select_cvu_channel(self, chan):
		# Example: ":CVU:CHANNEL 2" to select CVU card 2 for subsequent commands
		if chan not in [1, 2]:
			raise ValueError(f"Invalid CVU channel: {chan}. Valid channels are 1 and 2.")
		cmd = f':CVU:CHANNEL {chan}'
		self.instrument.write(cmd)

	# :CVU:CONFIG:ACVHI
	# This command defines the source terminal (AC only) for the CVU test.
	# Usage
	# :CVU:CONFIG:ACVHI source
	# source The source terminal to be used:
	# ▪ HCUR/HPOT (default): 1
	# ▪ LCUR/LPOT: 2
	def set_cvu_config_acvhi(self, source):
		# Example: ":CVU:CONFIG:ACVHI 1" to set the source terminal for the CVU test to HCUR/HPOT
		if source not in [1, 2]:
			raise ValueError(f"Invalid source terminal: {source}. Valid sources are HCUR/HPOT (1) and LCUR/LPOT (2).")
		cmd = f':CVU:CONFIG:ACVHI {source}'
		self.instrument.write(cmd)

	# :CVU:CONFIG:DCVHI
	# This command defines the source terminal (DC only) for the CVU test.
	# Usage
	# :CVU:CONFIG:DCVHI source
	# source The source terminal to be used:
	# ▪ HCUR/HPOT (default): 1
	# ▪ LCUR/LPOT: 2
	def set_cvu_config_dcvhi(self, source):
		# Example: ":CVU:CONFIG:DCVHI 1" to set the source terminal for the CVU test to HCUR/HPOT
		if source not in [1, 2]:
			raise ValueError(f"Invalid source terminal: {source}. Valid sources are HCUR/HPOT (1) and LCUR/LPOT (2).")
		cmd = f':CVU:CONFIG:DCVHI {source}'
		self.instrument.write(cmd)

	# :CVU:CORRECT
	# This command enables open, short, and load correction for the specified CVU card.
	# Usage
	# :CVU:CORRECT open, short, load
	# open Off: 0
	# On: 1
	# short Off: 0
	# On: 1
	# load Off: 0
	# On: 1
	# Details
	# Each of the parameters is a Boolean (0 = off, 1 = on).
	# This command enables the values set by the :CVU:CABLE:COMP:LOAD,
	# :CVU:CABLE:COMP:OPEN, and :CVU:CABLE:COMP:SHORT commands.
	# To disable the correction setting values, before sending :CVU:CORRECT, you must send
	# :CVU:RESET to set the CVU to its default settings.
	# Example 1
	# :CVU:RESET
	# :CVU:MEASZ?
	# :CVU:CORRECT 1,0,0
	# :CVU:MEASZ?
	# :CVU:RESET
	# :CVU:MODEL 2
	# :CVU:CORRECT 0,1,0
	# :CVU:MEASZ?
	# Reset the CVU to its default state.
	# Trigger and return a single measurement.
	# Enable open compensation.
	# Trigger and return a single measurement.
	# Reset the CVU to its default state.
	# Set the CVU model to Cp, Gp.
	# Enable short compensation and disable open compensation.
	# Trigger and return a single measurement.
	# Example 2
	# :CVU:RESET
	# :CVU:MEASZ?
	# :CVU:CORRECT 1,0,0
	# :CVU:MEASZ?
	# :CVU:CORRECT 1,1,0
	# :CVU:MEASZ?
	# Reset the CVU to its default state.
	# Trigger and return a single measurement.
	# Enable open compensation.
	# Trigger and return a single measurement.
	# Enable short compensation while keeping open compensation enabled.
	# Trigger and return a single measurement.
	def set_cvu_correction(self, open_corr, short_corr, load_corr):
		# Example: ":CVU:CORRECT 1, 0, 1" to enable open correction, disable short correction, and enable load correction
		if open_corr not in [0, 1]:
			raise ValueError(f"Invalid open correction value: {open_corr}. Valid values are 0 (off) and 1 (on).")
		if short_corr not in [0, 1]:
			raise ValueError(f"Invalid short correction value: {short_corr}. Valid values are 0 (off) and 1 (on).")
		if load_corr not in [0, 1]:
			raise ValueError(f"Invalid load correction value: {load_corr}. Valid values are 0 (off) and 1 (on).")
		cmd = f':CVU:CORRECT {open_corr}, {short_corr}, {load_corr}'
		self.instrument.write(cmd)

	# :CVU:DCV
	# This command sets the DC bias voltage for the specified CVU card.
	# Usage
	# :CVU:DCV dclevel
	# dclevel DC bias voltage: −30 to +30 (default is 0)
	# Details
	# In user mode, this takes immediate effect.
	# In system mode, the value is buffered for use in frequency and AC voltage sweeps and DC
	# bias/sample.
	def set_cvu_dc_voltage(self, dclevel):
		# Example: ":CVU:DCV 5" to set the DC bias voltage for the specified CVU card to 5 V
		if not (-30 <= dclevel <= 30):
			raise ValueError(f"Invalid DC voltage level: {dclevel}. DC voltage level must be between -30 and +30 V.")
		cmd = f':CVU:DCV {dclevel}'
		self.instrument.write(cmd)

	# :CVU:DCV:OFFSET
	# This command applies an offset value to the DC low terminal.
	# Usage
	# :CVU:DCV:OFFSET offsetv
	# offsetv Offset voltage: −30 to +30
	# Details
	# Voltage offset to apply while sampling Z measurements.
	def set_cvu_dc_voltage_offset(self, offsetv):
		# Example: ":CVU:DCV:OFFSET 2" to apply a DC voltage offset of 2 V
		if not (-30 <= offsetv <= 30):
			raise ValueError(f"Invalid DC voltage offset: {offsetv}. DC voltage offset must be between -30 and +30 V.")
		cmd = f':CVU:DCV:OFFSET {offsetv}'
		self.instrument.write(cmd)

	# :CVU:FREQ
	# This command sets the frequency for the AC source for the specified CVU card.
	# Usage
	# CVU:FREQ freq
	# freq Range (Hz): 1000 to 10000000; default is 100000
	# Details
	# Values that fall between supported frequencies are coerced to the nearest
	# supported frequency.
	# For the CVU-4210, values that fall between the supported discrete frequencies are coerced
	# to the closest discrete frequency.
	# For the CVU-4215, the values are adjusted to 1 kHz resolution.
	def set_cvu_frequency(self, freq):
		# Example: ":CVU:FREQ 1e6" to set the frequency for the AC source for the specified CVU card to 1 MHz
		if not (1e3 <= freq <= 10e6):
			raise ValueError(f"Invalid frequency: {freq}. Frequency must be between 1e3 and 10e6 Hz.")
		cmd = f':CVU:FREQ {freq}'
		self.instrument.write(cmd)


	# :CVU:LENGTH
	# This command selects the cable length for the specified CVU card.
	# Usage
	# :CVU:LENGTH len
	# len The cable length:
	# ▪ 0: 0 m (no cable compensation)
	# ▪ 1.5: 1.5 m CVU cable
	# ▪ 3.0: 3.0 m CVU cable
	# ▪ 4.0: Custom
	# ▪ 5.0: 1.5 m CVIV cable; 2-wire mode
	# ▪ 6.0: 1.5 m CVU to CVIV cable with 0.75 m CVIV to DUT cable; 4-wire mode
	# ▪ 7.0: Blue 1.5 m
	def set_cvu_cable_length(self, length):
		# Example: ":CVU:LENGTH 1.5" to select the cable length for the specified CVU card to 1.5 m
		if length not in [0, 1.5, 3.0, 4.0, 5.0, 6.0, 7.0]:
			raise ValueError(f"Invalid cable length: {length}. Valid lengths are 0 (no compensation), 1.5 m, 3.0 m, 4.0 m (custom), 5.0 m (2-wire mode), and 6.0 m (4-wire mode).")
		cmd = f':CVU:LENGTH {length}'
		self.instrument.write(cmd)

	# :CVU:MODE
	# This command sets the mode to User or System.
	# Usage
	# :CVU:MODE mode
	# mode The mode:
	# ▪ User mode: 0
	# ▪ System mode: 1
	def set_cvu_mode(self, mode):
		# Example: ":CVU:MODE 1" to set the mode to System
		if mode not in [0, 1]:
			raise ValueError(f"Invalid mode: {mode}. Valid modes are User (0) and System (1).")
		cmd = f':CVU:MODE {mode}'
		self.instrument.write(cmd)

	# :CVU:MODEL
	# This command sets the measurement model for the selected CVU card.
	# Usage
	# :CVU:MODEL model
	# model The model:
	# ▪ 0: Z, theta
	# ▪ 1: R + jx (default)
	# ▪ 2: Cp, Gp
	# ▪ 3: Cs, Rs
	# ▪ 4: Cp, D
	# ▪ 5: Cs, D
	# ▪ 7: Y, theta
	def set_cvu_model(self, model):
		# Example: ":CVU:MODEL 2" to set the measurement model for the selected CVU card to Cp, Gp
		if model not in [0, 1, 2, 3, 4, 5, 7]:
			raise ValueError(f"Invalid model: {model}. Valid models are 0 (Z, theta), 1 (R + jx), 2 (Cp, Gp), 3 (Cs, Rs), 4 (Cp, D), 5 (Cs, D), and 7 (Y, theta).")
		cmd = f':CVU:MODEL {model}'
		self.instrument.write(cmd)

	# :CVU:OUTPUT
	# This command enables or disables the CVU output.
	# Usage
	# :CVU:OUTPUT state
	# state The state of the CVU output:
	# ▪ Enable CVU output: 1
	# ▪ Disable the CVU output: 0

	def set_cvu_output_state(self, state):
		# Example: ":CVU:OUTPUT 1" to enable the CVU output
		if state not in [0, 1]:
			raise ValueError(f"Invalid state: {state}. Valid states are 0 (disable) and 1 (enable).")
		cmd = f':CVU:OUTPUT {state}'
		self.instrument.write(cmd)


	# :CVU:RESET
	# This command sends a soft reset to the specified card.
	# Usage
	# :CVU:RESET
	# Details
	# This command places the card in its default state.
	# The following parameters are reset to the following default values:
	# • DC voltage: 0 V
	# • AC voltage: 0.03 V (30 mV)
	# • Frequency: 100000 Hz (100 kHz)
	# • Model: R + jx
	# • Range: 0.001 A (1 mA)
	# *RST executes the :CVU:RESET command.

	def reset_cvu(self):
		# Example: ":CVU:RESET" to send a soft reset to the specified CVU card
		cmd = ':CVU:RESET'
		self.instrument.write(cmd)
		# Optionally, you can wait for the instrument to be ready or not busy
		# This can be done using a serial poll or other methods depending on the instrument's capabilities

	# :CVU:SPEED
	# This command sets the measurement speed for the selected CVU card.
	# Usage
	# :CVU:SPEED speed
	# :CVU:SPEED 3, delay_factor, filter_factor, aperture
	# speed Applies the speed selection:
	# ▪ Fast: 0
	# ▪ Normal: 1
	# ▪ Quiet: 2
	# ▪ Custom: 3
	# delay_factor Delay factor (Custom only): 0 to 100; see Details
	# filter_factor Filter factor (Custom only): 0 to 707; see Details
	# aperture Aperture (Custom only) in PLCs: 0.006 to 10.002
	def set_cvu_speed(self, speed, delay_factor=None, filter_factor=None, aperture=None):
		# Example: ":CVU:SPEED 2" to set the measurement speed for the selected CVU card to Quiet
		if speed not in [0, 1, 2, 3]:
			raise ValueError(f"Invalid speed: {speed}. Valid speeds are Fast (0), Normal (1), Quiet (2), and Custom (3).")

		if speed == 3:  # Custom speed
			if delay_factor is None or filter_factor is None or aperture is None:
				raise ValueError("For Custom speed, delay_factor, filter_factor, and aperture must be provided.")
			if not (0 <= delay_factor <= 100):
				raise ValueError(f"Invalid delay factor: {delay_factor}. Must be between 0 and 100.")
			if not (0 <= filter_factor <= 707):
				raise ValueError(f"Invalid filter factor: {filter_factor}. Must be between 0 and 707.")
			if not (0.006 <= aperture <= 10.002):
				raise ValueError(f"Invalid aperture: {aperture}. Must be between 0.006 and 10.002 PLCs.")
			cmd = f':CVU:SPEED {speed}, {delay_factor}, {filter_factor}, {aperture}'
		else:
			cmd = f':CVU:SPEED {speed}'

		self.instrument.write(cmd)

	# :CVU:TEST:COMPLETE?
	# This command queries the status of the test.
	# Usage
	# :CVU:TEST:COMPLETE?
	def is_cvu_test_complete(self):
		# Example: ":CVU:TEST:COMPLETE?" to query the status of the test
		print("Enviamos comando")
		time.sleep(5)  # Optional delay to ensure command is sent
		cmd = ':CVU:TEST:COMPLETE'
		response = self.instrument.query(cmd)
		print("comando enviado")
		time.sleep(5)  # Optional delay to ensure response is received
		if response.strip() == '1':
			return True
		elif response.strip() == '0':
			return False
		else:
			raise ValueError(f"Unexpected response from CVU test status query: {response}. Expected '1' for complete or '0' for not complete.")


	def config_CV(self, CV_parameters):
		try:
			# CV_parameters dictionary with:
			# "START" (V) (from -30 to 30), "STOP"(V), "STEP" (V) (from 0.01 to 5V), "OSC" (mV from 5 to 1100), "FREQ" (kHz from 1 to 10000),
			# Optional: "CIRCUIT_MODE" (Series/Paralell), "AVERAGE" (True/False)
			print("config_CV: Configuring CVU with parameters:", CV_parameters)
			# FIRST CHECK PARAMETERS
			if "START" in CV_parameters and "STOP" in CV_parameters and "STEP" in CV_parameters and "OSC" in CV_parameters and "FREQ" in CV_parameters:
				# parameters passed
				if -30 <= CV_parameters["START"] <= 30:
					if -30 <= CV_parameters["STOP"] <= 30:
						if 0.001 <= CV_parameters["STEP"] <= 5 or -5 <= CV_parameters["STEP"] <= -0.001:
							if 5 <= CV_parameters["OSC"] <= 1100:
								if not 1 <= CV_parameters["FREQ"] <= 10000:
									print("FREQUENCY not in range (1kHz, 10000kHz): " + str(CV_parameters["FREQ"]))
									return False
							else:
								print("OSCILLATION LEVEL not in range (5mV, 1100mv): " + str(CV_parameters["OSC"]))
								return False
						else:
							print("STEP VOLTAGE not in range (0.001V, 5V): " + str(CV_parameters["STEP"]))
							return False

					else:
						print("STOP BIAS not in range (-35V, 35V): " + str(CV_parameters["STOP"]))
						return False
				else:
					print("START BIAS not in range (-35V, 35V): " + str(CV_parameters["START"]))
					return False
			else:
				print("Parameters config CV not passed!")
				return False

			PN = -1
			if CV_parameters["START"] > CV_parameters["STOP"]:
				PN = 1

			# clear buffer
			self.clear_buffer()

			# set data ready bit
			self.instrument.write('DR1')

			self.reset_cvu()  # Reset CVU to default state

			# system mode
			self.set_cvu_mode(1)

			# enable zero correction
			self.set_cvu_correction(
				int(CV_parameters.get("CORRECT_OPEN", 0)),
				int(CV_parameters.get("CORRECT_SHORT", 0)),
				int(CV_parameters.get("CORRECT_LOAD", 0))
			)

			# circuit mode to parallel or series
			if "CIRCUIT_MODE" in CV_parameters:
				if CV_parameters["CIRCUIT_MODE"].lower() == "series":
					self.set_cvu_config_acvhi(1)
					# CP-GP model (2) or Cs-Rs model (3)
					self.set_cvu_model(3)
				elif CV_parameters["CIRCUIT_MODE"].lower() == "parallel":
					self.set_cvu_config_acvhi(2)
					# CP-GP model (2) or Cs-Rs model (3)
					self.set_cvu_model(2)
				else:
					print("Invalid CIRCUIT_MODE. Use 'Series' or 'Parallel'.")
					return False



			# Quiet speed as default
			speed = {"fast": 0, "normal": 1, "quiet": 2, "custom": 3}.get(
				CV_parameters.get("SPEED", "quiet").lower(), 2)

			self.set_cvu_speed(speed)

			# 1.5 m CVU cable
			self.set_cvu_cable_length(float(CV_parameters.get("CORRECTION_CABLE", 1.5)))

			# auto measurement range
			self.set_cvu_ac_measurement_range(0)

			# 100mV AC excitation -> 0.1V for 4210-CVU, 1V for 4215-CVU
			self.set_cvu_ac_voltage(CV_parameters['OSC']/(1000 if self.cvu_model == '4210' else 100))

			# set frequency
			self.set_cvu_frequency(CV_parameters['FREQ'] * 1000)  # Convert kHz to Hz

			# set DC sweep parameters
			self.configure_cvu_sweep_dc_voltage(CV_parameters['START'], CV_parameters['STOP'], CV_parameters['STEP'])

			# sweep delay
			self.set_cvu_delay_sweep(CV_parameters['SWEEP_DELAY'])  # Configurar el retraso del barrido a 0.0 segundos

			return True

		except Exception as e:
			print(f"Error configuring CV sweep: {e}")
			return False

	def config_CW(self, CW_parameters):
		try:
			print("config_CW: Configuring CVU for CW sweep with parameters:", CW_parameters)

			# Validar parámetros esperados
			if "START" in CW_parameters and "STOP" in CW_parameters and "OSC" in CW_parameters and "BIAS" in CW_parameters:
				if 5 <= CW_parameters["OSC"] <= 1100:
					if not 1 <= CW_parameters["START"] <= 10000 or not 1 <= CW_parameters["STOP"] <= 10000:
						print("FREQUENCY range must be within 1kHz to 10MHz")
						return False
				else:
					print("OSCILLATION LEVEL not in range (5mV, 1100mV): " + str(CW_parameters["OSC"]))
					return False
			else:
				print("Parameters config CW not passed!")
				return False

			# Limpiar buffers
			self.clear_buffer()

			# Resetear CVU
			self.reset_cvu()

			# Modo CVU
			self.set_cvu_mode(1)

			# Corrección (si se solicita)
			self.set_cvu_correction(
				int(CW_parameters.get("CORRECT_OPEN", 0)),
				int(CW_parameters.get("CORRECT_SHORT", 0)),
				int(CW_parameters.get("CORRECT_LOAD", 0))
			)

			# Modo de circuito
			if CW_parameters.get("CIRCUIT_MODE", "parallel").lower() == "series":
				self.set_cvu_config_acvhi(1)
				self.set_cvu_model(3)  # Cs-Rs
			else:
				self.set_cvu_config_acvhi(2)
				self.set_cvu_model(2)  # Cp-Gp

			# Velocidad
			speed = {"fast": 0, "normal": 1, "quiet": 2, "custom": 3}.get(
				CW_parameters.get("SPEED", "quiet").lower(), 2)
			self.set_cvu_speed(speed)

			# Longitud de cable
			self.set_cvu_cable_length(float(CW_parameters.get("CORRECTION_CABLE", 1.5)))

			# Rango automático
			self.set_cvu_ac_measurement_range(0)

			# Nivel de excitación (mV → V)
			self.set_cvu_ac_voltage(CW_parameters["OSC"] / (1000 if self.cvu_model == '4210' else 100))

			# Fijar el voltaje de polarización DC
			self.set_cvu_dc_voltage(CW_parameters["BIAS"])

			# Configurar barrido de frecuencia
			start_freq = CW_parameters["START"] * 1000  # kHz a Hz
			stop_freq = CW_parameters["STOP"] * 1000

			# Ejemplo: barrido lineal
			self.configure_cvu_sweep_frequency(start_freq, stop_freq, order=1)

			self.set_cvu_delay_sweep(CW_parameters['SWEEP_DELAY'])

			return True

		except Exception as e:
			print(f"Error configuring CW sweep: {e}")
			return False




	def measure_CV(self, CV_parameters, timeout=20000, hysteresis=False):
		"""
		Perform CV (Capacitance vs Voltage) measurement using CVU.

		:param CV_parameters: CV parameters dictionary
		:param timeout: instrument timeout in milliseconds
		:param hysteresis: hysteresis mode (default False)
		:return: Frequency, Capacitance (Cp or Cs), Conductance (Gp or Rs)
		"""
		self.run_cvu_test()
		print("measure_CV: Waiting for data to be ready...")
		self.data_ready(timeout)  # Wait for the measurement to be ready
		print("measure_CV: Data should be ready now.")
		# Read the data from the instrument
		xy = self.instrument.query(":CVU:DATA:Z?")  # queries readings of Cp-Gp

		Volt = self.instrument.query(":CVU:DATA:VOLT?")

		# close instrument to avoid errors in console if not hysteresis mode
		if not hysteresis:
			self.instrument.close()

		sep = ";"  # separator between Cp-Gp or Cs-Rs values

		voltage = Volt.split(",")  # splits voltage list at commas
		# replace empty strings in voltage
		voltage = [float(v) for v in voltage if v != ""]
		xyList = xy.split(",")  # splits Cp-Gp list or Cs-Rs list at commas

		x = []
		y = []
		for z in xyList:
			if z != "":
				x.append(float(z.split(sep)[0]))
				y.append(float(z.split(sep)[1]))

		print(f"Voltage: {voltage}")

		# Parallel mode: Cp = C, Gp = G
		x_text = "Capacitance (Cp)"
		y_text = "Conductance (Gp)"
		if CV_parameters.get("CIRCUIT_MODE", "").lower() == "series":
			# Series mode: Cs = C, Rs = G
			x_text = "Capacitance (Cs)"
			y_text = "Resistance (Rs)"

		print(f"{x_text}: {x}")
		print(f"{y_text}: {y}")

		# check range of values
		if not (len(voltage) == len(x) == len(y)):
			raise ValueError(f"Length of voltage {len(voltage)}, {x_text} {len(x)}, and {y_text} {len(y)} do not match.")

		return voltage, x, y

	def measure_CW(self, CW_parameters, timeout=20000):
		"""
		Perform CW (Capacitance vs Frequency) measurement using CVU.

		Returns:
			freq: list of frequency values (Hz)
			cap: list of capacitance values (Cp or Cs)
			cond: list of conductance or resistance values (Gp or Rs)
		"""
		self.run_cvu_test()
		print("measure_CW: Waiting for data to be ready...")
		self.data_ready(timeout)  # Wait for measurement to complete
		print("measure_CW: Data should be ready now.")

		# Query impedance data (Capacitance - Conductance/Resistance)
		raw_data = self.instrument.query(":CVU:DATA:Z?")
		freq_data = self.instrument.query(":CVU:DATA:FREQ?")

		self.instrument.close()

		sep = ";"  # Separator between Zx;Zy pairs

		freq_list = [float(f) for f in freq_data.split(",") if f != ""]
		raw_list = [r for r in raw_data.split(",") if r != ""]

		cap = []
		cond = []

		for z in raw_list:
			if z != "":
				try:
					z_real, z_imag = z.split(sep)
					cap.append(float(z_real))
					cond.append(float(z_imag))
				except ValueError as e:
					print(f"Skipping malformed data point: {z} ({e})")

		if not (len(freq_list) == len(cap) == len(cond)):
			raise ValueError(f"Data length mismatch: freq={len(freq_list)}, cap={len(cap)}, cond={len(cond)}")

		mode = CW_parameters.get("CIRCUIT_MODE", "").lower()
		cap_label = "Cp" if mode == "parallel" else "Cs"
		cond_label = "Gp" if mode == "parallel" else "Rs"

		print(f"Frequency: {freq_list}")
		print(f"Capacitance ({cap_label}): {cap}")
		print(f"{'Conductance' if mode == 'parallel' else 'Resistance'} ({cond_label}): {cond}")

		return freq_list, cap, cond


	def data_ready_old(self, timeout_ms=20000):
		time.sleep(timeout_ms/1000)

	def data_ready(self, timeout_ms=20000):
		"""
		Wait for the data ready bit to be set.
		This method checks the data ready bit and waits until it is set or the timeout is reached.
		"""
		start_time = time.time()
		pyvisa.timeout = timeout_ms / 1000.0  # Convert milliseconds to seconds
		while True:
			try:
				data = self.instrument.query(":CVU:DATA:Z?")
				break
			# except timeout
			except pyvisa.VisaIOError as e:
				# clear gpib errors
				time.sleep(1)  # wait for a short time before retrying
				print("Timeout waiting for service request:", e)

		print("Data is ready in time: ", time.time() - start_time)