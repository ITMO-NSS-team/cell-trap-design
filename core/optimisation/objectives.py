from core.optimisation.analytics import EvoAnalytics
from core.simulation.dummy import simulate


def calculate_objectives(population, visualiser=None):
    for ind_id, ind in enumerate(population):
        structure = ind.genotype
        effectiveness = simulate(structure)
        ind.objectives = [effectiveness]

        EvoAnalytics.save_cantidate(ind.population_number, ind.objectives,
                                    ind.analytics_objectives,
                                    ind.genotype,
                                    'common_dataset', ind_id)
