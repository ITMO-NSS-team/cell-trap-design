from core.optimisation.GA.GA import GA


class DefaultGA(GA):

    def solution(self, verbose=True, **kwargs):
        extended_debug = verbose
        self.generation_number = 0

        self.fitness()

        while self.generation_number <= self.params.max_gens:
            print(f'Generation {self.generation_number}')

            # if self.visualiser is not None:
            #    self.visualiser.state = VisualiserState(self.generation_number)

            for individ in self._pop:
                individ.population_number = self.generation_number

            selected = self.tournament_selection()

            self._pop.extend(self.reproduce(selected))

            self.fitness()

            self.generation_number += 1

        best = sorted(self._pop, key=lambda x: x.fitness)[0]
        return self._pop, best
