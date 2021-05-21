from core.optimisation.analytics import EvoAnalytics
from core.utils import GlobalEnv


def calculate_objectives(population, visualiser=None):
    model_func = GlobalEnv().model_func
    for ind_id, ind in enumerate(population):
        structure = ind.genotype
        effectiveness, speed_diff, idx = model_func(structure)
        ind.objectives = [-effectiveness]  # + speed_diff / 150 + structure.size / 100000]
        ind.analytics_objectives = [-effectiveness]
        EvoAnalytics.save_cantidate(ind.population_number, ind.objectives,
                                    ind.analytics_objectives,
                                    ind.genotype,
                                    'common_dataset', idx)


def calculate_objectives_multi(population, visualiser=None):
    model_func = GlobalEnv().model_func
    for ind_id, ind in enumerate(population):
        structure = ind.genotype
        effectiveness, speed_diff, idx = model_func(structure)
        ind.objectives = [-effectiveness + structure.size / 100000, speed_diff]
        ind.analytics_objectives = [-effectiveness]
        EvoAnalytics.save_cantidate(ind.population_number, ind.objectives,
                                    ind.analytics_objectives,
                                    ind.genotype,
                                    'common_dataset', idx)


def calculate_objectives_for_coevo(population, visualiser=None):
    model_func = GlobalEnv().model_func
    structures = []
    for pop in population:
        structure = None
        for ind_id, ind in enumerate(pop):
            if structure == None:
                structure = ind.genotype.polygons
            else:
                structure.polygons.extend(ind.genotype.polygons)
        structures.append(structure)

    for i, structure in enumerate(structures):
        effectiveness, speed_diff, idx = model_func(structure)
        for pop in population:
            ind = pop[i]
            ind.objectives = [-effectiveness]  # + speed_diff / 150 + structure.size / 100000]
            ind.analytics_objectives = [-effectiveness]
            EvoAnalytics.save_cantidate(ind.population_number, ind.objectives,
                                        ind.analytics_objectives,
                                        ind.genotype,
                                        'common_dataset', idx)
