from dataclasses import dataclass
from math import sqrt
from typing import List


@dataclass()
class PolygonPoint:
    x: float
    y: float


def xy_to_points(xy):
    return PolygonPoint(xy[0], xy[1])


class Polygon(object):
    def __init__(self, polygon_id: str, points: List[PolygonPoint]):
        self.polygoin_id = polygon_id
        self.points = points

    def get_length(self):
        assert len(self.points) > 2
        total_length = 0
        for i in range(1, len(self.points)):
            total_length += sqrt(
                (self.points[i - 1].x - self.points[i].x) ** 2 + (self.points[i - 1].y - self.points[i].y) ** 2)

        total_length += sqrt(
            (self.points[len(self.points) - 1].x - self.points[0].x) ** 2 +
            (self.points[len(self.points) - 1].y - self.points[0].y) ** 2)

        assert total_length >= 0

        return total_length
