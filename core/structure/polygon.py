from dataclasses import dataclass
from math import sqrt
from typing import List


@dataclass()
class PolygonPoint:
    _x: float
    _y: float

    @property
    def x(self):
        return round(self._x)

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return round(self._y)

    @y.setter
    def y(self, value):
        self._y = value


def xy_to_points(xy):
    return PolygonPoint(xy[0], xy[1])


class Polygon(object):
    def __init__(self, polygon_id: str, points: List[PolygonPoint]):
        self.polygoin_id = polygon_id
        self.points = points

    @property
    def length(self):
        total_length = 0
        for i in range(1, len(self.points)):
            total_length += sqrt(
                (self.points[i - 1].x - self.points[i].x) ** 2 + (self.points[i - 1].y - self.points[i].y) ** 2)

        total_length += sqrt(
            (self.points[len(self.points) - 1].x - self.points[0].x) ** 2 +
            (self.points[len(self.points) - 1].y - self.points[0].y) ** 2)

        assert total_length >= 0

        return total_length
