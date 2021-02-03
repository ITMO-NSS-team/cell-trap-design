class Domain:
    allowed_area = [(-125, 100), (-75, 155), (15, 155), (30, 90), (-40, -50), (-40, -155), (-125, -155)]

    @property
    def min_x(self):
        return min(p[0] for p in self.allowed_area)

    @property
    def max_x(self):
        return max(p[0] for p in self.allowed_area)

    @property
    def min_y(self):
        return min(p[1] for p in self.allowed_area)

    @property
    def max_y(self):
        return max(p[1] for p in self.allowed_area)

    @property
    def len_x(self):
        return abs(self.max_x - self.min_x)

    @property
    def len_y(self):
        return abs(self.max_y - self.min_y)
