import serial
ser = serial.Serial("COM4",9600)
ser.flushInput()
k=0
while k<5:
    linein = ser.readline()
    print(k,str(linein))
    # if len(str(linein))==7:
    #     print(str(k), ' ',len(str(linein)),' ',str(linein)[2:4])
    # else:
    #     print(str(k), ' ',len(str(linein)),' ',str(linein)[2:3])
    # print(str(linein)[2:4])
    # print(len(str(linein)),' ',str(linein))
    k=k+1
