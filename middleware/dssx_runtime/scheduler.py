class Scheduler:

    def __init__(self):

        self.tasks = []

    def register(self, task):

        self.tasks.append(task)

    def run(self):

        for task in self.tasks:

            task()
