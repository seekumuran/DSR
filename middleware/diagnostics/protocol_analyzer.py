import serial

ser = serial.Serial("COM3", 9600)

while True:

    packet = ser.read(11)

    print("==========")
    print(f"SYNC     : {hex(packet[0])}")
    print(f"VERSION  : {packet[1]}")
    print(f"DEVICE   : {packet[2]}")
    print(f"LX       : {packet[5]}")
    print(f"LY       : {packet[6]}")
    print(f"RX       : {packet[7]}")
    print(f"RY       : {packet[8]}")
