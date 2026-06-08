import random

drift = 0

while True:

    drift += random.uniform(-0.1, 0.1)

    print(f"Timing Drift: {drift:.4f} ms")
