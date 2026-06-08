import serial

ser = serial.Serial("COM3", 9600)

while True:

    packet = ser.read(11)

    buttons = packet[3]

    print(f"Buttons: {bin(buttons)}")
