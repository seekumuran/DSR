class Packet:

    def __init__(self):

        self.sync = 0xAA
        self.version = 1

    def encode(self):

        return bytes([
            self.sync,
            self.version
        ])
