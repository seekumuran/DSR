class ReplayValidator:

    def validate(self, original, replay):

        if original == replay:
            print("Replay Valid")
        else:
            print("Replay Corrupted")
