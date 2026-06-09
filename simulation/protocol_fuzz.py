import random

while True:

    fuzz = bytes([
        random.randint(0,255)
        for _ in range(11)
    ])

    print(fuzz.hex())
