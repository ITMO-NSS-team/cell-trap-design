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

    domain1 = Domain(name='A',
                     allowed_area=[(-98.5, -87.3), (-98.5, 87.4), (31.0, 87.4), (37.2, 43.5), (-9.7, -49.5),
                                   (-9.7, -75.4), (3.7, -87.3)], max_poly_num=4, min_dist=15)
    domain2 = Domain(name='P1',
                     allowed_area=[(13.62, -64.735), (13.62, -49.53), (30.575, -49.53), (30.575, -64.735)],
                     max_poly_num=1, min_dist=5)
    domain3 = Domain(name='P2',
                     allowed_area=[(24.515, -40.105), (24.515, -27.130), (30.572, -27.130), (30.572, -40.105)],
                     max_poly_num=1, min_dist=5)
    domain4 = Domain(name='P3',
                     allowed_area=[(36.355, -17.59), (36.355, -4.605), (43.195, -4.605), (43.195, -17.590)],
                     max_poly_num=1, min_dist=5)
    domain5 = Domain(name='P4',
                     allowed_area=[(48.315, 4.875), (48.315, 18.020), (57.078, 18.020), (57.078, 4.875)],
                     )
    domain6 = Domain(name='P5',
                     allowed_area=[(58.975, 27.38), (58.975, 43.020), (68.26, 43.02), (68.26, 27.38)],
                     max_poly_num=1, min_dist=5)
    domain7 = Domain(name='P6',
                     allowed_area=[(46.6, 52.5), (46.6, 82.5), (68.26, 82.50), (68.26, 52.50)],
                     max_poly_num=1, min_dist=5)

    domains = [domain1, domain2, domain3, domain4, domain5, domain6, domain7]

    global_env = GlobalEnv()
    global_env.domain = domains
    global_env.model_func = execute_comsol
    global_env.comsol_client = mph.Client(cores=1)
    global_env.full_save_load = False

    optimization_results = optimize(domains, max_gens=4, pop_size=4, mode='single_obj')

    for result in optimization_results:
        print(result.objectives)
    print(str(result.genotype))

    EvoAnalytics.create_boxplot()
