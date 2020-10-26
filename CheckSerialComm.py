import serial
ser = serial.Serial("COM4",9600)
ser.flushInput()
k=0

while k<4:
    linein = ser.readline()
    # print(str(linein)[2:4])
    print(len(str(linein)),' ',str(linein))
    k=k+1
