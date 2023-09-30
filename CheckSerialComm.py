# Simple program to read and plot data from the Arduino serial port
import numpy as np
import serial
from PlotData import PlotData # Function in a local file

# import platform
# plat = platform.platform().lower()
# if plat.find('win') != -1:
#     print("Windows OS - setting port to COM4 or COM6 - check this")
#     ser = serial.Serial("COM4", 9600)  # Port for Arduino NANO
#     # ser = serial.Serial("COM6", 9600)  # Port for Arduino NANO BLE
# elif plat.find('lin') != -1:
#     print("Linux OS - setting port to /dev/ttyUSB0 - check this")
#     ser = serial.Serial("/dev/ttyUSB0", 9600)  # Linux port, check this
# else:  # Assume Mac OS
#     print("Assuming MAC OS - setting port to /dev/ttyUSB0 - check this")
#     ser = serial.Serial("/dev/ttyUSB0", 9600)  # Linux port, check this

ser = serial.Serial("/dev/ttyACM0", 9600)  # Linux port, check this
ser.flushInput()
# import sys
# sys.exit(0) # instead of setting a breakpoint
numValues=40
x = np.empty(shape=numValues, dtype=float)  # initialize empty array
for k in range(numValues):
    linein = ser.readline()
    if linein==b'\x00\n': # Not sure why this doesn't convert, crashes here sometimes
        linein=0
    xf=float(linein) # Convert to a floating point variable
    x[k]=xf
print('Received data = ' + str(x))
PlotData(x)