import copy
import math
from random import randint

import numpy as np

from core.utils import GlobalEnv


class CoGA:
    def __init__(self, params, calculate_objectives, evolutionary_operators,
                 visualiser=None, greedy_heuristic=False,
                 is_refinement=False, is_surrogate=False):
        '''
         Genetic algorithm (GA)
        '''

        domains = GlobalEnv().domain

        self.co_num = len(domains)
        self.domains = domains

        self.params = params

        self.calculate_objectives = calculate_objectives
        self.operators = evolutionary_operators

        self._pops = []

        self.__init_operators()
        self.__init_populations()

        self.visualiser = visualiser
        self.greedy_heuristic = greedy_heuristic

        self.generation_number = 0

    def __init_operators(self):
        self.init_population = self.operators.init_population
        self.crossover = self.operators.crossover
        self.mutation = self.operators.mutation

    def __init_populations(self):
        for i in range(self.co_num):
            gens = self.init_population(self.params.pop_size, GlobalEnv().domain[i])
            _pop = [CoGA.Individ(genotype=gen) for gen in gens]
            self._pops.append(_pop)

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

        self.calculate_objectives(population=self._pops, visualiser=self.visualiser)
        for pop in self._pops:
            for ind in pop:
                ind.fitness = ind.objectives[0]

    def random_selection(self, group_size, pop):
        return [pop[randint(0, len(pop) - 1)] for _ in range(group_size)]

    def tournament_selection(self, pop, fraction=0.1):
        group_size = math.ceil(len(pop) * fraction)
        min_group_size = 2 if len(pop) > 1 else 1
        group_size = max(group_size, min_group_size)
        chosen = []
        n_iter = 0
        while len(chosen) < self.params.pop_size:
            n_iter += 1
            group = self.random_selection(group_size, pop)
            best = min(group, key=lambda ind: ind.fitness)
            best.generation_number = self.generation_number
            if best not in chosen:
                chosen.append(best)
            elif n_iter > self.params.pop_size + 100:
                print('RAND SELECTED')
                n_iter = 0
                rnd = pop[randint(0, len(pop) - 1)]
                chosen.append(rnd)
        return chosen

    def reproduce(self, selected, domain):

        children = []
        np.random.shuffle(selected)
        for pair_index in range(0, len(selected) - 1):
            p1 = selected[pair_index]
            p2 = selected[pair_index + 1]

            child_gen = self.crossover(p1.genotype, p2.genotype, self.params.crossover_rate, domain=domain)
            child_gen = self.mutation(child_gen, self.params.mutation_rate, domain=domain)
            if str(child_gen) != str(p1.genotype) and str(child_gen) != str(p2.genotype):
                child = CoGA.Individ(genotype=copy.deepcopy(child_gen))
                child.generation_number = self.generation_number
                children.append(child)

        return children
