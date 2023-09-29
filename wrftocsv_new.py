# -*- coding: utf-8 -*-
"""
This Python script is designed to process meteorological data from a NetCDF file.
It reads the file "wrfout_d01_2018-09-15_00:00:00" and extracts the variable "PM2_5_DRY."
The script performs slicing on the n-dimensional array, calculating the mean along the time axis.
The resulting data is then converted into a DataFrame and saved as "data7_13oct.csv."

Created on Thu Feb 11 23:43:17 2021
@author: hp
"""
#! /usr/bin/python

from netCDF4 import Dataset
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
file_nc = "wrfout_d01_2018-09-15_00:00:00"
nc1 = Dataset(file_nc, 'r+')

##extract variable from file
data = nc1.variables["PM2_5_DRY"][:]

##slicing in n-dimensional array
data_slice = data[528:696,0,:,:] ### time, layer, lat, lon

data_mean = data_slice.mean(axis =0)

df = pd.DataFrame(data_mean)
df.to_csv("data7_13oct.csv",index=False)
