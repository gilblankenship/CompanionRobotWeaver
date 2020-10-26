# Simple program to read data from the Arduino serial port
import struct

import serial
ser = serial.Serial("COM4",9600) # Set to the appropriate port
# ser = serial.Serial("/dev/ttyUSB0",9600) # Linux port, check this
ser.flushInput()
k=0
while k<10:
    linein = ser.readline()
    x = struct.unpack('f', linein)
    if x<0:
        start, end = 2, 9
    else:
        start, end = 2, 9
    rang=[*range(start, end)];
    print(k,',',str(x)[rang])
    k=k+1
