import copy
import random

from core.optimisation.constraints import check_constraints
from core.structure.structure import (Structure, get_random_point, get_random_poly, get_random_structure)

MAX_ITER = 50000


def crossover(s1: Structure, s2: Structure, rate=0.4):
    random_val = random.random()
    if random_val >= rate or len(s1.polygons) == 1 or len(s2.polygons) == 1:
        if random.random() > 0.5:
            return s1
        else:
            return s2

    is_correct = False
    n_iter = 0

    while not is_correct and n_iter < MAX_ITER:
        n_iter += 1
        print(n_iter)
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


def mutation(structure: Structure, rate):
    random_val = random.random()

    if random_val > rate:
        return structure

    is_correct = False

    min_pol_size = 4

    polygon_drop_mutation_prob = 0.2
    polygon_add_mutation_prob = 0.2
    point_drop_mutation_prob = 0.2
    point_add_mutation_prob = 0.2
    polygon_rotate_mutation_prob = 0.2

    changes_num = random.randint(1, 5)

    n_iter = 0

    new_structure = structure

    while not is_correct and n_iter < MAX_ITER:
        try:
            n_iter += 1
            print(n_iter)
            new_structure = copy.deepcopy(structure)

            for _ in range(changes_num):
                polygon_to_mutate = new_structure.polygons[random.randint(0, len(new_structure.polygons) - 1)]

                if random.random() < polygon_drop_mutation_prob and len(new_structure.polygons) > 1:
                    # if drop polygon from structure
                    new_structure.polygons.remove(polygon_to_mutate)
                elif random.random() < polygon_add_mutation_prob:
                    # if add polygon to structure
                    new_poly = get_random_poly(parent_structure=new_structure)
                    if new_poly is None:
                        continue
                    new_structure.polygons.append(new_poly)
                elif random.random() < polygon_rotate_mutation_prob:
                    # if add polygon to structure
                    polygon_to_mutate.rotate(float(random.randint(-180, 180)))
                else:
                    mutate_point_ind = random.randint(0, len(polygon_to_mutate.points) - 1)
                    point_to_mutate = polygon_to_mutate.points[mutate_point_ind]
                    if (random.random() < point_drop_mutation_prob and
                            len(polygon_to_mutate.points) > min_pol_size):
                        # if drop point from polygon
                        polygon_to_mutate.points.remove(point_to_mutate)
                    else:
                        # if change point in polygon

                        new_point = get_random_point(point_to_mutate, polygon_to_mutate, new_structure)
                        if new_point is None:
                            continue
                        # domain = GlobalEnv.domain
                        # params_x = [domain.len_x * 0.05, domain.len_x * 0.025]
                        # params_y = [domain.len_y * 0.05, domain.len_y * 0.025]

                        # mutation_ratio_x = abs(np.random.normal(params_x[0], params_x[1], 1)[0])
                        # mutation_ratio_y = abs(np.random.normal(params_y[0], params_y[1], 1)[0])

                        # sign = 1 if random.random() < 0.5 else -1

                        # new_point = copy.deepcopy(point_to_mutate)
                        # new_point.x += sign * mutation_ratio_x
                        # new_point.x = round(abs(new_point.x))
                        # new_point.y += sign * mutation_ratio_y
                        # new_point.y = round(abs(new_point.y))

                        if random.random() < point_add_mutation_prob:
                            if mutate_point_ind + 1 < len(polygon_to_mutate.points):
                                polygon_to_mutate.points.insert(mutate_point_ind + 1, new_point)
                            else:
                                polygon_to_mutate.points.insert(mutate_point_ind - 1, new_point)
                        else:
                            polygon_to_mutate.points[mutate_point_ind] = new_point

            is_correct = check_constraints(new_structure)
        except Exception as ex:
            print(ex)

    return new_structure


def initial_pop_random(size: int):
    population_new = []

    print('Start init')

    for _ in range(0, size):
        structure_size = random.randint(2, 4)
        print(f'Try to create size {structure_size}')

        is_correct = False
        while not is_correct:
            structure = get_random_structure(min_pols_num=structure_size, max_pols_num=structure_size,
                                             min_pol_size=5, max_pol_size=10)
            is_correct = check_constraints(structure)
            if is_correct:
                print(f'Created, size {structure_size}')
                population_new.append(structure)

    print('End init')
    return population_new
