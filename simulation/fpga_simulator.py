class FPGASimulator:

    def __init__(self):

        self.enabled = True

    def tick(self):

        print("FPGA Tick")

fpga = FPGASimulator()

while True:

    fpga.tick()
