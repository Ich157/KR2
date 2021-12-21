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
n_Q = 2
n_E = 2

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

result_file = open('results.csv', 'w')
individual_file = open('individual.csv', 'w')
result_writer = csv.writer(result_file)
individual_writer = csv.writer(individual_file)
result_writer.writerow(['network_size',
                        'avg computing times map random',
                        'avg computing times map min_fill',
                        'avg computing map times min_degree',
                        'avg computing times mpe random',
                        'avg computing times mpe min_fill',
                        'avg computing times mpe min_degree'
                        ])
individual_writer.writerow(['networksize', 'algorithm and ordering','run 1', 'run 2', 'run 3', 'run 4', 'run 5'])
for network_size in range (40,41,5):
    print("networksize")
    print(network_size)
    var, edges, cpts = create_network_params(network_size)

    baysnet = BayesNet()
    baysnet.create_bn(var,edges,cpts)
    keep_net = BNReasoner(baysnet)




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

        E = pd.Series({E_var[0]:False, E_var[1]:True})

        print("Q")
        print(Q)
        print("E")
        print(E)
       # keep_net.bn.draw_structure()

        #MAP with different heu
        print("map random")
        net = copy.deepcopy(keep_net)
        t_before = datetime.datetime.now()
        net.map_mpe(Q, E, "random")
        t_after = datetime.datetime.now()
        com_time_map_random.append(t_after-t_before)

        print("map min fill")
        net = copy.deepcopy(keep_net)
        t_before = datetime.datetime.now()
        net.map_mpe(Q, E, "min_fill")
        t_after = datetime.datetime.now()
        com_time_map_min_fill.append(t_after-t_before)

        print("map min_degree")
        net = copy.deepcopy(keep_net)
        t_before = datetime.datetime.now()
        net.map_mpe(Q, E, "min_degree")
        t_after = datetime.datetime.now()
        com_time_map_min_degree.append(t_after-t_before)

        #MPE with different heu
        print("mpe random")
        net = copy.deepcopy(keep_net)
        t_before = datetime.datetime.now()
        net.map_mpe([], E, "random")
        t_after = datetime.datetime.now()
        com_time_mpe_random.append(t_after - t_before)

        print("mpe min_fill")
        net = copy.deepcopy(keep_net)
        t_before = datetime.datetime.now()
        net.map_mpe([], E, "min_fill")
        t_after = datetime.datetime.now()
        com_time_mpe_min_fill.append(t_after - t_before)

        print("mpe min_degree")
        net = copy.deepcopy(keep_net)
        t_before = datetime.datetime.now()
        net.map_mpe([], E, "min_degree")
        t_after = datetime.datetime.now()
        com_time_mpe_min_degree.append(t_after - t_before)

    result_writer.writerow([network_size,
                            (sum(com_time_map_random, datetime.timedelta(0)) / len(com_time_map_random)).seconds * 1000000 + (sum(com_time_map_random, datetime.timedelta(0)) / len(com_time_map_random)).microseconds,
                            (sum(com_time_map_min_fill, datetime.timedelta(0)) / len(com_time_map_min_fill)).seconds * 1000000 + (sum(com_time_map_min_fill, datetime.timedelta(0)) / len(com_time_map_min_fill)).microseconds,
                            (sum(com_time_map_min_degree, datetime.timedelta(0)) / len(com_time_map_min_degree)).seconds * 1000000 + (sum(com_time_map_min_degree, datetime.timedelta(0)) / len(com_time_map_min_degree)).microseconds,
                            (sum(com_time_mpe_random, datetime.timedelta(0)) / len(com_time_mpe_random)).seconds * 1000000 + (sum(com_time_mpe_random, datetime.timedelta(0)) / len(com_time_mpe_random)).microseconds,
                            (sum(com_time_mpe_min_fill, datetime.timedelta(0)) / len(com_time_mpe_min_fill)).seconds * 1000000 + (sum(com_time_mpe_min_fill, datetime.timedelta(0)) / len(com_time_mpe_min_fill)).microseconds,
                            (sum(com_time_mpe_min_degree, datetime.timedelta(0)) / len(com_time_mpe_min_degree)).seconds * 1000000 + (sum(com_time_mpe_min_degree, datetime.timedelta(0)) / len(com_time_mpe_min_degree)).microseconds,
                            ])
    individual_writer.writerow([network_size,
                               'map_random',
                               com_time_map_random[0].seconds*1000000 + com_time_map_random[0].microseconds,
                               com_time_map_random[1].seconds*1000000 + com_time_map_random[1].microseconds,
                               com_time_map_random[2].seconds*1000000 + com_time_map_random[2].microseconds,
                               com_time_map_random[3].seconds*1000000 + com_time_map_random[3].microseconds,
                               com_time_map_random[4].seconds*1000000 + com_time_map_random[4].microseconds,
                               ])
    individual_writer.writerow([network_size,
                               'map_min_fill',
                               com_time_map_min_fill[0].seconds*1000000 + com_time_map_min_fill[0].microseconds,
                               com_time_map_min_fill[1].seconds*1000000 + com_time_map_min_fill[1].microseconds,
                               com_time_map_min_fill[2].seconds*1000000 + com_time_map_min_fill[2].microseconds,
                               com_time_map_min_fill[3].seconds*1000000 + com_time_map_min_fill[3].microseconds,
                               com_time_map_min_fill[4].seconds*1000000 + com_time_map_min_fill[4].microseconds,
                               ])
    individual_writer.writerow([network_size,
                               'map_min_degree',
                               com_time_map_min_degree[0].seconds*1000000 + com_time_map_min_degree[0].microseconds,
                               com_time_map_min_degree[1].seconds*1000000 + com_time_map_min_degree[1].microseconds,
                               com_time_map_min_degree[2].seconds*1000000 + com_time_map_min_degree[2].microseconds,
                               com_time_map_min_degree[3].seconds*1000000 + com_time_map_min_degree[3].microseconds,
                               com_time_map_min_degree[4].seconds*1000000 + com_time_map_min_degree[4].microseconds,
                               ])

    individual_writer.writerow([network_size,
                               'mpe_random',
                               com_time_mpe_random[0].seconds*1000000 + com_time_mpe_min_degree[0].microseconds,
                               com_time_mpe_random[1].seconds*1000000 + com_time_mpe_min_degree[1].microseconds,
                               com_time_mpe_random[2].seconds*1000000 + com_time_mpe_min_degree[2].microseconds,
                               com_time_mpe_random[3].seconds*1000000 + com_time_mpe_min_degree[3].microseconds,
                               com_time_mpe_random[4].seconds*1000000 + com_time_mpe_min_degree[4].microseconds,
                               ])
    individual_writer.writerow([network_size,
                               'mpe_min_fill',
                               com_time_mpe_min_fill[0].seconds*1000000 + com_time_mpe_min_fill[0].microseconds,
                               com_time_mpe_min_fill[1].seconds*1000000 + com_time_mpe_min_fill[0].microseconds,
                               com_time_mpe_min_fill[2].seconds*1000000 + com_time_mpe_min_fill[0].microseconds,
                               com_time_mpe_min_fill[3].seconds*1000000 + com_time_mpe_min_fill[0].microseconds,
                               com_time_mpe_min_fill[4].seconds*1000000 + com_time_mpe_min_fill[0].microseconds,
                               ])
    individual_writer.writerow([network_size,
                               'mpe_min_degree',
                               com_time_mpe_min_degree[0].seconds*1000000 + com_time_mpe_min_degree[0].microseconds,
                               com_time_mpe_min_degree[1].seconds*1000000 + com_time_mpe_min_degree[1].microseconds,
                               com_time_mpe_min_degree[2].seconds*1000000 + com_time_mpe_min_degree[2].microseconds,
                               com_time_mpe_min_degree[3].seconds*1000000 + com_time_mpe_min_degree[3].microseconds,
                               com_time_mpe_min_degree[4].seconds*1000000 + com_time_mpe_min_degree[4].microseconds,
                               ])

individual_writer.writerow("")
result_writer.writerow("")
print("experiment done")
