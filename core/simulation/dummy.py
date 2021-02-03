from core.structure.structure import Structure


def execute(structure: Structure) -> float:
    flow = sum([poly.length for poly in structure.polygons])
    return flow
