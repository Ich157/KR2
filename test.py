from BNReasoner import BNReasoner
from BayesNet import BayesNet
import pandas as pd

# net = BNReasoner("testing/dog_problem.BIFXML")
net = BNReasoner("testing/lecture_example.BIFXML")
variables = net.bn.get_all_variables()
#print(net.d_seperation(variables[0],variables[1],variables[2]))
# evidence = pd.Series({variables[4]:False})
# net.marginal_distributions(variables[1],evidence)
