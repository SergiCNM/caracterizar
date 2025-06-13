# from instrcomms import Communications
import pyvisa
import visa

from  pyvisa.constants import EventType, EventMechanism
import csv, time

INST_RESOURCE_STR = "GPIB0::17::INSTR"  # instrument resource string, obtained from NI-VISA Interactive
#my4200 = Communications(INST_RESOURCE_STR)  # opens the resource manager in PyVISA with the corresponding instrument resource string
print("Connecting to Keithley 4200A-SCS...")
rm = pyvisa.ResourceManager()  # creates a resource manager object
my4200 = rm.open_resource(INST_RESOURCE_STR)  # opens the instrument with the specified resource string and settings

# my4200._instrument_object = rm.open_resource(INST_RESOURCE_STR, read_termination='\r\n', write_termination='\r\n', timeout=1)  # opens the instrument with the specified resource string and settings

# my4200.connect()  # opens connections to the 4200A-SCS
print("Connected to:", my4200.query("*IDN?"))  # queries the instrument for its identification string

my4200.write("BC")
my4200.write("DR1")
# my4200._instrument_object.enable_event(
#     EventType.service_request,
#     EventMechanism.all
# )
my4200.write(":CVU:RESET")
my4200.write(":CVU:MODE 1")
my4200.write(":CVU:MODEL 2")
my4200.write(":CVU:SPEED 1")
my4200.write(":CVU:ACZ:RANGE 0")
my4200.write(":CVU:FREQ 1E6")
my4200.write(":CVU:SWEEP:DCV 5, -5, -0.2")
my4200.write(":CVU:DELAY:SWEEP 0.1")
my4200.write(":CVU:TEST:RUN")
print("Running CVU test...")
time.sleep(1)
# my4200._instrument_object.wait_for_srq()  # waits until data is ready by waiting for serial request coming from the 4200A-SCS

while True:
    try:
        # my4200._instrument_object.wait_for_srq(timeout=10000)  # waits for service request (SRQ) from the instrument, with a timeout of 10 seconds
        # my4200._instrument_object.wait_on_event(
        #    EventType.service_request, timeout=10000
        #)  # waits for service request (SRQ) from the instrument, with a timeout of 10 seconds

        # wait until the command CpGp = my4200.query(":CVU:DATA:Z?") doesn't gets an error
        print("Waiting for service request...")
        CpGp = my4200.query(":CVU:DATA:Z?")
        print("Waiting for data to be ready...")
        break
    # except timeout
    except visa.VisaIOError as e:
        # clear gpib errors
        time.sleep(1)  # wait for a short time before retrying
        print("Timeout waiting for service request:", e)


CpGp = my4200.query(":CVU:DATA:Z?")  # queries readings of Cp-Gp
Volt = my4200.query(":CVU:DATA:VOLT?")  # queries readings of Voltage

sep = ";"  # separator between Cp-Gp

VoltList = Volt.split(",")  # splits voltage list at commas
CpGpList = CpGp.split(",")  # splits Cp-Gp list at commas

CapList = []  # list only for capacitance values

for (z) in (CpGpList):  # separates the Cp-Gp list into only the Cp values, by removing the value after the semi-colon
    CapList.append(z.split(sep, 1)[0])

zipped_list = zip(VoltList, CapList)  # creates iterable zipped list

columns = ["Voltage (V)", "Capacitance (F)"]  # column headers
with open("output.csv", "w", newline="", encoding="utf-8") as f:  # opens and writes csv file
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(zipped_list)

f.close()  # close stream
# my4200.disconnect()  # close communications with the 4200A-SCS
my4200.close()  # close the instrument connection