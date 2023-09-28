# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 22:45:35 2021

This script reads geographic and pollution data, and generates a contour plot of CO levels
over a specific region, highlighting the Agra District in Uttar Pradesh, India. It also
includes additional geographical annotations and a colorbar for the pollution levels.

@author: hp
"""

from netCDF4 import Dataset
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import shapefile as shp
import seaborn as sns




shp_path = "C:/Users/hp/Desktop/agra/uttar_pradesh_administrative.shp"
sf = shp.Reader(shp_path)
def read_shapefile(sf):
    """
    Read a shapefile into a Pandas dataframe with a 'coords' 
    column holding the geometry information. This uses the pyshp
    package
    """
    fields = [x[0] for x in sf.fields][1:]
    records = sf.records()
    shps = [s.points for s in sf.shapes()]
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)
    return df

df1 = read_shapefile(sf)
def plot_shape(id,ax,s=None):
    """ PLOTS A SINGLE SHAPE """
    plt.figure()
    ax = plt.axes()
    ax.set_aspect('equal')
    shape_ex = sf.shape(id)
    x_lon = np.zeros((len(shape_ex.points),1))
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    plt.plot(x_lon,y_lat) 
    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    plt.text(x0, y0, s, fontsize=10)
    # use bbox (bounding box) to set plot limits
    plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])
    return x0, y0

comuna_agra = 'Agra'
com_id_agra = df1[df1.NAME == comuna_agra].index[0]
#df_agra =  df1[df1.NAME == "Agra"]

shape_ex_agra = sf.shape(com_id_agra)
x_lon_agra = np.zeros((len(shape_ex_agra.points),1))
y_lat_agra = np.zeros((len(shape_ex_agra.points),1))
for ip in range(len(shape_ex_agra.points)):
    x_lon_agra[ip] = shape_ex_agra.points[ip][0]
    y_lat_agra[ip] = shape_ex_agra.points[ip][1]

x0_agra = np.mean(x_lon_agra)
y0_agra = np.mean(y_lat_agra)















file = "1_31dec.csv"
lat = np.linspace(25.7,29.2,50)
lon = np.linspace(75.8,79.7,50)
df = pd.read_csv(file)
#data = df[:,1:]
data = df.values


X,Y = np.meshgrid(lon,lat)












sns.set(context="notebook", style="darkgrid",
        rc={"axes.axisbelow": False})
fig, ax = plt.subplots(figsize=(10,10),dpi = 300)


contour = plt.contour(X, Y, data,colors="white")

plt.clabel(contour, colors = 'black', fmt = '%2.f', fontsize=8)
plt.grid(True)
#plt.grid(True)

co_plot = ax.contourf(X,Y,data,cmap = "Reds",levels=np.linspace(0,20,11))
#ax.clabel(co_plot, inline=True)
plt.xlabel("Longitude(\N{DEGREE SIGN}E)")
plt.ylabel("Latitude(\N{DEGREE SIGN}N)")
#plt.title("Contour plot of CO levels")

plt.plot(x_lon_agra,y_lat_agra,color = "k") 
plt.text(x0_agra+0.6, y0_agra-0.05, "Agra District", fontsize=22)
plt.text(x0_agra-0.475, y0_agra+0.1, "Agra", fontsize=22)
plt.text(78,27,".",fontsize = 80) ##Point at lat lon

cbar = plt.colorbar(co_plot,extend='both',orientation = 'horizontal',pad = 0.1,aspect = 50)
cbar.set_label('Mean Monthly PM$_{2.5}$ Concentration(\u03BCg/m\u00b3) [Dec 2018] ')
#plot_shape(com_id,comuna,ax)
fig.savefig("1_31dec_bwr.png")
