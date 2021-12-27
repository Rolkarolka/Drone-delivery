class Drone:
    def __init__(self, index, coords, max_load):
        self.index = index
        self.coords = coords
        self.max_load = max_load
        self.ready = True

    def __repr__(self):
        return f"Drone {self.index}: {self.coords}"