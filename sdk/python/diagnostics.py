class Diagnostics:

    def packet_info(self, packet):

        print("Packet Length:", len(packet))
        print("Packet Hex:", packet.hex())
