import matplotlib.pyplot as plt
import random

samples = [
    random.uniform(0.5, 3.5)
    for _ in range(100)
]

plt.plot(samples)

plt.title("DSSX Latency")

plt.show()
