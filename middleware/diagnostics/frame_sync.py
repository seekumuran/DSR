import time

last = time.time()

while True:

    current = time.time()

    delta = (current - last) * 1000

    print(f"Frame Delta: {delta:.3f} ms")

    last = current

    time.sleep(0.016)
