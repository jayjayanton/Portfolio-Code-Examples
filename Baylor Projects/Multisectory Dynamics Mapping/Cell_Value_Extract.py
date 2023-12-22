import glob
import os
import numpy as np
from osgeo import osr
from osgeo import gdal
import pandas as pd

#################################################################################################################
### Code was used to sort through the range within the PFT and count values found within each pixel type ###
#################################################################################################################

Tif_files = sorted(glob.glob("*.tif"))

Excel_Folder = r"D:\\GCAM\\Landcover\\CLM\\PFT_78\\Excel Files\\Cell Value\\" # Set Excel folder 

for Name in Tif_files:
    basetfilename = os.path.basename(Name)
    CleanBaseStr = os.path.splitext(basetfilename)[0]
    PFT = CleanBaseStr.split('_',-1)[8]

    file = gdal.Open(Name)
    band = file.GetRasterBand(1)
    Cols = file.RasterXSize
    Rows = file.RasterYSize

    data = band.ReadAsArray(0, 0, Cols, Rows).astype(np.int8)

    array = np.array(band.ReadAsArray())
    values = np.unique((array))
    values_list =[]
    pixel_list = []
    for i in (values):
        count = data[data==i]
        pixel_count = len(count)
        unique_values = i
        values_list.append(unique_values)
        pixel_list.append(pixel_count)

        df = pd.DataFrame({"VALUE":values_list, "COUNT":pixel_list})

        df.drop(index=df.index[0], axis=0, inplace=True)

        out_csv = f"PFT_{PFT}_Cell_Value.xlsx"
        output_file = os.path.join(Excel_Folder, out_csv)
        df.to_excel(output_file,index=False)
