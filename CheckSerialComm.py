# Simple program to read data from the Arduino serial port
import numpy as np
import serial
import platform
from PlotData import PlotData

plat = platform.platform().lower()
if plat.find('win') != -1:
    print("Windows OS - setting port to COM4 - check this")
    ser = serial.Serial("COM4", 9600)  # Set to the appropriate port
elif plat.find('lin') != -1:
    print("Linux OS - setting port to /dev/ttyUSB0 - check this")
    ser = serial.Serial("/dev/ttyUSB0", 9600)  # Linux port, check this
else:  # Assume Mac OS
    print("Assuming MAC OS - setting port to /dev/ttyUSB0 - check this")
    ser = serial.Serial("/dev/ttyUSB0", 9600)  # Linux port, check this
ser.flushInput()
# import sys
# sys.exit(0)
k = 0
numValues=10
x = np.empty(shape=numValues, dtype=float)  # 3 element array
for k in range(numValues):
    linein = ser.readline()
    xs=str(linein)
    xf=float(xs[2:-3])
    x[k]=xf
PlotData(x)