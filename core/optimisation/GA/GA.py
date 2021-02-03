import copy
import math
from random import randint


class GA:
    def __init__(self, params, calculate_objectives, evolutionary_operators,
                 visualiser=None, greedy_heuristic=False,
                 is_refinement=False, is_surrogate=False):
        '''
         Genetic algorithm (GA)
        '''

        self.params = params

        self.calculate_objectives = calculate_objectives
        self.operators = evolutionary_operators

        self.__init_operators()
        self.__init_populations()

        self.visualiser = visualiser
        self.greedy_heuristic = greedy_heuristic

    def __init_operators(self):
        self.init_population = self.operators.init_population
        self.crossover = self.operators.crossover
        self.mutation = self.operators.mutation

    def __init_populations(self):

        gens = self.init_population(self.params.pop_size)
        self._pop = [GA.Individ(genotype=gen) for gen in gens]

    class Params:
        def __init__(self, max_gens, pop_size, crossover_rate, mutation_rate, mutation_value_rate):
            self.max_gens = max_gens
            self.pop_size = pop_size
            self.crossover_rate = crossover_rate
            self.mutation_rate = mutation_rate
            self.mutation_value_rate = mutation_value_rate

    class Individ:
        def __init__(self, genotype):
            self.objectives = ()
            self.analytics_objectives = []
            self.fitness = None
            self.genotype = copy.deepcopy(genotype)
            self.population_number = 0

    def solution(self, verbose=True, **kwargs):
        pass

    def fitness(self):

        self.calculate_objectives(population=self._pop, visualiser=self.visualiser)
        for ind in self._pop:
            ind.fitness = ind.objectives[0]

    def random_selection(self, group_size):
        return [self._pop[randint(0, len(self._pop) - 1)] for _ in range(group_size)]

    def tournament_selection(self, fraction=0.1):
        group_size = math.ceil(len(self._pop) * fraction)
        min_group_size = 2 if len(self._pop) > 1 else 1
        group_size = max(group_size, min_group_size)
        chosen = []
        for _ in range(self.params.pop_size):
            group = self.random_selection(group_size)
            best = min(group, key=lambda ind: ind.fitness)
            chosen.append(best)

        return chosen

    def reproduce(self, selected):

        children = []

        for pair_index in range(0, len(selected), 2):
            p1 = selected[pair_index]
            p2 = selected[pair_index + 1]

            child_gen = self.crossover(p1.genotype, p2.genotype, self.params.crossover_rate)
            child_gen = self.mutation(child_gen, self.params.mutation_rate)
            child = GA.Individ(genotype=child_gen)
            children.append(child)

        return children
