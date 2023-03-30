class PID:
    def __init__(self, p, i, d, max_i):
        self.P = p
        self.I = i
        self.D = d
        self.integral = 0
        self.max_i = max_i
        self.first_run = True
        self.last_error = 0

    def update(self, error, dt):
        if self.first_run:
            self.last_error = error
            self.first_run = False
        self.integral += self.I * error * dt
        diff = (error - self.last_error) / dt
        const_integral = constrain(self.integral, self.max_i, -self.max_i)
        control_out = self.P * error + self.D * diff + const_integral
        self.last_error = error
        return control_out


def constrain(val, min, max):
    if val > max:
        return max
    elif val < min:
        return min
    return val



