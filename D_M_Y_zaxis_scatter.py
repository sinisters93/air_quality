# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 22:20:49 2021

@author: Dell
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
file = "plotadnan_new.csv"
df = pd.read_csv(file)

df["Date"] = pd.to_datetime(df['Date'], format="%d-%m-%Y")
import matplotlib.dates as mdates
#df["Date"] = df.Date.map(lambda x: x.strftime("%d-%m"))
#df1 = df.groupby(pd.Grouper(freq='D', key='Date')).mean()
#df1.reset_index(inplace = True)



fig, ax = plt.subplots(figsize=(10,6),dpi = 300)
s = plt.scatter(x =df["Average of Ratio"], y =df["Average of O3"] , c=mdates.date2num(df["Date"]))
plt.xticks(rotation=20)

plt.ylabel("Avg O$_{3}$ concentration")
plt.xlabel("Avg Ratio")

#cbar = fig.colorbar(mappable=s, ax=ax)
#cbar.set_label('Date')


cb = plt.colorbar()
loc = mdates.AutoDateLocator()
cb.ax.yaxis.set_major_locator(loc)
cb.ax.yaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))

fig.savefig("sample.png", dpi=fig.dpi)
