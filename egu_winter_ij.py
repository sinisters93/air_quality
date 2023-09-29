"""
This Python script extracts specific atmospheric data from NetCDF files representing different time periods and levels, and then processes and combines this data to create a pandas DataFrame. The resulting DataFrame is subsequently saved as a CSV file named 'egu_winter_soa_.csv'.

The script follows these main steps:
1. Imports necessary libraries, including netCDF4, NumPy, and pandas.
2. Defines a function, 'wrfchemi2arr', to extract and process data from multiple NetCDF files and return an aggregated array.
3. Defines a list of variables, 'var_list', that represent the atmospheric data of interest.
4. Loops through each variable in 'var_list', extracts the data using the 'wrfchemi2arr' function, and appends it to 'Data_var'.
5. Combines the data from 'Data_var' into a single NumPy array.
6. Calculates the sum of the data along one axis and converts it into a pandas DataFrame.
7. Saves the DataFrame as a CSV file named 'egu_winter_soa_.csv'.

Make sure to modify the 'var_list' and file names accordingly for your specific data extraction needs.
"""
from netCDF4 import Dataset
import numpy as np
import pandas as pd


def wrfchemi2arr(var):
    file1 = ['11','12']
    file2 = ['01']
    #file3 = ['04','06','09']        
    Data = []
        
    for i in file1:
        a = 384
        file_nc1 = "wrfout_d01_2017-"+i+"-15_00:00:00"
        o3_nc1  = Dataset(file_nc1, 'r+')
        #extract variable from file
        data_o3_nc1 = o3_nc1.variables[var][:]
        data_slice1 = data_o3_nc1[a:,0,:,:] #time,level,lat,lon 

        Data.append(data_slice1)
        a+24
        
    for j in file2:
        a = 408
        file_nc2 = "wrfout_d01_2018-"+j+"-15_00:00:00"
        o3_nc2  = Dataset(file_nc2, 'r+')
        #extract variable from file
        data_o3_nc2 = o3_nc2.variables[var][:]
        data_slice2 = data_o3_nc2[a:,0,:,:]
        

        Data.append(data_slice2)
        
    array_tuple = (Data[0],Data[1],Data[2])
    arrays = np.vstack(array_tuple)
    final_data_arr = arrays.mean(axis = 0)
    return final_data_arr
    
#####
var_list = ["orgalk1i","orgalk1j","orgaro1i","orgaro1j","orgaro2i","orgaro2j","orgba1i","orgba1j","orgba2i","orgba2j","orgba3i","orgba3j","orgba4i","orgba4j","orgole1i","orgole1j"]

Data_var = []

for i in var_list:
    arr = wrfchemi2arr(i)
    Data_var.append(arr)
    
array_tuple = tuple(Data_var)
	
arrays = np.vstack(array_tuple)
final_data_arr = arrays.sum(axis = 0)
df = pd.DataFrame(final_data_arr)
df.to_csv("egu_winter_soa_.csv",index = False)

    
