from typing import Union
from BayesNet import BayesNet
import networkx as nx


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

    def d_seperation(self, X,Z,Y):
        bn = self.bn
        variables = self.bn.get_all_variables()
        for variable in variables:
            if len(bn.get_children(variable)) < 1:
                if not (X.__contains__(variable) or Y.__contains__(variable) or Z.__contains__(variable)):
                    bn.del_var(variable)
        children_Z = bn.get_children(Z)
        for child_Z in children_Z:
            bn.del_edge([Z, child_Z])

        interaction_graph= bn.get_interaction_graph()
        if nx.has_path(interaction_graph, X, Y):
            return False
        else: return True

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

    def min_fill(self, bn: BayesNet): #TODO has errors
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

    def marginal_distributions(self, Q, E):
        all_cpts = self.bn.get_all_cpts()
        new_cpts = all_cpts
        #print("old cpts")
        #print(all_cpts)
        for cpt in all_cpts:
            new_cpts[cpt] = self.bn.get_compatible_instantiations_table(E, all_cpts[cpt])
        #print("updated cpts")
        #print(new_cpts)
        variables = self.bn.get_all_variables()
        variables.remove(Q)
        ordering = self.min_degree(variables)
        for var in ordering:
            self.multi_out(new_cpts[var], var)
        #for var in ordering:

    #def summing_out(self):

    def multi_out(self, cpt, var):
        children_var = self.bn.get_children(var)
        child_cpts = []
        for child in children_var:
            child_cpts.append(self.bn.get_cpt(child))
        print("child cpts")
        rows_true = cpt.loc[cpt[var] == True]
        rows_false = cpt.loc[cpt[var] == False]
        for child_cpt in child_cpts:
            print("child cpt before")
            print(child_cpt)
            child_cpt.loc[child_cpt[var]==True , 'p'] = child_cpt.loc[child_cpt[child_cpt]==True] * rows_true.loc[rows_true[child_cpt==True], 'p']
            print("child cpt after")
            print(child_cpt)




        #children_A = self.bn.get_children(A)
        #A_cpt = self.bn.get_cpt(A)
        #A_true = A_cpt.loc[A_cpt[A]==True]
        #print(float(A_true['p']))
        #A_false = A_cpt.loc[A_cpt[A] == False]
        #for child in children_A:
        #    child_cpt = self.bn.get_cpt(child)
        #    rows_true = child_cpt.loc[child_cpt[A] == True]
        #    rows_true['p']*float(A_true['p'])
                #print(child_cpt)
                #row['p']=row['p']* A_true
                #child_cpt.loc[row, 'p'] = child_cpt.loc[row, 'p'] * A_true
                #print(child_cpt)
              #  child_cpt.loc[child_cpt['p']

            #undone. multiply False rows as well and integrate in A cpt
            #update cpts

        #add summup function-maybe inside multi-out bc now we would have true and falses for a and to som out we could add first element in true and first and false

        #