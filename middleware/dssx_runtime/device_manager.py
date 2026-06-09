class DeviceManager:

    def __init__(self):

        self.devices = []

    def register(self, device):

        self.devices.append(device)

    def list_devices(self):

        for device in self.devices:

            print(device)
