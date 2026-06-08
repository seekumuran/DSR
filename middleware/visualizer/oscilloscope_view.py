import numpy as np
import matplotlib.pyplot as plt

samples = np.sin(np.linspace(0, 50, 1000))

plt.plot(samples)

plt.title("UART Timing Waveform")

plt.xlabel("Samples")
plt.ylabel("Amplitude")

plt.show()
