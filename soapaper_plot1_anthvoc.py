# -*- coding: utf-8 -*-
"""
Converts WRF-Chem chemical species data from multiple netCDF files into a single DataFrame and exports it to a CSV file.

This script reads WRF-Chem chemical species data from multiple netCDF files, combines them into a single array, and then creates a DataFrame. 
The resulting DataFrame is exported to a CSV file named 'anthvoc_orgj.csv'. The script primarily uses the 'netCDF4' library for reading data and 'numpy' 
and 'pandas' for data manipulation.

Created on Sat Apr 3 11:29:03 2021
@author: Dell
"""

from netCDF4 import Dataset
import numpy as np
import pandas as pd
def wrfchemi2arr(var):
    
    final_data = []
    #file1 = ['11','12']

    #file2 = ['01','03','05','07','08','10']
    
    #file3 = ['04','06','09']
    file1 = ['12']
    file2 = ['01',"02",'03','04','05','06','07','08','09','10','11']
    
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
        
    array_tuple = (Data[0],Data[1],Data[2],Data[3],Data[4],Data[5],Data[6],Data[7],Data[8],Data[9],Data[10],Data[11])
    arrays = np.vstack(array_tuple)
    final_data_arr = arrays.sum(axis = 0)
    return final_data_arr
    
#####
var_list = ["E_ORGJ"]
Data_var = []

for i in var_list:
    arr = wrfchemi2arr(i)
    Data_var.append(arr)
    
array_tuple = tuple(Data_var)	
arrays = np.vstack(array_tuple)
final_data_arr = arrays.sum(axis = 0)
df = pd.DataFrame(final_data_arr)
df.to_csv("anthvoc_orgj.csv",index = False)

    
