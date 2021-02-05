from dataclasses import dataclass
from random import randint
from typing import List
from uuid import uuid4

import numpy as np

from core.structure.polygon import Polygon, PolygonPoint
from core.utils import GlobalEnv


@dataclass
class Structure:
    polygons: List[Polygon]

    def __str__(self):
        out_str = ''
        for i, pol in enumerate(self.polygons):
            out_str += f'\r\n Polygon {i}, size {len(pol.points)}: \r\n'
            for j, pt in enumerate(pol.points):
                out_str += f'Point {j}: x={round(pt.x, 2)}, y={round(pt.y, 2)}; '
        return out_str


def get_random_structure(min_pols_num=2, max_pols_num=4, max_pol_size=8) -> Structure:
    structure = Structure(polygons=[])

    num_pols = randint(min_pols_num, max_pols_num)
    is_large = num_pols == 1

    for _ in range(num_pols):
        polygon = get_random_poly(max_pol_size, is_large=is_large)
        structure.polygons.append(polygon)

    return structure


def get_random_poly(max_pol_size=8, is_large=False):
    domain = GlobalEnv.domain

    polygon = Polygon(polygon_id=str(uuid4), points=[])
    num_points = randint(4, max_pol_size)

    centroid = PolygonPoint(np.random.uniform(low=domain.min_x + 40, high=domain.max_x - 40),
                            np.random.uniform(low=domain.min_y + 40, high=domain.max_y - 40))

    for _ in range(num_points):
        if is_large:
            point = PolygonPoint(np.random.uniform(low=domain.min_x + 40, high=domain.max_x - 40),
                                 np.random.uniform(low=domain.min_y + 40, high=domain.max_y - 40))
        else:
            point = PolygonPoint(np.random.normal(centroid.x, domain.len_x * 0.05),
                                 np.random.normal(centroid.y, domain.len_y * 0.05))
        polygon.points.append(point)
    return polygon
