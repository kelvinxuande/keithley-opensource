"""
Initialize and configure input and output settings 
"""

# Hardware check (once at start):
import serial
import serial.tools.list_ports
import visa
ports = list(serial.tools.list_ports.comports())               
hardware_status = [0,0]                                        
for p in ports:
    if ("CH340" in p[1]):
        arduinoPort = p[0]
    if ("Arduino" in p[1]):
        arduinoPort = p[0]
try:
    arduinoUSB = serial.Serial('%s' % arduinoPort, 9600, timeout=None)
    arduinoUSB.flushInput()
    arduinoUSB.flushOutput()
    hardware_status[0] = 1	
except NameError as error:
    pass

try:
    resourceString = 'USB0::0x05E6::0x6500::04391587::INSTR'
    rm = visa.ResourceManager()
    scope = rm.open_resource(resourceString)
    scope.write_termination = '\n'
    scope.clear()                                             
    idn_response = scope.query('*IDN?')                     
    print('Hello, I am ' + idn_response)
    scope.clear()
    scope.write_termination = '\n'
    hardware_status[1] = 1
except:
    pass

# For demostration purposes, set both DMM and arduino push button status to be 'true' - connected.
# Commenting out the two lines below will enable full implementation	
hardware_status[1] = 1 # test code
hardware_status[0] = 1 # test code

# Fixed variables:
from datetime import datetime
excelFileName = datetime.now().strftime('outputs/DMM6500_Measurements %d%m%Y - %H%M.csv')
startDate = datetime.now().strftime('%d/%m/%Y')
startTime = datetime.now().strftime('%H:%M')

# Declare user updated variables, done once (for windows controller):
printerNumber = ""
designName = ""
printParameters = ""
measMode = [0,0]

numberOftimes = 0
period = 0