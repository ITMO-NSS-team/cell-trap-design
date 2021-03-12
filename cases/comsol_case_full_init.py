import random

import mph
import numpy as np
import scipy

from core.optimisation.analytics import EvoAnalytics
from core.optimisation.optimize import optimize
from core.simulation.comsol import execute as execute_comsol
from core.structure.domain import Domain
from core.structure.polygon import Polygon, PolygonPoint
from core.structure.structure import Structure
from core.utils import GlobalEnv

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
    global_env.initial_state = Structure([
        Polygon('initial1', [
            PolygonPoint(-104, -131),
            PolygonPoint(-44, -9),
            PolygonPoint(8, 61),
            PolygonPoint(17, 54),
            PolygonPoint(17, 44),
            PolygonPoint(-3, -17),
            PolygonPoint(4, 0),
            PolygonPoint(-0, -12),
            PolygonPoint(-16, -32),
            PolygonPoint(-17, -39),
            PolygonPoint(-10, -55),
            PolygonPoint(-54, -151),
            PolygonPoint(-90, -151),
            PolygonPoint(-102, -143)
        ]),
        Polygon('initial2', [
            PolygonPoint(-75, 90),
            PolygonPoint(-57, 114),
            PolygonPoint(17, 114),
            PolygonPoint(20, 103),
            PolygonPoint(-57, 35),
            PolygonPoint(-75, 62),
        ])
    ])

    optimization_results = optimize(domain, max_gens=300, pop_size=300, mode='single_obj')

    for result in optimization_results:
        print(result.objectives)
        print(str(result.genotype))

    EvoAnalytics.create_boxplot()
