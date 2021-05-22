import os
import time

from core.optimisation.analytics import EvoAnalytics
from core.optimisation.coGA.coGaBase import CoGA


class DefaultCoGA(CoGA):

    def solution(self, verbose=True, **kwargs):
        extended_debug = verbose
        self.generation_number = 0

        self.fitness()
        best = None
        while self.generation_number <= self.params.max_gens:
            print(f'Generation {self.generation_number}')

            while os.path.exists('C:/stop.txt'):
                time.sleep(60)

            # if self.visualiser is not None:
            #    self.visualiser.state = VisualiserState(self.generation_number)

            # self.fitness()

            # self._pop = [_ for _ in self._pop if _.fitness > 0]

            un_pop = set()
            for i, pop in enumerate(self._pops):
                pop = [un_pop.add(str(ind.genotype)) or ind for ind in pop
                       if str(ind.genotype) not in un_pop]

                pop.extend(self.reproduce(pop, self.domains[i]))

                for individ in pop:
                    individ.population_number = self.generation_number
                    # individ.analytics_objectives = ''

            self.fitness()

            # if len(set([_.fitness for _ in self._pop])) != \
            #        len(([_.fitness for _ in self._pop])):
            #    print("!")

            for i, pop in enumerate(self._pops):
                selected = self.tournament_selection(pop=pop)
                pop = sorted(selected, key=lambda x: x.fitness)  # [0:self.params.pop_size]
                best = sorted(pop, key=lambda x: x.fitness)[0]

            print(f'Best fitness is {best.fitness}')
            self.generation_number += 1
            EvoAnalytics.create_boxplot()

        return self._pops, best
