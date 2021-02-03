from core.optimisation.analytics import EvoAnalytics
from core.utils import GlobalEnv


def calculate_objectives(population, visualiser=None):
    model_func = GlobalEnv.model_func
    for ind_id, ind in enumerate(population):
        structure = ind.genotype
        effectiveness = -model_func(structure)
        ind.objectives = [effectiveness]

        EvoAnalytics.save_cantidate(ind.population_number, ind.objectives,
                                    ind.analytics_objectives,
                                    ind.genotype,
                                    'common_dataset', ind_id)
