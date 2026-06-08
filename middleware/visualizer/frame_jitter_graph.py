import matplotlib.pyplot as plt
import random

samples = [
    random.uniform(0.1, 3.0)
    for _ in range(200)
]

plt.plot(samples)

plt.title("Frame Jitter")

plt.xlabel("Frame")
plt.ylabel("Jitter (ms)")

plt.show()
