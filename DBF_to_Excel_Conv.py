import os
import glob
import numpy as np
import pandas as pd
from simpledbf import Dbf5

##########################
### Set the workspace  ###
##########################

path = r"E:\\TPWD Project\\Climate Variables\\Catchment Zonal Statistics\\ppt_excel\\ppt_excel_raw"

# Path for combined excel files
combined_path =  r'E:\\TPWD Project\\Climate Variables\\Catchment Zonal Statistics\\ppt_excel\\ppt_combined'

############################
### Search for dbf files ###
############################
directory =r"E:\\TPWD Project\\Climate Variables\\Catchment Zonal Statistics\\ppt\\Missing"
os.chdir(directory)
dbf_filenames = sorted(glob.glob("*.dbf"))


for file in dbf_filenames:
    basefilename = os.path.basename(file)

    # Name of File
    CleanBaseStr = os.path.splitext(basefilename)[0]

    # Create Variable for Gage Number
    # Gage = '_'.join(CleanBaseStr.split('_')[1:-1])
    # Create Variable for Year
    yearmonth = CleanBaseStr.split('_',2)[2]
    year = yearmonth[0:4]
    month = yearmonth[4:6]
    # print(yearmonth)
    ### Execute table to excel
    # Name Excel file
    out_xls = f"{CleanBaseStr}.txt"
    # print(out_xls)
    output_file = os.path.join(path,out_xls)
    #
    # # Open dbf files
    new_df = Dbf5(file)
    #
    # # Conver dbf to databframe
    df = new_df.to_dataframe()
    df['Year_Month'] = yearmonth
    df['Year'] = year
    df['Month'] = month
    # print(df)
    # # Save dataframe to excel
    df.to_csv(output_file)

        #######################################
        ## Loop through existing Excel list ###
        #######################################

# Path for excel files
path =  r'E:\\TPWD Project\\Climate Variables\\Catchment Zonal Statistics\\ppt_excel\\ppt_excel_raw'

os.chdir(path)
Excel_files = sorted(glob.glob("*.txt"))
Excel_list = []
#
for file in Excel_files:
    try:
        Excel_list.append(pd.read_csv(file))
    except:
        continue
# print(Excel_list)
# # merged excel file.
excl_merged = pd.DataFrame()

for excel_file in Excel_list:
    excl_merged = excl_merged.append(excel_file, ignore_index=True)

# # Group yearly prism files by Gage number
groupby_gagenum = excl_merged.groupby((excl_merged['Year'].shift() != excl_merged['Year']).cumsum())

for value, gagenum  in groupby_gagenum:
    print(f'[ID: {value}]')
    print(gagenum)
    Gage_Value = gagenum['FEATUREID'].iloc[0]
    print(Gage_Value)

    output_name =(f"ppt_{Gage_Value}.xlsx")
    output_file = os.path.join(combined_path,output_name)
    gagenum.to_excel(output_file, index=False)
