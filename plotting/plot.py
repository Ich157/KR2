# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 17:38:31 2021

@author: lefko
"""
import pandas as pd
import matplotlib.pyplot as plt
import os
import time

dir1 = 'D:\\arxeia\\AI_VU\\Knowledge_Representation\\2ndAss_GLM\\teamsRepo\\'
os.chdir(dir1)
results = 'results_avges.csv'
res = pd.read_csv(results, index_col=(0), header=1)
#turning to sec
res/1000000

#plotting MAP avges
ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tick_params(top=False ,right=False)
plt.ylabel('runtime (sec)'); plt.xlabel('network size (nodes)')
plt.title("Average performance: MAP" , fontsize=14)
plt.xticks(ticks = [10,15,20,25,30])
# ax.set_ylim(ymin, ymax)
x = res.index
y1=res['map random']
y2=res['map min_fill']
y3=res['map min_degree']
ax.plot(x,y1, label= 'map random', linewidth=2)
ax.plot(x,y2, label= 'map min_fill', linewidth=4)
ax.plot(x,y3, label= 'map min_degree', linewidth=2)
ax.legend()
# plt.fill_between(x,y2,y3, color = colorgcamp, alpha =0.25)
# plt.fill_between(x,y5,y6, color = colorisosb, alpha=0.25)
plt.savefig(dir1+'map_avg_plot' +time.strftime("%Y%m%d_%H%M"))
plt.show()

#plotting MAP avges
ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tick_params(top=False ,right=False)
plt.ylabel('runtime (sec)'); plt.xlabel('network size (nodes)')
plt.title("Average performance: MPE" , fontsize=14)
plt.xticks(ticks = [10,15,20,25,30])
# ax.set_ylim(ymin, ymax)
x = res.index
y1=res['mpe random']
y2=res['mpe min_fill']
y3=res['mpe min_degree']
ax.plot(x,y1, label= 'mpe random', linewidth=2)
ax.plot(x,y2, label= 'mpe min_fill', linewidth=4)
ax.plot(x,y3, label= 'mpe min_degree', linewidth=2)
ax.legend()
# plt.fill_between(x,y2,y3, color = colorgcamp, alpha =0.25)
# plt.fill_between(x,y5,y6, color = colorisosb, alpha=0.25)
plt.savefig(dir1+'mpe_avg' +time.strftime("%Y%m%d_%H%M"))
plt.show()

