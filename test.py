from BNReasoner import BNReasoner
from BayesNet import BayesNet
import pandas as pd
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# net = BNReasoner("testing/dog_problem.BIFXML")
net = BNReasoner("testing/lecture_example2.BIFXML")
variables = net.bn.get_all_variables()
print(variables)
#print(net.bn.draw_structure())
#net.bn.BNReasoner.marginal_distributions(variables[3], variables[1])
#print(net.d_seperation(variables[0],variables[1],variables[2]))
evidence = pd.Series({'O':True})
#net.marginal_distributions(['Wet Grass?', 'Slippery Road?'],evidence)
net.map_mpe(['I', 'J'],evidence)