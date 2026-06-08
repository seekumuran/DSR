import serial
import matplotlib.pyplot as plt
from collections import deque

ser = serial.Serial("COM3", 9600)

lx_vals = deque(maxlen=100)

plt.ion()

fig, ax = plt.subplots()

while True:

    packet = ser.read(11)

    lx = packet[5]

    lx_vals.append(lx)

    ax.clear()
    ax.plot(lx_vals)

    plt.pause(0.01)
