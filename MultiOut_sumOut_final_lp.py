# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 13:00:20 2021

@author: lefko
"""
import itertools
import pandas as pd
import numpy as np


def multi_out(self, var, allcpts):
    """multiplies all factors that refer to a variable.
        Creates a multiplied(larger) CPT for var. Should it also update it?
    
            :param  var: str. the name of variable
            :return: cpt with variables that appear together with var in their cpts (DataFrame)
            """

    # getting CPTs where var appears on, to be multiplied with each other
    relavent_cpts = []
    for cpt in allcpts.values():
        if cpt.columns.__contains__(var):
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
    for df in relavent_cpts:
        temp_cpt = temp_cpt.merge(df, on=list(df)[:-1], how='right')

    # getting only p col names, to multiply them
    pcols = list(temp_cpt)
    for x in var_cols:
        pcols.remove(x)

    # multiplication product will be stored in pmulti
    pmulti = pd.Series(data=1.0, index=temp_cpt.index)
    # multiplying all pcols
    for pcol in pcols:
        pmulti = pmulti * temp_cpt[pcol]
    # creating output
    outdf = temp_cpt[var_cols]
    outdf['p'] = pmulti  # throws settingWithCopyWarning- but works ok

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
    dfout = dfout.groupby(relevant_var_cols)['p'].sum()  # summing p from cols with same truth values
    dfout = dfout.reset_index()
    # print("reduced cpt:\n"+str(dfout))

    return dfout
