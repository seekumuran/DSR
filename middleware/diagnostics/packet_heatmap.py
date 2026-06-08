import numpy as np
import matplotlib.pyplot as plt

heatmap = np.random.rand(16, 16)

plt.imshow(heatmap)

plt.title("Packet Activity Heatmap")

plt.colorbar()

plt.show()
