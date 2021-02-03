from dataclasses import dataclass


@dataclass
class Domain:
    min_x: float
    max_x: float
    min_y: float
    max_y: float

    @property
    def len_x(self):
        return abs(self.max_x - self.min_x)

    @property
    def len_y(self):
        return abs(self.max_y - self.min_y)
