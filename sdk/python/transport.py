import serial

class Transport:

    def __init__(self, port):

        self.ser = serial.Serial(port, 9600)

    def read_packet(self):

        return self.ser.read(11)
