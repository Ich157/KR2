from typing import Union
from BayesNet import BayesNet
import os

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

    def min_degree(self, v):
        """

        :param net: Bayesian Network
        :return: ordering of variables (list)
        """
        g = self.bn.get_interaction_graph()
        #v = self.bn.get_all_variables()
        ordering = []
        while v:
            neighbours = []
            for i in v:
                neighbours.append(len(list(g.neighbors(i))))  # get the variable with the smallest number of neighbours
            min_n = min(neighbours)
            min_index = neighbours.index(min_n)
            min_deg_var = v[min_index]

            # add edge between every pair of non adjacent neighbours neighbours of min_deg_var
            min_deg_var_neigh = list(g.neighbors(min_deg_var))
            print(min_deg_var_neigh)
            for x in min_deg_var_neigh:
                for y in min_deg_var_neigh:
                    if not g.has_edge(x, y) or g.has_edge(y, x):
                        g.add_edge(x, y)

                # delete variable from graph and add to ordering
            g.remove_node(min_deg_var)
            v.remove(min_deg_var)
            ordering.append(min_deg_var)

        print(ordering)
        return ordering

    def min_fill(self, bn: BayesNet):
        """

        :param bn: Bayesian Network
        :return: ordering of variables (list)
        """
        g = bn.get_interaction_graph()
        v = bn.get_all_variables()
        ordering = []
        neighbours = []

        for i in v:
            # get the variable with the smallest number of neighbours
            neighbours.append(len(g.neighbors(i)))
            max_n = max(neighbours)
            max_index = neighbours.index(max_n)
            min_fill_var = v[max_index]
            min_fill_neigh = g.neighbors(min_fill_var)  # save neighbours of variable with minimal degree

            # add edge between every pair of non adjacent neighbours neighbours of min_deg_var
            edges = g.edges(min_fill_var)
            for x in min_fill_neigh:
                if (min_fill_var, x) not in edges:
                    g.add_edge(min_fill_var, x)

            # delete variable from graph and add to ordering
            g.remove_node(min_fill_var)
            v.remove(min_fill_var)
            ordering.append(min_fill_var)
            print(ordering)

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
                # TODO: add that the CPT must be updated.
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