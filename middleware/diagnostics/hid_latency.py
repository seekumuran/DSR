import time

while True:

    start = time.perf_counter()

    time.sleep(0.002)

    end = time.perf_counter()

    latency = (end - start) * 1000

    print(f"HID Injection Latency: {latency:.3f} ms")
