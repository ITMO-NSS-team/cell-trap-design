from copy import deepcopy
from multiprocessing import Pool

from core.algs.postproc import postprocess
from core.optimisation.constraints import check_constraints
from core.structure.structure import get_random_structure
from core.utils import GlobalEnv

MAX_ITER = 50000
NUM_PROC = 1


def initial_pop_random(size: int, domain=None):
    print('Start init')
    population_new = []

    env = GlobalEnv()

    if domain is None:
        domain = GlobalEnv().domain

    if env.initial_state is None:
        while len(population_new) < size:
            if NUM_PROC > 1:
                with Pool(NUM_PROC) as p:
                    new_items = p.map(get_pop_worker, [domain] * size)
            else:
                new_items = [get_pop_worker(domain) for _ in range(size)]

            for structure in new_items:
                population_new.append(structure)
                if len(population_new) == size:
                    return population_new
        print('End init')
    else:
        for _ in range(size):
            # if _ > size / 2:
            #    population_new.append(mutation(deepcopy(env.initial_state), 0.9))
            # else:
            population_new.append(deepcopy(env.initial_state))
    return population_new


def get_pop_worker(domain):
    structure_size = 1  # random.randint(1, 2)
    print(f'Try to create size {structure_size}')

    # new_env = GlobalEnv()
    # new_env.domain = domain

    is_correct = False
    while not is_correct:
        structure = get_random_structure(min_pols_num=structure_size, max_pols_num=structure_size,
                                         min_pol_size=3, max_pol_size=5, domain=domain)
        # structure.plot(title='Initial')
        structure = postprocess(structure, domain)
        # structure.plot(title='Initial post')
        is_correct = check_constraints(structure, is_lightweight=True, domain=domain)
        if is_correct:
            # structure.plot(title='Initial correct')
            print(f'Created, domain {domain.name}')
            return structure
