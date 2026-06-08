import random

packet = bytearray([0xAA] * 11)

while True:

    index = random.randint(0, 10)

    packet[index] = random.randint(0, 255)

    print(packet.hex())
