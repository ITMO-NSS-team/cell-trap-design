from core.optimisation.analytics import EvoAnalytics
from core.optimisation.optimize import optimize
from core.simulation.dummy import execute as execute_dummy
from core.structure.domain import Domain
from core.utils import GlobalEnv

EvoAnalytics.clear()

domain = Domain(min_x=0, max_x=10, min_y=0, max_y=5)
GlobalEnv.model_func = execute_dummy
GlobalEnv.domain = domain

optimization_results = optimize(domain)

for result in optimization_results:
    print(result.objectives)
    print(str(result.genotype))

EvoAnalytics.create_boxplot()
