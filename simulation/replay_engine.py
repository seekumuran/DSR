import time

class ReplayEngine:

    def __init__(self):

        self.frames = []

    def record(self, packet):

        self.frames.append(packet)

    def playback(self):

        for frame in self.frames:

            print(frame)

            time.sleep(0.01)
