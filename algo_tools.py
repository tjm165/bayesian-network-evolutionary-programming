import random
from network import network


def create_population(p_init, var_names):
    population = []

    for _ in range(p_init):
        matrix = []
        for _ in range(len(var_names)):
            array = [random.randint(0, 1) for _ in range(len(var_names))]
            matrix.append(array)

        population.append(network(matrix, var_names))

    return population
