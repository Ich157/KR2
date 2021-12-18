import copy

from BNReasoner import BNReasoner
from BayesNet import BayesNet
import pandas as pd
import os
import random
import itertools
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# net = BNReasoner("testing/dog_problem.BIFXML")
# net = BNReasoner("testing/lecture_example2.BIFXML")
# variables = net.bn.get_all_variables()
#print(variables)
#print(net.bn.draw_structure())
#net.bn.BNReasoner.marginal_distributions(variables[3], variables[1])
#print(net.d_seperation(variables[0],variables[1],variables[2]))

# evidence = pd.Series({'Winter?':True, 'Sprinkler?': False})
# out = net.marginal_distributions(['Wet Grass?', 'Slippery Road?'],evidence)
# net.map_mpe(['I', 'J'],evidence)


def create_network_params(n_variables):

    variables = []
    edges = []
    cpts = {}
    parents = {}

    #create variables with Interges as names
    for i in range(n_variables):
        variables.append(str(i))
        parents[str(i)] = []

    #create edges
    left_variables = copy.deepcopy(variables)
    for var in variables:
        left_variables.remove(var)
        n_childs = random.randint(1,3)
        while(n_childs>len(left_variables)):
            n_childs = n_childs - 1
        for i in range(n_childs):
            child = random.choice(left_variables)
            while(edges.__contains__([var,child])):
                child = random.choice(left_variables)
            edges.append([var,child])
            current_partens = parents[child]
            current_partens.append(var)
            parents[child] = current_partens

    # create cpt
    for var in variables:
        columns = parents[var].append(var)
        new_cpt = pd.DataFrame(list(itertools.product([False, True], repeat=len(parents[var])+1)), columns=columns)
        p_values = []
        for i in range(pow(2,len(parents[var]))):
            value = random.uniform(0, 1)
            p_values.append(value)
            p_values.append(1-value)
        new_cpt['p'] = p_values
        cpts[var] = new_cpt

    return variables, edges, cpts

var, edges, cpts = create_network_params(15)

#baysnet = BayesNet()
#baysnet.create_bn(var,edges,cpts)
#net = BNReasoner(baysnet)
#net.bn.draw_structure()
#all_cpts = net.bn.get_all_cpts()
#print(all_cpts)

net = BNReasoner("testing/lecture_example2.BIFXML")
Q= ['I', 'J']
E= pd.Series({'O':False, 'J':True})
# E= pd.Series({'O':True})

mapsol= net.map_mpe([],E)
# mapsol= net.map_mpe(Q,E)
# print(mapsol)