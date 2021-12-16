from typing import Union
from BayesNet import BayesNet
import networkx as nx
import itertools


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

    # self.bn.structure.pred returns parents
    # TODO Check dspe method

    def d_seperation(self, X, Z, Y):
        bn = self.bn
        variables = self.bn.get_all_variables()
        for variable in variables:
            if len(bn.get_children(variable)) < 1:
                if not (X.__contains__(variable) or Y.__contains__(variable) or Z.__contains__(variable)):
                    bn.del_var(variable)
        children_Z = bn.get_children(Z)
        for child_Z in children_Z:
            bn.del_edge([Z, child_Z])

        interaction_graph = bn.get_interaction_graph()
        if nx.has_path(interaction_graph, X, Y):
            return False
        else:
            return True

    def min_degree(self, X):
        """

        :param X: set of nodes
        :return: ordering of variables (list)
        """
        g = self.bn.get_interaction_graph()
        # v = self.bn.get_all_variables()
        ordering = []
        while len(X):
            degree_order = sorted(list(X), key=lambda n: (g.degree[n], n))
            #print(degree_order)
            node = degree_order[0]
            ordering.append(node)
            node_neighbours = list(g.neighbors(node))
            for x in node_neighbours:
                for y in node_neighbours:
                    if not g.has_edge(x, y) or g.has_edge(y, x):
                        g.add_edge(x, y)
            g.remove_node(node)
            X.remove(node)
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
        poss_edges = list(itertools.combinations(neighbours, r=2))  # check all possible edge combinations
        edges_present = list(filter(lambda e: e in graph.edges, poss_edges))  # extract all edges that are present
        edges_to_add = list(set(poss_edges) - set(edges_present))  # delete all present edges from the possible edges
        return edges_to_add

    def pruning(self, query, evidence):
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
                self.bn.del_edge((e, c))
            # TODO: update CPT

    def marginal_distributions(self, Q, E):
        self.bn.draw_structure()
        all_cpts = self.bn.get_all_cpts()
        new_cpts = all_cpts
        print("old cpts")
        #print(all_cpts)
        for cpt in all_cpts:
            new_cpts[cpt] = self.bn.get_compatible_instantiations_table(E, all_cpts[cpt])
        print("updated cpts")
        #print(new_cpts)
        variables = self.bn.get_all_variables()
        variables.remove(Q)
        ordering = self.min_degree(variables)
        print(ordering)
        for var in ordering:
            self.multi_out(new_cpts, var)

    # def summing_out(self):

    def multi_out(self, cpts, var):
        parents = self.bn.structure.pred[var]
        if len(parents) == 0:
            p = cpts[var]['p']

        children_var = self.bn.get_children(var)
        child_cpts = []
        for child in children_var:
            child_cpts.append(self.bn.get_cpt(child))
        #print("child cpts")
        #print(cpts.items())
        rows_true = cpts[var] == 'True'
        print(rows_true)
        rows_false = cpts.loc[cpts[var] == False]

        print(rows_true)
        print(rows_false)
        for child_cpt in child_cpts:
            print("child cpt before")
            print(child_cpt)
            child_cpt.loc[child_cpt[var] == True, 'p'] = child_cpt.loc[child_cpt[child_cpt] == True] * rows_true.loc[
                rows_true[child_cpt == True], 'p']
            print("child cpt after")
            print(child_cpt)
