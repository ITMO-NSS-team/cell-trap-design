from core.optimisation.operators import (crossover, initial, mutation)


class EvoOperators:
    def __init__(self, init_population, crossover, mutation):
        self.init_population = init_population
        self.crossover = crossover
        self.mutation = mutation


def default_operators():
    return EvoOperators(init_population=initial.initial_pop_random,
                        crossover=crossover.crossover,
                        mutation=mutation.mutation)
