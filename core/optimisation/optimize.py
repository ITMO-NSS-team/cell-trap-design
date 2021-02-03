from core.optimisation.SPEA2.DefaultSPEA2 import DefaultSPEA2
from core.optimisation.SPEA2.Operators import default_operators
from core.optimisation.objectives import calculate_objectives
from core.structure.domain import Domain
from core.utils import GlobalEnv


def optimize(domain: Domain):
    GlobalEnv.domain = domain
    params = DefaultSPEA2.Params(max_gens=10, pop_size=10, archive_size=5,
                                 crossover_rate=0.5, mutation_rate=0.5,
                                 mutation_value_rate=[])
    operators = default_operators()

    _, archive_history = DefaultSPEA2(
        params=params,
        calculate_objectives=calculate_objectives,
        evolutionary_operators=operators).solution(verbose=True)

    return archive_history
