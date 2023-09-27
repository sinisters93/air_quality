# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 13:05:50 2020

@author: Dell
"""

import numpy as np
from netCDF4 import Dataset
import csv
import pandas as pd



def netcdf2csv(filepath):
    nc1 = Dataset(filepath, 'r+')
    lat = nc1.variables['lat'][:]
    lon = nc1.variables['lon'][:]

    var_dict = nc1.variables
    var_list = list(var_dict.keys())
    variable = var_list[-1]
    
    iso = nc1.variables[variable][:]

    lat_len = len(lat)
    lon_len = len(lon)


    out_arr = np.zeros([lat_len,lon_len])
    a = np.mean(iso, axis = 0, out = out_arr) 

    ISO =[]
    LAT = []
    LON = []
    for i in range(len(lon)):
        for j in range(len(lat)):
            lon_i = lon[i]
            lat_j = lat[j]
            LAT.append(lat_j)
            LON.append(lon_i)
            c = a[j][i]
            ISO.append(c)

    df = pd.DataFrame()
    df['Lat'] = LAT
    df['Lon'] = LON
    df[variable] = ISO
    df.to_csv(filepath+'.csv',index=False)

file = ['']

for i in range(len(file)):
    f = file[i]
    netcdf2csv(f)