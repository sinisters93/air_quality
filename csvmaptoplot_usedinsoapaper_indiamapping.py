# -*- coding: utf-8 -*-
"""
This Python script reads a shapefile, processes its data, and generates a contour plot of annual VOC (Volatile Organic Compounds) emission rates.
It also superimposes the geographical coordinates of emission points and labels Agra District.
Created on Thu Feb 11 22:45:35 2021
@author: hp
"""

from netCDF4 import Dataset
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import shapefile as shp
import seaborn as sns

shp_path = "C:/Users/user/Desktop/agra/Admin2.shp"
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

def plot_map(sf, x_lim = None, y_lim = None, figsize = (11,9)):
    '''
    Plot map with lim coordinates
    '''
    plt.figure(figsize = figsize)
    id=0
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k')
        
        if (x_lim == None) & (y_lim == None):
            x0 = np.mean(x)
            y0 = np.mean(y)
            plt.text(x0, y0, id, fontsize=10)
        id = id+1
    
    if (x_lim != None) & (y_lim != None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)


com_id_agra  =df1

st_nm = df1["ST_NM"]
lat1 = []

lon1 = []

for i in st_nm:
    
    df_agra =  df1[df1.ST_NM == i]
    lst = df_agra["coords"].to_list()
    for j in range(len(lst[0])):
        lon1.append(lst[0][j][0])
        lat1.append(lst[0][j][1])

#lon1 = [x for x in lon1] ##+ right shift     ##left right shift
#lat1 = [x+0 for x in lat1] ##+ upper shift # up down shift
#plt.title(i)    
#x_lon_agra = np.zeros((len(shape_ex_agra.points),1))
#y_lat_agra = np.zeros((len(shape_ex_agra.points),1))
#plt.plot(x_lon_agra,y_lat_agra,color = "k")
#plot_map(sf)
#comuna_agra = 'Agra'
#com_id_agra  =df1
#df_agra =  df1[df1.NAME == "Agra"]
#shape_ex_agra = sf.shape(com_id_agra)
#x_lon_agra = np.zeros((len(shape_ex_agra.points),1))
#y_lat_agra = np.zeros((len(shape_ex_agra.points),1))
#for ip in range(len(shape_ex_agra.points)):

file = "annual_soa_fortable_.csv"
lat = np.linspace(5,max(lat1),75) # 35.7
lon = np.linspace(61,max(lon1),75) #95.3
df = pd.read_csv(file)
#data = df[:,1:]
data = df.values
X,Y = np.meshgrid(lon,lat)
sns.set(context="notebook", style="darkgrid",
        rc={"axes.axisbelow": False})
fig, ax = plt.subplots(figsize=(5,8),dpi = 300)

#contour = plt.contour(X, Y, data,colors="white")
#plt.clabel(contour, colors = 'black', fmt = '%2.f', fontsize=8)
#plt.grid(True)
#plt.grid(True)

co_plot = ax.contourf(X,Y,data,cmap = "Blues",levels=np.linspace(np.amin(data),np.amax(data),11))
#ax.clabel(co_plot, inline=True)
plt.xlabel("Longitude(\N{DEGREE SIGN}E)")
plt.ylabel("Latitude(\N{DEGREE SIGN}N)")
#plt.title("Contour plot of CO levels")
    
plt.scatter(lon1,lat1,marker = '.',s = 0.1,color = "k")
plt.grid(False)
#plt.plot(x_lon_agra,y_lat_agra,color = "k") 
#plt.text(x0_agra+0.6, y0_agra-0.05, "Agra District", fontsize=22)
#plt.text(x0_agra-0.475, y0_agra+0.1, "Agra", fontsize=22)
#plt.text(78,27,".",fontsize = 80) ##Point at lat lon

cbar = plt.colorbar(co_plot,extend='both',orientation = 'horizontal',pad = 0.1,aspect = 50)
cbar.set_label('Annual VOC Emission Rate(ton/km\u00b2) [2018] ')
#plot_shape(com_id,comuna,ax)
fig.savefig("soapaper_annual_voc.png")
