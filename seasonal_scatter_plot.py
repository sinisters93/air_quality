# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 12:04:41 2021

@author: Dell

Description:
This Python script reads data from a CSV file named "seasonal.csv" containing seasonal data, 
and it generates a scatter plot to visualize the relationship between two variables - 'WSIS' and 'PM2.5'.
The data is grouped by the 'Date' column, and each group is represented with a distinct color 
according to the season categories ('Winter', 'Pre Monsoon', 'Monsoon', 'Post Monsoon').
The resulting scatter plot is saved as "seasonal_scatter.png".

Dependencies:
- pandas
- numpy
- matplotlib

"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
file = "seasonal.csv"
df = pd.read_csv(file)

#df["Date"] = pd.to_datetime(df['Date'], format="%d-%m-%Y")

colors = {'Winter':'red', 'Pre Monsoon':'blue', 'Monsoon':'green', 'Post Monsoon':'black'}

fig, ax = plt.subplots(figsize=(10,6),dpi = 300)
grouped = df.groupby('Date')
for key, group in grouped:
    group.plot(ax=ax, kind='scatter', x='WSIS', y='PM2.5', label=key, color=colors[key])
plt.legend(title="Season",fontsize='small', fancybox=True)
fig.savefig("seasonal_scatter.png", dpi=fig.dpi)
