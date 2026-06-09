import matplotlib.pyplot as plt
import random

runtime = [
    random.uniform(0.1, 1.0)
    for _ in range(200)
]

plt.plot(runtime)

plt.title("Runtime Timing")

plt.show()
