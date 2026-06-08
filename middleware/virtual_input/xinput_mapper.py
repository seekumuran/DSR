import serial
import vgamepad as vg

ser = serial.Serial("COM3", 9600)

pad = vg.VX360Gamepad()

while True:

    packet = ser.read(11)

    if packet[3] & 0x10:
        pad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    else:
        pad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)

    pad.update()
