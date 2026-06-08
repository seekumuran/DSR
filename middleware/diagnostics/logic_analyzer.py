import serial
import time

ser = serial.Serial("COM3", 9600)

timestamps = []

while True:

    packet = ser.read(11)

    timestamps.append(time.time())

    print("==============")
    print(f"TIME : {timestamps[-1]}")
    print(f"DATA : {packet.hex()}")
