"""
This Python script imports necessary libraries, reads data from a NetCDF file, and performs calculations on emissions data.
It starts by importing the required libraries: numpy, netCDF4, csv, pandas, and matplotlib.
Then, it opens a NetCDF file named 'ECLIPSE_V6b_CLE_base_NOx.nc' located at 'C:/Users/Lenovo/Downloads/'. 
It extracts time, emissions data ('emis_all'), latitude, and longitude from the NetCDF file.
The script calculates a specific value 'emi_del' from the emissions data and prints it.
Next, it extracts a subset of data 'emi_del_out' from a portion of the emissions data.
Finally, it calculates the sum of values in 'emi_del_out' and prints the result.
This script is designed for data analysis and manipulation of emissions data from the specified NetCDF file.
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

