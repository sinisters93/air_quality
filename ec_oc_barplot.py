# -*- coding: utf-8 -*-
"""
Created on Wed May  5 19:38:05 2021

@author: Dell
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
filepath = "C:/Users/Dell/Downloads/sim_oc_month.csv"

filepath1 = "C:/Users/Dell/Downloads/sim_ec_month.csv"








df = pd.read_csv(filepath)

df1 = pd.read_csv(filepath1)

df1 = df1.transpose()

a1 = df1.iloc[0]

df1 = df1.rename(columns = a1, inplace = False)
df1 = df1.iloc[1: , :]




df = df.transpose()

a = df.iloc[0]

df = df.rename(columns = a, inplace = False)

df = df.iloc[1: , :]

labels = a.to_list()
a1 = a1.to_list()
a1.extend(labels)



mon = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']


df["Month"] = mon
df1["Month"] = mon

df = df.set_index("Month")

df1 = df1.set_index("Month")


fig, ax = plt.subplots(2,1,figsize=(12,12),dpi = 300)
l1 = df1.plot.bar(rot=0,ylabel = "EC (\u03BCg/m\u00b3)",legend = False, color=['Red', 'Black'],ax = ax[0],fontsize = 16)
l2 = df.plot.bar(rot=0,ylabel= "OC (\u03BCg/m\u00b3)",color=['Blue', 'Green','Orange'],legend = False,ax = ax[1],fontsize = 16)

ax[0].set_ylabel("EC (\u03BCg/m\u00b3)",fontsize = 16)

ax[1].set_ylabel("OC (\u03BCg/m\u00b3)",fontsize = 16)

ax[1].set_xlabel("Month",fontsize = 16)
ax[0].set_xlabel("Month",fontsize = 16)

fig.legend([l1, l2], labels=a1,ncol = 3,bbox_to_anchor=(0.825,0.975),fontsize = 16)

fig.savefig("barplot_ec_co.png",dpi = fig.dpi)

