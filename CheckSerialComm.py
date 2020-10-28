# Simple program to read data from the Arduino serial port
import numpy as np
import serial
import platform
from PlotData import PlotData

plat = platform.platform().lower()
if plat.find('win') != -1:
    print("Windows OS - setting port to COM4 or COM6 - check this")
    ser = serial.Serial("COM4", 9600)  # Port for Arduino NANO
    # ser = serial.Serial("COM6", 9600)  # Port for Arduino NANO BLE
elif plat.find('lin') != -1:
    print("Linux OS - setting port to /dev/ttyUSB0 - check this")
    ser = serial.Serial("/dev/ttyUSB0", 9600)  # Linux port, check this
else:  # Assume Mac OS
    print("Assuming MAC OS - setting port to /dev/ttyUSB0 - check this")
    ser = serial.Serial("/dev/ttyUSB0", 9600)  # Linux port, check this
ser.flushInput()
# import sys
# sys.exit(0)
numValues=10
x = np.empty(shape=numValues, dtype=float)  # initialize empty array
print("Start loop")
for k in range(numValues):
    print(k)
    linein = ser.readline()
    print(linein)
    xs=str(linein)
    xf=float(xs[2:-3])
    x[k]=xf
PlotData(x)