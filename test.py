import copy

from BNReasoner import BNReasoner
from BayesNet import BayesNet
import pandas as pd
import os
import random
import itertools
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# net = BNReasoner("testing/dog_problem.BIFXML")
keep_net = BNReasoner("testing/lecture_example.BIFXML")
variables = keep_net.bn.get_all_variables()
print(variables)
#print(net.bn.draw_structure())
#print(net.bn.BNReasoner.marginal_distributions(variables[3], variables[1]))
net = copy.deepcopy(keep_net)
print(net.d_seperation([variables[0]],[variables[1]],[variables[2]]))
net = copy.deepcopy(keep_net)
print(net.d_seperation([variables[0],variables[1]],[variables[2]],[variables[4],variables[3]]))

evidence = pd.Series({'Rain?':True, 'Sprinkler?': False})
net = copy.deepcopy(keep_net)
print("marginals solution")
print(net.marginal_distributions(['Wet Grass?', 'Slippery Road?'],evidence, "min_degree"))
net = copy.deepcopy(keep_net)
print("map solution")
print(net.map_mpe(['Wet Grass?', 'Winter?'],evidence,"min_degree"))
net = copy.deepcopy(keep_net)
print("mpe solution")
print(net.map_mpe([],evidence, "min_fill"))

outmarg = (net.marginal_distributions(['Wet Grass?', 'Slippery Road?'],evidence, "min_degree"))