# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 18:36:09 2021

@author: Dell
"""

from netCDF4 import Dataset
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression


df = pd.read_csv("C:/Users/Dell/Downloads/soa_50_testdata.csv")


x = df["Obs"].to_numpy().reshape((-1, 1))
y = df["Sim"].to_numpy()






model = LinearRegression()

model.fit(x,y)

model = LinearRegression().fit(x, y)

r_sq = model.score(x, y)

R = np.sqrt(r_sq)
c = model.intercept_

m = model.coef_

y_model = m*df["Obs"] + c


groups = df.groupby("city")

    

fig, ax = plt.subplots(figsize=(5,5),dpi = 300)

for name, group in groups:
    plt.plot(group["Obs"], group["Sim"], marker="o", linestyle="", label=name)

plt.legend(bbox_to_anchor=(1.0, 1.025))  ###(side,up-down)

plt.xlabel("Observed Concentration (\u03BCg/m\u00b3)")
plt.ylabel("Simulated Concentration (\u03BCg/m\u00b3)")

y = df["Sim"].to_list()
y.append(0)


plt.plot(y,y)

y = np.array(y)


y_50_plus = (np.tan(1.178097))*y 




plt.plot(y,y_50_plus,linestyle='dashed')

y_50_minus = (np.tan(0.3926991))*y


plt.plot(y,y_50_minus,linestyle='dashed')



ax.spines['left'].set_position('zero')

ax.spines['bottom'].set_position('zero')

plt.ylim(0,max(y))
plt.xlim(0,max(y))


plt.text(13,2, "y = {:.2f}x {:.2f}".format(m[0],c))
plt.text(13,1, "R = {:.2f}".format(R))

fig.savefig("soa_testdata.png",dpi = fig.dpi)