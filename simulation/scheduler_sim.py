import time

tasks = [
    "INPUT",
    "ADC",
    "PACKET",
    "UART"
]

while True:

    for task in tasks:

        print(f"Running {task}")

        time.sleep(0.05)
