# -*- coding: utf-8 -*-

"""

Created on Thu Feb 11 23:43:17 2021



@author: hp

"""



#! /usr/bin/python



from netCDF4 import Dataset
import numpy as np
import pandas as pd



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
            data_slice1 = data_o3_nc1[a:,0,58,32]
            data_slice1 = data_slice1.tolist()
            Data.extend(data_slice1)
            a + 24
	
        for j in file2:
            a = 408
            file_nc2 = "wrfout_d01_2018-"+j+"-15_00:00:00"
            o3_nc2  = Dataset(file_nc2, 'r+')
            #extract variable from file
            data_o3_nc2 = o3_nc2.variables[n][:]
            data_slice2 = data_o3_nc2[a:,0,58,32]
            data_slice2 = data_slice2.tolist()
            Data.extend(data_slice2)

        for k in file3:
            a = 384
            file_nc3 = "wrfout_d01_2018-"+k+"-15_00:00:00"
            o3_nc3  = Dataset(file_nc3, 'r+')
            #extract variable from file
            data_o3_nc3 = o3_nc3.variables[n][:]
            data_slice3 = data_o3_nc3[a:,0,58,32]
            data_slice3 = data_slice3.tolist()
            Data.extend(data_slice3)


        file_nc4 = "wrfout_d01_2018-02-15_00:00:00"
        o3_nc4  = Dataset(file_nc4, 'r+')
        ##extract variable from file
        data_o3_nc4 = o3_nc4.variables[n][:]
        data_slice4 = data_o3_nc4[360:,0,58,32]
        data_slice4 = data_slice4.tolist()
        Data.extend(data_slice4)
    
    
        final_data.append(Data)
        
    final_data_arr = np.array(final_data)
    final_data_arr = final_data_arr.T

    df = pd.DataFrame(final_data_arr, columns = var_list)
    df.to_csv("data.csv",index = False)
    return df
    

#####

var_list = ["o3"]

df = wrf2var_csv(var_list)