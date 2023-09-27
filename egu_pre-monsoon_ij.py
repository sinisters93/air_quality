
from netCDF4 import Dataset
import numpy as np
import pandas as pd


def wrfchemi2arr(var):
    #file1 = ['11','12']
    file2 = ['03']
    file3 = ['04']        
    Data = []
        
    for j in file2:
        a = 408
        file_nc2 = "wrfout_d01_2018-"+j+"-15_00:00:00"
        o3_nc2  = Dataset(file_nc2, 'r+')
        #extract variable from file
        data_o3_nc2 = o3_nc2.variables[var][:]
        data_slice2 = data_o3_nc2[a:,0,:,:]
        Data.append(data_slice2)
        
    for k in file3:
            a = 384
            file_nc3 = "wrfout_d01_2018-"+k+"-15_00:00:00"
            o3_nc3  = Dataset(file_nc3, 'r+')
            #extract variable from file
            data_o3_nc3 = o3_nc3.variables[var][:]
            data_slice3 = data_o3_nc3[a:,0,:,:]
            Data.append(data_slice3)
            

            file_nc4 = "wrfout_d01_2018-02-15_00:00:00"
            o3_nc4  = Dataset(file_nc4, 'r+')
        ##extract variable from file
            data_o3_nc4 = o3_nc4.variables[var][:]
            data_slice4 = data_o3_nc4[360:,0,:,:]
            Data.append(data_slice4)
        
    array_tuple = (Data[0],Data[1],Data[2])
    arrays = np.vstack(array_tuple)
    final_data_arr = arrays.mean(axis = 0)
    return final_data_arr
    

#####

var_list = ["eci","ecj"]

Data_var = []


for i in var_list:
    arr = wrfchemi2arr(i)
    Data_var.append(arr)
    
array_tuple = tuple(Data_var)
	
arrays = np.vstack(array_tuple)
final_data_arr = arrays.sum(axis = 0)
df = pd.DataFrame(final_data_arr)
df.to_csv("egu_premonsoon_ec_.csv",index = False)

    