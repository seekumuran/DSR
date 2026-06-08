class DSSXPacket:

    def __init__(self, raw):

        self.sync = raw[0]
        self.version = raw[1]
        self.device = raw[2]

        self.buttons1 = raw[3]
        self.buttons2 = raw[4]

        self.lx = raw[5]
        self.ly = raw[6]

        self.rx = raw[7]
        self.ry = raw[8]

        self.crc_h = raw[9]
        self.crc_l = raw[10]

    def __str__(self):

        return f"""
SYNC      : {hex(self.sync)}
VERSION   : {self.version}
DEVICE    : {self.device}

BUTTONS1  : {bin(self.buttons1)}
BUTTONS2  : {bin(self.buttons2)}

LX        : {self.lx}
LY        : {self.ly}

RX        : {self.rx}
RY        : {self.ry}
"""
