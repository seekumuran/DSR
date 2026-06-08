import serial

ser = serial.Serial("COM3", 9600)

expected = 0
lost = 0

while True:

    packet = ser.read(11)

    seq = packet[2]

    if seq != expected:
        lost += 1

    expected = (seq + 1) % 256

    print(f"Lost Packets: {lost}")
