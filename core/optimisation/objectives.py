from core.simulation.dummy import simulate


def calculate_objectives(population, visualiser=None):
    for ind in population:
        structure = ind.genotype
        effectiveness = simulate(structure)
        print(effectiveness)
        ind.objectives = [effectiveness]
