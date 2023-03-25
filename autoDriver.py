from arcade import clamp

class autoDriver:
    def __init__(self, location):
        # self.ship = ship
        self.location = location
        self.last = self.location  # last location
        self.i = 0

    def pid(self):
        p = self.location
        i = self.i + 0.2 * self.location
        d = self.location - self.last

        self.last = self.location  # save the last location

        return p, i * 0.05, d
