import random

while True:

    packet = bytes([
        random.randint(0, 255)
        for _ in range(11)
    ])

    print(packet.hex())
