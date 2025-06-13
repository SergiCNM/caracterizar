# CONTACT PROGRAM : contact_test variable
# -1 : first die, init program
# return 0: not contact
# return 1: some in contact but not all (be carefull)
# return 2: all in contact
# return 3: abort test

global kbridge, commbridge
global contact_test, contact_errors, test_status, actual_height

from PBaccesslib.main import chip_test
from PBaccesslib.keithley_bridge import KBridge
from PBaccesslib.comm_bridge import CommBridge


LIBPATH = "/Users/User/Desktop/linda-lib.dll"
DATA_FOLDER_PATH = "/Users/User/Desktop/data"

# contact_test = -1 (beggining)
# FIRST DIE (INIT)
if str(dieActual)=="1" and str(moduleActual)=="1" and contact_test==-1:
	""" Start bridge and instrument"""
	IP_commbridge = "192.168.1.101"
	IP_kbridge = "192.168.1.170"

	SYNC = 32000
	ASYNC = 32001
	KEITHLEY_ADRESS = "TCPIP0::"+IP_kbridge+"::inst0::INSTR"

	kbridge = KBridge(KEITHLEY_ADRESS)
	commbridge = CommBridge(IP_commbridge, SYNC, ASYNC, LIBPATH)

	kbridge.clear_inst()
	kbridge.set_values(50e-3, 100e-3, 20, 2.5) # a_l, b_l, rnge, level
	contact_errors = 0
	

# -----------
# TESTING DIE
# -----------
kbridge.set_2v5_on() # keithley ON
bin_array, test_output = kbridge.read_compare(2.2, 10e-3, 2.2, 25e-3) # READ & COMPARE
t_out = commbridge.touch_down() # TOUCHDOWN
kbridge.set_2v5_off() # keithley OFF

def return_contact_test(bin_array, test_output, t_out):
	# return 0: not contact
	# return 1: some in contact but not all (be carefull)
	# return 2: all in contact
	# return 3: abort test
	global contact_test, test_status
	
	contact_test = -1
	max_contact_errors = 3

	if bin_array==[1,0,1,0] and t_out==(0,3):
		contact_test = 0

	if bin_array[0]==1 and bin_array[2]==1 and (t_out==(0,1) or t_out==(0,2)):
		contact_test = 1

	if bin_array==[1,1,1,1] and t_out==(0,0):
		contact_test = 2

	if bin_array[0]==0 or bin_array[2]==0 or (bin_array[0]==1 and bin_array[2]==1 and t_out==(0,0) and (bin_array==[1,0,1,1] or bin_array==[1,1,1,0])):
		contact_test = 3

	if contact_test==-1:
		contact_test = 3

	if contact_test==3:
		contact_errors += 1

	if contact_errors==max_contact_errors:
		test_status.status = "ABORTED"

	# communication error
	if t_out[0]==1:
		test_status.status = "ABORTED"		

return_contact_test(bin_array, test_output, t_out)

