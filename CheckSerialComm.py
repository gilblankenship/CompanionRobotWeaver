# Simple program to read data from the Arduino serial port
import serial
ser = serial.Serial("COM4",9600) # Set to the appropriate port
# ser = serial.Serial("/dev/ttyUSB0",9600) # Linux port, check this
ser.flushInput()
k=0
while k<10:
    linein = ser.readline()
    print(k,',',str(linein))
    k=k+1
