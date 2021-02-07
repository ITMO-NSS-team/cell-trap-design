from core.optimisation.GA.GA import GA
from core.optimisation.analytics import EvoAnalytics


class DefaultGA(GA):

    def solution(self, verbose=True, **kwargs):
        extended_debug = verbose
        self.generation_number = 0

        self.fitness()
        best = None
        while self.generation_number <= self.params.max_gens:
            print(f'Generation {self.generation_number}')

            # if self.visualiser is not None:
            #    self.visualiser.state = VisualiserState(self.generation_number)

            # self.fitness()

            # self._pop = [_ for _ in self._pop if _.fitness > 0]

            un_pop = set()
            self._pop = \
                [un_pop.add(str(ind.genotype)) or ind for ind in self._pop
                 if str(ind.genotype) not in un_pop]

            self._pop.extend(self.reproduce(self._pop))

            for individ in self._pop:
                individ.population_number = self.generation_number
                individ.analytics_objectives = ''  # individ.genotype.text_id

            self.fitness()

            if len(set([_.fitness for _ in self._pop])) != \
                    len(([_.fitness for _ in self._pop])):
                print("!")

            selected = self.tournament_selection()
            self._pop = sorted(selected, key=lambda x: x.fitness)  # [0:self.params.pop_size]
            best = sorted(self._pop, key=lambda x: x.fitness)[0]
            print(f'Best fitness is {best.fitness}')
            self.generation_number += 1
            EvoAnalytics.create_boxplot()

        return self._pop, best
