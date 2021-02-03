from core.structure.structure import Structure


def simulate(structure: Structure) -> float:
    flow = sum([poly.length for poly in structure.polygons])
    return flow
