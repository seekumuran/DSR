import random
import matplotlib.pyplot as plt

samples = [
    random.uniform(1, 8)
    for _ in range(1000)
]

plt.hist(samples)

plt.title("Latency Histogram")

plt.xlabel("Latency (ms)")
plt.ylabel("Samples")

plt.show()
