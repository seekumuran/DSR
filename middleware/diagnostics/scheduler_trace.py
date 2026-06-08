import time

tasks = [
    "INPUT",
    "PACKET",
    "UART"
]

while True:

    for task in tasks:

        print(f"[TRACE] Executing: {task}")

        time.sleep(0.1)
