from shapely.geometry import Polygon as GeomPolygon, Point as GeomPoint

from core.structure.polygon import Polygon
from core.structure.structure import Structure
from core.utils import GlobalEnv

MIN_DIST = 15


def check_constraints(structure: Structure) -> bool:
    return not (_out_of_bound(structure) or _too_close(structure))


def _out_of_bound(structure: Structure) -> bool:
    for poly in structure.polygons:
        for pt in poly.points:
            if (pt.x < GlobalEnv.domain.min_x or
                    pt.x > GlobalEnv.domain.max_x or
                    pt.y < GlobalEnv.domain.min_y or
                    pt.y > GlobalEnv.domain.max_y):
                return True
    return False


def _too_close(structure: Structure) -> bool:
    is_self_intersection = any(
        [any([_pairwise_dist(poly_1, poly_2) < MIN_DIST for poly_2 in structure.polygons]) for poly_1
         in structure.polygons])
    return is_self_intersection


def _pairwise_dist(poly_1: Polygon, poly_2: Polygon):
    if poly_1 is poly_2:
        return 9999
    pts1 = [GeomPoint(pt.x, pt.y) for pt in poly_1.points]
    pts2 = [GeomPoint(pt.x, pt.y) for pt in poly_2.points]

    geom_poly_1 = GeomPolygon(pts1)
    geom_poly_2 = GeomPolygon(pts2)

    return geom_poly_1.distance(geom_poly_2)
