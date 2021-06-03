from dataclasses import dataclass
from math import sqrt
from typing import List

import matplotlib.pyplot as plt
from shapely import affinity
from shapely.geometry import Point as GeomPoint, Polygon as GeomPolygon


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

    def plot(self):
        plt.plot(self.x, self.y, marker='o', markersize=3, color="red")

    def as_geom(self):
        return GeomPoint(self.x, self.y)


def xy_to_points(xy):
    return PolygonPoint(xy[0], xy[1])


class Polygon(object):
    def __init__(self, polygon_id: str, points: List[PolygonPoint]):
        self.polygoin_id = polygon_id
        self.points = points

    @property
    def length(self):
        if len(self.points) < 1:
            return 0

        total_length = 0
        for i in range(1, len(self.points)):
            total_length += sqrt(
                (self.points[i - 1].x - self.points[i].x) ** 2 + (self.points[i - 1].y - self.points[i].y) ** 2)

        total_length += sqrt(
            (self.points[len(self.points) - 1].x - self.points[0].x) ** 2 +
            (self.points[len(self.points) - 1].y - self.points[0].y) ** 2)

        assert total_length >= 0

        return total_length

    def as_geom(self):
        # if self.points is None or len(self.points) <= 2:
        #    raise ValueError('Not enough point for polygon')
        return GeomPolygon([GeomPoint(pt.x, pt.y) for pt in self.points])

    def plot(self):
        x, y = self.as_geom().exterior.xy
        plt.plot(x, y)

    def show(self):
        self.plot()
        plt.show()

    def resize(self, x_scale, y_scale):
        geom_polygon = self.as_geom()

        rescaled_geom_polygon = affinity.scale(geom_polygon,
                                               x_scale, y_scale)

        self.points = [PolygonPoint(x, y) for x, y in
                       zip(list(rescaled_geom_polygon.exterior.xy[0]),
                           list(rescaled_geom_polygon.exterior.xy[1]))]

    def rotate(self, angle: float):
        geom_polygon = self.as_geom()

        rotated_geom_polygon = affinity.rotate(geom_polygon, angle, 'center')

        self.points = [PolygonPoint(x, y) for x, y in
                       zip(list(rotated_geom_polygon.exterior.xy[0]),
                           list(rotated_geom_polygon.exterior.xy[1]))]

    def contains(self, point: PolygonPoint):
        geom_poly_allowed = self.as_geom()
        geom_pt = GeomPoint(point.x, point.y)
        return geom_poly_allowed.contains(geom_pt)
