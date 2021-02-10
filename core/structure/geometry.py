from shapely.geometry import Point as GeomPoint, Polygon as GeomPolygon
from shapely.ops import nearest_points
from shapely.validation import explain_validity

from core.structure.polygon import Polygon
from core.utils import GlobalEnv

MIN_DIST = 15


def out_of_bound(structure: 'Structure') -> bool:
    geom_poly_allowed = GeomPolygon([GeomPoint(pt[0], pt[1]) for pt in GlobalEnv.domain.allowed_area])

    for poly in structure.polygons:
        for pt in poly.points:
            geom_pt = GeomPoint(pt.x, pt.y)
            if not geom_poly_allowed.contains(geom_pt):
                return True

    return False


def too_close(structure: 'Structure') -> bool:
    is_self_intersection = any(
        [any([_pairwise_dist(poly_1, poly_2) < MIN_DIST for
              poly_2 in structure.polygons]) for poly_1
         in structure.polygons])
    return is_self_intersection


def _pairwise_dist(poly_1: Polygon, poly_2: Polygon):
    if poly_1 is poly_2:
        return 9999

    nearest_pts = nearest_points(poly_1.as_geom(), poly_2.as_geom())
    return nearest_pts[0].distance(nearest_pts[1])


def self_intersection(structure: 'Structure'):
    return any([len(poly.points) > 2 and explain_validity(
        GeomPolygon([GeomPoint(pt.x, pt.y) for pt in poly.points])) != 'Valid Geometry'
                for poly in structure.polygons])
