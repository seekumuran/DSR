class DeviceRegistry:

    def __init__(self):

        self.registry = {}

    def add(self, device_id, device):

        self.registry[device_id] = device

    def get(self, device_id):

        return self.registry.get(device_id)
