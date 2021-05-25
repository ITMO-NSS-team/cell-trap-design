from copy import deepcopy

from shapely.geometry.polygon import Polygon as ShapelyPolygon
from shapely.ops import nearest_points

from core.structure.domain import Domain
from core.structure.geometry import out_of_bound, self_intersection, too_close
from core.structure.structure import GeomPoint, Polygon, Structure


def postprocess(structure: Structure, domain: Domain):
    corrected_structure = deepcopy(structure)

    for poly in corrected_structure.polygons:
        local_structure = Structure([poly])
        if out_of_bound(local_structure, domain):
            poly = _correct_wrong_point(poly, domain)
        if self_intersection(local_structure):
            poly = _correct_self_intersection(poly)

    if too_close(structure):
        corrected_structure = _correct_closeness(corrected_structure)

    return corrected_structure


def _correct_wrong_point(poly: Polygon, domain: Domain):
    for point in poly.points:
        point.x = max(point.x, domain.min_x)
        point.y = max(point.y, domain.min_y)
        point.x = min(point.x, domain.max_x)
        point.y = min(point.y, domain.max_y)
        if not domain.contains(point):
            _, nearest_correct_position = \
                nearest_points(point.as_geom(),
                               domain.as_geom().boundary)
            point.x = nearest_correct_position.x
            point.y = nearest_correct_position.y
    return poly


def _correct_self_intersection(poly: Polygon):
    # change self-intersected poly to convex
    convex = poly.as_geom().convex_hull
    if isinstance(convex, ShapelyPolygon):
        poly.points = []
        for convex_pt in list(convex.exterior.coords.xy):
            poly.points.append(GeomPoint(convex_pt[0], convex_pt[1]))
    return poly


def _correct_closeness(structure: Structure):
    # shrink all polygons
    for poly in structure.polygons:
        poly.resize(0.8, 0.8)
    return structure
