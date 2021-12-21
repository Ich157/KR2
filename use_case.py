# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 14:38:17 2021

@author: lefko
"""
import copy

from BNReasoner import BNReasoner
from BayesNet import BayesNet
import pandas as pd
import os
import random
import itertools
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

# keep net
keep_net = BNReasoner("testing/foodWaste.BIFXML")
variables = keep_net.bn.get_all_variables()
print(variables)
# keep_net.bn.draw_structure()  -----------------i cant draw structure
allCpts = keep_net.bn.get_all_cpts()

'''RQ: Is the variable Developed Country, given Good Looking Preference, 
indepen-dent from Food Waste? (d-separation)'''

net = copy.deepcopy(keep_net)
print(net.d_seperation(['Developed Country'],['Good Looking Preference'],['Food Waste'])) #False


'''RQ: What is the probability of High IncomeHousehold  and  
Developed  Country  equal  to  True,
 given  Food  Waste  equal  to true? (posterior probability)'''
net = copy.deepcopy(keep_net) 
evidence = pd.Series({'Food Waste':True})
print(net.marginal_distributions(['High Income Household', 'Developed Country'],evidence, "min_fill")) 



'''RQ: prior prob......'''
print(net.marginal_distributions(['High Income Household', 'Developed Country'],[], "min_fill")) #
 
 
 
'''RQ: Food waste is observed to be True, 
what are themost likely values of all the other model variables (MPE)---changed it!'''
evidence = pd.Series({'Developed Country': True,  'High Temperature': True, 'High Income Household': True}) #when only foodwaste= T then no truth values are returned
net = copy.deepcopy(keep_net)
print(net.map_mpe([],evidence, "min_degree"))

'''RQ: Given that Food Wasteis observed to be True, which is the 
most likely instantiation of the variables HighIncome Household 
together with Retail Waste? (MAP)'''
evidence = pd.Series({'Bad Storage':True, 'Developed Country': False}) #
net = copy.deepcopy(keep_net)
print(net.map_mpe(['Home Waste'],evidence, "random"))




 