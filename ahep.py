import copy
import random
from algo_tools import *
from mdl_scorer import MDL_Scorer

"""
def merge(list_of_networks):
    pass

def __increase_routine(offspring_networks,
                       rand_1, 
                       current_population_size, 
                       max_population_size, 
                       current_generation_number,
                       max_generation_number):
    
    next_generation = []
    new_population_size = current_population_size
    i = 0
    while (rand_1 > current_population_size / max_population_size and 
           rand_2 > current_generation_number / max_generation_number and 
           i < current_population_size):
        for network in offspring_networks: #networks are the mutated offspring
            if avg_distance(network) > far_factor.cross(num_nodes(network)):
                next_generation.append(network) # and both its parents
                new_population_size += 1
                
    return next_generation
            
def __decrease_routine():
    pass
"""


def A_HEP(p_init, Gen_total, dataframe):
    """
    p_init : Initial population size
    Gen_total: Total generation number
    num_attr: The number of attributes in the data
    """

    num_attr = len(dataframe.columns)

    scorer = MDL_Scorer(dataframe)

    Gen_c = 0  # current generation number
    population = create_population(p_init, list(dataframe.columns))
    p_c = len(population)  # current population size

    while Gen_c < Gen_total:
        shuffled = population.copy()
        random.shuffle(shuffled)
        to_merge = shuffled[:int(len(shuffled)/2)]
        # merge(to_merge)
        unselected = shuffled[int(len(shuffled)/2):]

        offspring = []
        for network in unselected:
            offspring.append(network.mutate())
        population += offspring

        Gen_c += 1
        # p_new = this is the increase and decrease routines
        # p_c = p_new

    return scorer.lowest_score(population)
