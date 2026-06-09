import matplotlib.pyplot as plt
import random

values = [
    random.randint(0,255)
    for _ in range(100)
]

plt.plot(values)

plt.title("DSSX Device Scope")

plt.show()
