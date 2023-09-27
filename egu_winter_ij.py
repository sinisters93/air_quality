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

    