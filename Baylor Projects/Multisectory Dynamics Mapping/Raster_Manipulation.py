from osgeo import gdal
import glob
import os
import numpy as np
from osgeo import osr
import numpy as np
import arcpy

Tiff_Files = sorted(glob.glob("*.tif"))

arcpy.env.workspace = r"D:\\GCAM\\Landcover\\CLM\\PFT_78\\Projected Raster"

for t_file in Tiff_Files:
    basetfilename = os.path.basename(t_file)
    CleanBaseStr = os.path.splitext(basetfilename)[0]
    PFT = CleanBaseStr.split('_',-1)[7]
    Layer = CleanBaseStr.removesuffix(f"_WGS84_PFT_{PFT}")
    OutFileName = f"{Layer}_NAD83_PFT_{PFT}.tif"

    arcpy.management.ProjectRaster(t_file, OutFileName,"7603.prj"
        , "NEAREST","5389.06979187904", "WGS_1984_(ITRF00)_To_NAD_1983", "#","#","#")

################################################## 
# Information used for the file transformation 
# NAD_1983_Contiguous_USA_Albers.prj            
# WGS_1984_(ITRF00)_To_NAD_1983
# 5389.06979187904
###################################################
os.chdir(arcpy.env.workspace)

# Import Landcover Data for 2008
inlayer = r"D:\\GCAM\\Landcover\\CLM\\PFT_78\\Landcover_2008.tif"

# Create Path for ExtractByMask Layers
Extracted_Layers = "D:\\GCAM\\Landcover\\CLM\\PFT_78\\Reexported Raster\\"
# Set Up RasterAttributeTable
Projected_files = sorted(glob.glob("*.tif"))

for p_files in Projected_files:
    try:
        arcpy.management.BuildRasterAttributeTable(p_files, "Overwrite")
        Extracted_Filename = "Extract_" + p_files
        output_file = os.path.join(Extracted_Layers, Extracted_Filename)
        outExtractByMask = arcpy.sa.ExtractByMask(p_files, inlayer, "INSIDE")
        outExtractByMask.save(output_file)
    except:
        continue
