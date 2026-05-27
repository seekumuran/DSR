import serial

ser = serial.Serial(
    port='COM3',
    baudrate=9600
)

print("DualShock Series X Connected")

while True:

    buttons1 = int.from_bytes(ser.read(), byteorder='big')
    buttons2 = int.from_bytes(ser.read(), byteorder='big')

    lx = int.from_bytes(ser.read(), byteorder='big')
    ly = int.from_bytes(ser.read(), byteorder='big')

    rx = int.from_bytes(ser.read(), byteorder='big')
    ry = int.from_bytes(ser.read(), byteorder='big')

    print("----------------------------------")

    print("LEFT STICK :", lx, ly)
    print("RIGHT STICK:", rx, ry)

    if buttons1 & 0x01:
        print("UP")

    if buttons1 & 0x02:
        print("DOWN")

    if buttons1 & 0x04:
        print("LEFT")

    if buttons1 & 0x08:
        print("RIGHT")

    if buttons1 & 0x10:
        print("A")

    if buttons1 & 0x20:
        print("B")

    if buttons1 & 0x40:
        print("X")

    if buttons1 & 0x80:
        print("Y")

    if buttons2 & 0x01:
        print("L1")

    if buttons2 & 0x02:
        print("R1")

    if buttons2 & 0x04:
        print("L2")

    if buttons2 & 0x08:
        print("R2")

    if buttons2 & 0x10:
        print("START")

    if buttons2 & 0x20:
        print("SELECT")

    if buttons2 & 0x40:
        print("HOME")
