import matplotlib.pyplot as plt
import random

rates = [125, 250, 500, 1000]

samples = [
    random.randint(1, 5)
    for _ in rates
]

plt.bar(rates, samples)

plt.title("Polling Rate Stability")

plt.xlabel("Polling Rate")
plt.ylabel("Packet Jitter")

plt.show()
