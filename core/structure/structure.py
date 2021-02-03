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


def get_random_structure(max_pols_num=4, max_pol_size=8) -> Structure:
    structure = Structure(polygons=[])

    num_pols = randint(1, max_pols_num)

    domain = GlobalEnv.domain

    for _ in range(num_pols):
        polygon = Polygon(polygon_id=str(uuid4), points=[])
        num_points = randint(3, max_pol_size)

        for _ in range(num_points):
            point = PolygonPoint(np.random.uniform(low=domain.min_x, high=domain.max_x),
                                 np.random.uniform(low=domain.min_y, high=domain.max_y))
            polygon.points.append(point)
        structure.polygons.append(polygon)

    return structure
