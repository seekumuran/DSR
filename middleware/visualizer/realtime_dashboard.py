import serial
import matplotlib.pyplot as plt

ser = serial.Serial("COM3", 9600)

lx_vals = []

plt.ion()

fig, ax = plt.subplots()

while True:

    packet = ser.read(11)

    lx_vals.append(packet[5])

    if len(lx_vals) > 200:
        lx_vals.pop(0)

    ax.clear()

    ax.plot(lx_vals)

    ax.set_title("ARES Real-Time Axis Dashboard")

    plt.pause(0.01)
