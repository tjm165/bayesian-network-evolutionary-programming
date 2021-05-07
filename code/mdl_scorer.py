import copy
from pgmpy.estimators import BicScore
from more_itertools import sort_together
from network import network


class MDL_Scorer:
    def __init__(self, dataframe):
        self.estimator = BicScore(dataframe)
        self.hashed_local_scores = {}

    def local_score(self, node_name, parent_names):
        key = node_name + str(parent_names)
        if key not in self.hashed_local_scores:
            score = abs(self.estimator.local_score(node_name, parent_names))
            self.hashed_local_scores[key] = score

        return self.hashed_local_scores[key]

    def score(self, network, verbose=0):
        total = 0
        if verbose > 2:
            print("starting scoring")
        for i in range(network.num_nodes()):
            if verbose > 3:
                print("node", i)

            parents = network.get_parents(i)  # get parents

            node_name = network.node_names(i)
            parent_names = network.node_names(parents)
            # print("node", node_name, "parents", parent_names)
            if verbose > 3:
                print("starting local score")
            local_score_ = self.local_score(node_name, parent_names)
            if verbose > 3:
                print("ended local score")
            # print("node", node_name, "parents",
            #      parent_names, "local score", local_score)
            total += local_score_
        if verbose > 2:
            print("ended scoring")

        return total

    # this performance can be improved
    def n_lowest_score(self, n, networks, score_history_list, network_history_list, verbose=False):
        networks_sorted = networks.copy()
        scores = []
        for network in networks:
            score_ = self.score(network, verbose=verbose)
            scores.append(score_)

        x, y = sort_together([scores, networks_sorted])
        score_history_list += list(x)
        network_history_list += list(y)

        y = list(y[:n])
        return y

    def lowest_score(self, networks, verbose=False):
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
