import random
from network import network


def create_population(p_init, var_names):
    population = []

    for _ in range(p_init):
        matrix = create_random_matrix(var_names)
        population.append(network(matrix, var_names))

    return population


def create_random_matrix(var_names):
    matrix = []
    for i in range(len(var_names)):
        array = [random.randint(0, 1) for _ in range(len(var_names))]
        array[i] = 0
        matrix.append(array)

    return matrix


def create_blank_matrix(size):
    matrix = []
    for i in range(size):
        array = [0 for _ in range(size)]
        array[i] = 0
        matrix.append(array)

    return matrix
