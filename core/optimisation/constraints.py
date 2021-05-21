from core.structure.geometry import out_of_bound, self_intersection, too_close
from core.structure.structure import Structure
from core.utils import GlobalEnv


def check_constraints(structure: Structure, is_lightweight: bool = False, domain=None) -> bool:
    if domain is None:
        domain = GlobalEnv().domain

    try:
        if any([(poly is None or
                 len(poly.points) == 0 or
                 any([pt is None for pt in poly.points]))
                for poly in structure.polygons]):
            print('Wrong structure')
            return False

        # structure.plot()
        structurally_correct = (not (out_of_bound(structure, domain) or
                                     too_close(structure) or
                                     self_intersection(structure)))

        if structurally_correct and not is_lightweight:
            print('Check heavy constraint')
            model_func = GlobalEnv().model_func
            obj, _, _ = model_func(structure)
            return -obj < 0
        else:
            print('Constraint violated')
    except Exception as ex:
        print(ex)
        return False

    return structurally_correct
