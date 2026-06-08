import serial
import vgamepad as vg

ser = serial.Serial("COM3", 9600)

controller = vg.VDS4Gamepad()

while True:

    packet = ser.read(11)

    lx = packet[5]
    ly = packet[6]

    controller.left_joystick(
        x_value=lx * 257,
        y_value=ly * 257
    )

    controller.update()
