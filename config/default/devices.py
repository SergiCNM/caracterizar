

# ===================================
# =           INSTRUMENTS           =
# ===================================
instruments = {}
# -----------  HP4192A -----------
instruments["HP_4192A"] = {}
instruments["HP_4192A"]["address"] = 'GPIB0::23::INSTR'
instruments["HP_4192A"]["read_termination"] = '\r\n'
instruments["HP_4192A"]["write_termination"] = '\r\n'
instruments["HP_4192A"]["timeout"] = '10000' # 10 segundos medida

# -----------  HP4155B  -----------
instruments["HP_4155B"] = {}
instruments["HP_4155B"]["address"] = 'GPIB0::17::INSTR'
instruments["HP_4155B"]["read_termination"] = '\n'
instruments["HP_4155B"]["write_termination"] = '\n'
instruments["HP_4155B"]["timeout"] = '30000'


# -----------  Keysight B1500  -----------
instruments["Keysight_B1500"] = {}
instruments["Keysight_B1500"]["address"] = 'GPIB0::17::INSTR'
instruments["Keysight_B1500"]["read_termination"] = '\n'
instruments["Keysight_B1500"]["write_termination"] = '\n'
# configure slots  for SMUS used (SMU1, SMU2, SMU3, SMU4)
instruments["Keysight_B1500"]["smu1_slot"] = 'A' # A = slot1
instruments["Keysight_B1500"]["smu2_slot"] = 'B' # B = slot2
instruments["Keysight_B1500"]["smu3_slot"] = 'C' # C = slot3
instruments["Keysight_B1500"]["smu4_slot"] = 'D' # D = slot4
instruments["Keysight_B1500"]["timeout"] = '30000'


# -----------  Keysight B1500LAN  -----------
instruments["Keysight_B1500LAN"] = {}
instruments["Keysight_B1500LAN"]["address"] = 'TCPIP0::169.254.248.246::5025::SOCKET'
instruments["Keysight_B1500LAN"]["read_termination"] = '\n'
instruments["Keysight_B1500LAN"]["write_termination"] = '\n'
#instruments["Keysight_B1500LAN"]["timeout"] = '200000'


# -----------  Keithley 42000-SCS  -----------
instruments["Keithley_4200"] = {}
instruments["Keithley_4200"]["address"] = 'GPIB0::17::INSTR'
instruments["Keithley_4200"]["read_termination"] = '\r\n'
instruments["Keithley_4200"]["write_termination"] = '\r\n'
instruments["Keithley_4200"]["timeout"] = '5000'

# -----------  Keithley 2470  -----------
instruments["Keithley_2470"] = {}
instruments["Keithley_2470"]["address"] = 'GPIB0::4::INSTR'
instruments["Keithley_2470"]["read_termination"] = '\n'
instruments["Keithley_2470"]["write_termination"] = '\n'
instruments["Keithley_2470"]["timeout"] = '50000'
instruments["Keithley_2470"]["buffer_name"] = 'defbuffer1'

# -----------  LINDA  -----------
instruments["DEEPDETECTION_LINDA"] = {}
instruments["DEEPDETECTION_LINDA"]["address"] = 'FPGA'
instruments["DEEPDETECTION_LINDA"]["read_termination"] = ''
instruments["DEEPDETECTION_LINDA"]["write_termination"] = '\n'

# -----------  CNM_RELAYS  -----------
instruments["CNM_RELAYS"] = {}
instruments["CNM_RELAYS"]["port"] = 'COM1'
instruments["CNM_RELAYS"]["baudrate"] = '9600'
instruments["CNM_RELAYS"]["bytesize"] = 8
instruments["CNM_RELAYS"]["stopbits"] = 1
instruments["CNM_RELAYS"]["parity"] = "none"
#instruments["CNM_RELAYS"]["timeout"] = "None"


# ----------- LeCroy W62XS Oscilloscope -----------
instruments["LeCroy_W62XS"] = {}
instruments["LeCroy_W62XS"]["address"] = 'VICP::169.254.228.254::INSTR'
instruments["LeCroy_W62XS"]["read_termination"] = ''
instruments["LeCroy_W62XS"]["write_termination"] = ''
instruments["LeCroy_W62XS"]["timeout"] = '10000' # 10 sec


# -----------  Keysight E4990A  -----------
instruments["Keysight_E4990A"] = {}
instruments["Keysight_E4990A"]["address"] = 'GPIB0::18::INSTR'
instruments["Keysight_E4990A"]["read_termination"] = '\n'
instruments["Keysight_E4990A"]["write_termination"] = '\n'
instruments["Keysight_E4990A"]["timeout"] = '40000'

# ======  End of INSTRUMENTS  =======



# ===============================
# =           PROBERS           =
# ===============================
probers = {}
# -----------  CNM TEST  -----------
probers["CNM_TEST"] = {}
probers["CNM_TEST"]["address"] = 'GPIB0::00::INSTR'
probers["CNM_TEST"]["read_termination"] = '\n'
probers["CNM_TEST"]["write_termination"] = '\n'
probers["CNM_TEST"]["timeout"] = 10
probers["CNM_TEST"]["soft_contact"] = False
probers["CNM_TEST"]["progressive_contact"] = {}
probers["CNM_TEST"]["progressive_contact"]["enable"] = False
probers["CNM_TEST"]["progressive_contact"]["program"] = "testcontact_random.py"
probers["CNM_TEST"]["progressive_contact"]["steps"] = 5 # steps incremental between separation and contact height
probers["CNM_TEST"]["progressive_contact"]["max_tries"] = 2 # max tries when some in contact but not all
probers["CNM_TEST"]["progressive_contact"]["reach_contact"] = False # If True always try to move to contact height if not contact detected
probers["CNM_TEST"]["progressive_contact"]["measure_always"] = True # If True always measure, False not measure if contact not reached

# -----------  MPI TS2000SE  -----------
probers["MPI_TS2000SE"] = {}
probers["MPI_TS2000SE"]["address"] = 'GPIB0::13::INSTR'
probers["MPI_TS2000SE"]["read_termination"] = '\n'
probers["MPI_TS2000SE"]["write_termination"] = '\n'
probers["MPI_TS2000SE"]["timeout"] = 10
probers["MPI_TS2000SE"]["soft_contact"] = True
probers["MPI_TS2000SE"]["progressive_contact"] = {}
probers["MPI_TS2000SE"]["progressive_contact"]["enable"] = False
probers["MPI_TS2000SE"]["progressive_contact"]["program"] = "testcontact_random.py"
probers["MPI_TS2000SE"]["progressive_contact"]["steps"] = 10 # steps incremental between separation and contact height
probers["MPI_TS2000SE"]["progressive_contact"]["max_tries"] = 4 # max tries when some in contact but not all
probers["MPI_TS2000SE"]["progressive_contact"]["reach_contact"] = False # If True always try to move to contact height if not contact detected
probers["MPI_TS2000SE"]["progressive_contact"]["measure_always"] = True # If True always measure, False not measure if contact not reached

# -----------  KARLSUSS PA200  -----------
probers["KARLSUSS_PA200"] = {}
probers["KARLSUSS_PA200"]["address"] = 'GPIB0::1::INSTR'
probers["KARLSUSS_PA200"]["read_termination"] = '\r\n'
probers["KARLSUSS_PA200"]["write_termination"] = '\r\n'
probers["KARLSUSS_PA200"]["timeout"] = 10
probers["KARLSUSS_PA200"]["soft_contact"] = False
probers["KARLSUSS_PA200"]["progressive_contact"] = {}
probers["KARLSUSS_PA200"]["progressive_contact"]["enable"] = False

# ======  End of PROBERS  =======



