import serial

class TransportLayer:

    def __init__(self, port):

        self.ser = serial.Serial(port, 9600)

    def read(self):

        return self.ser.read(11)

    def write(self, packet):

        self.ser.write(packet)
