import time
import serial

ser = serial.Serial("COM3", 9600)

last = time.time()

while True:

    packet = ser.read(11)

    now = time.time()

    latency = (now - last) * 1000

    print(f"Packet latency: {latency:.2f} ms")

    last = now
