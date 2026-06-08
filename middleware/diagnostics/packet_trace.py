import serial
import time

ser = serial.Serial("COM3", 9600)

packet_count = 0

start = time.time()

while True:

    packet = ser.read(11)

    packet_count += 1

    elapsed = time.time() - start

    if elapsed >= 1:

        print(f"PPS: {packet_count}")

        packet_count = 0
        start = time.time()
