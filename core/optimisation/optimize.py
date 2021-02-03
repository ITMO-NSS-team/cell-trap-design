from core.optimisation.GA.DefaultGA import DefaultGA
from core.optimisation.SPEA2.DefaultSPEA2 import DefaultSPEA2
from core.optimisation.SPEA2.Operators import default_operators
from core.optimisation.objectives import calculate_objectives
from core.structure.domain import Domain
from core.utils import GlobalEnv


def optimize(domain: Domain, mode='single_obj'):
    GlobalEnv.domain = domain
    operators = default_operators()
    results = []
    if mode == 'single_obj':
        params = DefaultGA.Params(max_gens=120, pop_size=20,
                                  crossover_rate=0.4, mutation_rate=0.6,
                                  mutation_value_rate=[])
        _, best = DefaultGA(
            params=params,
            calculate_objectives=calculate_objectives,
            evolutionary_operators=operators).solution(verbose=False)

        results = [best]

    elif mode == 'multi_obj':

        params = DefaultSPEA2.Params(max_gens=40, pop_size=30, archive_size=10,
                                     crossover_rate=0.5, mutation_rate=0.5,
                                     mutation_value_rate=[])

        _, results = DefaultSPEA2(
            params=params,
            calculate_objectives=calculate_objectives,
            evolutionary_operators=operators).solution(verbose=True)

    return results
