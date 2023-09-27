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

