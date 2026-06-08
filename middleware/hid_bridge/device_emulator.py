class VirtualController:

    def __init__(self):

        self.connected = True

    def inject_packet(self, packet):

        print("Injected:", packet.hex())
