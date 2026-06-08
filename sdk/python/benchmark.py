import time

class Benchmark:

    def start(self):

        self.start_time = time.time()

    def stop(self):

        elapsed = time.time() - self.start_time

        print(f"Elapsed: {elapsed:.3f} sec")
