"""
This Python script converts data from WRF (Weather Research and Forecasting) model output files to a CSV file containing annual emissions data for a specified variable.

The script imports necessary libraries, including numpy, pandas, matplotlib, and netCDF4, to handle data manipulation and visualization.

The 'wrf2emis_table_csv' function processes the data from WRF output files for specific months and years, extracts the desired variable ('EBIO_LIM' in this case), and combines it into an annual dataset. The resulting data is then saved to a CSV file named 'data_annual_lim.csv'.

To use this script, make sure you have the required netCDF4 files ('wrfout_d01_YYYY-MM-DD_HH:MM:SS') in the same directory and specify the variable of interest in the 'var_list' variable.

Author: Dell
Creation Date: April 4, 2021
"""

#! /usr/bin/python

import numpy as np

import pandas as pd

from matplotlib import pyplot as plt

from netCDF4 import Dataset



def wrf2emis_table_csv(var_list):

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

            data_slice1 = data_o3_nc1[a:,:,:] #time,level,lat,lon 

            Data.append(data_slice1)

            a + 24

	

        for j in file2:

            a = 408

            file_nc2 = "wrfout_d01_2018-"+j+"-15_00:00:00"

            o3_nc2  = Dataset(file_nc2, 'r+')

            #extract variable from file

            data_o3_nc2 = o3_nc2.variables[n][:]

            data_slice2 = data_o3_nc2[a:,:,:]

            Data.append(data_slice2)



        for k in file3:

            a = 384

            file_nc3 = "wrfout_d01_2018-"+k+"-15_00:00:00"

            o3_nc3  = Dataset(file_nc3, 'r+')

            #extract variable from file

            data_o3_nc3 = o3_nc3.variables[n][:]

            data_slice3 = data_o3_nc3[a:,:,:]

            Data.append(data_slice3)







        file_nc4 = "wrfout_d01_2018-02-15_00:00:00"

        o3_nc4  = Dataset(file_nc4, 'r+')

        ##extract variable from file

        data_o3_nc4 = o3_nc4.variables[n][:]

        data_slice4 = data_o3_nc4[360:,:,:]

        Data.append(data_slice4)

        

        

    array_tuple = (Data[0],Data[1],Data[2],Data[3],Data[4],Data[5],Data[6],

                   Data[7],Data[8],Data[9],Data[10],Data[11])

    arrays = np.vstack(array_tuple)

    final_data_arr = arrays.sum(axis = 0)

    df = pd.DataFrame(final_data_arr)

    df.to_csv("data_annual_lim.csv",index = False)

    return df

    



var_list = ["EBIO_LIM"]



df = wrf2emis_table_csv(var_list)
