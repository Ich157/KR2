import copy

from BNReasoner import BNReasoner
from BayesNet import BayesNet
import pandas as pd
import os
import random
import itertools
import csv
import datetime
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

n_executions = 5
n_Q = 3
n_E = 3
network_size = 10

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
        columns = parents[var]
        columns.append(var)
        new_cpt = pd.DataFrame(list(itertools.product([False, True], repeat=len(columns))), columns=columns)
        p_values = []
        for i in range(pow(2,len(columns)-1)):
            value = random.uniform(0, 1)
            p_values.append(value)
            p_values.append(1-value)
        new_cpt['p'] = p_values
        cpts[var] = new_cpt

    return variables, edges, cpts

var, edges, cpts = create_network_params(network_size)

baysnet = BayesNet()
baysnet.create_bn(var,edges,cpts)
net = BNReasoner(baysnet)

result_file = open('results.csv', 'w')
result_writer = csv.writer(result_file)
result_writer.writerow(['network_size',
                        'computing times map random','avg computing times map random',
                        'computing times map min_fill','avg computing times map min_fill',
                        'computing times map min_degree','avg computing map times min_degree',
                        'computing times mpe random', 'avg computing times mpe random',
                        'computing times mpe min_fill', 'avg computing times mpe min_fill',
                        'computing times mpr min_degree', 'avg computing times mpe min_degree'
                        ])

com_time_map_random = []
com_time_map_min_fill = []
com_time_map_min_degree = []
com_time_mpe_random = []
com_time_mpe_min_fill = []
com_time_mpe_min_degree = []

for i in range(n_executions):
    Q = []
    E_var = []
    for n in range(n_E):
        e = random.choice(var)
        while(E_var.__contains__(e)):
            e = random.choice(var)
        E_var.append(e)
    for n in range(n_Q):
        q = random.choice(var)
        while(Q.__contains__(q) or E_var.__contains__(q)):
            q = random.choice(var)
        Q.append(q)

    E = pd.Series({E_var[0]:False, E_var[1]:True, E_var[2]:False})

    #MAP with different heu
    print("map random")
    t_before = datetime.datetime.now()
    net.map_mpe(Q, E, "random")
    t_after = datetime.datetime.now()
    com_time_map_random.append(t_after-t_before)
    print("map min fill")
    t_before = datetime.datetime.now()
    net.map_mpe(Q, E, "min_fill")
    t_after = datetime.datetime.now()
    com_time_map_min_fill.append(t_after-t_before)
    print("map min_degree")
    t_before = datetime.datetime.now()
    net.map_mpe(Q, E, "min_degree")
    t_after = datetime.datetime.now()
    com_time_map_min_degree.append(t_after-t_before)

    #MPE with different heu
    print("mpe random")
    t_before = datetime.datetime.now()
    net.map_mpe([], E, "random")
    t_after = datetime.datetime.now()
    com_time_mpe_random.append(t_after - t_before)
    print("mpe min_fill")
    t_before = datetime.datetime.now()
    net.map_mpe([], E, "min_fill")
    t_after = datetime.datetime.now()
    com_time_mpe_min_fill.append(t_after - t_before)
    print("mpe min_degree")
    t_before = datetime.datetime.now()
    net.map_mpe([], E, "min_degree")
    t_after = datetime.datetime.now()
    com_time_mpe_min_degree.append(t_after - t_before)

result_writer.writerow([network_size,
                        com_time_map_random,
                        (sum(com_time_map_random, datetime.timedelta(0)) / len(com_time_map_random)).seconds * 1000000 + (sum(com_time_map_random, datetime.timedelta(0)) / len(com_time_map_random)).microseconds,
                        com_time_map_min_fill,
                        (sum(com_time_map_min_fill, datetime.timedelta(0)) / len(com_time_map_min_fill)).seconds * 1000000 + (sum(com_time_map_min_fill, datetime.timedelta(0)) / len(com_time_map_min_fill)).microseconds,
                        com_time_map_min_degree,
                        (sum(com_time_map_min_degree, datetime.timedelta(0)) / len(com_time_map_min_degree)).seconds * 1000000 + (sum(com_time_map_min_degree, datetime.timedelta(0)) / len(com_time_map_min_degree)).microseconds,
                        com_time_mpe_random,
                        (sum(com_time_mpe_random, datetime.timedelta(0)) / len(com_time_mpe_random)).seconds * 1000000 + (sum(com_time_mpe_random, datetime.timedelta(0)) / len(com_time_mpe_random)).microseconds,
                        com_time_mpe_min_fill,
                        (sum(com_time_mpe_min_fill, datetime.timedelta(0)) / len(com_time_mpe_min_fill)).seconds * 1000000 + (sum(com_time_mpe_min_fill, datetime.timedelta(0)) / len(com_time_mpe_min_fill)).microseconds,
                        com_time_mpe_min_degree,
                        (sum(com_time_mpe_min_degree, datetime.timedelta(0)) / len(com_time_mpe_min_degree)).seconds * 1000000 + (sum(com_time_mpe_min_degree, datetime.timedelta(0)) / len(com_time_mpe_min_degree)).microseconds,
                        ])
