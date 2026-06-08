import random
import time

while True:

    packet = [
        0xAA,
        0x01,
        0x01,
        random.randint(0,255),
        random.randint(0,255),
        random.randint(0,255),
        random.randint(0,255),
        random.randint(0,255),
        random.randint(0,255),
        0x00,
        0x00
    ]

    print(packet)

    time.sleep(0.01)
