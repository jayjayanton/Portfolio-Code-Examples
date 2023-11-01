from osgeo import gdal
import glob
import os
from osgeo import osr

prefix = 'HDF4_EOS:EOS_GRID:"'
suffix = '":PCT_PFT'

NCfilenames = sorted(glob.glob("*.nc"))
pft_path = f"Enter Directory Here" # PFT Directory

for ncfile in NCfilenames:
    basencfilename = os.path.basename(ncfile)

    PCT_name = f"{prefix}{basencfilename}{suffix}"
   
    CleanBaseStr = os.path.splitext(basencfilename)[0]

    PCT_ds = gdal.Open(PCT_name, gdal.GA_ReadOnly)
    width = PCT_ds.RasterXSize
    height = PCT_ds.RasterYSize

    # Looks at number of raster bands in NC/HDF file
    Count = PCT_ds.RasterCount

    for i in range(Count): # for loop for range of rasterbands

        PCT_band = PCT_ds.GetRasterBand(i) # Extract raster band that is needed
        OutFileName = f"{CleanBaseStr}_WGS84_PFT_{i+1}.tif" #Name of tif file

        output_file = os.path.join(pft_path,OutFileName)

        PCT_arr = PCT_band.ReadAsArray(0,0,width,height)

        # top left x, w-e pixel resolution, rotation, top left y, rotation, n-s pixel resolution
        gt2 = ([-180,0.05,0,90,0,-0.05])
        wkt = PCT_ds.GetProjection()

        driver = gdal.GetDriverByName("GTiff")
        out_ds = driver.Create(output_file, PCT_band.XSize, PCT_band.YSize, 1, gdal.GDT_Int16)

        #writing output raster
        out_ds.GetRasterBand(1).WriteArray(PCT_arr)
        out_ds.GetRasterBand(1).SetNoDataValue(0)

        # setting extent of output raster
        out_ds.SetGeoTransform(gt2)

        # setting spatial reference of output raster
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326)
        out_ds.SetProjection(srs.ExportToWkt())
print('Processing Done')
