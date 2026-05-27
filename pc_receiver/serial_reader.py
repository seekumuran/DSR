import serial

ser = serial.Serial(
    port='COM3',
    baudrate=9600
)

print("Controller Connected")

while True:

    data = ser.read()

    value = int.from_bytes(data, byteorder='big')

    print("--------------------------------")

    print("RAW:", bin(value))

    if value & 0x01:
        print("UP")

    if value & 0x02:
        print("DOWN")

    if value & 0x04:
        print("LEFT")

    if value & 0x08:
        print("RIGHT")

    if value & 0x10:
        print("A")

    if value & 0x20:
        print("B")

    if value & 0x40:
        print("X")

    if value & 0x80:
        print("Y")
