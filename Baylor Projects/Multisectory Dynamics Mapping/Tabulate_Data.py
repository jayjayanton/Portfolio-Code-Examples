# Note: Found in D:\GCAM\Landcover\CLM\PFT_78\Reexported Raster

import glob
import os
from osgeo import osr
import arcpy
from arcpy.sa import *
from arcpy import env

#######################################################################################################################################
### Predominantly uses the Arcpy tool 'Tabulate Area' to find the area of the MSD basemap for the year 2008 overlayed with all PFTs ###
#######################################################################################################################################

Tiff_files = sorted(glob.glob("*.tif"))

arcpy.env.workspace = r"D:\\GCAM\\Landcover\\CLM\\PFT_78\\Tabulated Data\\"
arcpy.env.overwriteOutput = True
# Folder for excel files
Excel_Folder = r"D:\\GCAM\\Landcover\\CLM\\PFT_78\\Excel Files\\"

inlayer = r"D:\\GCAM\\Landcover\\CLM\\PFT_78\\Landcover_2008.tif" # Add tif file containing Multisector basemap for CONUs for the year 2008
zone_field = "Value"
class_field = "Value"
processingCellSize = 30

for tiff in Tiff_files:
    basetfilename = os.path.basename(tiff)
    CleanBaseStr = os.path.splitext(basetfilename)[0]
    OutFileName = f"{CleanBaseStr}.dbf"
    arcpy.sa.TabulateArea(tiff, zone_field, inlayer, class_field, OutFileName, processingCellSize, "CLASSES_AS_FIELDS")
    print(f"Done:{CleanBaseStr}")

### Converts dbf files into usable excel files ###

os.chdir(arcpy.env.workspace)

Dbf_files = sorted(glob.glob("*.dbf"))

arcpy.env.workspace = r"D:\\GCAM\\Landcover\\CLM\\PFT_78\\Tabulated Data\\"
arcpy.env.overwriteOutput = True

Excel_Folder = r"D:\\GCAM\\Landcover\\CLM\\PFT_78\\Excel Files\\Tabulate Area V_4_19"

for Name in Dbf_files:
    basetfilename = os.path.basename(Name)
    CleanBaseStr = os.path.splitext(basetfilename)[0]
    PFT = CleanBaseStr.split('_',-1)[8]
    out_xls = f"PFT_{PFT}.xlsx"
    output_file = os.path.join(Excel_Folder, out_xls)
    arcpy.conversion.TableToExcel(Name, output_file)
