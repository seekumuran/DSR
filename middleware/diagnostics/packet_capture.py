import serial

ser = serial.Serial("COM3", 9600)

capture = open("capture.bin", "wb")

while True:

    packet = ser.read(11)

    capture.write(packet)
