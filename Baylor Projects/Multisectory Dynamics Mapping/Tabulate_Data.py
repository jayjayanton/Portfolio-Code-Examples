# Note: Found in D:\GCAM\Landcover\CLM\PFT_78\Reexported Raster

import glob
import os
from osgeo import osr
import arcpy
from arcpy.sa import *
from arcpy import env

Tiff_files = sorted(glob.glob("*.tif"))

arcpy.env.workspace = r"D:\\GCAM\\Landcover\\CLM\\PFT_78\\Tabulated Data\\"
arcpy.env.overwriteOutput = True
# Folder for excel files
Excel_Folder = r"D:\\GCAM\\Landcover\\CLM\\PFT_78\\Excel Files\\"

inlayer = r"D:\\GCAM\\Landcover\\CLM\\PFT_78\\Landcover_2008.tif"
zone_field = "Value"
class_field = "Value"
processingCellSize = 30


for tiff in Tiff_files:
    basetfilename = os.path.basename(tiff)
    CleanBaseStr = os.path.splitext(basetfilename)[0]
    OutFileName = f"{CleanBaseStr}.dbf"
    arcpy.sa.TabulateArea(tiff, zone_field, inlayer, class_field, OutFileName, processingCellSize, "CLASSES_AS_FIELDS")
    print(f"Done:{CleanBaseStr}")
