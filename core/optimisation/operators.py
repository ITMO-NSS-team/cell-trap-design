import copy
import random
from copy import deepcopy
from multiprocessing import Pool

import numpy as np

from core.algs.postproc import postprocess
from core.optimisation.constraints import check_constraints
from core.structure.structure import Structure, get_random_point, get_random_poly, get_random_structure
from core.utils import GlobalEnv

MAX_ITER = 50000
NUM_PROC = 1


def crossover(s1: Structure, s2: Structure, rate=0.4, domain=None):
    random_val = random.random()
    if random_val >= rate or len(s1.polygons) == 1 or len(s2.polygons) == 1:
        if random.random() > 0.5:
            return s1
        else:
            return s2

    if domain is None:
        domain = GlobalEnv().domain

    is_correct = False
    n_iter = 0

    new_structure = s1

    while not is_correct and n_iter < MAX_ITER:
        n_iter += 1
        print('cross', n_iter)
        if NUM_PROC > 1:
            with Pool(NUM_PROC) as p:
                new_items = p.map(crossover_worker,
                                  [[s1, s2, domain] for _ in range(NUM_PROC)])
        else:
            new_items = [crossover_worker([s1, s2, domain]) for _ in range(NUM_PROC)]

        for structure in new_items:
            if structure is not None:
                # is_correct = check_constraints(structure, domain=domain, is_lightweight=True)
                # if is_correct:
                new_structure = structure
                break

    return new_structure


def crossover_worker(args):
    s1, s2, domain = args[0], args[1], args[2]
    # new_env = GlobalEnv()
    # new_env.domain = domain

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

    new_structure = postprocess(new_structure, domain)
    is_correct = check_constraints(new_structure, is_lightweight=True, domain=domain)
    if not is_correct:
        return None

    return new_structure


def mutation(structure: Structure, rate, domain=None):
    random_val = random.random()

    if random_val > rate:
        return structure

    if domain is None:
        domain = GlobalEnv().domain

    is_correct = False

    min_pol_size = 4
    changes_num = 1

    n_iter = 0

    new_structure = structure

    while not is_correct and n_iter < MAX_ITER:
        n_iter += 1
        print('mut', n_iter)

        if NUM_PROC > 1:
            with Pool(NUM_PROC) as p:
                new_items = \
                    p.map(mutate_worker,
                          [[new_structure, changes_num, min_pol_size, domain] for _ in range(NUM_PROC)])
        else:
            new_items = [mutate_worker([new_structure, changes_num, min_pol_size, domain]) for _ in range(NUM_PROC)]

        for structure in new_items:
            if structure is not None:
                #       is_correct = check_constraints(structure, domain=domain, is_lightweight=True)
                #       if is_correct:
                new_structure = structure
                break

    return new_structure


def initial_pop_random(size: int, domain=None):
    print('Start init')
    population_new = []

    env = GlobalEnv()

    if domain is None:
        domain = GlobalEnv().domain

    if env.initial_state is None:
        while len(population_new) < size:
            # import ray
            if NUM_PROC > 1:
                with Pool(NUM_PROC) as p:
                    new_items = p.map(get_pop_worker, [domain] * size)
            else:
                new_items = [get_pop_worker(domain) for _ in range(size)]

            for structure in new_items:
                #     structure = postprocess(structure, domain)
                #     is_correct = check_constraints(structure, domain=domain, is_lightweight=True)
                #     if is_correct:
                #         print(f'Created')
                population_new.append(structure)
                if len(population_new) == size:
                    return population_new
        print('End init')
    else:
        for _ in range(size):
            if _ > 150:
                population_new.append(mutation(deepcopy(env.initial_state), 0.9))
            else:
                population_new.append(deepcopy(env.initial_state))
    return population_new


def mutate_worker(args):
    structure, changes_num, min_pol_size, domain = args[0], args[1], args[2], args[3]

    # new_env = GlobalEnv()
    # new_env.domain = domain

    polygon_drop_mutation_prob = 0.2
    polygon_add_mutation_prob = 0.2
    point_drop_mutation_prob = 0.5
    point_add_mutation_prob = 0.2
    polygon_rotate_mutation_prob = 0.5
    polygon_reshape_mutation_prob = 0.5

    try:
        new_structure = copy.deepcopy(structure)

        for _ in range(changes_num):
            polygon_to_mutate = new_structure.polygons[random.randint(0, len(new_structure.polygons) - 1)]

            if random.random() < polygon_drop_mutation_prob and len(new_structure.polygons) > 1:
                # if drop polygon from structure
                new_structure.polygons.remove(polygon_to_mutate)
            elif random.random() < polygon_add_mutation_prob:
                # if add polygon to structure
                new_poly = get_random_poly(parent_structure=new_structure, domain=domain)
                if new_poly is None:
                    continue
                new_structure.polygons.append(new_poly)
            elif random.random() < polygon_rotate_mutation_prob:
                # if add polygon to structure
                angle = float(random.randint(-30, 30))
                polygon_to_mutate.rotate(angle)
            elif random.random() < polygon_reshape_mutation_prob:
                # if add polygon to structure
                polygon_to_mutate.resize(
                    max(0.25, float(np.random.normal(1, 0.5, 1)[0])),
                    max(0.25, float(np.random.normal(1, 0.5, 1)[0])))
            else:
                mutate_point_ind = random.randint(0, len(polygon_to_mutate.points) - 1)
                point_to_mutate = polygon_to_mutate.points[mutate_point_ind]
                if (random.random() < point_drop_mutation_prob and
                        len(polygon_to_mutate.points) > min_pol_size):
                    # if drop point from polygon
                    polygon_to_mutate.points.remove(point_to_mutate)
                else:
                    # if change point in polygon

                    if point_to_mutate is not None and not domain.contains(point_to_mutate):
                        print("!!!!!!!!!!!!!!1")
                        raise ValueError('Wrong prev_point')

                    new_point = get_random_point(point_to_mutate, polygon_to_mutate,
                                                 new_structure, domain=domain)
                    if new_point is None:
                        continue
                    # domains = GlobalEnv().domains
                    # params_x = [domains.len_x * 0.05, domains.len_x * 0.025]
                    # params_y = [domains.len_y * 0.05, domains.len_y * 0.025]

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

        new_structure = postprocess(new_structure, domain)
        is_correct = check_constraints(new_structure, is_lightweight=True, domain=domain)
        if not is_correct:
            return None
        return new_structure
    except Exception as ex:
        print(f'Mutation error: {ex}')
        return None


def get_pop_worker(domain):
    structure_size = 1  # random.randint(1, 2)
    print(f'Try to create size {structure_size}')

    # new_env = GlobalEnv()
    # new_env.domain = domain

    is_correct = False
    while not is_correct:
        structure = get_random_structure(min_pols_num=structure_size, max_pols_num=structure_size,
                                         min_pol_size=3, max_pol_size=6, domain=domain)
        structure = postprocess(structure, domain)
        is_correct = check_constraints(structure, is_lightweight=True, domain=domain)
        if is_correct:
            print(f'Created, size {structure_size}')
            return structure
