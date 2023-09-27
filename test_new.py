# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 14:28:51 2021

@author: Dell
"""



import numpy as np
from netCDF4 import Dataset
import csv
import pandas as pd

#Program to make all the value zero and put a value on given latitude and longitude
#NETCDF file of 13 level is given

lat_station = 22.05
lon_station = 88.15
val         = 123 


filepath = "D:/Bhai/13_level_BENZENE.nc"


nc = Dataset(filepath,"r+")

emi = nc.variables["emis_tot"][:]



lat = nc.variables["lat"][:]

lon = nc.variables["lon"][:]

emi = emi*0

a = np.where(lat == lat_station)[0][0]
b = np.where(lon == lon_station)[0][0]


for i in range(13):
    emi[i][a][b] = val
    
nc.variables['emis_tot'][:] = emi
nc.close()