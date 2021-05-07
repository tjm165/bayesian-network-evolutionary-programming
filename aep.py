import copy
import random
from algo_tools import *
from mdl_scorer import MDL_Scorer


def avg_distance(base_network, network_list):
    total = 0
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


def AEP(p_init, p_max, Gen_total, dataframe,  pop_threshold, gen_threshold, distance_theshold=1, verbose=0):
    """
    p_init : Initial population size
    Gen_total: Total generation number
    num_attr: The number of attributes in the data
    """

    score_history_dict = {}
    network_history_dict = {}
    pop_size_history = []

    num_attr = len(dataframe.columns)

    scorer = MDL_Scorer(dataframe)

    Gen_c = 0  # current generation number
    if verbose > 1:
        print("starting create pop")
    population = create_population(p_init, list(dataframe.columns))
    if verbose > 1:
        print("population created")
    p_c = len(population)  # current population size

    while Gen_c < Gen_total:
        print("Running Generation", Gen_c)
        score_history_dict[Gen_c] = []
        network_history_dict[Gen_c] = []

        shuffled = population.copy()
        random.shuffle(shuffled)
        to_merge = shuffled[:int(len(shuffled)/2)]
        # merge(to_merge)
        unselected = shuffled[int(len(shuffled)/2):]
        parents = unselected

        offspring = []
        for network in unselected:
            network.marker = 0
            m = network.mutate()
            m.marker = 1
            offspring.append(m)

        # increase routine
        print("     increase routine")
        p_new = p_c
        a = 0

        offspring_to_keep = []
        parents_to_keep = []
        c_i = 0
        while p_new < p_max and pop_threshold > (p_new / p_max) and Gen_c < gen_threshold and a < p_c and c_i < len(offspring):
            for child_i in range(len(offspring)):
                c_i += 1
                child = offspring[child_i]
                parent = child.parent
                if avg_distance(child, offspring) > distance_theshold:
                    offspring_to_keep.append(child)
                    parents_to_keep.append(parent)
                    p_new += 2
            a += 1

        if len(offspring_to_keep) + len(parents_to_keep) == 0:
            parents_to_keep = parents
            offspring_to_keep = unselected

        population += offspring_to_keep
        population += parents_to_keep

        # decrease routine
        print("     decrease routine")
        repeat = set()
        pop_size_before_decrease = len(population)
        for j in range(len(offspring_to_keep)):
            for k in range(len(offspring_to_keep)):
                if j != k and str(k) + str(j) not in repeat:
                    repeat.add(str(j) + str(k))

                    # mark then as offspring BEFORE starting decrease routine? Not really sure actually
                    offspring_j = offspring_to_keep[j]
                    offspring_j.marker = 1
                    offspring_k = offspring_to_keep[k]
                    offspring_k.marker = 1

                    parent_j = offspring_j.parent
                    parent_j.marker = 0
                    parent_k = offspring_k.parent
                    parent_k.marker = 0

                    selected = [offspring_j, offspring_k, parent_j, parent_k]

                    score_history_dict[Gen_c] = []
                    network_history_dict[Gen_c] = []

                    best = scorer.n_lowest_score(
                        2, selected, score_history_dict[Gen_c], network_history_dict[Gen_c])

                    if distance(best[0], best[1]) == 0:
                        try:
                            population.remove(best[0])
                        except ValueError:
                            pass
                    elif best[0].marker == 1 and best[1].marker == 1:
                        try:
                            population.remove(best[0])
                        except ValueError:
                            pass

        pop_size_history.append(len(population))

        Gen_c += 1

    return scorer.lowest_score(population), score_history_dict, network_history_dict, pop_size_history
