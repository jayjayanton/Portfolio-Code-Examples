import glob
import os
from osgeo import osr
from osgeo import gdal
import arcpy
from arcpy.sa import *
from arcpy import env
from simpledbf import Dbf5
import pandas as pd
import numpy as np
from natsort import natsorted
from functools import reduce

######################################################################################################################################################
### Script converts CLM raster to point specific shapefiles, merges them into a single dataframe and changes the output into a reusable excel file ### 
######################################################################################################################################################

outputdir = r"E:\\CLM\\Raster Point Data\\PFT_Rasters\\" # Create an output directory
arcpy.env.workspace = r"D:\\GCAM\\Landcover\\CLM\\PFT_78\\Reexported Raster\\" # Create an Arcpy Environmental Workspace

arcpy.env.overwriteOutput = True
tif_files = sorted(glob.glob("*.tif"))

for tif in tif_files:
    basetfilename = os.path.basename(tif)
    CleanBaseStr = os.path.splitext(basetfilename)[0]
    PFT = CleanBaseStr.split('_',-1)[8]
    OutFileName = f"PFT_{PFT}.shp"
    output_file = os.path.join(outputdir, OutFileName)
    field = "VALUE"
    arcpy.RasterToPoint_conversion(tif, output_file, field)

path = os.chdir(outputdir)
arcpy.env.workspace = outputdir
dbf_files = sorted(glob.glob("*.dbf"))

# Read USA dbf file. This dbf file was an empty file covering the entire CONUS and was used as a place holder to have a unique id to compare with converted files
USA_dbf = Dbf5(r"E:\CLM\\Raster Point Data\\USA_Raster_to_Point.dbf")  
USA_df = USA_dbf.to_dataframe()
USA_df['pointid']=USA_df['pointid'].astype(float)
USA_df['grid_code']=USA_df['grid_code'].astype(float)

pieces = 30
new_arrays = np.array_split(dbf_files, pieces)
Dataframe_List = []
for array in new_arrays[0:30]:
    for dbf in array:
        basetfilename = os.path.basename(dbf)
        CleanBaseStr = os.path.splitext(basetfilename)[0]
        PFT = CleanBaseStr.split('_',-1)[1]
        Lat = "Lat" # Y-coordinate
        Lat_type = "Double"
        Long = "Long" # X-coordinate
        Long_type = "Double"
        
        arcpy.management.AddField(dbf, Lat, Lat_type)
        geometry_property_Lat = 'POINT_Y'
        coordinate_system = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
        coordinate_format = 'SAME_AS_INPUT'

        arcpy.management.AddField(dbf, Long, Long_type)
        geometry_property_Long = 'POINT_X'
        coordinate_system = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
        coordinate_format = 'SAME_AS_INPUT'
      
        arcpy.management.CalculateGeometryAttributes(dbf, [[Lat, geometry_property_Lat], [Long, geometry_property_Long]], '','', coordinate_system, coordinate_format)

        #Open DBF files
        new_df = Dbf5(dbf)
        df = new_df.to_dataframe()
        df.drop('pointid', inplace=True, axis=1)
        df = df.rename(columns={"grid_code":f"PFT_{PFT}"})
        df[f"PFT_{PFT}"] = df[f"PFT_{PFT}"]
        Dataframe_List.append(df)

PFT_Dfs = reduce(lambda  left,right: pd.merge(left,right,on=['Lat','Long']), Dataframe_List)
PFT_xls = "PFTs_Merged.xlsx"
output_file = os.path.join(outputdir, PFT_xls)
PFT_Dfs.to_excel(output_file)
USA_df = USA_df.merge(df, on=['Lat', 'Long'], how='left')

# ### Dataframe to Excel
USA_df = USA_df.reindex(natsorted(USA_df.columns), axis=1)
# print(USA_df)
out_xls = f"USA_df.xlsx"
output_file = os.path.join(outputdir, out_xls)
USA_df.to_excel(output_file,index=False)
#
print("processing done")
