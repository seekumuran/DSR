import serial
import time

ser = serial.Serial("COM3", 9600)

button_presses = 0

while True:

    packet = ser.read(11)

    if packet[3] != 0:
        button_presses += 1

    print(f"Input Events: {button_presses}")

    time.sleep(0.05)
