from typing import List, Optional

from shapely.geometry import Point as GeomPoint, Polygon as GeomPolygon

from core.structure.polygon import PolygonPoint


class Domain:
    def __init__(self, name='main', allowed_area: Optional[List] = None):
        self.name = name
        if allowed_area is None:
            allowed_area = [(-125, 100),
                            (-75, 155),
                            (15, 155),
                            (40, 90),
                            (-10, -130),
                            (-10, -155),
                            (-125, -155)]
        self.allowed_area = allowed_area

    @property
    def min_x(self):
        return min(p[0] for p in self.allowed_area) + 15

    @property
    def max_x(self):
        return max(p[0] for p in self.allowed_area) - 15

    @property
    def min_y(self):
        return min(p[1] for p in self.allowed_area) + 15

    @property
    def max_y(self):
        return max(p[1] for p in self.allowed_area) - 15

    @property
    def len_x(self):
        return abs(self.max_x - self.min_x)

    @property
    def len_y(self):
        return abs(self.max_y - self.min_y)

    def contains(self, point: PolygonPoint):
        geom_poly_allowed = GeomPolygon([GeomPoint(pt[0], pt[1]) for pt in self.allowed_area])
        geom_pt = GeomPoint(point.x, point.y)
        return geom_poly_allowed.contains(geom_pt)
