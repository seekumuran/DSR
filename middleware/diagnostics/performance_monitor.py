import time

start = time.time()

frames = 0

while True:

    frames += 1

    elapsed = time.time() - start

    if elapsed >= 1:

        print(f"FPS: {frames}")

        frames = 0
        start = time.time()
