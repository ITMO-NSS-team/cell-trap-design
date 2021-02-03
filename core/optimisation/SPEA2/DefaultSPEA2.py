from core.optimisation.SPEA2.SPEA2 import SPEA2


class DefaultSPEA2(SPEA2):

    def solution(self, verbose=False, **kwargs):
        extended_debug = verbose
        archive_history = []
        history = SPEA2.ErrorHistory()

        self.generation_number = 0

        while self.generation_number <= self.params.max_gens:
            print(f'Generation {self.generation_number}')

            for individ in self._pop:
                individ.population_number = self.generation_number

            self.fitness()

            self._archive = self.environmental_selection(self._pop, self._archive)

            union = self._archive + self._pop
            selected = self.selected(self.params.pop_size, union)

            self._pop = self.reproduce(selected, self.params.pop_size)

            self.generation_number += 1

        return history, self._archive
