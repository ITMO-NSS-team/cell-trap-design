import copy
import random

import numpy as np

from core.optimisation.constraints import check_constraints
from core.structure.structure import get_random_structure, Structure


def crossover(s1: Structure, s2: Structure, rate=0.4):
    random_val = random.random()
    if random_val >= rate:
        return s1

    is_correct = False

    while not is_correct:
        new_structure = copy.deepcopy(s1)

        crossover_point = random.randint(1, len(new_structure.polygons))

        part_1 = s1.polygons[0:crossover_point]
        if not isinstance(part_1, list):
            part_1 = [part_1]
        part_2 = s2.polygons[crossover_point:len(s1.polygons)]
        if not isinstance(part_2, list):
            part_2 = [part_2]

        result = copy.deepcopy(part_1)
        result.extend(copy.deepcopy(part_2))

        new_structure.polygons = result

        is_correct = check_constraints(new_structure)

    return new_structure


def mutation(structure: Structure, rate=0.6):
    random_val = random.random()

    if random_val > - rate:
        return structure

    is_correct = False

    while not is_correct:
        new_structure = copy.deepcopy(structure)

        polygon_to_mutate = new_structure.polygons[random.randint(len(new_structure.polygons))]
        point_to_mutate = new_structure.polygons[random.randint(len(polygon_to_mutate.points))]

        params = [2, 0.5, 1]

        mutation_ratio_x = abs(np.random.normal(params[0], params[1], params[2])[0])
        mutation_ratio_y = abs(np.random.normal(params[0], params[1], params[2])[0])

        sign = 1 if random.random() < 0.5 else -1

        point_to_mutate.x += sign * mutation_ratio_x
        point_to_mutate.x = round(abs(point_to_mutate.x))
        point_to_mutate.y += sign * mutation_ratio_y
        point_to_mutate.y = round(abs(point_to_mutate.y))
        is_correct = check_constraints(new_structure)

    return new_structure


def initial_pop_random(size: int):
    population_new = []

    for _ in range(0, size):
        while len(population_new) < size:
            structure = get_random_structure()
            is_correct = check_constraints(structure)
            if is_correct:
                population_new.append(structure)

    return population_new