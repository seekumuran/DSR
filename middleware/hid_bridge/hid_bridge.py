import serial
import vgamepad as vg

ser = serial.Serial("COM3", 9600)

gamepad = vg.VX360Gamepad()

while True:

    packet = ser.read(11)

    if len(packet) != 11:
        continue

    buttons1 = packet[3]
    buttons2 = packet[4]

    lx = packet[5]
    ly = packet[6]
    rx = packet[7]
    ry = packet[8]

    if buttons1 & 0x01:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)

    if buttons1 & 0x10:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

    gamepad.left_joystick(
        x_value=(lx - 128) * 256,
        y_value=(ly - 128) * 256
    )

    gamepad.right_joystick(
        x_value=(rx - 128) * 256,
        y_value=(ry - 128) * 256
    )

    gamepad.update()
