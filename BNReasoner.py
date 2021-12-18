from typing import Union
from BayesNet import BayesNet
import networkx as nx
import itertools
import copy
import pandas as pd
import numpy as np
import random
from string import ascii_lowercase


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
            # print(degree_order)
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

    def random_order(self, X):
        order = random.sample(X, len(X))
        return order

    def pruning(self, query, evidence):
        """
        Given a set of query variables Q and evidence E, function node-prunes the
        Bayesian network
        :return: returns pruned Bayesian network
        """

        var = self.bn.get_all_variables()
        # node pruning
        for v in var:

            if (v not in query) and (v not in evidence) and (len(self.bn.get_children(v)) == 0):
                self.bn.del_var(v)
                # TODO: add that the CPT must be updated.
        # edge pruning
        print(evidence.index)
        for e in evidence.index:
            children = self.bn.get_children(e)
            for c in children:
                self.bn.del_edge((e, c))
            # TODO: update CPT

    def marginal_distributions(self, Q, E, order_heu):
        """Calculates marginal distribution for variables in Q (list) given evidence E (pd series of dict). 

                eliminates every var not in q and updates cpts in new_cpts. Returns a cpt (dataframe) with onle the Q vars
                """
        # self.bn.draw_structure()
        all_cpts = self.bn.get_all_cpts()
        new_cpts = all_cpts.copy()
        # print("old cpts")
        # print(all_cpts)
        for cpt in all_cpts:
            new_cpts[cpt] = self.bn.get_compatible_instantiations_table(E, all_cpts[cpt])
        # print("updated cpts")
        # print(new_cpts)
        variables = self.bn.get_all_variables()
        for var in Q:
            variables.remove(var)
        ordering = self.random_order(variables)
        if order_heu == "min_degree":
            ordering = self.min_degree(variables)
        if order_heu == "min_fill":
            ordering = self.min_fill(variables)
        print(ordering)
        for i in range(len(ordering)):
            var = ordering[i]
            # print("variable to eliminate:")
            # print(var)
            out = self.multi_out(var, new_cpts)
            summed = self.sum_out(var, out)
            # updating new-cpt with REDUCED cpt from variable that was just eliminated
            new_cpts[var] = summed
            # print(summed)
            # deleting previously calculated factor, as var has been eliminated!!!!!
            if i > 0:
                new_cpts.pop(ordering[i - 1])

        # the new CPT, with only Q vars, is the one of the last var that was calculated!.
        # normalising on the sum of the rowss
        new_cpts[var]['p'] = new_cpts[var]['p'] / new_cpts[var]['p'].sum()
        return new_cpts[var]

    def multi_out(self, var, updatedCPTs):
        """multiplies all factors that refer to a variable.
            Creates a multiplied(larger) CPT for var. 

                :param  var: str. the name of variable
                :return: cpt with variables that appear together with var in their cpts (DataFrame)
                """
        # t = self.bn.get_all_cpts()
        # getting CPTs where var appears on, to be multiplied with each other
        relavent_cpts = []
        for cpt in updatedCPTs.values():
            if cpt.columns.__contains__(var) or cpt.columns.__contains__(int(var)):
                relavent_cpts.append(cpt)

        # will store unique variable/columns from list of dfs. So will contain all the vars thet the multiplied cpt needs to have
        var_cols = []
        for df in relavent_cpts:
            for col in df.columns:
                if col not in var_cols:
                    var_cols.append(col)
        var_cols.remove('p')

        temp_cpt = pd.DataFrame(list(itertools.product([False, True], repeat=len(var_cols))), columns=var_cols)

        # merging all dfs , according to cols of the right(smallest) one (p cols included) together
        it = iter(ascii_lowercase) # to not get same p col names
        for df in relavent_cpts:
            temp_cpt = temp_cpt.merge(df, on=list(df)[:-1], how='right', suffixes= ('_' + next(it), '_' + next(it)))

        # getting only p col names, to multiply them
        pcols = list(temp_cpt)
        for x in var_cols:
            pcols.remove(x)

        # multiplication product will be stored in pmulti
        pmulti = pd.Series(data=1.0, index=temp_cpt.index)
        # multiplying all pcols
        for pcol in pcols:
            try:
                pmulti = pmulti * temp_cpt[pcol]
            except:
                print("temp cpt in multi")
                print(temp_cpt)
        # creating output
        outdf = temp_cpt[var_cols]
        outdf['p'] = pmulti  # throws settingWithCopyWarning- but works ok
        if len(outdf.columns) <= 1:
            print("multi end temp cpt")
            print(temp_cpt)
            print("multi end var")
            print(var)
            print("multi end updated cpts")
            print(updatedCPTs)
        return outdf

    def sum_out(self, var, multipliedCPT):
        """eliminates var from multipliedCPT by summing out

        :param  var: str. the name of variable
        :param  multipliedCPT: cpt with multiplied factors where var appears on (DataFrame, output of multi_out function)
        :return: cpt with var eliminated (DataFrame)
        """
        # creating output,without the col of var we want to eliminate
        dfout = multipliedCPT.copy()  # if we chose to update ct inside multi out function, then we just need to get_cpt(
        # var) here
        dfout = dfout.drop(columns=var)

        # getting sum of rows with same truth values(they will correspond to the 2rows where our var to be eliminated is true and F)
        relevant_var_cols = [i for i in dfout.columns if
                             i != 'p']  # making sure that it wont group by p column, will also skip columns with p in name!!fix it
        try:
            dfout = dfout.groupby(relevant_var_cols)['p'].sum()  # summing p from cols with same truth values
        except:

            print("relevant_var_cols")
        dfout = dfout.reset_index()
        # print("reduced cpt:\n"+str(dfout))

        return dfout

    def map_mpe(self, Q: list, E: pd.Series, order_heu):
        MAP = True
        bn = self
        all_vars = bn.bn.get_all_variables()

        # for mpe there is no Q, not E becomes Q in that case
        if not Q:
            MAP = False
            for var in all_vars:
                if var not in E:
                    Q.append(var)

        # prune network by evidence
        bn.pruning(Q, E)
        # solution = pd.Series()
        if MAP:
            # calculate the map_cpt
            map_cpt = bn.marginal_distributions(Q, E, order_heu)
            # indentify the row with highes p
            max_index = map_cpt['p'].idxmax()
            # safe values into solution
            for var in Q:
                truth_value = []
                truth_value.append(map_cpt.iloc[max_index, map_cpt.columns.get_loc(var)])
                # sol = pd.Series([var, truth_value])
                # solution.append(sol)
            return pd.DataFrame(data=[truth_value], index=Q)
        else:
            mep_cpt = bn.marginal_distributions(Q, E, order_heu)
            max_index = mep_cpt['p'].idxmax()
            for var in Q:
                truth_value = []
                try:
                    truth_value.append(mep_cpt.iloc[max_index, mep_cpt.columns.get_loc(var)])
                except:
                    print(var)
                print(truth_value)
                # sol = pd.Series([var, truth_value])
                # solution.append(sol)
            return pd.DataFrame(data=[truth_value], index=Q)
        
    # def map_mpe(self, M: list, E: pd.Series):
    #     MAP = True
    #     bn = self
    #     all_vars = bn.bn.get_all_variables()

    #     # for mpe there is no Q, not E becomes Q in that case
    #     if not (M):
    #         MAP = False
    #         for var in all_vars:
    #             if not E.index._contains_(var):
    #                 M.append(var)

    #     # prune network by evidence
    #     bn.pruning(M, E)
    #     solution = []
    #     if MAP:
    #         # get non map vars
    #         nonMap_vars = all_vars
    #         for var in M:
    #             nonMap_vars.remove(var)
    #         # calculate the map_cpt
    #         map_cpt = bn.marginal_distributions(nonMap_vars, E)
    #         # indentify the row with highes p
    #         print(map_cpt['p'])
    #         max_index = map_cpt['p'].idxmax()
    #         # safe values into solution
    #         print(max_index)
    #         for var in M:
    #             solution.append([var, map_cpt.iloc[max_index, map_cpt.columns.get_loc(var)]])
    #         print(solution)
    #         return solution
    #     else:
    #         pass


""""
    def get_rel_cpts(self, cpts, var):
        parents = self.bn.structure.pred[var]
        if len(parents) == 0:
            p = cpts[var]['p']

        children_var = self.bn.get_children(var)
        node_cpt = self.bn.get_cpt(var)
        #print(children_var)
        if children_var:
            relevant_cpts = {n: cpts[n] if n in cpts.keys() else cpts[n] for n in children_var}
            #print(relevant_cpts)
            for c in children_var:
                new_cpt = self.multi_out(node_cpt, relevant_cpts[c])
                del cpts[c]
            if var in cpts:
                del cpts[var]
            new_cpt = self.sum_out(new_cpt, var)
            return new_cpt
        else:
            del cpts[var]


    def multi_out(self, node_cpt, cpt):

        col_cpt1 = set(node_cpt.columns[:-1])
        col_cpt2 = set(cpt.columns[:-1])

        alpha = col_cpt2 - col_cpt1
        #print(alpha)
        #print(node_cpt)
        #print(cpt)

        for a in alpha:
            index = len(col_cpt1) - 1
            if {True, False}.issubset(set(cpt[a])):
                cpt_copy = copy.deepcopy(node_cpt)
                node_cpt.insert(index, a, True)
                #print(node_cpt)
                new = pd.concat([node_cpt, cpt_copy])
                new = new.replace(np.nan, False, regex=True)  # fill up the rest of the rows with False
                #print(new)

        # TODO: checkout what needs to be multiplicated with what
        for index1, index2 in new.iterrows():
            print(index1)
            print(index2)
            for _, rows in cpt.iterrows():
                #print(rows)
                if index2[col_cpt1].equals(rows[col_cpt1]):
                    new.at[index1, 'p'] *= rows['p']

        print(new)

    def sum_out(self, cpt, var):
        pass

        #print("child cpts")
        #print(cpts.items())
        rows_true = cpts[var] == 'True'
        #print(rows_true)
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
"""