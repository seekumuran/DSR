import serial

ser = serial.Serial("COM3", 9600)

while True:

    packet = ser.read(11)

    print("====================")
    print(f"SYNC    : {hex(packet[0])}")
    print(f"BTN1    : {bin(packet[3])}")
    print(f"BTN2    : {bin(packet[4])}")
    print(f"LX      : {packet[5]}")
    print(f"LY      : {packet[6]}")
