import copy
import random
import math

from pgmpy.estimators import BicScore
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from more_itertools import sort_together


def create_population(p_init, var_names):
    population = []

    for _ in range(p_init):
        matrix = []
        for _ in range(len(var_names)):
            array = [random.randint(0, 1) for _ in range(len(var_names))]
            matrix.append(array)

        population.append(network(matrix, var_names))

    return population
