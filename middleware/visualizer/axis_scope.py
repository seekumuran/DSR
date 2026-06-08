import serial
import matplotlib.pyplot as plt

ser = serial.Serial("COM3", 9600)

x = []

plt.ion()

fig, ax = plt.subplots()

while True:

    packet = ser.read(11)

    x.append(packet[5])

    if len(x) > 100:
        x.pop(0)

    ax.clear()
    ax.plot(x)

    plt.pause(0.01)
