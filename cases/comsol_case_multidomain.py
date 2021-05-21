import random

import mph
import numpy as np
import scipy

from core.optimisation.analytics import EvoAnalytics
from core.optimisation.optimize import optimize
from core.simulation.comsol import execute as execute_comsol
from core.structure.domain import Domain
from core.utils import GlobalEnv

if __name__ == '__main__':
    random.seed(42)
    np.random.seed(42)
    scipy.random.seed(42)

    EvoAnalytics.clear()

    domain1 = Domain(allowed_area=[(-125, 100),
                                   (-75, 155),
                                   (15, 155),
                                   (40, 90),
                                   (-10, -130),
                                   (-10, -155),
                                   (-125, -155)])
    domain2 = Domain(allowed_area=[(-125, 100),
                                   (-75, 155),
                                   (15, 155),
                                   (40, 90),
                                   (-10, -130),
                                   (-10, -155),
                                   (-125, -155)])

    domains = [domain1, domain2]

    global_env = GlobalEnv()
    global_env.domain = domains
    global_env.model_func = execute_comsol
    global_env.comsol_client = mph.Client(cores=12)
    global_env.full_save_load = False

    optimization_results = optimize(domains, max_gens=4, pop_size=4, mode='single_obj')

    for result in optimization_results:
        print(result.objectives)
        print(str(result.genotype))

    EvoAnalytics.create_boxplot()
