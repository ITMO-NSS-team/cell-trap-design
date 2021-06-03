import copy
import random
from copy import deepcopy
from multiprocessing import Pool

import numpy as np

from core.algs.postproc import postprocess
from core.optimisation.constraints import check_constraints
from core.optimisation.operators.initial import MAX_ITER, NUM_PROC
from core.structure.structure import Structure, get_random_point, get_random_poly
from core.utils import GlobalEnv


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
                is_correct = True
                break

    return new_structure


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
            elif random.random() < polygon_add_mutation_prob and \
                    len(new_structure.polygons) < domain.max_poly_num:
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
                if point_to_mutate in domain.fixed_points:
                    continue
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

            for fixed in domain.fixed_points:
                if fixed not in polygon_to_mutate.points:
                    polygon_to_mutate.points.append(deepcopy(fixed))

        new_structure = postprocess(new_structure, domain)
        is_correct = check_constraints(new_structure, is_lightweight=True, domain=domain)
        if not is_correct:
            return None
        return new_structure
    except Exception as ex:
        print(f'Mutation error: {ex}')
        import traceback
        print(traceback.format_exc())
        return None
