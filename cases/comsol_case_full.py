import random

import mph
import numpy as np

from core.optimisation.analytics import EvoAnalytics
from core.optimisation.optimize import optimize
from core.simulation.comsol import execute as execute_comsol
from core.structure.domain import Domain
from core.utils import GlobalEnv

random.seed(42)
np.random.seed(42)

EvoAnalytics.clear()

domain = Domain(min_x=-125, max_x=25, min_y=-150, max_y=135)

GlobalEnv.domain = domain
GlobalEnv.model_func = execute_comsol
GlobalEnv.comsol_client = mph.Client(cores=4)

optimization_results = optimize(domain)

for result in optimization_results:
    print(result.objectives)
    print(str(result.genotype))

EvoAnalytics.create_boxplot()
