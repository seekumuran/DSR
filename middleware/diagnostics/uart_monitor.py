import serial

ser = serial.Serial("COM3", 9600)

while True:

    data = ser.read()

    print(hex(data[0]))
