class Path:

    def __init__(self, x_path, y_path, period, speed=1):
        self.xt = x_path
        self.yt = y_path
        self.T = period
        self.speed = speed

    def get_pos(self, t):
        if t*self.speed > self.T:
            t = t * self.speed % self.T
        return self.xt(t), self.yt(t)

    def get_period_thirds(self):
        return self.T / 3
