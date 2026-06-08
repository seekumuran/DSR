import time

capture = [
    bytes([0xAA] * 11)
    for _ in range(100)
]

for packet in capture:

    print(packet.hex())

    time.sleep(0.01)
