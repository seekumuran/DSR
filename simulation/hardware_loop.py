import time

class HardwareLoop:

    def __init__(self):

        self.running = True

    def run(self):

        while self.running:

            print("Simulating Hardware Tick")

            time.sleep(0.01)

loop = HardwareLoop()

loop.run()
