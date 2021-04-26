import copy
from pgmpy.estimators import BicScore
from more_itertools import sort_together


class MDL_Scorer:
    def __init__(self, dataframe):
        self.estimator = BicScore(dataframe)

    def score(self, network):
        total = 0
        for i in range(network.num_nodes()):
            parents = network.get_parents(i)  # get parents

            node_name = network.node_names(i)
            parent_names = network.node_names(parents)
            # print("node", node_name, "parents", parent_names)
            local_score = self.estimator.local_score(node_name, parent_names)
            # print("node", node_name, "parents", parent_names, "local score", local_score)
            total += local_score

        return total

    # this performance can be improved
    def n_lowest_score(self, n, networks):
        networks_sorted = networks.copy()
        scores = []
        for network in networks:
            scores.append(self.score(network))

        x, y = sort_together([scores, networks_sorted])

        y = list(y[:n])
        return y

    def lowest_score(self, networks):
        result = {'best_index': -1,
                  'best_score': float('inf'),
                  'best_network': None}

        for i in range(len(networks)):
            network = networks[i]
            local = self.score(network)

            if local < result['best_score']:
                result['best_index'] = i
                result['best_score'] = local
                result['best_network'] = networks[i]

        return result
