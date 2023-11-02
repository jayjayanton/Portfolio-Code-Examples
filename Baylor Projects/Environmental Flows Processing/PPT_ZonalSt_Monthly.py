import arcpy
import os
import glob
from arcpy.sa import *
from arcpy import env

##################################################################################################################################
### Used an Arcpy script to perform zonal statistics for monthly Precipitation (PPT) rasters on overlapping watershed polygons ###
################################################################################################################################## 

####################
# Set the workspace#
####################

arcpy.env.overwriteOutput=True
arcpy.env.workspace = r'D:\Prism\vpdmax files\vpdmax_Zonal_Statistics_Remaining'

#############################
#Select Layers by Attributes#
#############################

# Create Search cursor to find GAGE_ID
inlayer = r"D:\Prism\Prism Data\Prism Data.gdb\WS_Selected" 

# WS Attribute columnes: OBJECTID, Shape*, GAGE_ID, Area, Shape_Leng, Shape_Length, Shape_Area

#Field we want to work with
field = ['GAGE_ID']

# Search for field within feature layer
with arcpy.da.SearchCursor(inlayer, field) as cursor:
    count = 0

    for row in cursor:
        count +=1

        my_value = row[0]
        outlayer = my_value

        query = "\"GAGE_ID\" = \'" + my_value + "\'"
        arcpy.MakeFeatureLayer_management (inlayer, outlayer)
        selected = arcpy.SelectLayerByAttribute_management(outlayer, "NEW_SELECTION", query)

        #################################
        # Nest for loop Zonal Statistics#
        #################################

        try:
            for gages in selected:
                # print(gages)
                bilfiles = sorted(glob.glob("*.bil"))
                field_2 = 'GAGE_ID'
                selected = [0]

                for bil in bilfiles:
                        basebilname = os.path.basename(bil)
                     
                        CleanBaseStr = os.path.splitext(basebilname)[0][26:32]
        
                        OutFileName = CleanBaseStr
                        # Set the local variables

                        inZoneData = gages
                        zoneField = field_2
                        inValueRaster = basebilname
                        outTable = f"ppt_{my_value}_{OutFileName}.dbf"
                       
                        outZSaT = ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, outTable, "NODATA", "ALL", "CURRENT_SLICE", [90], "AUTO_DETECT")
        except:
            continue
