from BNReasoner import BNReasoner
from BayesNet import BayesNet
import pandas as pd
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# net = BNReasoner("testing/dog_problem.BIFXML")
net = BNReasoner("testing/lecture_example.BIFXML")
variables = net.bn.get_all_variables()
#print(variables)
#print(net.bn.draw_structure())
#net.bn.BNReasoner.marginal_distributions(variables[3], variables[1])
#print(net.d_seperation(variables[0],variables[1],variables[2]))
evidence = pd.Series({variables[0]:False})
net.marginal_distributions(variables[4],evidence)
