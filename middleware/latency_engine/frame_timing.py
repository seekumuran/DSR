import time

frames = []

while True:

    start = time.time()

    time.sleep(0.016)

    end = time.time()

    frames.append((end - start) * 1000)

    if len(frames) >= 60:

        avg = sum(frames) / len(frames)

        print(f"Frame Time Avg: {avg:.3f} ms")

        frames.clear()
