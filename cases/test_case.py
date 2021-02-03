from core.optimisation.optimize import optimize
from core.structure.domain import Domain

domain = Domain(min_x=0, max_x=10, min_y=0, max_y=5)
optimization_results = optimize(domain)

for result in optimization_results:
    print(len(result.genotype.polygons), result.objectives)
