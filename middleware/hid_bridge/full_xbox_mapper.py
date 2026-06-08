import serial
import vgamepad as vg

ser = serial.Serial("COM3", 9600)

pad = vg.VX360Gamepad()

while True:

    packet = ser.read(11)

    b1 = packet[3]
    b2 = packet[4]

    lx = packet[5]
    ly = packet[6]

    rx = packet[7]
    ry = packet[8]

    if b1 & 0x01:
        pad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
    else:
        pad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)

    if b1 & 0x02:
        pad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    else:
        pad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)

    if b1 & 0x10:
        pad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    else:
        pad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

    if b1 & 0x20:
        pad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    else:
        pad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)

    pad.left_joystick(
        x_value=(lx - 128) * 256,
        y_value=(ly - 128) * 256
    )

    pad.right_joystick(
        x_value=(rx - 128) * 256,
        y_value=(ry - 128) * 256
    )

    pad.update()
