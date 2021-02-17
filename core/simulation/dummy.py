from core.structure.structure import Structure


def execute(structure: Structure):
    flow1 = sum([poly.length for poly in structure.polygons])
    flow2 = sum([len(poly.points) for poly in structure.polygons])
    return flow1, flow2, 'idx'
