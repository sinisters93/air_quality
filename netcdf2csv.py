# -*- coding: utf-8 -*-
"""
This script extracts data from a NetCDF file containing PM2.5 emissions data and
saves it in a CSV file. It focuses on a specific latitude and longitude range,
calculates emissions, and creates a DataFrame for the selected data.

Created on Thu Mar 4 12:59:16 2021
@author: hp
"""

import numpy as np
from netCDF4 import Dataset
import csv
import pandas as pd

import matplotlib.pyplot as plt
filepath_PM25 = 'C:/Users/hp/Desktop/sectoremissions/v50_BC_2015_IND.0.1x0.1.nc'
nc_co = Dataset(filepath_PM25, 'r+')

lat =  nc_co.variables["lat"][:]
emi = nc_co.variables["emi_bc"][:]
emi = emi*24*3600*12*12*10**6

lat_new = lat[1165:1181]
lat_new = lat_new.tolist()

lat_new = [round(num, 2) for num in lat_new]

lon =  nc_co.variables['lon'][:]
lon_new = lon[769:791]   
lon_new = lon_new.tolist()

lon_new = [round(num, 2) for num in lon_new]

Lat = []
Lon = []
Emi = []
for i in range(1165,1181,1):
    for j in range(769,791,1):
        Lat.append(lat[i])
        Lon.append(lon[j])
        Emi.append(emi[i][j])
        
df1 = pd.DataFrame()
df1["lat"] = Lat
df1["lon"] = Lon
df1["BC"] = Emi

df1.to_csv("BC.csv",index = False)
