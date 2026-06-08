import serial
import time

ser = serial.Serial("COM3", 9600)

count = 0

start = time.time()

while True:

    ser.read(11)

    count += 11

    elapsed = time.time() - start

    if elapsed >= 1:

        print(f"Throughput: {count} B/s")

        count = 0
        start = time.time()
