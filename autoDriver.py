
class autoDriver:
    def __init__(self, p, i, d):
        self.p = p
        self.i = i
        self.d = d
        self.last_i = 0
        self.last_vs = 0

    def pid(self, vs, dvs):
        p = vs - dvs
        ii = self.last_i + p
        if -100 <= ii <= 100:
            i = ii
        d = vs - self.last_vs
        if self.last_vs == 0:
            d = 0
        self.last_i = i  # update
        self.last_vs = vs  # update
        print(f'p: {p}, i: {i}, d: {d}')

        return (self.p * p) + (self.i * i) + (self.d * d)
