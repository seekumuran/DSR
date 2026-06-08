class Device:

    def __init__(self, name):

        self.name = name
        self.connected = False

    def connect(self):

        self.connected = True

    def disconnect(self):

        self.connected = False
