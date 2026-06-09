import matplotlib.pyplot as plt

devices = [
    "DSSX-1",
    "DSSX-2"
]

counts = [120, 80]

plt.bar(devices, counts)

plt.title("Connected DSSX Devices")

plt.show()
