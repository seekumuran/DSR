import serial
import time

ser = serial.Serial("COM3", 9600)

timestamps = []

while True:

    ser.read(11)

    timestamps.append(time.time())

    if len(timestamps) > 100:

        diffs = []

        for i in range(1, len(timestamps)):
            diffs.append(
                (timestamps[i] - timestamps[i - 1]) * 1000
            )

        avg = sum(diffs) / len(diffs)

        print(f"Average jitter: {avg:.3f} ms")

        timestamps.clear()
