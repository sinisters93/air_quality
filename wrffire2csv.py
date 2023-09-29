# -*- coding: utf-8 -*-
"""
This Python script extracts data from netCDF files containing ozone (o3) concentrations
for specific date and time ranges in multiple runs of a simulation. The extracted data
is then processed and saved as a CSV file.

Created on Tue Apr 13 12:31:09 2021
@author: Dell
"""
#! /usr/bin/python
import numpy as np
import pandas as pd
from netCDF4 import Dataset

def convert(list):
    return tuple(i for i in list)

var = "o3"
file1 = ['12','01','03','05','07','08','10']    
#file2 = ['01','03','05','07','08','10']
file2 = ['04','06','09',"11"]
folder2 = ["run4","run6","run9","run11"]
#Data = []
folder1 = ["run","run1","run3","run5","run7","run8","run10"]
#file = []
Data = []
year = "2017"
f_n_1 = 0
for i in file1:
    for d in range(1,32):
        d = str(d)
        if len(d) == 1:
            d = "0"+d
        else:
            d = d
        for h in range(24):
            h = str(h)
            if len(h)==1:
                h = "0"+h
            else:
                h = h
            file_nc1 = folder1[f_n_1]+"/wrffirechemi_d01_"+year+"-"+i+"-"+d+"_"+h+":00:00"
            print(file_nc1)
            o3_nc1  = Dataset(file_nc1, 'r+')
            data_o3_nc1 = o3_nc1.variables[var][:]
            Data.append(data_o3_nc1)
            year = "2018"
    f_n_1 = f_n_1 +1

year = "2018"
f_n_2 = 0
for i in file2:
    for d in range(1,31):
        d = str(d)
        if len(d) == 1:
            d = "0"+d
        else:
            d = d
        for h in range(24):
            h = str(h)
            if len(h)==1:
                h = "0"+h
            else:
                h = h
            file_nc2 = folder2[f_n_2]+"/wrffirechemi_d01_"+year+"-"+i+"-"+d+"_"+h+":00:00"
            print(file_nc2)
            o3_nc2  = Dataset(file_nc2, 'r+')
            data_o3_nc2 = o3_nc2.variables[var][:]
            Data.append(data_o3_nc2)
    f_n_2 = f_n_2 +1

for d in range(1,29):
    d = str(d)
    if len(d) == 1:
        d = "0"+d
    else:
        d = d
    for h in range(24):
        h = str(h)
        if len(h)==1:
            h = "0"+h
        else:
            h = h
        file_nc3 = "run2/wrffirechemi_d01_"+year+"-02-"+d+"_"+h+":00:00"
        print(file_nc3)
        o3_nc1  = Dataset(file_nc1, 'r+')
        data_o3_nc1 = o3_nc1.variables[var][:]
        Data.append(data_o3_nc1)

array_tuple = convert(Data)

arrays = np.vstack(array_tuple)
final_data_arr = arrays.sum(axis = 0)
df = pd.DataFrame(final_data_arr)
df.to_csv("wrffirechemi2"+var+".csv",index = False)
