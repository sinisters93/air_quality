# -*- coding: utf-8 -*-
"""
This script reads data from a NetCDF file (wrfout_d01_2018-02-15_00:00:00) containing PM2.5 data,
slices the data to extract a specific time range and spatial region, calculates the mean over time,
and saves the resulting data as a CSV file (1_31dec.csv).

Created on Thu Feb 11 23:43:17 2021
@author: hp
"""

#! /usr/bin/python

from netCDF4 import Dataset
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
file_nc = "wrfout_d01_2018-02-15_00:00:00"
nc1 = Dataset(file_nc, 'r+')

##extract variable from file
data = nc1.variables["PM2_5_DRY"][:]




##slicing in n-dimensional array
data_slice = data[1848:2587,0,:,:] ### time, layer, lat, lon

data_mean = data_slice.mean(axis =0)


df = pd.DataFrame(data_mean)
df.to_csv("1_31dec.csv",index=False)
