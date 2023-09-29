# -*- coding: utf-8 -*-
"""
Description:
This Python script is designed to manipulate a NETCDF file containing 13 levels of data. The primary purpose is to set all values to zero and assign a specific value to a given latitude and longitude location within the file. 

Variables:
- lat_station: The target latitude for assigning the value.
- lon_station: The target longitude for assigning the value.
- val: The value to be assigned to the specified latitude and longitude coordinates.
- filepath: The path to the NETCDF file containing the data.
- nc: The NETCDF dataset object used to access and modify the data.
- emi: An array holding the 'emis_tot' variable data from the NETCDF file.
- lat: An array holding latitude values from the NETCDF file.
- lon: An array holding longitude values from the NETCDF file.

Procedure:
1. Load the NETCDF dataset from the specified file.
2. Initialize the 'emi' variable with the 'emis_tot' data from the NETCDF file.
3. Set all values in the 'emi' array to zero.
4. Find the indices in the 'lat' and 'lon' arrays corresponding to the target latitude and longitude.
5. Assign the specified 'val' to the 'emi' array at the identified latitude and longitude.
6. Update the 'emis_tot' variable in the NETCDF dataset with the modified 'emi' array.
7. Close the NETCDF dataset.

Note: Ensure that the specified file path ('filepath') leads to a valid NETCDF file containing the 'emis_tot' variable and that the target latitude and longitude coordinates ('lat_station' and 'lon_station') exist within the provided data.
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

filepath = "D:/sahir/13_level_BENZENE.nc"
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
