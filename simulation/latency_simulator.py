import random
import time

while True:

    simulated_latency = random.uniform(1, 5)

    print(f"Latency: {simulated_latency:.2f} ms")

    time.sleep(0.5)
