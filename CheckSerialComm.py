# Simple program to read data from the Arduino serial port
import struct
import serial
import platform

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

# import sys
# sys.exit(0)

ser.flushInput()
k = 0
while k < 10:
    linein = ser.readline()
    print(k, ',', str(linein))
    # x = struct.unpack('f', linein)
    # if x < 0:
    #     start, end = 2, 9
    # else:
    #     start, end = 2, 9
    # rang = [*range(start, end)];
    # print(k, ',', str(x)[rang])
    k = k + 1
