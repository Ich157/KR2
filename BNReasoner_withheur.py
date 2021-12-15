from typing import Union
from BayesNet import BayesNet
import os
import networkx as nx
import itertools

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class BNReasoner:
    def __init__(self, net: Union[str, BayesNet]):
        """
        :param net: either file path of the bayesian network in BIFXML format or BayesNet object
        """
        if type(net) == str:
            # constructs a BN object
            self.bn = BayesNet()
            # Loads the BN from an BIFXML file
            self.bn.load_from_bifxml(net)
        else:
            self.bn = net

    # TODO: This is where your methods should go

    def d_sep(self, x, y, z):
        """
        given 3 sets of variables X, Y, and Z. d_sep checks if X is independent from Y given Z.
        :return: true or false
        """
        g = self.bn.get_interaction_graph()
        var = self.bn.get_all_variables()

        for v in var:
            g.

    def min_degree(self, X):
        """

        :param X: set of nodes
        :return: ordering of variables (list)
        """
        g = self.bn.get_interaction_graph()
        #v = self.bn.get_all_variables()
        ordering = []
        while X:
            degree_order = sorted(list(X), key=lambda n: (g.degree[n], n))
            print(degree_order)
            node = degree_order[0]
            ordering.append(node)
            node_neighbours = list(g.neighbors(node))
            for x in node_neighbours:
                for y in node_neighbours:
                    if not g.has_edge(x, y) or g.has_edge(y, x):
                        g.add_edge(x, y)
            g.remove_node(node)
        return ordering

    def min_fill(self, X):
        """

        :param X: set of nodes
        :return: list of ordering for variable eliminiation
        """

        g = self.bn.get_interaction_graph()
        ordering = sorted(list(X), key=lambda x: (len(self.search_edges(x, g)), x))
        return ordering


    def search_edges(self, node, graph: nx.DiGraph):
        neighbours = list(graph.neighbors(node))
        poss_edges = list(itertools.combinations(neighbours, r=2))  #check all possible edge combinations
        edges = list(filter(lambda e: e in graph.edges, poss_edges))
        edges_to_add = list(set(poss_edges) - set(edges))
        return edges_to_add


    def pruning(self, query , evidence):
        """
        Given a set of query variables Q and evidence E, function node-prunes the
        Bayesian network
        :return: returns pruned Bayesian network
        """

        var = self.bn.get_all_variables()
        # node pruning
        for v in var:
            if (v not in query) and (v not in evidence) and (not self.bn.get_children(v)):
                self.bn.del_var(v)
        # edge pruning
        for e in evidence:
            children = self.bn.get_children(e)
            for c in children:
                self.bn.del_edge([e, c])
            # TODO: update CPT

    def marg_distr(self, q, e):
        """

        :return:
        """
        var = self.bn.get_all_variables()
        ordering = self.min_degree(var)

        cpt =