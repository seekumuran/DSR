import serial

ser = serial.Serial("COM3", 9600)

while True:

    packet = ser.read(11)

    print("RAW:", packet.hex())
