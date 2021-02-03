from dataclasses import dataclass
from random import randint, random
from typing import List
from uuid import uuid4

from core.structure.polygon import Polygon, PolygonPoint


@dataclass
class Structure:
    polygons: List[Polygon]


def get_random_structure(max_pols_num=4, max_pol_size=8) -> Structure:
    structure = Structure(polygons=[])

    num_pols = randint(1, max_pols_num)
    for _ in range(num_pols):
        polygon = Polygon(polygon_id=str(uuid4), points=[])
        num_points = randint(3, max_pol_size)

        for _ in range(num_points):
            point = PolygonPoint(random(), random())
            polygon.points.append(point)
        structure.polygons.append(polygon)

    return structure
