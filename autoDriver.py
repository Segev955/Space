
class autoDriver:
    def __init__(self, p, i, d):
        self.p = p
        self.i = i
        self.d = d
        self.last_i = 0
        self.last_vs = 0

    def pid(self, vs, dvs):
        p = vs - dvs
        i = self.last_i + p
        d = vs - self.last_vs
        if self.last_vs == 0:
            d = 0
        self.last_i = i  # update
        self.last_vs = vs  # update

        return (self.p * p) + (self.i * i) + (self.d * d)
