#import modules

import warnings
warnings.filterwarnings("ignore")
from pyproj import Transformer
import pandas as pd
import os
from shapely.geometry import Point
import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt


basepath = r"E:\PAVITRA Emissions"

# Projection
reproject_crs="+proj=merc +units=m +a=6370000.0 +b=6370000. +lon_0=80.0 +lat_ts=15.0 + no_defs"
assign_crs="+proj=lcc +lat_1=33.000000 +lat_2=45.000000 +lat_0=40.000000 +lon_0=-97.000000 +x_0=0 +y_0=0 +a=6370997.000000 +b=6370997.000000 +to_meter=1"
transformer = Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)           


def set_df(path_excel):
    df = pd.read_excel(path_excel)
    new_columns = df.iloc[0].to_list()  # Use the second row as new column names
    new_columns[-1] = df.columns[-1]  # Retain the original name for the last column
    df.columns = new_columns

    # Remove the first and last rows (now that we've set the new column names)
    df_updated = df.iloc[1:-1]
    return df_updated

def excel_shapefile_dom(data_df,proxy_file_path,descriptor):
    
    #data_df['Descriptor'] = data_df['Code'].str.lower()
    
    data_df = data_df[data_df["Descriptor"] == descriptor].iloc[:,2:]
    print(data_df)
    
    column_name = data_df.columns
    column_name = column_name[:-1]
    user_input = input("Please enter the number corresponding to the column you wish to select, if you select more species please separate it by comma:\n"
                   "0. All\n"
                   "1. "+ column_name[0]+"\n"
                   "2. "+ column_name[1]+"\n"
                   "3. "+ column_name[2]+"\n"
                   "4. "+ column_name[3]+"\n"
                   "5. "+ column_name[4]+"\n"
                   "6. "+ column_name[5]+"\n"
                   "7. "+ column_name[6]+"\n"
                   "8. "+ column_name[7]+"\n"
                   "9. "+ column_name[8]+"\n"
                   "10. "+ column_name[9]+"\n"
                   
                   "Your choice: ")
    
    data_df = data_df.rename(columns={'PM2.5': 'PM2_5'})
    print(data_df)
    if user_input==str(0):
        data_df_sub = data_df.iloc[:,:-1]
    
    else:
        user_input1 = user_input.split(",")
        user_input1  = [int(item)-1 for item in user_input1]
        data_df_sub = data_df.iloc[:, user_input1]
        
        
    col_name = data_df_sub.columns
    
    for i in range(len(col_name)):

        col_name = data_df_sub.columns
        
        value = data_df_sub.iloc[:,i].values[0]
        
        proxy_file_name = data_df.iloc[:, -1].values[0]     
        
        file_proxy = proxy_file_path + ' / '.strip()+proxy_file_name +'.xlsx'
        print("Excel file in making. It takes some time. Please wait!")
        df_proxy = pd.read_excel(file_proxy)
        df_proxy_sub = df_proxy.iloc[:,2:]
        
        df_proxy_sub1 = value*df_proxy_sub
        df_proxy_sub1["Annual"] =  df_proxy_sub1.sum(axis=1)
        df_proxy_sub1.loc[len(df_proxy_sub1)] = df_proxy_sub1.sum(axis=0)
        
        
      
        df_proxy_sub0 =  df_proxy.iloc[:,:2]
        lat_lon = ["sum","sum"]
        df_proxy_sub0.loc[len(df_proxy_sub0)] = lat_lon
        
        df_proxy_sub_f = pd.concat([df_proxy_sub0, df_proxy_sub1], axis=1)
        df_proxy_sub_f.to_excel(basepath+ "\Output\ ".strip() + proxy_file_name+ '_' +descriptor + '_' + col_name[i] +'.xlsx', index=False)
        
        print("Excel file created for {} Check it in the Output folder of pavitra emmision".format(col_name[i]))
        
        
        mon_name = df_proxy_sub_f.columns[2:]
        
        user_input_mon = input("Please enter the number corresponding to the months of data you wish to select, if you select more than 1 month please separate it by comma:\n"
                           "1. "+ mon_name[0]+"\n"
                           "2. "+ mon_name[1]+"\n"
                           "3. "+ mon_name[2]+"\n"
                           "4. "+ mon_name[3]+"\n"
                           "5. "+ mon_name[4]+"\n"
                           "6. "+ mon_name[5]+"\n"
                           "7. "+ mon_name[6]+"\n"
                           "8. "+ mon_name[7]+"\n"
                           "9. "+ mon_name[8]+"\n"
                           "10. "+ mon_name[9]+"\n"
                           "11. "+ mon_name[10]+"\n"
                           "12. "+ mon_name[11]+"\n"
                           "13. "+ mon_name[12]+"\n"
                           "Your choice: ")
        
        
        print("Hang tight, Getting things ready...")
        user_input2 = user_input_mon.split(",")
        user_input2  = [int(item)-1 for item in user_input2]
        
        
        data_df_mon = df_proxy_sub1.iloc[:, user_input2]
        data_df_mon = data_df_mon.iloc[:-1,:]
        
        col_name_mon = data_df_mon.columns
        
        for j in col_name_mon:
            
        
            df_shp = pd.DataFrame()
            df_shp["Lat"] =  df_proxy_sub_f["Lat"].iloc[:-1]
            df_shp["Lon"] =  df_proxy_sub_f["Lon"].iloc[:-1]
        
            
        
            df_shp["Lat1"] = df_shp["Lat"] - 0.025
            df_shp["Lon1"] = df_shp["Lon"] - 0.025
            df_shp["Lat2"] = df_shp["Lat"] - 0.025
            df_shp["Lon2"] = df_shp["Lon"] + 0.025
            df_shp["Lat3"] = df_shp["Lat"] + 0.025
            df_shp["Lon3"] = df_shp["Lon"] + 0.025
            df_shp["Lat4"] = df_shp["Lat"] + 0.025
            df_shp["Lon4"] = df_shp["Lon"] - 0.025
            
            
            
            df_shp["Points"] = df_shp.apply(lambda row: [(row["Lon1"], row["Lat1"]),(row["Lon2"], row["Lat2"]), (row["Lon3"], row["Lat3"]), (row["Lon4"], row["Lat4"])], axis=1)
            
            df_shp['geometry'] = df_shp['Points'].apply(lambda x: Polygon(x))
            
            df_shp["Points1"] = df_shp.apply(lambda row: (row["Lon"], row["Lat"]), axis=1)
            df_shp['geometry1'] = df_shp['Points1'].apply(lambda x: Point(x))
            
            df_new = pd.DataFrame()
            df_new[col_name[i]] = data_df_mon[j]
            df_new["geometry"] = df_shp["geometry"]
            gdf_wgs84 = gpd.GeoDataFrame(df_new, crs='epsg:4326',geometry='geometry')
            gdf_wgs84['quantiles'] = pd.qcut(gdf_wgs84[col_name[i]], 10, labels=False, duplicates='drop')
            
            
            
            output_path_wgs = basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_EPSG_4326_polygon.shp'
            

            gdf_wgs84.to_file(output_path_wgs)
            print("Shapefile of {} {} for EPSG:4326 has been created. Check it in Output folder of pavitra emmision".format(col_name[i],j))
            
            
            
            
            gdf_inmap = gdf_wgs84.to_crs(crs=reproject_crs)
            gdf_inmap.crs=assign_crs
            gdf_inmap['quantiles'] = pd.qcut(gdf_inmap[col_name[i]], 10, labels=False, duplicates='drop')
            output_path_inmap = basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_InMAP_polygon.shp'
            gdf_inmap.to_file(output_path_inmap)
            
            
            print("Shapefile of {} {} for InMAP(Polygon)  has been created. Check it in Output folder of pavitra emmision".format(col_name[i],j))
       
            df_new1 = pd.DataFrame()
            df_new1[col_name[i]] = data_df_mon[j]
            df_new1["geometry"] = df_shp["geometry1"]
            gdf1_wgs84 = gpd.GeoDataFrame(df_new1, crs='epsg:4326',geometry='geometry')
            
            gdf1_wgs84['quantiles'] = pd.qcut(gdf1_wgs84[col_name[i]], 10, labels=False, duplicates='drop')
            output1_path_wgs = basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_EPSG_4326_point.shp'
            gdf1_wgs84.to_file(output1_path_wgs)
            
            
            gdf1_inmap = gdf1_wgs84.to_crs(crs=reproject_crs)
            gdf1_inmap.crs=assign_crs
            gdf1_inmap['quantiles'] = pd.qcut(gdf1_inmap[col_name[i]], 10, labels=False, duplicates='drop')
            output_path_inmap1 = basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_InMAP_point.shp'
            gdf1_inmap.to_file(output_path_inmap1)
            print("Shapefile of {} {} for InMAP(Point)  has been created. Check it in Output folder of pavitra emmision".format(col_name[i],j))
            
            user_input_plot = input("Which shapefile you wish to plot,:\n"
                               "1. " + "WGS 84 Polygon"+"\n"
                               "2. " + "WGS 84 Point"+"\n"
                               "3. " + "InMAP Polygon"+"\n"
                               "4. " + "InMAP Point"+"\n"
                               "Your choice: ")
            
            if user_input_plot == "1":
                
                plt.close('all')
                fig, ax = plt.subplots(figsize=(10, 6))
                gdf_wgs84.plot(column='quantiles', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8')

                # Add colorbar (adjusting for possibly fewer bins)
                sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=gdf_wgs84['quantiles'].min(), vmax=10))
                sm._A = []
                cbar = fig.colorbar(sm, ax=ax)
                cbar.set_label(col_name[i])
                fig.savefig( basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_EPSG_4326_polygon.png' )
            
            if user_input_plot == "2":
                
                plt.close('all')
                fig, ax = plt.subplots(figsize=(10, 6))
                gdf1_wgs84.plot(column='quantiles', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8')

                # Add colorbar (adjusting for possibly fewer bins)
                sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=gdf1_wgs84['quantiles'].min(), vmax=10))
                sm._A = []
                cbar = fig.colorbar(sm, ax=ax)
                cbar.set_label(col_name[i])
                fig.savefig( basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_EPSG_4326_point.png' )
            
            elif user_input_plot == "3":
                
                plt.close('all')
                fig, ax = plt.subplots(figsize=(10, 6))
                gdf_inmap.plot(column='quantiles', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8')

                # Add colorbar (adjusting for possibly fewer bins)
                sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=gdf_inmap['quantiles'].min(), vmax=10))
                sm._A = []
                cbar = fig.colorbar(sm, ax=ax)
                cbar.set_label(col_name[i])
                fig.savefig( basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_InMAP_polygon.png' )
    
            elif user_input_plot == "4":
               plt.close('all')
               fig, ax = plt.subplots(figsize=(10, 6))
               gdf1_inmap.plot(column='quantiles', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8')

               # Add colorbar (adjusting for possibly fewer bins)
               sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=gdf1_inmap['quantiles'].min(), vmax=10))
               sm._A = []
               cbar = fig.colorbar(sm, ax=ax)
               cbar.set_label(col_name[i])
               fig.savefig( basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_InMAP_point.png' )
            
           

def excel_shapefile(data_df,proxy_file_path,Code):
    
    data_df['Code'] = data_df['Code'].str.lower()
    
    data_df = data_df[data_df["Code"] == Code].iloc[:,2:]
    print(data_df)
    
    column_name = data_df.columns
    column_name = column_name[:-1]
    user_input = input("Please enter the number corresponding to the column you wish to select, if you select more species please separate it by comma:\n"
                   "0. All\n"
                   "1. "+ column_name[0]+"\n"
                   "2. "+ column_name[1]+"\n"
                   "3. "+ column_name[2]+"\n"
                   "4. "+ column_name[3]+"\n"
                   "5. "+ column_name[4]+"\n"
                   "6. "+ column_name[5]+"\n"
                   "7. "+ column_name[6]+"\n"
                   "8. "+ column_name[7]+"\n"
                   "9. "+ column_name[8]+"\n"
                   "10. "+ column_name[9]+"\n"
                   
                   "Your choice: ")
    
    data_df = data_df.rename(columns={'PM2.5': 'PM2_5'})
    print(data_df)
    if user_input==str(0):
        data_df_sub = data_df.iloc[:,:-1]
    
    else:
        user_input1 = user_input.split(",")
        user_input1  = [int(item)-1 for item in user_input1]
        data_df_sub = data_df.iloc[:, user_input1]
        
        
    col_name = data_df_sub.columns
    
    for i in range(len(col_name)):

        col_name = data_df_sub.columns
        
        value = data_df_sub.iloc[:,i].values[0]
        
        proxy_file_name = data_df.iloc[:, -1].values[0]     
        
        file_proxy = proxy_file_path + ' / '.strip()+proxy_file_name +'.xlsx'
        print("Excel file in making. It takes some time. Please wait!")
        df_proxy = pd.read_excel(file_proxy)
        df_proxy_sub = df_proxy.iloc[:,2:]
        
        df_proxy_sub1 = value*df_proxy_sub
        df_proxy_sub1["Annual"] =  df_proxy_sub1.sum(axis=1)
        df_proxy_sub1.loc[len(df_proxy_sub1)] = df_proxy_sub1.sum(axis=0)
        
        
      
        df_proxy_sub0 =  df_proxy.iloc[:,:2]
        lat_lon = ["sum","sum"]
        df_proxy_sub0.loc[len(df_proxy_sub0)] = lat_lon
        
        df_proxy_sub_f = pd.concat([df_proxy_sub0, df_proxy_sub1], axis=1)
        df_proxy_sub_f.to_excel(basepath+ "\Output\ ".strip() +  proxy_file_name+ '_' +code + '_' + col_name[i] +'.xlsx', index=False)
        
        print("Excel file created for {} Check it in the Output folder of pavitra emmision".format(col_name[i]))
        
        
        mon_name = df_proxy_sub_f.columns[2:]
        
        user_input_mon = input("Please enter the number corresponding to the months of data you wish to select, if you select more than 1 month please separate it by comma:\n"
                           "1. "+ mon_name[0]+"\n"
                           "2. "+ mon_name[1]+"\n"
                           "3. "+ mon_name[2]+"\n"
                           "4. "+ mon_name[3]+"\n"
                           "5. "+ mon_name[4]+"\n"
                           "6. "+ mon_name[5]+"\n"
                           "7. "+ mon_name[6]+"\n"
                           "8. "+ mon_name[7]+"\n"
                           "9. "+ mon_name[8]+"\n"
                           "10. "+ mon_name[9]+"\n"
                           "11. "+ mon_name[10]+"\n"
                           "12. "+ mon_name[11]+"\n"
                           "13. "+ mon_name[12]+"\n"
                           "Your choice: ")
        
        
        print("Hang tight, Getting things ready...")
        user_input2 = user_input_mon.split(",")
        user_input2  = [int(item)-1 for item in user_input2]
        
        
        data_df_mon = df_proxy_sub1.iloc[:, user_input2]
        data_df_mon = data_df_mon.iloc[:-1,:]
        
        col_name_mon = data_df_mon.columns
        
        for j in col_name_mon:
            
        
            df_shp = pd.DataFrame()
            df_shp["Lat"] =  df_proxy_sub_f["Lat"].iloc[:-1]
            df_shp["Lon"] =  df_proxy_sub_f["Lon"].iloc[:-1]
        
            
        
            df_shp["Lat1"] = df_shp["Lat"] - 0.025
            df_shp["Lon1"] = df_shp["Lon"] - 0.025
            df_shp["Lat2"] = df_shp["Lat"] - 0.025
            df_shp["Lon2"] = df_shp["Lon"] + 0.025
            df_shp["Lat3"] = df_shp["Lat"] + 0.025
            df_shp["Lon3"] = df_shp["Lon"] + 0.025
            df_shp["Lat4"] = df_shp["Lat"] + 0.025
            df_shp["Lon4"] = df_shp["Lon"] - 0.025
            
            df_shp["Points"] = df_shp.apply(lambda row: [(row["Lon1"], row["Lat1"]),(row["Lon2"], row["Lat2"]), (row["Lon3"], row["Lat3"]), (row["Lon4"], row["Lat4"])], axis=1)
            
            df_shp['geometry'] = df_shp['Points'].apply(lambda x: Polygon(x))
            
            df_shp["Points1"] = df_shp.apply(lambda row: (row["Lon"], row["Lat"]), axis=1)
            df_shp['geometry1'] = df_shp['Points1'].apply(lambda x: Point(x))
            
            df_new = pd.DataFrame()
            df_new[col_name[i]] = data_df_mon[j]
            df_new["geometry"] = df_shp["geometry"]
            gdf_wgs84 = gpd.GeoDataFrame(df_new, crs='epsg:4326',geometry='geometry')
            
            
            gdf_wgs84['quantiles'] = pd.qcut(gdf_wgs84[col_name[i]], 10, labels=False, duplicates='drop')
            
            output_path_wgs = basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_EPSG_4326_polygon.shp'
            gdf_wgs84.to_file(output_path_wgs)
            
            
            
            print("Shapefile of {} {} for EPSG:4326 has been created. Check it in Output folder of pavitra emmision".format(col_name[i],j))
            
            
            
            
            gdf_inmap = gdf_wgs84.to_crs(crs=reproject_crs)
            gdf_inmap.crs=assign_crs
            gdf_inmap['quantiles'] = pd.qcut(gdf_inmap[col_name[i]], 10, labels=False, duplicates='drop')
            output_path_inmap = basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_InMAP_polygon.shp'
            gdf_inmap.to_file(output_path_inmap)
            
            
    
            
            
            print("Shapefile of {} {} for InMAP(Polygon)  has been created. Check it in Output folder of pavitra emmision".format(col_name[i],j))
            
            
            
            df_new1 = pd.DataFrame()
            df_new1[col_name[i]] = data_df_mon[j]
            df_new1["geometry"] = df_shp["geometry1"]
            gdf1_wgs84 = gpd.GeoDataFrame(df_new1, crs='epsg:4326',geometry='geometry')
            gdf1_wgs84['quantiles'] = pd.qcut(gdf1_wgs84[col_name[i]], 10, labels=False, duplicates='drop')
            output_path1_wgs = basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_EPSG_4326_point.shp'
            gdf1_wgs84.to_file(output_path1_wgs)
            
            
            gdf1_inmap = gdf1_wgs84.to_crs(crs=reproject_crs)
            gdf1_inmap.crs=assign_crs
            gdf1_inmap['quantiles'] = pd.qcut(gdf1_inmap[col_name[i]], 10, labels=False, duplicates='drop')
            output_path_inmap1 = basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_InMAP_point.shp'
            gdf1_inmap.to_file(output_path_inmap1)
            print("Shapefile of {} {} for InMAP(Point)  has been created. Check it in Output folder of pavitra emmision".format(col_name[i],j))
            
            
            user_input_plot = input("Which shapefile you wish to plot,:\n"
                               "1. " + "WGS 84 Polygon"+"\n"
                               "2. " + "WGS 84 Point"+"\n"
                               "3. " + "InMAP Polygon"+"\n"
                               "4. " + "InMAP Point"+"\n"
                               "Your choice: ")
            
            if user_input_plot == "1":
                
                plt.close('all')
                fig, ax = plt.subplots(figsize=(10, 6))
                gdf_wgs84.plot(column='quantiles', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8')

                # Add colorbar (adjusting for possibly fewer bins)
                sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=gdf_inmap['quantiles'].min(), vmax=10))
                sm._A = []
                cbar = fig.colorbar(sm, ax=ax)
                cbar.set_label(col_name[i])
                fig.savefig( basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_EPSG_4326_polygon.png' )
            
            if user_input_plot == "2":
                
                plt.close('all')
                fig, ax = plt.subplots(figsize=(10, 6))
                gdf1_wgs84.plot(column='quantiles', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8')

                # Add colorbar (adjusting for possibly fewer bins)
                sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=gdf1_wgs84['quantiles'].min(), vmax=10))
                sm._A = []
                cbar = fig.colorbar(sm, ax=ax)
                cbar.set_label(col_name[i])
                fig.savefig( basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_EPSG_4326_point.png' )
            
            elif user_input_plot == "3":
                
                plt.close('all')
                fig, ax = plt.subplots(figsize=(10, 6))
                gdf_inmap.plot(column='quantiles', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8')

                # Add colorbar (adjusting for possibly fewer bins)
                sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=gdf_inmap['quantiles'].min(), vmax=10))
                sm._A = []
                cbar = fig.colorbar(sm, ax=ax)
                cbar.set_label(col_name[i])
                fig.savefig( basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_InMAP_polygon.png' )
    
            elif user_input_plot == "4":
               plt.close('all')
               fig, ax = plt.subplots(figsize=(10, 6))
               gdf1_inmap.plot(column='quantiles', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8')

               # Add colorbar (adjusting for possibly fewer bins)
               sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=gdf1_inmap['quantiles'].min(), vmax=10))
               sm._A = []
               cbar = fig.colorbar(sm, ax=ax)
               cbar.set_label(col_name[i])
               fig.savefig( basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_InMAP_point.png' )



def excel_shapefile_energy(data_df,proxy_file_path,Code):
    
    data_df['Code'] = data_df['Code'].str.lower()
    
    data_df = data_df[data_df["Code"] == Code].iloc[:,2:]
    print(data_df)
    
    column_name = data_df.columns
    column_name = column_name[:-1]
    user_input = input("Please enter the number corresponding to the column you wish to select, if you select more species please separate it by comma:\n"
                   "0. All\n"
                   "1. "+ column_name[0]+"\n"
                   "2. "+ column_name[1]+"\n"
                   "3. "+ column_name[2]+"\n"
                   "4. "+ column_name[3]+"\n"
                   "5. "+ column_name[4]+"\n"
                   "6. "+ column_name[5]+"\n"
                   "7. "+ column_name[6]+"\n"
                   "8. "+ column_name[7]+"\n"
                   "9. "+ column_name[8]+"\n"
                   "10. "+ column_name[9]+"\n"
                   
                   "Your choice: ")
    
    data_df = data_df.rename(columns={'PM2.5': 'PM2_5'})
    print(data_df)
    if user_input==str(0):
        data_df_sub = data_df.iloc[:,:-1]
    
    else:
        user_input1 = user_input.split(",")
        user_input1  = [int(item)-1 for item in user_input1]
        data_df_sub = data_df.iloc[:, user_input1]
        
        
    col_name = data_df_sub.columns
    
    for i in range(len(col_name)):

        col_name = data_df_sub.columns
        
        value = data_df_sub.iloc[:,i].values[0]
        
        proxy_file_name = data_df.iloc[:, -1].values[0]     
        
        file_proxy = proxy_file_path + ' / '.strip()+proxy_file_name +'.xlsx'
        print("Excel file in making. It takes some time. Please wait!")
        df_proxy = pd.read_excel(file_proxy)
        df_proxy_sub = df_proxy.iloc[:,2:]
        
        df_proxy_sub1 = value*df_proxy_sub
        df_proxy_sub1["Annual"] =  df_proxy_sub1.sum(axis=1)
        df_proxy_sub1.loc[len(df_proxy_sub1)] = df_proxy_sub1.sum(axis=0)
        
        
      
        df_proxy_sub0 =  df_proxy.iloc[:,:2]
        lat_lon = ["sum","sum"]
        df_proxy_sub0.loc[len(df_proxy_sub0)] = lat_lon
        
        df_proxy_sub_f = pd.concat([df_proxy_sub0, df_proxy_sub1], axis=1)
        df_proxy_sub_f.to_excel(basepath+ "\Output\ ".strip() +  proxy_file_name+ '_' +code + '_' + col_name[i] +'.xlsx', index=False)
        
        print("Excel file created for {}".format(col_name[i]))
        
        
        mon_name = df_proxy_sub_f.columns[2:]
        
        user_input_mon = input("Please enter the number corresponding to the months of data you wish to select, if you select more than 1 month please separate it by comma:\n"
                           "1. "+ mon_name[0]+"\n"
                           "2. "+ mon_name[1]+"\n"
                           "3. "+ mon_name[2]+"\n"
                           "4. "+ mon_name[3]+"\n"
                           "5. "+ mon_name[4]+"\n"
                           "6. "+ mon_name[5]+"\n"
                           "7. "+ mon_name[6]+"\n"
                           "8. "+ mon_name[7]+"\n"
                           "9. "+ mon_name[8]+"\n"
                           "10. "+ mon_name[9]+"\n"
                           "11. "+ mon_name[10]+"\n"
                           "12. "+ mon_name[11]+"\n"
                           "13. "+ mon_name[12]+"\n"
                           "Your choice: ")
        
        
        print("Hang tight, Getting things ready...")
        user_input2 = user_input_mon.split(",")
        user_input2  = [int(item)-1 for item in user_input2]
        
        
        data_df_mon = df_proxy_sub1.iloc[:, user_input2]
        data_df_mon = data_df_mon.iloc[:-1,:]
        
        col_name_mon = data_df_mon.columns
        
        for j in col_name_mon:
            
        
            df_shp = pd.DataFrame()
            df_shp["Lat"] =  df_proxy_sub_f["Lat"].iloc[:-1]
            df_shp["Lon"] =  df_proxy_sub_f["Lon"].iloc[:-1]
        
            
    
            
            df_shp["Points"] = df_shp.apply(lambda row: (row["Lon"], row["Lat"]), axis=1)
            df_shp['geometry'] = df_shp['Points'].apply(lambda x: Point(x))
            
            
            df_new = pd.DataFrame()
            df_new[col_name[i]] = data_df_mon[j]
            df_new["geometry"] = df_shp["geometry"]
            df_new["height"] = 220
            df_new["diam"]   = 5.1
            df_new["temp"] = 453
            df_new["velocity"] = 22.5
            
            ##WGS84
            gdf_wgs84 = gpd.GeoDataFrame(df_new, crs='epsg:4326',geometry='geometry')
            output_path_wgs = basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_EPSG_4326_point.shp'
            gdf_wgs84['quantiles'] = pd.qcut(gdf_wgs84[col_name[i]], 10, labels=False, duplicates='drop')
            gdf_wgs84.to_file(output_path_wgs)
            print("Elevated Shapefile of {} {} for EPSG:4326 has been created. Check it in Output folder of pavitra emmision".format(col_name[i],j))
            
            
            
            ##Inmap projection
            gdf_inmap = gdf_wgs84.to_crs(crs=reproject_crs)
            gdf_inmap.crs=assign_crs
            gdf_inmap['quantiles'] = pd.qcut(gdf_inmap[col_name[i]], 10, labels=False, duplicates='drop')
            output_path_inmap = basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_InMAP_point.shp'
            gdf_inmap.to_file(output_path_inmap)
            

            print("Elevated Shapefile of {} {} for InMAP projection  has been created. Check it in Output folder of pavitra emmision".format(col_name[i],j))
            
            
            user_input_plot = input("Which shapefile you wish to plot,:\n"
                               "1. " + "WGS 84 Point"+"\n"
                               "2. " + "InMAP Point"+"\n"
                               "Your choice: ")
            
            if user_input_plot == "1":
                
                plt.close('all')
                fig, ax = plt.subplots(figsize=(10, 6))
                gdf_wgs84.plot(column='quantiles', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8')

                # Add colorbar (adjusting for possibly fewer bins)
                sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=gdf_wgs84['quantiles'].min(), vmax=10))
                sm._A = []
                cbar = fig.colorbar(sm, ax=ax)
                cbar.set_label(col_name[i])
                fig.savefig( basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_EPSG_4326_polygon.png' )
            
            if user_input_plot == "2":
                
                plt.close('all')
                fig, ax = plt.subplots(figsize=(10, 6))
                gdf_inmap.plot(column='quantiles', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8')

                # Add colorbar (adjusting for possibly fewer bins)
                sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=gdf_inmap['quantiles'].min(), vmax=10))
                sm._A = []
                cbar = fig.colorbar(sm, ax=ax)
                cbar.set_label(col_name[i])
                fig.savefig( basepath+ "\Output\ ".strip()+ proxy_file_name+ '_' + col_name[i] + "_"+ j+'_EPSG_4326_point.png' )
            
           
            
           
            
            
#sectors
sectors = {
    "Energy (EN)": {
        "Thermal Power Plant (TPP)": {
            "Thermal Power Plant_Fossil_Coal (TPP_FC)": {
                "divisions": {
                    "1Aai EN_TPP_FC_BSB_CCL_SbC_S1_N1_P1": "EN_TPP_FC_BSB_CCL_SbC_S1_N1_P1",
                    "1Aaii EN_TPP_FC_BSB_CCL_SbC_S2_N2_P1": "EN_TPP_FC_BSB_CCL_SbC_S2_N2_P1",
                    "1Aaiii EN_TPP_FC_BSB_CCL_SbC_S3_N3_P2": "EN_TPP_FC_BSB_CCL_SbC_S3_N3_P2",
                    "1Aaiv EN_TPP_FC_BSB_CCL_SbC_S3_N3_P3": "EN_TPP_FC_BSB_CCL_SbC_S3_N3_P3",
                    "1Aav EN_TPP_FC_BSB_CCL_SuC_S2_N2_P1": "EN_TPP_FC_BSB_CCL_SuC_S2_N2_P1",
                    "1Aavi EN_TPP_FC_BSB_CCL_SuC_S3_N3_P2": "EN_TPP_FC_BSB_CCL_SuC_S3_N3_P2",
                    "1Aavii EN_TPP_FC_BSB_CCL_SuC_S3_N3_P3": "EN_TPP_FC_BSB_CCL_SuC_S3_N3_P3",
                    "1Aaviii EN_TPP_FC_BSB_ECL_SbC_S1_N1_P1": "EN_TPP_FC_BSB_ECL_SbC_S1_N1_P1",
                    "1Aaix EN_TPP_FC_BSB_ECL_SbC_S2_N2_P1": "EN_TPP_FC_BSB_ECL_SbC_S2_N2_P1",
                    "1Aax EN_TPP_FC_BSB_ECL_SbC_S3_N3_P2": "EN_TPP_FC_BSB_ECL_SbC_S3_N3_P2",
                    "1Aaxi EN_TPP_FC_BSB_ECL_SbC_S3_N3_P3": "EN_TPP_FC_BSB_ECL_SbC_S3_N3_P3",
                    "1Aaxii EN_TPP_FC_BSB_MCL_SbC_S3_N3_P3": "EN_TPP_FC_BSB_MCL_SbC_S3_N3_P3",
                    "1Aaxiii EN_TPP_FC_BSB_MCL_SuC_S2_N2_P1": "EN_TPP_FC_BSB_MCL_SuC_S2_N2_P1",
                    "1Aaxiv EN_TPP_FC_BSB_MCL_SuC_S3_N3_P2": "EN_TPP_FC_BSB_MCL_SuC_S3_N3_P2",
                    "1Aaxv EN_TPP_FC_BSB_NCL_SbC_S1_N1_P1": "EN_TPP_FC_BSB_NCL_SbC_S1_N1_P1",
                    "1Aaxvi EN_TPP_FC_BSB_NCL_SbC_S2_N2_P1": "EN_TPP_FC_BSB_NCL_SbC_S2_N2_P1",
                    "1Aaxvii EN_TPP_FC_BSB_NCL_SbC_S3_N3_P2": "EN_TPP_FC_BSB_NCL_SbC_S3_N3_P2",
                    "1Aaxviii EN_TPP_FC_BSB_NCL_SbC_S3_N3_P3": "EN_TPP_FC_BSB_NCL_SbC_S3_N3_P3",
                    "1Aaxix EN_TPP_FC_BSB_NCL_SuC_S1_N1_P1": "EN_TPP_FC_BSB_NCL_SuC_S1_N1_P1",
                    "1Aaxx EN_TPP_FC_BSB_NCL_SuC_S2_N2_P1": "EN_TPP_FC_BSB_NCL_SuC_S2_N2_P1",
                    "1Aaxxi EN_TPP_FC_BSB_NCL_SuC_S3_N3_P2": "EN_TPP_FC_BSB_NCL_SuC_S3_N3_P2",
                    "1Aaxxii EN_TPP_FC_BSB_NCL_SuC_S3_N3_P3": "EN_TPP_FC_BSB_NCL_SuC_S3_N3_P3",
                    "1Aaxxiii EN_TPP_FC_BSB_NCL_CCL_SbC_S3_N3_P2": "EN_TPP_FC_BSB_NCL_CCL_SbC_S3_N3_P2",
                    "1Aaxxiv EN_TPP_FC_BSB_NCL_CCL_SbC_S3_N3_P3": "EN_TPP_FC_BSB_NCL_CCL_SbC_S3_N3_P3",
                    "1Aaxxv EN_TPP_FC_BSB_NCL_WCL_SbC_S2_N2_P1": "EN_TPP_FC_BSB_NCL_WCL_SbC_S2_N2_P1",
                    "1Aaxxvi EN_TPP_FC_BSB_NCL_WCL_SbC_S3_N3_P2": "EN_TPP_FC_BSB_NCL_WCL_SbC_S3_N3_P2",
                    "1Aaxxvii EN_TPP_FC_BSB_NCL_WCL_SbC_S3_N3_P3": "EN_TPP_FC_BSB_NCL_WCL_SbC_S3_N3_P3",
                    "1Aaxxviii EN_TPP_FC_BSB_NCL_WCL_SuC_S2_N2_P1": "EN_TPP_FC_BSB_NCL_WCL_SuC_S2_N2_P1",
                    "1Aaxxix EN_TPP_FC_BSB_SCCL_SbC_S2_N2_P1": "EN_TPP_FC_BSB_SCCL_SbC_S2_N2_P1",
                    "1Aaxxx EN_TPP_FC_BSB_SCCL_SbC_S3_N3_P2": "EN_TPP_FC_BSB_SCCL_SbC_S3_N3_P2",
                    "1Aaxxxi EN_TPP_FC_BSB_SCCL_SbC_S3_N3_P3": "EN_TPP_FC_BSB_SCCL_SbC_S3_N3_P3",
                    "1Aaxxxii EN_TPP_FC_BSB_SCCL_SuC_S1_N1_P1": "EN_TPP_FC_BSB_SCCL_SuC_S1_N1_P1",
                    "1Aaxxxiii EN_TPP_FC_BSB_SCCL_SuC_S2_N2_P1": "EN_TPP_FC_BSB_SCCL_SuC_S2_N2_P1",
                    "1Aaxxxiv EN_TPP_FC_BSB_SCCL_SuC_S2_N3_P1": "EN_TPP_FC_BSB_SCCL_SuC_S2_N3_P1",
                    "1Aaxxxv EN_TPP_FC_BSB_SCCL_SuC_S3_N3_P2": "EN_TPP_FC_BSB_SCCL_SuC_S3_N3_P2",
                    "1Aaxxxvi EN_TPP_FC_BSB_SCCL_SuC_S3_N3_P3": "EN_TPP_FC_BSB_SCCL_SuC_S3_N3_P3",
                    "1Aaxxxvii EN_TPP_FC_BSB_SECL_SbC_S1_N1_P1": "EN_TPP_FC_BSB_SECL_SbC_S1_N1_P1",
                    "1Aaxxxviii EN_TPP_FC_BSB_SECL_SbC_S2_N2_P1": "EN_TPP_FC_BSB_SECL_SbC_S2_N2_P1",
                    "1Aaxxxix EN_TPP_FC_BSB_SECL_SbC_S3_N3_P2": "EN_TPP_FC_BSB_SECL_SbC_S3_N3_P2",
                    "1Aaxl EN_TPP_FC_BSB_SECL_SbC_S3_N3_P3": "EN_TPP_FC_BSB_SECL_SbC_S3_N3_P3",
                    "1Aaxli EN_TPP_FC_BSB_SECL_SuC_S1_N1_P1": "EN_TPP_FC_BSB_SECL_SuC_S1_N1_P1",
                    "1Aaxlii EN_TPP_FC_BSB_SECL_SuC_S2_N2_P1": "EN_TPP_FC_BSB_SECL_SuC_S2_N2_P1",
                    "1Aaxliii EN_TPP_FC_BSB_SECL_SuC_S3_N3_P3": "EN_TPP_FC_BSB_SECL_SuC_S3_N3_P3",
                    "1Aaxliv EN_TPP_FC_BSB_WCL_SbC_S2_N2_P1": "EN_TPP_FC_BSB_WCL_SbC_S2_N2_P1",
                    "1Aaxlv EN_TPP_FC_BSB_WCL_SbC_S3_N3_P2": "EN_TPP_FC_BSB_WCL_SbC_S3_N3_P2",
                    "1Aaxlvi EN_TPP_FC_BSB_WCL_SbC_S3_N3_P3": "EN_TPP_FC_BSB_WCL_SbC_S3_N3_P3",
                    "1Aaxlvii EN_TPP_FC_BSB_WCL_SuC_S1_N1_P1": "EN_TPP_FC_BSB_WCL_SuC_S1_N1_P1",
                    "1Aaxlviii EN_TPP_FC_BSB_WCL_SuC_S2_N2_P1": "EN_TPP_FC_BSB_WCL_SuC_S2_N2_P1",
                    "1Aaxlix EN_TPP_FC_BSB_WCL_SuC_S3_N3_P2": "EN_TPP_FC_BSB_WCL_SuC_S3_N3_P2",
                    "1Aal EN_TPP_FC_BSB_WCL_SuC_S3_N3_P3": "EN_TPP_FC_BSB_WCL_SuC_S3_N3_P3",
                    "1Aali EN_TPP_FC_BIT_IMPORT_SbC_S2_N2_P1": "EN_TPP_FC_BIT_IMPORT_SbC_S2_N2_P1",
                    "1Aalii EN_TPP_FC_BIT_IMPORT_SbC_S2_N3_P2": "EN_TPP_FC_BIT_IMPORT_SbC_S2_N3_P2",
                    "1Aaliii EN_TPP_FC_BIT_IMPORT_SbC_S3_N3_P3": "EN_TPP_FC_BIT_IMPORT_SbC_S3_N3_P3",
                    "1Aaliv EN_TPP_FC_BIT_IMPORT_SuC_S2_N2_P1": "EN_TPP_FC_BIT_IMPORT_SuC_S2_N2_P1",
                    "1Aalv EN_TPP_FC_LIG_SbC_S1_N1_P1": "EN_TPP_FC_LIG_SbC_S1_N1_P1",
                    "1Aalvi EN_TPP_FC_LIG_SbC_S2_N2_P1": "EN_TPP_FC_LIG_SbC_S2_N2_P1",
                    "1Aalvii EN_TPP_FC_LIG_SbC_S3_N3_P2": "EN_TPP_FC_LIG_SbC_S3_N3_P2",
                    "1Aalviii EN_TPP_FC_LIG_SbC_S3_N3_P3": "EN_TPP_FC_LIG_SbC_S3_N3_P3",
                    # ... more divisions
                    # ... divisions for TPP_FC
                },
                "abbreviations": {
                    "Fuel_type": ["BSB - Bituminous/SubBituminous", "BIT_IMPORT - Bituminous", "LIG - Lignite"],
                    "Fuel_Source": ["CCL - Central Coal Field ltd", "ECL - Eastern Coal Field Ltd", "MCL - Mahanadi Coal Field Ltd", "NCL - Northern Coal Field Ltd", "WCL - Western Coal Field Ltd", "SCCL - Singareni Collieries Company Ltd", "SECL - South-Eastern Coal Field Ltd"],
                    "Technology_type": ["SbC - Sub-Critical", "SuC - Super critical"],
                    "APCD_SOx": ["S1 - FGD", "S2 - Spray Drying", "S3 - Uncontrolled/Furnace Injection"],
                    "APCD_NOx": ["N1 - SCR/SNCR", "N2 - Low NOx burner", "N3 - Overfire air"],
                    "APCD_PM2.5": ["P1 - Cyclone+ESP", "P2 - Cyclone+Scrubber","P3 - Multiple Cyclone"],
                    # ... abbreviations for TPP_FC
                },
            },
            "TPP_Fossil_Oil_Gas (FOG)": {
                "divisions": {
                    "1Abi EN_TPP_FOG_DIESEL": "EN_TPP_FOG_DIESEL",
                    "1Abii EN_TPP_FOG_GAS": "EN_TPP_FOG_GAS",
                    "1Abiii EN_TPP_FOG_NAPT": "EN_TPP_FOG_NAPT",
                    # ... divisions for FOG
                },
                "abbreviations": {
                    "Fuel_type": ["NAPT - NAPTHA"],
                    # ... abbreviations for FOG
                },
            },
            # ... more Source-Categories in TPP
        },
        "Fuel Extraction (FE)": {
            "Coal, Mining and Handling (CMH)": {
                "divisions": {
                    "1Bai EN_FE_CMH_UND_MIN":"EN_FE_CMH_UND_MIN",
                    "1Baii EN_FE_CMH_UND_POST_MIN" : "EN_FE_CMH_UND_POST_MIN",
                    "1Baiii EN_FE_CMH_SUR_MIN": "EN_FE_CMH_SUR_MIN",
                    "1Baiv EN_FE_CMH_SUR_POST_MIN":"EN_FE_CMH_SUR_POST_MIN",
                    # ... divisions for CMH
                },
                "abbreviations": {
                    "Mining_type": ["UND - Underground", "SUR - Surface"],
                    # ... abbreviations for CMH
                },
            },
            "Crude oil (CO) & Natural gas (NG)": {
                "divisions": {
                    "1Bbi EN_FE_NC_CO_PROD_EXPL": "EN_FE_NC_CO_PROD_EXPL",
                    "1Bbii EN_FE_NC_NG_PROD_PROC": "EN_FE_NC_NG_PROD_PROC",
                    # ... divisions for CO & NG
                },
                "abbreviations": {
                    "Process_type": ["NC - Non Combustion", "PROD - Production", "EXPL - Exploration", "PROC - Processing"],
                    # ... abbreviations for CO & NG
                },
            },
            # ... more divisions under Fuel Extraction
        },
        "Private Electricity Generation (PEG)-Commercial & public use": {
            "Diesel Genset Residential (DGR)": {
                "divisions": {
                    "1Ca EN_PEG_DGR": "EN_PEG_DGR",
                },
                "abbreviations": {
                    "": ["Not Applicable"],
                    # ... abbreviations for CO & NG
                },
                # Add abbreviations if necessary
            },
            "Diesel Genset Mobile Tower Commercial (DGMTC)": {
                "divisions": {
                    "1Cb EN_PEG_DGMTC": "EN_PEG_DGMTC",
                },
                "abbreviations": {
                    "": ["Not Applicable"],
                    # ... abbreviations for CO & NG
                },
                # Add abbreviations if necessary
            },
            # ... other divisions under PEG
        },
        # ... other Sub-Sectors in Energy
    },
    
    "Industry (IND)": {
    "Heavy Industry (HI)": {
        "HI_Cement (CEM)": {
            "divisions": {
                "2Aai IND_HI_CEM_PROD_PETCOKE": "IND_HI_CEM_PROD_PETCOKE",
                "2Aaii IND_HI_CEM_PROD_IMPORTED_COAL": "IND_HI_CEM_PROD_IMPORTED_COAL",
                "2Aaiii IND_HI_CEM_PROD_LIGNITE": "IND_HI_CEM_PROD_LIGNITE",
                "2Aaiv IND_HI_CEM_PROD_FUELOIL": "IND_HI_CEM_PROD_FUELOIL",
                "2Aav IND_HI_CEM_PROD_CLINKER": "IND_HI_CEM_PROD_CLINKER",
                "2Aavi IND_HI_CEM_PROC_CEMENT": "IND_HI_CEM_PROC_CEMENT",
                "2Aavii IND_HI_CEM_PROC_CLINKER": "IND_HI_CEM_PROC_CLINKER",
                "2Aaviii IND_HI_CEM_CP_COAL": "IND_HI_CEM_CP_COAL",
                "2Aaix IND_HI_CEM_CP_DIESEL": "IND_HI_CEM_CP_DIESEL",
                "2Aax IND_HI_CEM_CP_NATURAL_GAS": "IND_HI_CEM_CP_NATURAL_GAS",
            },
            "abbreviations": {
                "": [
                    "CEM-Cement",
                    "PROD-Clinker Production in Kiln",
                    "PROC-Non-Combustion Emission",
                    "CP-Captive Power"
                ],
            },
        },
        "HI_Refinery (REF)": {
            "divisions": {
                "2Abi IND_HI_REF_PROD_FUEL_OIL": "IND_HI_REF_PROD_FUEL_OIL",
                "2Abii IND_HI_REF_PROD_NATURAL_GAS": "IND_HI_REF_PROD_NATURAL_GAS",
                "2Abiii IND_HI_REF_PROD_NAPTHA": "IND_HI_REF_PROD_NAPTHA",
                "2Abiv IND_HI_REF_PROD_REFINERY_GAS": "IND_HI_REF_PROD_REFINERY_GAS",
                "2Abv IND_HI_REF_PROC_CRUDE_OIL": "IND_HI_REF_PROC_CRUDE_OIL",
                "2Abvi IND_HI_REF_FUG_CRUDE_OIL": "IND_HI_REF_FUG_CRUDE_OIL",
                "2Abvii IND_HI_REF_FUG_GASOLINE": "IND_HI_REF_FUG_GASOLINE",
                "2Abviii IND_HI_REF_CP_FUEL_OIL": "IND_HI_REF_CP_FUEL_OIL",
                "2Abix IND_HI_REF_CP_NATURAL_GAS": "IND_HI_REF_CP_NATURAL_GAS",
                "2Abx IND_HI_REF_CP_NAPTHA": "IND_HI_REF_CP_NAPTHA",
                "2Abxi IND_HI_REF_CP_REFINERY_GAS": "IND_HI_REF_CP_REFINERY_GAS",
            },
            "abbreviations": {
                "": [
                    "PROD-Production of Petroleum Products",
                    "PROC-Crude Oil Processing",
                    "FUG-Figitive",
                    "CP-Captive Power"
                ],
            },
        },
        "HI_Fertilizer (FERT)": {
            "divisions": {
                "2Aci IND_HI_FERT_PROD_COAL": "IND_HI_FERT_PROD_COAL",
                "2Acii IND_HI_FERT_PROD_FUEL_OIL": "IND_HI_FERT_PROD_FUEL_OIL",
                "2Aciii IND_HI_FERT_PROD_NATURAL_GAS": "IND_HI_FERT_PROD_NATURAL_GAS",
                "2Aciv IND_HI_FERT_PROC1_AMMONIA": "IND_HI_FERT_PROC1_AMMONIA",
                "2Acv IND_HI_FERT_PROC2_UREA": "IND_HI_FERT_PROC2_UREA",
                "2Acvi IND_HI_FERT_PROC3_AMMSULPH": "IND_HI_FERT_PROC3_AMMSULPH",
                "2Acvii IND_HI_FERT_PROC4_AMMPHOS": "IND_HI_FERT_PROC4_AMMPHOS",
                "2Acviii IND_HI_FERT_CP_COAL": "IND_HI_FERT_CP_COAL",
                "2Acix IND_HI_FERT_CP_DIESEL": "IND_HI_FERT_CP_DIESEL",
                "2Acx IND_HI_FERT_CP_NATURAL_GAS": "IND_HI_FERT_CP_NATURAL_GAS",
            },
            "abbreviations": {
                "": [
                    "PROD-Fertilizer Production",
                    "PROC1-Ammonia Production",
                    "PROC2-Urea Production",
                    "PROC3-Ammonium Sulphate Production",
                    "PROC4-Ammonium Phosphate Production",
                    "CP-Captive Power"
                ],
            },
        },
        "HI_Non-ferrous metal (NFM)": {
            "divisions": {
                "2Adi IND_HI_NFM_PROD_COAL": "IND_HI_NFM_PROD_COAL",
                "2Adii IND_HI_NFM_PROD_FUEL_OIL": "IND_HI_NFM_PROD_FUEL_OIL",
                "2Adiii IND_HI_NFM_PROD_LPG": "IND_HI_NFM_PROD_LPG",
                "2Adiv IND_HI_NFM_PROC1_ALUMINA": "IND_HI_NFM_PROC1_ALUMINA",
                "2Adv IND_HI_NFM_PROC2_ALUMINIUM": "IND_HI_NFM_PROC2_ALUMINIUM",
                "2Advi IND_HI_NFM_PROC3_PRIMARY_LEAD": "IND_HI_NFM_PROC3_PRIMARY_LEAD",
                "2Advii IND_HI_NFM_PROC4_PRIMARY_ZINC": "IND_HI_NFM_PROC4_PRIMARY_ZINC",
                "2Adviii IND_HI_NFM_PROC5_CU_CATHODE": "IND_HI_NFM_PROC5_CU_CATHODE",
                "2Adix IND_HI_NFM_FUG_CU_CATHODE": "IND_HI_NFM_FUG_CU_CATHODE",
                "2Adx IND_HI_NFM_CP_COAL": "IND_HI_NFM_CP_COAL",
                "2Adxi IND_HI_NFM_CP_DIESEL": "IND_HI_NFM_CP_DIESEL",
                "2Adxii IND_HI_NFM_CP_NATURAL_GAS": "IND_HI_NFM_CP_NATURAL_GAS",
            },
            "abbreviations": {
                "": [
                    "PROD-Metal Production",
                    "PROC1-Alumina Production",
                    "PROC2-Aluminium Production",
                    "PROC3-Primary Lead Production",
                    "PROC4-Primary Zinc Production",
                    "PROC5-Copper Cathode Production",
                    "CP-Captive Power",
                    "FUG-Fugitive"
                ],
            },
        },
        "HI_Iron and Steel (IS)": {
            "divisions": {
                "2Aei IND_HI_IS_PROD1_COKING_COAL": "IND_HI_IS_PROD1_COKING_COAL",
                "2Aeii IND_HI_IS_PROD1_COKE": "IND_HI_IS_PROD1_COKE",
                "2Aeiii IND_HI_IS_FUG_PROD1_COKING_COAL": "IND_HI_IS_FUG_PROD1_COKING_COAL",
                "2Aeiv IND_HI_IS_FUG_PROD1_COKE": "IND_HI_IS_FUG_PROD1_COKE",
                "2Aev IND_HI_IS_PROD2_SINTER": "IND_HI_IS_PROD2_SINTER",
                "2Aevi IND_HI_IS_PROD3_HOT_METAL": "IND_HI_IS_PROD3_HOT_METAL",
                "2Aevii IND_HI_IS_PROD3_FUEL_OIL": "IND_HI_IS_PROD3_FUEL_OIL",
                "2Aeviii IND_HI_IS_CP_PROD345_COAL": "IND_HI_IS_CP_PROD345_COAL",
                "2Aeix IND_HI_IS_PROD6_SPONGE_IRON": "IND_HI_IS_PROD6_SPONGE_IRON",
                "2Aex IND_HI_IS_PROD6_NATURAL_GAS": "IND_HI_IS_PROD6_NATURAL_GAS",
                "2Aexi IND_HI_IS_FUG_PROD2_SINTER": "IND_HI_IS_FUG_PROD2_SINTER",
                "2Aexii IND_HI_IS_FUG_PROD23_COKE": "IND_HI_IS_FUG_PROD23_COKE",
                "2Aexiii IND_HI_IS_FUG_PROD23_IRON_ORE": "IND_HI_IS_FUG_PROD23_IRON_ORE",
                "2Aexiv IND_HI_IS_FUG_PROD3_HOT_METAL": "IND_HI_IS_FUG_PROD3_HOT_METAL",
                "2Aexv IND_HI_IS_FUG_PROD7_CRUDE_STEEL": "IND_HI_IS_FUG_PROD7_CRUDE_STEEL",
                "2Aexvi IND_HI_IS_FUG_PROD5_SPONGE_IRON": "IND_HI_IS_FUG_PROD5_SPONGE_IRON",
                "2Aexvii IND_HI_IS_FUG_PROD8_CRUDE_STEEL": "IND_HI_IS_FUG_PROD8_CRUDE_STEEL",
            },
            "abbreviations": {
                "": [
                    "PROD1-Coke Production",
                    "PROD2-Sinter Production",
                    "PROD3-Hot metal production",
                    "PROD4-Corex hot metal production",
                    "PROD5-Coal based sponge iron production",
                    "PROD6-Gas-based sponge iron production",
                    "PROD23-PROD2 and PROD3",
                    "PROD345-PROD3, PROD4, PROD5",
                    "PROD7-BOF steel production",
                    "PROD8-EAF steel production",
                    "CP-Captive Power",
                    "FUG-Fugitive"
                ],
            },
        },
    },
        "Medium, Small & Micro_Formal Industry (MSM_FI)": {
            "Manufacture of Food Products (FP)":{
                "divisions":{
                    "2Bai IND_MSM_FI_FP_CF_COAL_LIG": "IND_MSM_FI_FP_CF_COAL_LIG",
                    "2Baii IND_MSM_FI_FP_CF_LPG": "IND_MSM_FI_FP_CF_LPG",
                    "2Baiii IND_MSM_FI_FP_CF_DIESEL": "IND_MSM_FI_FP_CF_DIESEL",
                    "2Baiv IND_MSM_FI_FP_CB_RMIL_RHSK": "IND_MSM_FI_FP_CB_RMIL_RHSK",
                    "2Bav IND_MSM_FI_FP_CB_DMIL_WOOD": "IND_MSM_FI_FP_CB_DMIL_WOOD",
                    "2Bavi IND_MSM_FI_FP_CB_JAGG_BAGS": "IND_MSM_FI_FP_CB_JAGG_BAGS",
                    "2Bavii IND_MSM_FI_FP_NC": "IND_MSM_FI_FP_NC",
                        },
                "abbreviations":{
                    "": [
    "CF- Combustion Fossil",
    "CB- Combustion Biomass",
    "LIG- Lignite",
    "RMIL- Rice mill",
    "RHSK- Rice husk",
    "DMIL- Dal Mill",
    "JAGG- Jaggery",
    "BAGS- Baggesse",
    "NC- Non-Combustion"
],},
                },
            "Manufacture of Beverages (BEV)":{
                "divisions":{
                    "2Bbi IND_MSM_FI_BEV_CF_COAL_LIG": "IND_MSM_FI_BEV_CF_COAL_LIG",
"2Bbii IND_MSM_FI_BEV_CF_LPG": "IND_MSM_FI_BEV_CF_LPG",
"2Bbiii IND_MSM_FI_BEV_CF_DIESEL": "IND_MSM_FI_BEV_CF_DIESEL",
"2Bbiv IND_MSM_FI_BEV_NC": "IND_MSM_FI_BEV_NC",
},
"abbreviations":{
   "": [
    "CF- Combustion Fossil",
    "LIG- Lignite",
    "NC- Non-Combustion"
],},
},
            "Manufacture of Tobacco Products(TP)":{
                "divisions":{
                    "2Bci IND_MSM_FI_TP_CF_COAL_LIG": "IND_MSM_FI_TP_CF_COAL_LIG",
"2Bcii IND_MSM_FI_TP_CF_LPG": "IND_MSM_FI_TP_CF_LPG",
"2Bciii IND_MSM_FI_TP_CF_DIESEL": "IND_MSM_FI_TP_CF_DIESEL",
                    },
                "abbreviations":{
                    "":[
    "CF- Combustion Fossil",
    "LIG- Lignite"
],},},
            "Manufacture of Textiles(TEX)":{
                "divisions":{
                    "2Bdi IND_MSM_FI_TEX_CF_COAL_LIG": "IND_MSM_FI_TEX_CF_COAL_LIG",
"2Bdii IND_MSM_FI_TEX_CF_LPG": "IND_MSM_FI_TEX_CF_LPG",
"2Bdiii IND_MSM_FI_TEX_CF_DIESEL": "IND_MSM_FI_TEX_CF_DIESEL",
},
"abbreviations":{
    "":[
    "CF- Combustion Fossil",
    "LIG- Lignite"
],},},
            "Manufacture of Wearing Apparel(AP)":{
                "divisions":{
                    "2Bei IND_MSM_FI_AP_CF_COAL_LIG": "IND_MSM_FI_AP_CF_COAL_LIG",
"2Beii IND_MSM_FI_AP_CF_LPG": "IND_MSM_FI_AP_CF_LPG",
"2Beiii IND_MSM_FI_AP_CF_DIESEL": "IND_MSM_FI_AP_CF_DIESEL",
},
"abbreviations":{
    "":[
    "CF- Combustion Fossil",
    "LIG- Lignite"
],},},
            "Manufacture of Leather & related Products (LRP)":{
                "divisions":{
                    "2Bfi IND_MSM_FI_LRP_CF_COAL_LIG": "IND_MSM_FI_LRP_CF_COAL_LIG",
"2Bfii IND_MSM_FI_LRP_CF_LPG": "IND_MSM_FI_LRP_CF_LPG",
"2Bfiii IND_MSM_FI_LRP_CF_DIESEL": "IND_MSM_FI_LRP_CF_DIESEL",
},
"abbreviations":{
    "":[
    "CF- Combustion Fossil",
    "LIG- Lignite"
],},},
            "Manufacture of wood and products of wood and cork, except furniture; manufacture of articles of straw and plaiting materials (WP)":{
                "divisions":{
                    "2Bgi IND_MSM_FI_WP_CF_COAL_LIG": "IND_MSM_FI_WP_CF_COAL_LIG",
"2Bgii IND_MSM_FI_WP_CF_LPG": "IND_MSM_FI_WP_CF_LPG",
"2Bgiii IND_MSM_FI_WP_CF_DIESEL": "IND_MSM_FI_WP_CF_DIESEL",
},
"abbreviations":{
    "":[
    "CF- Combustion Fossil",
    "LIG- Lignite"
],},},
            "Manufacture of paper and paper products (PP)":{
                "divisions":{
                    "2Bhi IND_MSM_FI_PP_CF_COAL_LIG": "IND_MSM_FI_PP_CF_COAL_LIG",
"2Bhii IND_MSM_FI_PP_CF_LPG": "IND_MSM_FI_PP_CF_LPG",
"2Bhiii IND_MSM_FI_PP_CF_DIESEL": "IND_MSM_FI_PP_CF_DIESEL",},
"abbreviations":{
    "":[
    "CF- Combustion Fossil",
    "LIG- Lignite"
],},},
            "Printing and reproduction of recorded media(PRM)":{
                "divisions":{
                    "2Bi_i IND_MSM_FI_PRM_CF_COAL_LIG": "IND_MSM_FI_PRM_CF_COAL_LIG",
"2Bi_ii IND_MSM_FI_PRM_CF_LPG": "IND_MSM_FI_PRM_CF_LPG",
"2Bi_iii IND_MSM_FI_PRM_CF_DIESEL": "IND_MSM_FI_PRM_CF_DIESEL",},
"abbreviations":{
   "":[
    "CF- Combustion Fossil",
    "LIG- Lignite"
], },},
            "Manufacture of coke and refined petroleum products (CRP)":{
                "divisions":{
                    "2Bji IND_MSM_FI_CRP_CF_COAL_LIG": "IND_MSM_FI_CRP_CF_COAL_LIG",
"2Bjii IND_MSM_FI_CRP_CF_LPG": "IND_MSM_FI_CRP_CF_LPG",
"2Bjiii IND_MSM_FI_CRP_CF_DIESEL": "IND_MSM_FI_CRP_CF_DIESEL",
"2Bjiv IND_MSM_FI_CRP_CC_COKING_COAL": "IND_MSM_FI_CRP_CC_COKING_COAL",
"2Bjv IND_MSM_FI_CRP_CC_COKE": "IND_MSM_FI_CRP_CC_COKE",
"2Bjvi IND_MSM_FI_CRP_NC_PROD_COKING_COAL": "IND_MSM_FI_CRP_NC_PROD_COKING_COAL",
"2Bjvii IND_MSM_FI_CRP_NC_PROD_COKE": "IND_MSM_FI_CRP_NC_PROD_COKE",},
"abbreviations":{
    "":[
    "CF- Combustion Fossil",
    "LIG- Lignite",
    "NC- Non-Combustion",
    "PROD- Production",
    "CC- Coking Coal"
],},},
            "Manufacture of chemicals and chemical products (CHEM)":{
                "divisions":{
                    "2Bki IND_MSM_FI_CHEM_CF_COAL_LIG": "IND_MSM_FI_CHEM_CF_COAL_LIG",
"2Bkii IND_MSM_FI_CHEM_CF_LPG": "IND_MSM_FI_CHEM_CF_LPG",
"2Bkiii IND_MSM_FI_CHEM_CF_DIESEL": "IND_MSM_FI_CHEM_CF_DIESEL",
"2Bkiv IND_MSM_FI_CHEM_NC_CPL_PROD": "IND_MSM_FI_CHEM_NC_CPL_PROD",
"2Bkv IND_MSM_FI_CHEM_NC_CAC2_PROD": "IND_MSM_FI_CHEM_NC_CAC2_PROD",
"2Bkvi IND_MSM_FI_CHEM_NC_TIO2_PROD1": "IND_MSM_FI_CHEM_NC_TIO2_PROD1",
"2Bkvii IND_MSM_FI_CHEM_NC_TIO2_PROD2": "IND_MSM_FI_CHEM_NC_TIO2_PROD2",
"2Bkviii IND_MSM_FI_CHEM_NC_SODA_ASH_PROD": "IND_MSM_FI_CHEM_NC_SODA_ASH_PROD",
"2Bkix IND_MSM_FI_CHEM_NC_CH3OH": "IND_MSM_FI_CHEM_NC_CH3OH",
"2Bkx IND_MSM_FI_CHEM_NC_C2H4": "IND_MSM_FI_CHEM_NC_C2H4",
"2Bkxi IND_MSM_FI_CHEM_NC_EDC": "IND_MSM_FI_CHEM_NC_EDC",
"2Bkxii IND_MSM_FI_CHEM_NC_VCM": "IND_MSM_FI_CHEM_NC_VCM",
"2Bkxiii IND_MSM_FI_CHEM_NC_EtO": "IND_MSM_FI_CHEM_NC_EtO",
"2Bkxiv IND_MSM_FI_CHEM_NC_CBLK_PROD": "IND_MSM_FI_CHEM_NC_CBLK_PROD",
"2Bkxv IND_MSM_FI_CHEM_NC_LDPE_PROD": "IND_MSM_FI_CHEM_NC_LDPE_PROD",
"2Bkxvi IND_MSM_FI_CHEM_NC_HDPE_PROD": "IND_MSM_FI_CHEM_NC_HDPE_PROD",
"2Bkxvii IND_MSM_FI_CHEM_NC_PVC_PROD": "IND_MSM_FI_CHEM_NC_PVC_PROD",
"2Bkxviii IND_MSM_FI_CHEM_NC_PP_PROD": "IND_MSM_FI_CHEM_NC_PP_PROD",
"2Bkxix IND_MSM_FI_CHEM_NC_PS_PROD": "IND_MSM_FI_CHEM_NC_PS_PROD",
"2Bkxx IND_MSM_FI_CHEM_NC_CH2O_PROD": "IND_MSM_FI_CHEM_NC_CH2O_PROD",
"2Bkxxi IND_MSM_FI_CHEM_NC_SBR_PROD": "IND_MSM_FI_CHEM_NC_SBR_PROD",
"2Bkxxii IND_MSM_FI_CHEM_NC_STR_ORGCHEM": "IND_MSM_FI_CHEM_NC_STR_ORGCHEM",
"2Bkxxiii IND_MSM_FI_CHEM_NC_PAINT_PROD": "IND_MSM_FI_CHEM_NC_PAINT_PROD",},
                
                "abbreviations":{
                    "": [
    "CF- Combustion Fossil",
    "LIG- Lignite",
    "NC- Non-Combustion",
    "CPL- Caprolactum",
    "PROD- Production",
    "CAC 2- Calcium Carbide Production",
    "TIO 2- Titanium dioxide",
    "CH 3OH- Methanol",
    "C 2H4- Ethylene",
    "EDC- Ethylene dichloride",
    "VCM- Vinyl Chloride monomer",
    "EtO- Ethylene Oxide",
    "CBLK- Carbon Black",
    "LDPE- Polyethelene low density",
    "HDPE- Polythelene high density",
    "PVC- Polyvinylchloride",
    "PP- Polypropylene",
    "PS- Polystyrene",
    "CH 2O- Formaldehyde",
    "SBR- Synthetic rubber",
    "ORGCHEM- Organic chemicals",
    "PROD1- Production1",
    "PROD2- Production2"
],},
},
            "Manufacture of pharmaceuticals, medicinal chemical and botanical products (PHARM)":{
                "divisions":{
                    "2Bli IND_MSM_FI_PHARM_CF_COAL_LIG": "IND_MSM_FI_PHARM_CF_COAL_LIG",
"2Blii IND_MSM_FI_PHARM_CF_LPG": "IND_MSM_FI_PHARM_CF_LPG",
"2Bliii IND_MSM_FI_PHARM_CF_DIESEL": "IND_MSM_FI_PHARM_CF_DIESEL",},
"abbreviations":{
    "":[
     "CF- Combustion Fossil",
     "LIG- Lignite"
 ],
    },},
            "Manufacture of rubber and plastics products (RP)":{
                "divisions":{
                    "2Bmi IND_MSM_FI_RP_CF_COAL_LIG": "IND_MSM_FI_RP_CF_COAL_LIG",
"2Bmii IND_MSM_FI_RP_CF_LPG": "IND_MSM_FI_RP_CF_LPG",
"2Bmiii IND_MSM_FI_RP_CF_DIESEL": "IND_MSM_FI_RP_CF_DIESEL",
"2Bmiv IND_MSM_FI_RP_NC_TYRE": "IND_MSM_FI_RP_NC_TYRE",},
"abbreviations":{
    "":[
    "CF- Combustion Fossil",
    "LIG- Lignite",
    "NC- Non-Combustion"
],},},
            "Manufacture of other non-metallic mineral products (NMM)":{
                "divisions":{
                    "2Bni IND_MSM_FI_NMM_CF_COAL_LIG": "IND_MSM_FI_NMM_CF_COAL_LIG",
"2Bnii IND_MSM_FI_NMM_CF_LPG": "IND_MSM_FI_NMM_CF_LPG",
"2Bniii IND_MSM_FI_NMM_CF_DIESEL": "IND_MSM_FI_NMM_CF_DIESEL",
"2Bniv IND_MSM_FI_NMM_NC_LIMESTONE_PROD": "IND_MSM_FI_NMM_NC_LIMESTONE_PROD",
"2Bnv IND_MSM_FI_NMM_NC_BITUMEN_PROD": "IND_MSM_FI_NMM_NC_BITUMEN_PROD",},
"abbreviations":{
    "":[
    "CF- Combustion Fossil",
    "LIG- Lignite",
    "NC- Non-Combustion",
    "PROD- Production"
],},},
            "Manufacture of basic metals (MET)":{
                "divisions":{
                    "2Boi IND_MSM_FI_MET_CF_COAL_LIG": "IND_MSM_FI_MET_CF_COAL_LIG",
"2Boii IND_MSM_FI_MET_CF_LPG": "IND_MSM_FI_MET_CF_LPG",
"2Boiii IND_MSM_FI_MET_CF_DIESEL": "IND_MSM_FI_MET_CF_DIESEL",},
"abbreviations":{
    "":[
     "CF- Combustion Fossil",
     "LIG- Lignite"
 ],},},
            "Manufacture of fabricated metal products, except machinery and equipment (FMP)":{
                "divisions":{
                    "2Bpi IND_MSM_FI_FMP_CF_COAL_LIG": "IND_MSM_FI_FMP_CF_COAL_LIG",
"2Bpii IND_MSM_FI_FMP_CF_LPG": "IND_MSM_FI_FMP_CF_LPG",
"2Bpiii IND_MSM_FI_FMP_CF_DIESEL": "IND_MSM_FI_FMP_CF_DIESEL",},
"abbreviations":{
    "":[
     "CF- Combustion Fossil",
     "LIG- Lignite"
 ],},},
            "Manufacture of computer, electronic and optical products (CEOP)":{
                "divisions":{
                    "2Bqi IND_MSM_FI_CEOP_CF_COAL_LIG": "IND_MSM_FI_CEOP_CF_COAL_LIG",
"2Bqii IND_MSM_FI_CEOP_CF_LPG": "IND_MSM_FI_CEOP_CF_LPG",
"2Bqiii IND_MSM_FI_CEOP_CF_DIESEL": "IND_MSM_FI_CEOP_CF_DIESEL",},
"abbreviations":{
   "":[
    "CF- Combustion Fossil",
    "LIG- Lignite"
],},},
            "Manufacture of electrical equipment (EE)":{
                "divisions":{
                    "2Bri IND_MSM_FI_EE_CF_COAL_LIG": "IND_MSM_FI_EE_CF_COAL_LIG",
"2Brii IND_MSM_FI_EE_CF_LPG": "IND_MSM_FI_EE_CF_LPG",
"2Briii IND_MSM_FI_EE_CF_DIESEL": "IND_MSM_FI_EE_CF_DIESEL",},
"abbreviations":{
   "":[
    "CF- Combustion Fossil",
    "LIG- Lignite"
],}, },
"Manufacture of machinery and equipment n.e.c.(ME)":{
    "divisions":{
       "2Bsi IND_MSM_FI_ME_CF_COAL_LIG": "IND_MSM_FI_ME_CF_COAL_LIG",
"2Bsii IND_MSM_FI_ME_CF_LPG": "IND_MSM_FI_ME_CF_LPG",
"2Bsiii IND_MSM_FI_ME_CF_DIESEL": "IND_MSM_FI_ME_CF_DIESEL", },
"abbreviations":{
   "":[
    "CF- Combustion Fossil",
    "LIG- Lignite"
], },},
            "Manufacture of motor vehicles, trailers and semi-trailers (MVTST)":{
                "divisions":{
                    "2Bti IND_MSM_FI_MVTST_CF_COAL_LIG": "IND_MSM_FI_MVTST_CF_COAL_LIG",
"2Btii IND_MSM_FI_MVTST_CF_LPG": "IND_MSM_FI_MVTST_CF_LPG",
"2Btiii IND_MSM_FI_MVTST_CF_DIESEL": "IND_MSM_FI_MVTST_CF_DIESEL",},
"abbreviations":{
   "":[
    "CF- Combustion Fossil",
    "LIG- Lignite"
], },},
            "Manufacture of other transport equipment(OTE)":{
                "divisions":{
                    "2Bui IND_MSM_FI_OTE_CF_COAL_LIG": "IND_MSM_FI_OTE_CF_COAL_LIG",
"2Buii IND_MSM_FI_OTE_CF_LPG": "IND_MSM_FI_OTE_CF_LPG",
"2Buiii IND_MSM_FI_OTE_CF_DIESEL": "IND_MSM_FI_OTE_CF_DIESEL",},
"abbreviations":{
    "":[
     "CF- Combustion Fossil",
     "LIG- Lignite"
 ],},
    },
            "Manufacture of furniture (FUR)":{
                "divisions":{
                    "2Bvi IND_MSM_FI_FUR_CF_COAL_LIG": "IND_MSM_FI_FUR_CF_COAL_LIG",
"2Bvii IND_MSM_FI_FUR_CF_LPG": "IND_MSM_FI_FUR_CF_LPG",
"2Bviii IND_MSM_FI_FUR_CF_DIESEL": "IND_MSM_FI_FUR_CF_DIESEL",},
"abbreviations":{
  "":[
    "CF- Combustion Fossil",
    "LIG- Lignite"
],},},
            "Other manufacturing (OM)":{
                "divisions":{
                    "2Bwi IND_MSM_FI_OM_CF_COAL_LIG": "IND_MSM_FI_OM_CF_COAL_LIG",
"2Bwii IND_MSM_FI_OM_CF_LPG": "IND_MSM_FI_OM_CF_LPG",
"2Bwiii IND_MSM_FI_OM_CF_DIESEL": "IND_MSM_FI_OM_CF_DIESEL",},
"abbreviations":{
    "":[
      "CF- Combustion Fossil",
      "LIG- Lignite"
  ],},},
            "Repair and installation of machinery and equipment (RIME)":{
                "divisions":{
                    "2Bxi IND_MSM_FI_RIME_CF_COAL_LIG": "IND_MSM_FI_RIME_CF_COAL_LIG",
"2Bxii IND_MSM_FI_RIME_CF_LPG": "IND_MSM_FI_RIME_CF_LPG",
"2Bxiii IND_MSM_FI_RIME_CF_DIESEL": "IND_MSM_FI_RIME_CF_DIESEL",},
"abbreviations":{
    "":[
      "CF- Combustion Fossil",
      "LIG- Lignite"
  ],},},
            "Solvent (SOLV)":{
                "divisions":{
                    "2Byi IND_MSM_FI_SOLV_IND _AUT_MAN_PAI_APP": "IND_MSM_FI_SOLV_IND _AUT_MAN_PAI_APP",
"2Byii IND_MSM_FI_SOLV_IND_OTH_IND_PAI_APP": "IND_MSM_FI_SOLV_IND_OTH_IND_PAI_APP",
"2Byiii IND_MSM_FI_SOLV_IND_VEH_TRE": "IND_MSM_FI_SOLV_IND_VEH_TRE",
"2Byiv IND_MSM_FI_SOLV_DOM_USE_SOLV": "IND_MSM_FI_SOLV_DOM_USE_SOLV",
"2Byv IND_MSM_FI_SOLV_DOM_PAI_APP": "IND_MSM_FI_SOLV_DOM_PAI_APP",},
"abbreviations":{
    "": [
    "PAI- Paint",
    "IND- Industry",
    "AUT- Automobile",
    "MAN- Manufacturing",
    "APP- Application",
    "OTH- Other",
    "VEH- Vehicle",
    "DOM- Domestic"
],},},
            "Electricity, Gas, Steam and Aircondition Supply(EGSAS)":{
                "divisions":{
                    "2Bzi IND_MSM_FI_EGSAS_NC_NATGAS_TRANSM_DISTB": "IND_MSM_FI_EGSAS_NC_NATGAS_TRANSM_DISTB",
"2Bzii IND_MSM_FI_EGSAS_NC_CONDENSATE_DISTB": "IND_MSM_FI_EGSAS_NC_CONDENSATE_DISTB",},
"abbreviations":{
    "":[
    "NC- Non-Combustion",
    "TRANSM- Transmission",
    "DISTB- Distribution"
],},},
            "Land transport and transport via pipelines(LT)":{
                "divisions":{
                    "2Baai IND_MSM_FI_LT_NC_PIPE_TRNS_OIL": "IND_MSM_FI_LT_NC_PIPE_TRNS_OIL",
"2Baaii IND_MSM_FI_LT_NC_TRUCK_TRNS_OIL": "IND_MSM_FI_LT_NC_TRUCK_TRNS_OIL",},
"abbreviations":{
   "":[
    "NC- Non-Combustion",
    "TRNS- Transport"
], },},
            "Diesel electricity generation (DEG)":{
                "divisions":{
                    "2Bab IND_MSM_FI_DEG_DIESEL":"IND_MSM_FI_DEG_DIESEL",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            # ... sub-sectors, divisions, and abbreviations for MSM_FI
        },
        "Medium, Small & Micro_Informal Industry (MSM_INFI)": {
    "Manufacture of food products(FP)": {
        "divisions": {
            "2Cai IND_MSM_INFI_FP_CF_COAL_LIG": "IND_MSM_INFI_FP_CF_COAL_LIG",
            "2Caii IND_MSM_INFI_FP_CF_LPG": "IND_MSM_INFI_FP_CF_LPG",
            "2Caiii IND_MSM_INFI_FP_CF_DIESEL": "IND_MSM_INFI_FP_CF_DIESEL",
            "2Caiv IND_MSM_INFI_FP_CB_RMIL_RHSK": "IND_MSM_INFI_FP_CB_RMIL_RHSK",
            "2Cav IND_MSM_INFI_FP_CB_DMIL_WOOD": "IND_MSM_INFI_FP_CB_DMIL_WOOD",
            "2Cavi IND_MSM_INFI_FP_CB_JAGG_BAGS": "IND_MSM_INFI_FP_CB_JAGG_BAGS",
            "2Cavii IND_MSM_INFI_FP_NC": "IND_MSM_INFI_FP_NC",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "CB- Combustion Biomass",
                "RMIL- Rice mill",
                "DMIL- Dal Mill",
                "JAGG- Jaggery",
                "BAGS- Baggesse",
                "NC- Non-Combustion"
            ],
        },
    },
    "Manufacture of Beverages (BEV)": {
        "divisions": {
            "2Cbi IND_MSM_INFI_BEV_CF_COAL_LIG": "IND_MSM_INFI_BEV_CF_COAL_LIG",
            "2Cbii IND_MSM_INFI_BEV_CF_LPG": "IND_MSM_INFI_BEV_CF_LPG",
            "2Cbiii IND_MSM_INFI_BEV_CF_DIESEL": "IND_MSM_INFI_BEV_CF_DIESEL",
            "2Cbiv IND_MSM_INFI_BEV_NC": "IND_MSM_INFI_BEV_NC",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite",
                "NC- Non-Combustion"
            ],
        },
    },
    "Manufacture of Tobacco Products(TP)": {
        "divisions": {
            "2Cci IND_MSM_INFI_TP_CF_COAL_LIG": "IND_MSM_INFI_TP_CF_COAL_LIG",
            "2Ccii IND_MSM_INFI_TP_CF_LPG": "IND_MSM_INFI_TP_CF_LPG",
            "2Cciii IND_MSM_INFI_TP_CF_DIESEL": "IND_MSM_INFI_TP_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Manufacture of Textiles(TEX)": {
        "divisions": {
            "2Cdi IND_MSM_INFI_TEX_CF_COAL_LIG": "IND_MSM_INFI_TEX_CF_COAL_LIG",
            "2Cdii IND_MSM_INFI_TEX_CF_LPG": "IND_MSM_INFI_TEX_CF_LPG",
            "2Cdiii IND_MSM_INFI_TEX_CF_DIESEL": "IND_MSM_INFI_TEX_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Manufacture of Wearing Apparel(AP)": {
        "divisions": {
            "2Cei IND_MSM_INFI_AP_CF_COAL_LIG": "IND_MSM_INFI_AP_CF_COAL_LIG",
            "2Ceii IND_MSM_INFI_AP_CF_LPG": "IND_MSM_INFI_AP_CF_LPG",
            "2Ceiii IND_MSM_INFI_AP_CF_DIESEL": "IND_MSM_INFI_AP_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Manufacture of Leather & related Products (LRP)": {
        "divisions": {
            "2Cfi IND_MSM_INFI_LRP_CF_COAL_LIG": "IND_MSM_INFI_LRP_CF_COAL_LIG",
            "2Cfii IND_MSM_INFI_LRP_CF_LPG": "IND_MSM_INFI_LRP_CF_LPG",
            "2Cfiii IND_MSM_INFI_LRP_CF_DIESEL": "IND_MSM_INFI_LRP_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Manufacture of wood and products of wood and cork, except furniture; manufacture of articles of straw and plaiting materials (WP)": {
        "divisions": {
            "2Cgi IND_MSM_INFI_WP_CF_COAL_LIG": "IND_MSM_INFI_WP_CF_COAL_LIG",
            "2Cgii IND_MSM_INFI_WP_CF_LPG": "IND_MSM_INFI_WP_CF_LPG",
            "2Cgiii IND_MSM_INFI_WP_CF_DIESEL": "IND_MSM_INFI_WP_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Manufacture of paper and paper products (PP)": {
        "divisions": {
            "2Chi IND_MSM_INFI_PP_CF_COAL_LIG": "IND_MSM_INFI_PP_CF_COAL_LIG",
            "2Chii IND_MSM_INFI_PP_CF_LPG": "IND_MSM_INFI_PP_CF_LPG",
            "2Chiii IND_MSM_INFI_PP_CF_DIESEL": "IND_MSM_INFI_PP_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Printing and reproduction of recorded media(PRM)": {
        "divisions": {
            "2Ci_i IND_MSM_INFI_PRM_CF_COAL_LIG": "IND_MSM_INFI_PRM_CF_COAL_LIG",
            "2Ci_ii IND_MSM_INFI_PRM_CF_LPG": "IND_MSM_INFI_PRM_CF_LPG",
            "2Ci_iii IND_MSM_INFI_PRM_CF_DIESEL": "IND_MSM_INFI_PRM_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Manufacture of coke and refined petroleum products (CRP)": {
        "divisions": {
            "2Cji IND_MSM_INFI_CRP_CF_COAL_LIG": "IND_MSM_INFI_CRP_CF_COAL_LIG",
            "2Cjii IND_MSM_INFI_CRP_CF_LPG": "IND_MSM_INFI_CRP_CF_LPG",
            "2Cjiii IND_MSM_INFI_CRP_CF_DIESEL": "IND_MSM_INFI_CRP_CF_DIESEL",
            "2Cjiv IND_MSM_INFI_CRP_CC_COKING_COAL": "IND_MSM_INFI_CRP_CC_COKING_COAL",
            "2Cjv IND_MSM_INFI_CRP_CC_COKE": "IND_MSM_INFI_CRP_CC_COKE",
            "2Cjvi IND_MSM_INFI_CRP_NC_COKING_COAL_PROD": "IND_MSM_INFI_CRP_NC_COKING_COAL_PROD",
            "2Cjvii IND_MSM_INFI_CRP_NC_COKE_PROD": "IND_MSM_INFI_CRP_NC_COKE_PROD",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite",
                "NC- Non-Combustion",
                "CC- Coking Coal",
                "PROD- Production"
            ],
        },
    },
    "Manufacture of chemicals and chemical products (CHEM)": {
        "divisions": {
            "2Cki IND_MSM_INFI_CHEM_CF_COAL_LIG": "IND_MSM_INFI_CHEM_CF_COAL_LIG",
            "2Ckii IND_MSM_INFI_CHEM_CF_LPG": "IND_MSM_INFI_CHEM_CF_LPG",
            "2Ckiii IND_MSM_INFI_CHEM_CF_DIESEL": "IND_MSM_INFI_CHEM_CF_DIESEL",
            "2Ckiv IND_MSM_INFI_CHEM_NC_CPL_PROD": "IND_MSM_INFI_CHEM_NC_CPL_PROD",
            "2Ckv IND_MSM_INFI_CHEM_NC_CAC2_PROD": "IND_MSM_INFI_CHEM_NC_CAC2_PROD",
            "2Ckvi IND_MSM_INFI_CHEM_NC_TIO2_PROD1": "IND_MSM_INFI_CHEM_NC_TIO2_PROD1",
            "2Ckvii IND_MSM_INFI_CHEM_NC_TIO2_PROD2": "IND_MSM_INFI_CHEM_NC_TIO2_PROD2",
            "2Ckviii IND_MSM_INFI_CHEM_NC_SODA_ASH_PROD": "IND_MSM_INFI_CHEM_NC_SODA_ASH_PROD",
            "2Ckix IND_MSM_INFI_CHEM_NC_CH3OH": "IND_MSM_INFI_CHEM_NC_CH3OH",
            "2Ckx IND_MSM_INFI_CHEM_NC_C2H4": "IND_MSM_INFI_CHEM_NC_C2H4",
            "2Ckxi IND_MSM_INFI_CHEM_NC_EDC": "IND_MSM_INFI_CHEM_NC_EDC",
            "2Ckxii IND_MSM_INFI_CHEM_NC_VCM": "IND_MSM_INFI_CHEM_NC_VCM",
            "2Ckxiii IND_MSM_INFI_CHEM_NC_EtO": "IND_MSM_INFI_CHEM_NC_EtO",
            "2Ckxiv IND_MSM_INFI_CHEM_NC_CBLK_PROD": "IND_MSM_INFI_CHEM_NC_CBLK_PROD",
            "2Ckxv IND_MSM_INFI_CHEM_NC_LDPE_PROD": "IND_MSM_INFI_CHEM_NC_LDPE_PROD",
            "2Ckxvi IND_MSM_INFI_CHEM_NC_HDPE_PROD": "IND_MSM_INFI_CHEM_NC_HDPE_PROD",
            "2Ckxvii IND_MSM_INFI_CHEM_NC_PVC_PROD": "IND_MSM_INFI_CHEM_NC_PVC_PROD",
            "2Ckxviii IND_MSM_INFI_CHEM_NC_PP_PROD": "IND_MSM_INFI_CHEM_NC_PP_PROD",
            "2Ckxix IND_MSM_INFI_CHEM_NC_PS_PROD": "IND_MSM_INFI_CHEM_NC_PS_PROD",
            "2Ckxx IND_MSM_INFI_CHEM_NC_CH2O_PROD": "IND_MSM_INFI_CHEM_NC_CH2O_PROD",
            "2Ckxxi IND_MSM_INFI_CHEM_NC_SBR_PROD": "IND_MSM_INFI_CHEM_NC_SBR_PROD",
            "2Ckxxii IND_MSM_INFI_CHEM_NC_STR_ORGCHEM": "IND_MSM_INFI_CHEM_NC_STR_ORGCHEM",
            "2Ckxxiii IND_MSM_INFI_CHEM_NC_PAINT_PROD": "IND_MSM_INFI_CHEM_NC_PAINT_PROD",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite",
                "NC- Non-Combustion",
                "CPL- Caprolactum",
                "PROD- Production",
                "CAC2- Calcium Carbide Production",
                "TIO2- Titanium dioxide",
                "CH3OH- Methanol",
                "C2H4- Ethylene",
                "EDC- Ethylene dichloride",
                "VCM- Vinyl Chloride monomer",
                "EtO- Ethylene Oxide",
                "CBLK- Carbon Black",
                "LDPE- Polyethylene low density",
                "HDPE- Polyethylene high density",
                "PVC- Polyvinyl chloride",
                "PP- Polypropylene",
                "PS- Polystyrene",
                "CH2O- Formaldehyde",
                "SBR- Synthetic rubber",
                "ORGCHEM- Organic chemicals",
                "PROD1- Production1",
                "PROD2- Production2"
            ],
        },
    },
    "Manufacture of pharmaceuticals, medicinal chemical and botanical products (PHARM)": {
        "divisions": {
            "2Cli IND_MSM_INFI_PHARM_CF_COAL_LIG": "IND_MSM_INFI_PHARM_CF_COAL_LIG",
            "2Clii IND_MSM_INFI_PHARM_CF_LPG": "IND_MSM_INFI_PHARM_CF_LPG",
            "2Cliii IND_MSM_INFI_PHARM_CF_DIESEL": "IND_MSM_INFI_PHARM_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Manufacture of rubber and plastics products(RP)": {
        "divisions": {
            "2Cmi IND_MSM_INFI_RP_CF_COAL_LIG": "IND_MSM_INFI_RP_CF_COAL_LIG",
            "2Cmii IND_MSM_INFI_RP_CF_LPG": "IND_MSM_INFI_RP_CF_LPG",
            "2Cmiii IND_MSM_INFI_RP_CF_DIESEL": "IND_MSM_INFI_RP_CF_DIESEL",
            "2Cmiv IND_MSM_INFI_RP_NC_TYRE": "IND_MSM_INFI_RP_NC_TYRE",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite",
                "NC- Non-Combustion"
            ],
        },
    },
    "Manufacture of other non-metallic mineral products (NMM)": {
        "divisions": {
            "2Cni IND_MSM_INFI_NMM_CF_COAL_LIG": "IND_MSM_INFI_NMM_CF_COAL_LIG",
            "2Cnii IND_MSM_INFI_NMM_CF_LPG": "IND_MSM_INFI_NMM_CF_LPG",
            "2Cniii IND_MSM_INFI_NMM_CF_DIESEL": "IND_MSM_INFI_NMM_CF_DIESEL",
            "2Cniv IND_MSM_INFI_NMM_NC_LIMESTONE_PROD": "IND_MSM_INFI_NMM_NC_LIMESTONE_PROD",
            "2Cnv IND_MSM_INFI_NMM_NC_BITUMEN_PROD": "IND_MSM_INFI_NMM_NC_BITUMEN_PROD",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite",
                "PROD- Production",
                "NC- Non-Combustion"
            ],
        },
    },
    "Manufacture of basic metals (MET)": {
        "divisions": {
            "2Coi IND_MSM_INFI_MET_CF_COAL_LIG": "IND_MSM_INFI_MET_CF_COAL_LIG",
            "2Coii IND_MSM_INFI_MET_CF_LPG": "IND_MSM_INFI_MET_CF_LPG",
            "2Coiii IND_MSM_INFI_MET_CF_DIESEL": "IND_MSM_INFI_MET_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Manufacture of fabricated metal products, except machinery and equipment (FMP)": {
        "divisions": {
            "2Cpi IND_MSM_INFI_FMP_CF_COAL_LIG": "IND_MSM_INFI_FMP_CF_COAL_LIG",
            "2Cpii IND_MSM_INFI_FMP_CF_LPG": "IND_MSM_INFI_FMP_CF_LPG",
            "2Cpiii IND_MSM_INFI_FMP_CF_DIESEL": "IND_MSM_INFI_FMP_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Manufacture of computer, electronic and optical products (CEOP)": {
        "divisions": {
            "2Cqi IND_MSM_INFI_CEOP_CF_COAL_LIG": "IND_MSM_INFI_CEOP_CF_COAL_LIG",
            "2Cqii IND_MSM_INFI_CEOP_CF_LPG": "IND_MSM_INFI_CEOP_CF_LPG",
            "2Cqiii IND_MSM_INFI_CEOP_CF_DIESEL": "IND_MSM_INFI_CEOP_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Manufacture of electrical equipment (EE)": {
        "divisions": {
            "2Cri IND_MSM_INFI_EE_CF_COAL_LIG": "IND_MSM_INFI_EE_CF_COAL_LIG",
            "2Crii IND_MSM_INFI_EE_CF_LPG": "IND_MSM_INFI_EE_CF_LPG",
            "2Criii IND_MSM_INFI_EE_CF_DIESEL": "IND_MSM_INFI_EE_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Manufacture of machinery and equipment n.e.c.(ME)": {
        "divisions": {
            "2Csi IND_MSM_INFI_ME_CF_COAL_LIG": "IND_MSM_INFI_ME_CF_COAL_LIG",
            "2Csii IND_MSM_INFI_ME_CF_LPG": "IND_MSM_INFI_ME_CF_LPG",
            "2Csiii IND_MSM_INFI_ME_CF_DIESEL": "IND_MSM_INFI_ME_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Manufacture of motor vehicles, trailers and semi-trailers (MVTST)": {
        "divisions": {
            "2Cti IND_MSM_INFI_MVTST_CF_COAL_LIG": "IND_MSM_INFI_MVTST_CF_COAL_LIG",
            "2Ctii IND_MSM_INFI_MVTST_CF_LPG": "IND_MSM_INFI_MVTST_CF_LPG",
            "2Ctiii IND_MSM_INFI_MVTST_CF_DIESEL": "IND_MSM_INFI_MVTST_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Manufacture of other transport equipment(OTE)": {
        "divisions": {
            "2Cui IND_MSM_INFI_OTE_CF_COAL_LIG": "IND_MSM_INFI_OTE_CF_COAL_LIG",
            "2Cuii IND_MSM_INFI_OTE_CF_LPG": "IND_MSM_INFI_OTE_CF_LPG",
            "2Cuiii IND_MSM_INFI_OTE_CF_DIESEL": "IND_MSM_INFI_OTE_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Manufacture of furniture (FUR)": {
        "divisions": {
            "2Cvi IND_MSM_INFI_FUR_CF_COAL_LIG": "IND_MSM_INFI_FUR_CF_COAL_LIG",
            "2Cvii IND_MSM_INFI_FUR_CF_LPG": "IND_MSM_INFI_FUR_CF_LPG",
            "2Cviii IND_MSM_INFI_FUR_CF_DIESEL": "IND_MSM_INFI_FUR_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Other manufacturing (OM)": {
        "divisions": {
            "2Cwi IND_MSM_INFI_OM_CF_COAL_LIG": "IND_MSM_INFI_OM_CF_COAL_LIG",
            "2Cwii IND_MSM_INFI_OM_CF_LPG": "IND_MSM_INFI_OM_CF_LPG",
            "2Cwiii IND_MSM_INFI_OM_CF_DIESEL": "IND_MSM_INFI_OM_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Repair and installation of machinery and equipment (RIME)": {
        "divisions": {
            "2Cxi IND_MSM_INFI_RIME_CF_COAL_LIG": "IND_MSM_INFI_RIME_CF_COAL_LIG",
            "2Cxii IND_MSM_INFI_RIME_CF_LPG": "IND_MSM_INFI_RIME_CF_LPG",
            "2Cxiii IND_MSM_INFI_RIME_CF_DIESEL": "IND_MSM_INFI_RIME_CF_DIESEL",
        },
        "abbreviations": {
            "": [
                "CF- Combustion Fossil",
                "LIG- Lignite"
            ],
        },
    },
    "Brick Production (BP)": {
        "divisions": {
            "2Cyi IND_MSM_INFI_BP_BTK_FC": "IND_MSM_INFI_BP_BTK_FC",
            "2Cyii IND_MSM_INFI_BP_BTK_CB": "IND_MSM_INFI_BP_BTK_CB",
            "2Cyiii IND_MSM_INFI_BP_ZIG_FC": "IND_MSM_INFI_BP_ZIG_FC",
            "2Cyiv IND_MSM_INFI_BP_ZIG_CB": "IND_MSM_INFI_BP_ZIG_CB",
            "2Cyv IND_MSM_INFI_BP_CDH_FC": "IND_MSM_INFI_BP_CDH_FC",
            "2Cyvi IND_MSM_INFI_BP_CDH_CB": "IND_MSM_INFI_BP_CDH_CB",
        },
        "abbreviations": {
            "": [
                "BTK- Bull's Trench Kiln",
                "ZIG- Zigzag",
                "CDH- Clamps, DDK, Hoffman",
                "FC- 100 % Coal",
                "CB- Coal+Biomass"
            ],
        },
    },
    # ... sub-sectors, divisions, and abbreviations for MSM_INFI
},
        # ... other Sub-Sectors in Industry
    },
    "Transport (TR)":{
        "Passenger Public (PPU)":{
            "CNG (C)":{
                "divisions":{
                    "3Aai TR_PPU_C_HB_BSII_BSIII": "TR_PPU_C_HB_BSII_BSIII",
"3Aaii TR_PPU_C_HB_BSIV": "TR_PPU_C_HB_BSIV",},
"abbreviations":{
    "":[
    "HB- HDV buses",
    "BS- Bharat Standard"
],},},
"Diesel (D)":{
    "divisions":{
        "3Abi TR_PPU_D_HB_BSI_BSII_BSIII": "TR_PPU_D_HB_BSI_BSII_BSIII",
"3Abii TR_PPU_D_HB_BSIV": "TR_PPU_D_HB_BSIV",},
"abbreviations":{
   "":[
    "HB- HDV buses",
    "BS- Bharat Standard"
], },},},
        "Passenger Private (PPR)":{
            "CNG (C)":{
                "divisions":{
                    "3Bai TR_PPR_C_LP_BSII_BSIII": "TR_PPR_C_LP_BSII_BSIII",
"3Baii TR_PPR_C_LP_BSIV": "TR_PPR_C_LP_BSIV",
"3Baiii TR_PPR_C_4W_BSII_BSIII": "TR_PPR_C_4W_BSII_BSIII",
"3Baiv TR_PPR_C_4W_BSIV": "TR_PPR_C_4W_BSIV",},
"abbreviations":{
    "":[
    "4W- Four Wheeler",
    "LP- LMV Passenger",
    "BS- Bharat Standard"
],},},
"Diesel (D)":{
    "divisions":{
        "3Bbi TR_PPR_D_4W_BSI_BSII_BSIII": "TR_PPR_D_4W_BSI_BSII_BSIII",
"3Bbii TR_PPR_D_4W_BSIV": "TR_PPR_D_4W_BSIV",},
"abbreviations":{
    "":[
    "4W- Four Wheeler",
    "BS- Bharat Standard"
],},},
"Gasoline(G)":{
    "divisions":{
        "3Bci TR_PPR_G_2W_BSI_BSII_BSIII": "TR_PPR_G_2W_BSI_BSII_BSIII",
"3Bcii TR_PPR_G_2W_BSIV": "TR_PPR_G_2W_BSIV",
"3Bciii TR_PPR_G_LP_BSI_BSII_BSIII": "TR_PPR_G_LP_BSI_BSII_BSIII",
"3Bciv TR_PPR_G_LP_BSIV": "TR_PPR_G_LP_BSIV",
"3Bcv TR_PPR_G_4W_BSI_BSII_BSIII": "TR_PPR_G_4W_BSI_BSII_BSIII",
"3Bcvi TR_PPR_G_4W_BSIV": "TR_PPR_G_4W_BSIV",},
"abbreviations":{
    "":[
    "4W- Four Wheeler",
    "2W- Two Wheeler",
    "LP- LMV Passenger",
    "BS- Bharat Standard"
],},},
},
        "Freight (FRE)":{
            "CNG (C)":{
                "divisions":{
                    "3Cai TR_FRE_C_LG_3W_BSII_BSIII": "TR_FRE_C_LG_3W_BSII_BSIII",
"3Caii TR_FRE_C_LG_3W_BSIV": "TR_FRE_C_LG_3W_BSIV",
"3Caiii TR_FRE_C_LG_4W_BSII_BSIII": "TR_FRE_C_LG_4W_BSII_BSIII",
"3Caiv TR_FRE_C_LG_4W_BSIV": "TR_FRE_C_LG_4W_BSIV",},
"abbreviations":{
    "":[
    "4W- Four Wheeler",
    "3W- Three Wheeler",
    "LG- LMV Goods",
    "BS- Bharat Standard"
],},},
"Diesel (D)":{
    "divisions":{
        "3Cbi TR_FRE_D_LG_3W_BSI_BSII_BSIII": "TR_FRE_D_LG_3W_BSI_BSII_BSIII",
"3Cbii TR_FRE_D_LG_3W_BSIV": "TR_FRE_D_LG_3W_BSIV",
"3Cbiii TR_FRE_D_LG_4W_BSI_BSII_BSIII": "TR_FRE_D_LG_4W_BSI_BSII_BSIII",
"3Cbiv TR_FRE_D_LG_4W_BSIV": "TR_FRE_D_LG_4W_BSIV",
"3Cbv TR_FRE_D_HT_BSI_BSII_BSIII": "TR_FRE_D_HT_BSI_BSII_BSIII",
"3Cbvi TR_FRE_D_HT_BSIV": "TR_FRE_D_HT_BSIV",
"3Cbvii TR_FRE_D_OT_BSI_BSII_BSIII": "TR_FRE_D_OT_BSI_BSII_BSIII",
"3Cbviii TR_FRE_D_OT_BSIV": "TR_FRE_D_OT_BSIV",},
"abbreviations":{
    "":[
    "4W- Four Wheeler",
    "3W- Three Wheeler",
    "LG- LMV Goods",
    "BS- Bharat Standard",
    "HT- HDV Trucks",
    "OT- Others"
],},},},},
        
    "Agriculture Practices (AP)":{
        "Agriculture Residue Burning (ARB)":{
            "Rice":{
                "divisions":{
                    "4Aa AP_ARB_Rice": "AP_ARB_Rice",},
                "abbreviations":{
                  "":["Not Applicable"],},},
            "Wheat":{
                "divisions":{
                    "4Ab AP_ARB_Wheat": "AP_ARB_Wheat",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Sugarcane":{
                "divisions":{
                    "4Ac AP_ARB_Sugarcane": "AP_ARB_Sugarcane",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Other Cereals (OTH_CER)":{
                "divisions":{
                    "4Ad AP_ARB_OTH_CER": "AP_ARB_OTH_CER",},
                "abbreviations":{
                   "":["Not Applicable"],},},
            "Non Cereals (NON_CER)":{
                "divisions":{
                    "4Ae AP_ARB_NON_CER": "AP_ARB_NON_CER",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Banana":{
                "divisions":{
                    "4Af AP_ARB_Banana": "AP_ARB_Banana"},
                "abbreviations":{
                    "":["Not Applicable"],},},},
        
        "Agriculture Diesel Pump (ADP)":{
            "Shallow Tubewell (SHT)":{
                "divisions":{
                    "4Ba AP_ADP_DP_SHT": "AP_ADP_DP_SHT",},
                "abbreviations":{
                   "":["Not Applicable"],},},
            "Dug Tubewell (DGT)":{
                "divisions":{
                    "4Bb AP_ADP_DP_DGT": "AP_ADP_DP_DGT",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Medium Tubewell (MDT)":{
                "divisions":{
                    "4Bc AP_ADP_DP_MDT": "AP_ADP_DP_MDT",},
                "abbreviations":{
                   "":["Not Applicable"],},},
            "Deep Tubewell (DPT)":{
                "divisions":{
                    "4Bd AP_ADP_DP_DPT": "AP_ADP_DP_DPT",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Surface Lift (SFL)":{
                "divisions":{
                    "4Be AP_ADP_DP_SFL": "AP_ADP_DP_SFL",},
                "abbreviations":{
                    "":["DP-Diesel Pump"],},},
            },
        "Agriculture Diesel Tractor (ADT)":{
            "Diesel Tractor Power Rating (DT_PR)":{
                "divisions":{
                    "4Cai AP_ADT_DT_PR_25HP": "AP_ADT_DT_PR_25HP",
"4Caii AP_ADT_DT_PR_25-50HP": "AP_ADT_DT_PR_25-50HP",
"4Caiii AP_ADT_DT_PR_50HP": "AP_ADT_DT_PR_50HP",},
"abbreviations":{
    "":["HP-Horse Power"],},},},
        },
    "Domestic (DOM)":{
        "Residential Cooking (RES_COO)":{
            "Fuel wood":{
                "divisions":{
                    "5Aa DOM_RES_COO_Fuel_wood": "DOM_RES_COO_Fuel_wood",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Crop Residue":{
                "divisions":{
                    "5Ab DOM_RES_COO_Crop_residue": "DOM_RES_COO_Crop_residue",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Dung cake":{
                "divisions":{
                    "5Ac DOM_RES_COO_dung_cake": "DOM_RES_COO_dung_cake",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "LPG":{
                "divisions":{
                    "5Ad DOM_RES_COO_LPG": "DOM_RES_COO_LPG",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Biogas":{
                "divisions":{
                    "5Ae DOM_RES_COO_Biogas": "DOM_RES_COO_Biogas",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Angeethi":{
                "divisions":{
                    "5Af DOM_RES_COO_Angeethi_Coal": "DOM_RES_COO_Angeethi_Coal",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Kerosene":{
                "divisions":{
                    "5Ag DOM_RES_COO_Kerosene": "DOM_RES_COO_Kerosene",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Electric":{
                "divisions":{
                    "5Ah DOM_RES_COO_Electric": "DOM_RES_COO_Electric",},
                "abbreviations":{
                   "":["Not Applicable"],},},
            },
        "Water heating (WH)":{
            "Fuel wood":{
                "divisions":{
                    "5Ba DOM_WH_Fuel_wood": "DOM_WH_Fuel_wood",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Crop Residue":{
                "divisions":{
                    "5Bb DOM_WH_Crop_residue": "DOM_WH_Crop_residue",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Dung cake":{
                "divisions":{
                    "5Bc DOM_WH_Dung_cake": "DOM_WH_Dung_cake",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Electric":{
                "divisions":{
                    "5Bd DOM_WH_Electric": "DOM_WH_Electric",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            },
        "Space heating (SH)(home+night-time worker)":{
            "Fuel wood":{
                "divisions":{
                    "5Ca DOM_SH_Fuel_wood": "DOM_SH_Fuel_wood",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Crop Residue":{
                "divisions":{
                    "5Cb DOM_SH_Crop_residue": "DOM_SH_Crop_residue",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Dung cake":{
                "divisions":{
                    "5Cc DOM_SH_Dung_cake": "DOM_SH_Dung_cake",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            "Charcoal":{
                "divisions":{
                    "5Cd DOM_SH_Charcoal": "DOM_SH_Charcoal",},
                "abbreviations":{
                    "":["Not Applicable"],},},
            },
        "Lighting (LI)":{
            "Fuel wood":{
                "divisions":{
                    "5Da DOM_NIGHT_LI_fuel_wood": "DOM_NIGHT_LI_fuel_wood",},
                "abbreviations":{
                   "":["Not Applicable"],},},
            "Wicklamp Kerosene":{
                "divisions":{
                    "5Db DOM_LI_wicklamp_kerosene": "DOM_LI_wicklamp_kerosene",},
                "abbreviations":{
                   "":["Not Applicable"],},},
            "Hurricanelamp Kerosene":{
                "divisions":{
                    "5Dc DOM_LI_hurricanelamp_kerosene": "DOM_LI_hurricanelamp_kerosene",},
                "abbreviations":{
                    "":["Not Applicable"],},},},
        },
        
    }




chosen_filenames = []

def get_user_selection(options, prompt):
    print(f"\n{prompt}")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    selection = input("Enter the number(s) of your choice, separated by commas (e.g., 1,2,3), or 0 to select all: ")
    if '0' in selection.split(','):
        return options
    selected_indices = [int(index.strip()) - 1 for index in selection.split(',') if index.strip().isdigit()]
    return [options[i] for i in selected_indices if i < len(options)]
    

def display_abbreviations(abbreviations):
    if abbreviations:  # Check if there are any abbreviations to display
        print("\nAbbreviations:")
        for category, details in abbreviations.items():
            print(f"{category}: {'; '.join(details)}")
    else:
        print("\nNo abbreviations available for this selection.")
        


def extract_division_keys(sectors, sector_name, sub_sector_name=None):
    filenames = []
    if sector_name in sectors:
        for sub_sector, categories in sectors[sector_name].items():
            if sub_sector_name and sub_sector != sub_sector_name:
                continue
            for category, details in categories.items():
                if 'divisions' in details:
                    for division_key in sectors[sector_name][sub_sector][category]['divisions'].keys():
                        division_code = division_key.split(' - ')[0]
                        filename = f"{division_code}.xlsx".replace(' ', '_').replace('/', '_')
                        filenames.append(filename)
    return filenames

# User interaction for sector selection
sectors_options = list(sectors.keys())
selected_sectors = get_user_selection(sectors_options, "Select Sector(s):")

# Choose between global sector division extraction or subsector-level extraction
print("\nChoose an option:")
print("1. Choose all files from the chosen sector(s)")
print("2. Select a specific subsector and extract all division keys from it")

user_choice = input("Enter your choice (1 or 2): ")

if user_choice == "1":
    for sector in selected_sectors:
        filenames = extract_division_keys(sectors, sector)
        print(f"\nDivision keys for {sector}: {filenames}")
else:
    for sector in selected_sectors:
        sub_sectors_options = list(sectors[sector].keys())
        selected_sub_sectors = get_user_selection(sub_sectors_options, f"Select Sub-sector(s) in {sector}:")
        for sub_sector in selected_sub_sectors:
            print(f"Do you to  choose all files for subsector '{sub_sector}'? (yes/no)")
            all_files = input().lower() == 'yes'
            if all_files:
                filenames = extract_division_keys(sectors, sector, sub_sector)
                print(f"\nDivision keys for {sub_sector} in {sector}: {filenames}")
            else:
                filenames = []
                source_categories_options = list(sectors[sector][sub_sector].keys())
                selected_source_categories = get_user_selection(source_categories_options, f"Select Source Category(ies) in {sub_sector}:")

                for source_category in selected_source_categories:
                    abbreviations = sectors[sector][sub_sector][source_category].get("abbreviations", {})
                    display_abbreviations(abbreviations)

                    divisions_options = sectors[sector][sub_sector][source_category]["divisions"]
                    division_selections = [f"{code}" for code, name in divisions_options.items()]
                    selected_divisions = get_user_selection(division_selections, f"Select Division(s) in {source_category}:")
                    for division in selected_divisions:
                        division_code = division.split(' - ')[0]
                        filename = f"{division_code}.xlsx".replace(' ', '_').replace('/', '_')
                        filenames.append(filename)

chosen_filenames = filenames



proxy_file_path = "E:/PAVITRA Emissions/SpatialProxy/Seperated"


for file_identifiers in chosen_filenames:
    file_identifiers1 = file_identifiers.lower()
    if "DOM".lower() in file_identifiers1:
        
        file_path = basepath + "\DOM_emissions.xlsx"
        
        xls = pd.ExcelFile(file_path)
        # Load the content of 'Sheet1'
        sheet_data = pd.read_excel(xls, sheet_name='Sheet1',skiprows=1)

        # Identify rows that are entirely NaN, as these could indicate the separation between tables
        blank_rows = sheet_data.isnull().all(axis=1)

        # Find indices of blank rows to understand where the tables might be separated
        blank_row_indices = blank_rows[blank_rows].index.tolist()

        # Extract tables based on the blank row indices
        # Assuming there's at least one blank row separating two tables, and possibly header rows for the second table
        if blank_row_indices:
            first_table = sheet_data.iloc[:blank_row_indices[0]]
            second_table_start_index = blank_row_indices[0] + 1  # Assuming one blank row separator
            second_table = sheet_data.iloc[second_table_start_index:]
        else:
            first_table, second_table = None, None

        df = first_table
        df.rename(columns={df.columns[2]: 'Population'}, inplace=True)
        df['Descriptor'] = df['Descriptor'].str.strip()
        df['Descriptor'] = df['Descriptor'].str.lower()

    
        if "Kerosene".lower() in file_identifiers1:
            descriptor = "Kerosene".lower()
    
        elif "Kerosene".lower() not in file_identifiers1:
            if "5Ad".lower() in file_identifiers1:
                descriptor = "LPG".lower()
            elif "5Ae".lower() in file_identifiers1:
                descriptor = "Biogas".lower()
            elif "5A".lower() or "5B".lower() or "5C".lower() or "5D".lower():
                descriptor = "Solid fuel".lower()
        df = df.drop(df.columns[2], axis=1)
        data_df = df[df["Descriptor"] == descriptor]    
        
        
    
        excel_shapefile_dom(data_df,proxy_file_path,descriptor)
        
       
                
    elif "AP".lower() in file_identifiers1:
        
        
        
        descriptor = file_identifiers1.split(".")[0][4:]
        if "ARB".lower() in file_identifiers1:
        
            path_excel_arb = basepath + r"\Agriculture\Agriculture_Residue_Burning\AP_ARB_Emissions.xlsx" 
            df_arb = set_df(path_excel_arb)
                
            excel_shapefile(df_arb,proxy_file_path,descriptor)
            
        elif "ADP".lower() in file_identifiers1:
        
            path_excel_adp = basepath + r"\Agriculture\Agriculture_Diesel_Pump\AP_ADP_Emissions.xlsx"
            df_adp = set_df(path_excel_adp)
            excel_shapefile(df_adp,proxy_file_path,descriptor)
            
        elif "ADT".lower() in file_identifiers1:
            
            path_excel_adt = basepath + r"\Agriculture\Agriculture_Diesel_Tractor\AP_ADT_Emissions.xlsx"
           
            df_adt = set_df(path_excel_adt)
            excel_shapefile(df_adt,proxy_file_path,descriptor)
    
    elif "TR".lower() in file_identifiers1:
        code = file_identifiers1.split("_")[0][:-1]
        
        if "FRE".lower() in file_identifiers1:
            
            
            path_excel_fre =  basepath + r"\Transport\Frieght\FRE_Emissions.xlsx" 
            
            df = pd.read_excel(path_excel_fre)
            new_columns = df.iloc[0].to_list()  # Use the second row as new column names
            new_columns[-1] = df.columns[-1]  # Retain the original name for the last column
            df.columns = new_columns
            # Remove the first and last rows (now that we've set the new column names)
            df_updated = df.iloc[1:,:]    
            df_updated.iloc[:, -1] = df_updated.iloc[0:1, -1].values[0]
            df_fre = df_updated
            
            df_fre = df_fre.drop(df_fre.columns[2], axis=1)
            
            
            descript = "_".join(file_identifiers1.split("_")[3])
            
            
            if descript.lower() == "c":
                descriptor = df_fre["Descriptor"][1].lower()
            elif descript.lower() == "d":
                descriptor = df_fre["Descriptor"][2].lower()

            
            excel_shapefile(df_fre,proxy_file_path,code)
            
        elif "PPR".lower() in file_identifiers1:
        
            path_excel_ppr =  basepath + r"\Transport\Passenger Private\PPR_Emissions.xlsx" 
            #df_arb = set_df(path_excel_arb)
            ##
            df = pd.read_excel(path_excel_ppr)
            new_columns = df.iloc[0].to_list()  # Use the second row as new column names
            new_columns[-1] = df.columns[-1]  # Retain the original name for the last column
            df.columns = new_columns
            # Remove the first and last rows (now that we've set the new column names)
            df_updated = df.iloc[1:,:]    
            df_updated.iloc[:, -1] = df_updated.iloc[0:1, -1].values[0]
            df_ppr = df_updated
            
            df_ppr = df_ppr.drop(df_ppr.columns[2], axis=1)
            descript = "_".join(file_identifiers1.split("_")[3])
            
            if descript.lower() == "c":
                descriptor = df_ppr["Descriptor"][1].lower()
            elif descript.lower() == "d":
                descriptor = df_ppr["Descriptor"][2].lower()
            elif descript.lower() == "g":
                descriptor = df_ppr["Descriptor"][3].lower()
            
            excel_shapefile(df_ppr,proxy_file_path,code)
            
        elif "PPU".lower() in file_identifiers1:
            
            path_excel_ppu =  basepath + r"\Transport\Passenger Public\PPU_Emissions.xlsx" 
            #df_arb = set_df(path_excel_arb)
            ##
            df = pd.read_excel(path_excel_ppu)
            new_columns = df.iloc[0].to_list()  # Use the second row as new column names
            new_columns[-1] = df.columns[-1]  # Retain the original name for the last column
            df.columns = new_columns
            # Remove the first and last rows (now that we've set the new column names)
            df_updated = df.iloc[1:,:]    
            df_updated.iloc[:, -1] = df_updated.iloc[0:1, -1].values[0]
            df_ppu = df_updated
            
            df_ppu = df_ppu.drop(df_ppu.columns[2], axis=1)
            descript = "_".join(file_identifiers1.split("_")[3])
            
            if descript.lower() == "c":
                descriptor = df_ppu["Descriptor"][1].lower()
            elif descript.lower() == "d":
                descriptor = df_ppu["Descriptor"][2].lower()
                
            
            excel_shapefile(df_ppu,proxy_file_path,code)
            
    elif "IND".lower() in file_identifiers1:
        code = file_identifiers1.split("_")[0][:-1]
        if "HI".lower() in file_identifiers1:
            
            
            path_excel_hi =  basepath + r"\Industry\Heavy\HI_emissions.xlsx"
            
            df = pd.read_excel(path_excel_hi)
            new_columns = df.iloc[0].to_list()  # Use the second row as new column names
            new_columns[-1] = df.columns[-1]  # Retain the original name for the last column
            df.columns = new_columns
            # Remove the first and last rows (now that we've set the new column names)
            df_updated = df.iloc[1:-1,:]    
            
            df_hi = df_updated
            
            df_hi = df_hi.drop(df_hi.columns[2], axis=1)
            
            
            

            
            excel_shapefile(df_hi,proxy_file_path,code)
            
        elif "MSM_FI".lower() in file_identifiers1:
            
            
            path_excel_fi = basepath + r"\Industry\Formal\FI_emissions.xlsx"
           
            df = pd.read_excel(path_excel_fi)
            new_columns = df.iloc[0].to_list()  # Use the second row as new column names
            new_columns[-1] = df.columns[-1]  # Retain the original name for the last column
            df.columns = new_columns
            # Remove the first and last rows (now that we've set the new column names)
            df_updated = df.iloc[1:-1,:]    
            df_updated.iloc[:, -1] = df_updated.iloc[0:1, -1].values[0]
            df_fi = df_updated
            
           
            
            excel_shapefile(df_fi,proxy_file_path,code)
            
        elif "MSM_INFI".lower() in file_identifiers1:
            
            
            path_excel_infi =  basepath + r"\Industry\Informal\INFI_emissions.xlsx"
            #df_arb = set_df(path_excel_arb)
            ##
            df = pd.read_excel(path_excel_infi)
            new_columns = df.iloc[0].to_list()  # Use the second row as new column names
            new_columns[-1] = df.columns[-1]  # Retain the original name for the last column
            df.columns = new_columns
            # Remove the first and last rows (now that we've set the new column names)
            df_updated = df.iloc[1:-1,:]    
            df_updated.iloc[:, -1] = df_updated.iloc[0:1, -1].values[0]
            df_infi = df_updated
            
            #df_fi = df_fi.drop(df_fi.columns[2], axis=1)
            

            
            excel_shapefile(df_infi,proxy_file_path,code)
            
    elif "EN".lower() in file_identifiers1:
       
        if "TPP_FC".lower() in file_identifiers1:
            
            
            path_excel_tpp_fc =  basepath + r"\Energy\TPP_COAL\EN_TPP_Coal_Emission.xlsx"
            #df_arb = set_df(path_excel_arb)
            ##
            df = pd.read_excel(path_excel_tpp_fc)
            new_columns = df.iloc[0].to_list()  # Use the second row as new column names
            new_columns[-1] = df.columns[-1]  # Retain the original name for the last column
            df.columns = new_columns
            # Remove the first and last rows (now that we've set the new column names)
            df_updated = df.iloc[1:-1,:]    
            
            df_tpp_fc = df_updated
            
            #df_tpp_fc = df_tpp_fc.drop(df_tpp_fc.columns[2], axis=1)
            
            code = file_identifiers1.split("_")[0][:-1]
            

            
            excel_shapefile_energy(df_tpp_fc,proxy_file_path,code)
            
        elif "TPP_FOG".lower() in file_identifiers1:
            
            
            path_excel_tpp_fog =  basepath + r"\Energy\TPP_Oil_GAS\EN_TPP_OilGAS_Emissions.xlsx"
            
            
            df = pd.read_excel(path_excel_tpp_fog)
            new_columns = df.iloc[0].to_list()  # Use the second row as new column names
            new_columns[-1] = df.columns[-1]  # Retain the original name for the last column
            df.columns = new_columns
            # Remove the first and last rows (now that we've set the new column names)
            df_updated = df.iloc[1:-1,:]    
            
            df_tpp_fog = df_updated
            
           
            
            code = file_identifiers1.split("_")[0][:-1]
            

            
            excel_shapefile_energy(df_tpp_fog,proxy_file_path,code)
            
        elif "FE".lower() in file_identifiers1:
            
            
            path_excel_fe =  basepath + r"\Energy\Fuel_Extraction\EN_FE_Emissions.xlsx"
            
            
            df = pd.read_excel(path_excel_fe)
            new_columns = df.iloc[0].to_list()  # Use the second row as new column names
            new_columns[-1] = df.columns[-1]  # Retain the original name for the last column
            df.columns = new_columns
            # Remove the first and last rows (now that we've set the new column names)
            df_updated = df.iloc[1:-1,:]    
            
            df_fe = df_updated
            code = file_identifiers1.split("_")[0][:-1]

            excel_shapefile_energy(df_fe,proxy_file_path,code)
            
        elif "PEG".lower() in file_identifiers1:
            
            
            path_excel_peg =  basepath + r"\Energy\Private_Electricity_Generation\PEG_emissions.xlsx"
            
            
            df = pd.read_excel(path_excel_peg)
            new_columns = df.iloc[0].to_list()  # Use the second row as new column names
            new_columns[-1] = df.columns[-1]  # Retain the original name for the last column
            df.columns = new_columns
            # Remove the first and last rows (now that we've set the new column names)
            df_updated = df.iloc[1:-1,:]    
            
            df_peg = df_updated
            df_peg = df_peg.drop(df_peg.columns[2], axis=1)
            
            code = file_identifiers1.split("_")[0]

            excel_shapefile_energy(df_peg,proxy_file_path,code)
