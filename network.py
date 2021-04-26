import copy
import random
import math

from pgmpy.estimators import BicScore
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from more_itertools import sort_together


def check_for_self_pointers(matrix):
    for i in range(len(matrix)):
        if matrix[i][i] == 1:
            matrix[i][i] = 0


class network:
    def __init__(self, matrix, var_names):
        """
        matrix is [parents_of_node, parents_of_node, ...]
        """

        check_for_self_pointers(matrix)

        self.matrix = pd.DataFrame(matrix)
        self.var_names = var_names

    def node_names(self, nodes):
        if isinstance(nodes, list):
            names = []
            for i in nodes:
                names.append(self.__node_name(i))
            return names
        return self.__node_name(nodes)

    def __node_name(self, i):
        return self.var_names[i]

    def num_nodes(self):
        return len(self.var_names)

    def get_node(i, j=None):
        if j is None:
            return self.matrix.item(i)
        return self.item((i, j))

    def get_parents(self, i):
        """
        returns the column indices of the parents of node i
        """

        parents = []
        possible_parents = list(range(self.num_nodes()))

        for possible_parent_i in possible_parents:
            if self.matrix[i][possible_parent_i] == 1:  # might be flipped
                parents.append(possible_parent_i)

        return parents

    def mutate(self):
        mutations = [network.__delete_edge]
        num_nodes = len(self.matrix)

        node = random.randint(0, num_nodes - 1)
        parent = random.randint(0, num_nodes - 1)
        mutation = random.randint(0, len(mutations) - 1)

        return mutations[mutation](self, node, parent)

    def copy(self):
        return network(copy.deepcopy(self.matrix), self.var_names)

    def __delete_edge(self, node, parent):
        network2 = self.copy()
        network2.matrix[node][parent] = 0
        return network2

    def draw(self):
        #matrix = pd.DataFrame([[0, 1, 1], [0, 0, 0], [0, 0, 0]])
        #var_names = ['A', 'B', 'C']
        matrix = self.matrix
        var_names = self.var_names

        from_ = []
        to = []

        for col in range(len(matrix.columns)):
            for row in range(len(matrix[col])):
                if matrix[col][row] == 1:
                    from_.append(var_names[row])
                    to.append(var_names[col])

        net_frame = pd.DataFrame({'from': from_, 'to': to})
        G = nx.from_pandas_edgelist(
            net_frame, 'from', 'to', create_using=nx.DiGraph())
        nx.draw(G, with_labels=True)
        plt.show()
