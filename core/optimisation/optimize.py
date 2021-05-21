from typing import List, Union

from core.optimisation.GA.DefaultGA import DefaultGA
from core.optimisation.SPEA2.DefaultSPEA2 import DefaultSPEA2
from core.optimisation.SPEA2.Operators import default_operators
from core.optimisation.coGA.coGA import DefaultCoGA
from core.optimisation.objectives import calculate_objectives, calculate_objectives_multi
from core.structure.domain import Domain
from core.utils import GlobalEnv


def optimize(domain: Union[Domain, List[Domain]], max_gens=300, pop_size=300, mode='single_obj'):
    GlobalEnv().domain = domain
    operators = default_operators()
    results = []
    if isinstance(domain, list):
        params = DefaultCoGA.Params(max_gens=max_gens, pop_size=pop_size,
                                    crossover_rate=0.6, mutation_rate=0.6,
                                    mutation_value_rate=[])
        _, best = DefaultCoGA(
            params=params,
            calculate_objectives=calculate_objectives,
            evolutionary_operators=operators).solution(verbose=False)

        results = [best]
    else:
        if mode == 'single_obj':
            params = DefaultGA.Params(max_gens=max_gens, pop_size=pop_size,
                                      crossover_rate=0.6, mutation_rate=0.6,
                                      mutation_value_rate=[])
            _, best = DefaultGA(
                params=params,
                calculate_objectives=calculate_objectives,
                evolutionary_operators=operators).solution(verbose=False)

            results = [best]

        elif mode == 'multi_obj':
            params = DefaultSPEA2.Params(max_gens=max_gens, pop_size=pop_size, archive_size=int(round(pop_size / 4)),
                                         crossover_rate=0.6, mutation_rate=0.6,
                                         mutation_value_rate=[])

            _, results = DefaultSPEA2(
                params=params,
                calculate_objectives=calculate_objectives_multi,
                evolutionary_operators=operators).solution(verbose=True)

    return results
