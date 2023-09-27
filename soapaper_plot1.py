# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 11:29:03 2021

@author: Dell
"""

from netCDF4 import Dataset
import numpy as np
import pandas as pd
def wrfchemi2csv(var):
    final_data = []
    file1 = ['12']
    file2 = ['01',"02",'03','04','05','06','07','08','09','10',"11"]
    
    Data = []
    for i in file1:
        a = 384
        file_nc1 = "wrfchemi_d01_2017-"+i+"-15_00:00:00"
        o3_nc1  = Dataset(file_nc1, 'r+')
        #extract variable from file
        data_o3_nc1 = o3_nc1.variables[var][:]

        Data.append(data_o3_nc1)
        a+24
        
    for j in file2:
        a = 408
        file_nc2 = "wrfchemi_d01_2018-"+j+"-15_00:00:00"
        o3_nc2  = Dataset(file_nc2, 'r+')
        #extract variable from file
        data_o3_nc2 = o3_nc2.variables[var][:]
        

        Data.append(data_o3_nc2)
    array_tuple = (Data[0],Data[1],Data[2],Data[3],Data[4],Data[5],Data[6],
                   Data[7],Data[8],Data[9],Data[10],Data[11])
    arrays = np.vstack(array_tuple)
    final_data_arr = arrays.sum(axis = 0)
    final_data_arr = final_data_arr.reshape(final_data_arr.shape[1],final_data_arr.shape[2])    
    df = pd.DataFrame(final_data_arr)
    df.to_csv("data_wrfchemi.csv",index = False)
    return df
    

#####

var = "E_ORGJ"

df = wrfchemi2csv(var)
    