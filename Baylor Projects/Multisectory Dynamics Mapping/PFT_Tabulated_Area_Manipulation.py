# Note: File found in D:\GCAM\Landcover\CLM\PFT_78\Excel Files

import glob
import os
import numpy as np
from osgeo import osr
import pandas as pd
import math

Tabulated_Area = r"E:\\GCAM Project\\CLM\\Tabulated Data\\Tabulated Excel Folder\\"
Cell_Value = r"D:\\GCAM\\Landcover\\CLM\\PFT_78\\Excel Files\\Cell Value\\"
Finalized_Product = r"E:\\GCAM Project\\CLM\\Tabulated Data\\Final Tabuated Area\\"
Extracted_Row = r"E:\\GCAM Project\\CLM\\Tabulated Data\\Accumulated Sum\\"


### Open Raster Value Excel Files
path = os.chdir(Cell_Value)

Cell_Value_Files = sorted(glob.glob("*.xlsx"))

# Create a list with all Cell Values
Cell_Value_Appended_List = []
for Name in Cell_Value_Files:
    basetfilename = os.path.basename(Name)
    CleanBaseStr = os.path.splitext(basetfilename)[0]
    PFT = CleanBaseStr.split('_',-1)[1]
    df = pd.read_excel(Name)
    df.insert(0,'PFT', PFT )

    # df = df.sort_values(by='PFT', ascending=True)
    Cell_Value_Appended_List.append(df)

# Merge Dataframe by PFT
Cell_Value_df = pd.DataFrame()
for PFT_file in Cell_Value_Appended_List:
    Cell_Value_df = Cell_Value_df.append(PFT_file, ignore_index=True)

# Group Raster Values by PFT
groupby_PFT = Cell_Value_df.groupby((Cell_Value_df['PFT'].shift() != Cell_Value_df['PFT']).cumsum())

### Open Tabulated Area Excel
path = os.chdir(Tabulated_Area)
Tabulated_Files = sorted(glob.glob("*.xlsx"))

Tabulated_Area_Appended_List = []
for Excel in Tabulated_Files:
    basetfilename = os.path.basename(Excel)
    CleanBaseStr = os.path.splitext(basetfilename)[0]
    PFT_Tabulate = CleanBaseStr.split('_',-1)[1]

    # Read Tabulated Area as df
    Tabulated_df = pd.read_excel(Excel)
    Tabulated_df.insert(0,'PFT', PFT_Tabulate )

    # Merge Tabulated Area with Cell Value
    Merged_df = Tabulated_df.merge(Cell_Value_df)

    # Move Pixel Count
    column_to_move = Merged_df.pop("COUNT")
    Merged_df.insert(3, 'PIXEL COUNT', column_to_move)

    # Add Columns for Area
    Merged_df.insert(4, 'PIXEL AREA', '')
    Merged_df["PIXEL AREA"] = Merged_df['PIXEL COUNT'].astype(int)
    square_function = math.pow(5389.06979187904,2)
    Merged_df["PIXEL AREA"] = Merged_df['PIXEL AREA']*square_function
    Merged_df.insert(5, 'TABULATED AREA', Tabulated_df.sum(axis=1))

    #Total sum per column:
    Merged_df.loc['Total',4:] = Merged_df.sum(axis=0)

    #Add PFT Value
    Merged_df.iloc[-1:,0] = PFT_Tabulate

    #Dataframe to Excel
    out_xls = f"PFT_{PFT_Tabulate}_Final_Tabulated.xlsx"
    output_file = os.path.join(Finalized_Product, out_xls)
    Merged_df.to_excel(output_file,index=False)

    # Select Last Row
    Selected_Row = Merged_df.iloc[-1:,]
    out_xls_sums = f"PFT_{PFT_Tabulate}_Sum_Tabulated.xlsx"
    output_sums = os.path.join(Extracted_Row, out_xls_sums)
    Selected_Row.to_excel(output_sums,index=False)

print("Process is Done")
