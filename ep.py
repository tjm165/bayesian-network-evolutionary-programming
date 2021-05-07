import copy
import random
from algo_tools import *
from mdl_scorer import MDL_Scorer


def EP(p_init, Gen_total, dataframe, verbose=0):
    """
    p_init : Initial population size
    Gen_total: Total generation number
    num_attr: The number of attributes in the data
    """

    score_history_dict = {}
    network_history_dict = {}

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
        score_history_dict[Gen_c] = []
        network_history_dict[Gen_c] = []
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
            int(len(population) / 2), population, score_history_dict[Gen_c], network_history_dict[Gen_c], verbose=verbose)

        Gen_c += 1
        # p_new = this is the increase and decrease routines
        # p_c = p_new

    return scorer.lowest_score(population), score_history_dict, network_history_dict
