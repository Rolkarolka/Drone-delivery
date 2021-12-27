class Drone:
    def __init__(self, index, coordinates, max_load):
        self.index = index
        self.coordinates = coordinates
        self.max_load = max_load
        self.ready = True

    def __repr__(self):
        return f"Drone {self.index}: {self.coordinates}"
