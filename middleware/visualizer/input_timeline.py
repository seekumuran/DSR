import time

events = []

while True:

    events.append(time.time())

    print(events[-10:])

    time.sleep(0.1)
