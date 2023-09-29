"""
This Python script demonstrates the process of loading and manipulating data from a NetCDF file, specifically the ECLIPSE_V6b_CLE_base_NOx.nc dataset. It uses libraries such as numpy, netCDF4, csv, pandas, and matplotlib to perform the following tasks:

1. Import necessary libraries: Import numpy, netCDF4, csv, pandas, and matplotlib to work with data, NetCDF files, and visualize results.

2. Open the NetCDF file: Open the ECLIPSE_V6b_CLE_base_NOx.nc file located at "C:/Users/Lenovo/Downloads/ECLIPSE_V6b_CLE_base_NOx.nc" in read mode using the netCDF4 library.

3. Extract data: Retrieve data from the NetCDF file for variables 'time,' 'emis_all,' 'lat,' and 'lon' and store them in respective variables.

4. Data manipulation: Perform various operations on the data, including extracting a specific element from the 'emis_all' array, calculating the sum of a subset of 'emis_all,' and printing the results.

Feel free to adapt and extend this code for your specific analysis or visualization needs.
"""

import numpy as np
from netCDF4 import Dataset
import csv
import pandas as pd
from matplotlib import pyplot as plt
from netCDF4 import Dataset




file_nc1 =  "C:/Users/Lenovo/Downloads/ECLIPSE_V6b_CLE_base_NOx.nc"
nc1 = Dataset(file_nc1, 'r+')


time = nc1.variables["time"][:]
emi = nc1.variables["emis_all"][:][6]
lat = nc1.variables["lat"][:]
lon = nc1.variables["lon"][:]


emi_del = emi[237][514]
print(emi_del)


emi_del_out = emi[235:240,512:517]

sum_emi_del_out = sum(sum(emi_del_out))
print(sum_emi_del_out)

