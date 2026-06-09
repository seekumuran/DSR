import serial

ser = serial.Serial("COM3", 9600)

while True:

    packet = ser.read(11)

    if packet[0] == 0xAA:
        print("VALID DSSX STREAM")
    else:
        print("STREAM ERROR")
