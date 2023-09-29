# -*- coding: utf-8 -*-
"""
WRF Data Processing Script

This script extracts and processes data from WRF (Weather Research and Forecasting) model output files.
It calculates the average values of specified variables for different time periods and stores the results
in a NumPy array. The processed data can be used for further analysis or visualization.

Created on Sun Apr  4 11:03:39 2021
Author: Dell
"""
#! /usr/bin/python

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from netCDF4 import Dataset

def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))
def Average(lst):
    return sum(lst) / len(lst)


def wrf2var_csv(var_list):
    final_data = []
    for n in var_list:
        file1 = ['11','12']
        file2 = ['01','03','05','07','08','10']
        file3 = ['04','06','09']
        Data = []
        for i in file1:
            a = 384
            file_nc1 = "wrfout_d01_2017-"+i+"-15_00:00:00"
            o3_nc1  = Dataset(file_nc1, 'r+')
            #extract variable from file
            data_o3_nc1 = o3_nc1.variables[n][:]
            data_slice1 = data_o3_nc1[a:,0,58,32] #time,level,lat,lon 
            data_slice1 = data_slice1.tolist()
            data_slice1_avg = Average(data_slice1) 
            Data.append(data_slice1_avg)
            a + 24
        '''
        for j in file2:
            a = 408
            file_nc2 = "wrfout_d01_2018-"+j+"-15_00:00:00"
            o3_nc2  = Dataset(file_nc2, 'r+')
            #extract variable from file
            data_o3_nc2 = o3_nc2.variables[n][:]
            data_slice2 = data_o3_nc2[a:,0,58,32]
            data_slice2 = data_slice2.tolist()
            data_slice2_avg = Average(data_slice2) 
            Data.append(data_slice2_avg)

        for k in file3:
            a = 384
            file_nc3 = "wrfout_d01_2018-"+k+"-15_00:00:00"
            o3_nc3  = Dataset(file_nc3, 'r+')
            #extract variable from file
            data_o3_nc3 = o3_nc3.variables[n][:]
            data_slice3 = data_o3_nc3[a:,0,58,32]
            data_slice3 = data_slice3.tolist()
            data_slice3_avg = Average(data_slice3) 
            Data.append(data_slice3_avg)

        '''

        file_nc4 = "wrfout_d01_2018-02-15_00:00:00"
        o3_nc4  = Dataset(file_nc4, 'r+')
        ##extract variable from file
        data_o3_nc4 = o3_nc4.variables[n][:]
        data_slice4 = data_o3_nc4[360:,0,58,32]
        data_slice4 = data_slice4.tolist()
        data_slice3_avg = Average(data_slice3) 
        Data.append(data_slice3_avg)
        
        final_data.extend(Data)
        
    final_data_arr = np.array(final_data)
    final_data_arr = final_data_arr.T
    print(final_data_arr)
    print(type(final_data_arr))
    print(final_data_arr.shape)
    #final_data_arr = final_data_arr().reshape(12,len(var_list),order = "F")	
    #df = pd.DataFrame(final_data_arr, columns = var_list)
    #month = [12,1,2,4,6,8,9,11,5,7,10,3]
    #df["month"] = month
    #df = df.sort_values(by = 'month')
    #df.reset_index(inplace = True)
    #df.to_csv("data.csv",index = False)
    return final_data_arr
    



var_list = ["orgalk1i"]

df = wrf2var_csv(var_list)
