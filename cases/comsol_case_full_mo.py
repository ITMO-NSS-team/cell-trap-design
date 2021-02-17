import random

import mph
import numpy as np
import scipy

from core.optimisation.analytics import EvoAnalytics
from core.optimisation.optimize import optimize
from core.simulation.comsol import execute as execute_comsol
from core.structure.domain import Domain
from core.utils import GlobalEnv

# mport ray

if __name__ == '__main__':
    random.seed(42)
    np.random.seed(42)
    scipy.random.seed(42)

    EvoAnalytics.clear()

    domain = Domain()

    global_env = GlobalEnv()
    global_env.domain = domain
    global_env.model_func = execute_comsol
    global_env.comsol_client = mph.Client(cores=12)
    global_env.full_save_load = False

    optimization_results = optimize(domain, max_gens=300, pop_size=300, mode='multi_obj')

    for result in optimization_results:
        print(result.objectives)
        print(str(result.genotype))

    EvoAnalytics.create_boxplot()
