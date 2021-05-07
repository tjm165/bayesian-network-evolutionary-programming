import copy
import random
from algo_tools import *
from mdl_scorer import MDL_Scorer


def merge(list_of_networks):
    pass


def avg_distance(network_index, network_list):
    total = 0
    base_network = network_list[network_index]
    for network in network_list:
        total += distance(base_network, network)

    return total / len(network_list)


def distance(base_network, network):
    total = 0
    for i in range(base_network.num_nodes()):
        for j in range(base_network.num_nodes()):
            base_edge = base_network.get_edge(i, j)
            edge = network.get_edge(i, j)
            if base_edge != edge:
                total += 1

    return total


def __increase_routine(offspring_networks,
                       parent_networks,
                       current_population_size,
                       max_population_size,
                       current_generation_number,
                       max_generation_number,
                       far_factor):

    rand_1 = 0.5
    rand_2 = 0.5

    next_generation = []
    new_population_size = current_population_size
    i = 0

    print(current_population_size, max_population_size,
          current_population_size / max_population_size)
    print(current_generation_number, max_generation_number,
          current_generation_number / max_generation_number)

    print(current_population_size < max_population_size)
    print(rand_1 > current_population_size / max_population_size)
    print(rand_2 > current_generation_number / max_generation_number)
    print(i < current_population_size)

    printed = False
    while (current_population_size < max_population_size and
            rand_1 > current_population_size / max_population_size and
            rand_2 > current_generation_number / max_generation_number and
            i < current_population_size):
        if not printed:
            print("in")
            printed = True

        for j in range(len(offspring_networks)):
            network = offspring_networks[j]
            if avg_distance(j, offspring_networks) > far_factor * network.num_nodes():
                next_generation.append(network)
                next_generation.append(parent_networks[j])
                new_population_size += 1

    print("out")
    return next_generation, new_population_size


def __decrease_routine():
    pass


def AHEP(p_init, Gen_total, dataframe, max_population_size=50, verbose=0, far_factor=0.8):
    """
    p_init : Initial population size
    Gen_total: Total generation number
    num_attr: The number of attributes in the data
    """

    num_attr = len(dataframe.columns)

    scorer = MDL_Scorer(dataframe)

    Gen_c = 0  # current generation number
    if verbose > 1:
        print("starting create pop")
    population = create_population(p_init, list(dataframe.columns))
    if verbose > 1:
        print("population created")
    p_c = len(population)  # current population size

    # Evolutionary Programming Search Space
    while Gen_c < Gen_total:
        if Gen_c % 2 == 0 and verbose > 0:
            print("Gen_c:", Gen_c)
        shuffled = population.copy()
        random.shuffle(shuffled)
        to_merge = shuffled[:int(len(shuffled)/2)]
        # merge(to_merge)
        unselected = shuffled[int(len(shuffled)/2):]

        offspring = []
        for network in unselected:
            offspring.append(network.mutate())
        population += offspring
        population = scorer.n_lowest_score(
            int(len(population) / 2), population, verbose=verbose)

        Gen_c += 1

        population, p_c = __increase_routine(
            offspring_networks=offspring,
            parent_networks=unselected,
            current_population_size=p_c,
            max_population_size=max_population_size,
            current_generation_number=Gen_c,
            max_generation_number=Gen_total,
            far_factor=far_factor)
        # p_c = p_new

    return scorer.lowest_score(population)
