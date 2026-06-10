import matplotlib.pyplot as plt
import random

samples = [
    random.randint(0,100)
    for _ in range(100)
]

plt.plot(samples)

plt.title("DSSX Runtime Graph")

plt.show()
