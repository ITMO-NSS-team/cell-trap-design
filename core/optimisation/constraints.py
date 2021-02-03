from core.structure.structure import Structure
from core.utils import GlobalEnv


def check_constraints(structure: Structure) -> bool:
    for poly in structure.polygons:
        for pt in poly.points:
            if (pt.x < GlobalEnv.domain.min_x or
                    pt.x > GlobalEnv.domain.max_x or
                    pt.y < GlobalEnv.domain.min_y or
                    pt.y > GlobalEnv.domain.max_y):
                return False
    return True
