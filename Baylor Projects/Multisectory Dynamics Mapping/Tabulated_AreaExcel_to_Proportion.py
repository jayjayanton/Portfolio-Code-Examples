import glob
import os
import numpy as np
from osgeo import osr
import pandas as pd

##########################################################################################################
### Script used to convert tabulated area files into weighted proportion files for each individual PFT ###
##########################################################################################################

Proportion_Tables  = r"D:\\GCAM\\Landcover\\CLM\\PFT_78\\Excel Files\\Weighted Tabulation\\" # Create directory to send the output files to

Final_Tabulated_Values = sorted(glob.glob("*.xlsx"))

for Name in Final_Tabulated_Values:
    basetfilename = os.path.basename(Name)
    CleanBaseStr = os.path.splitext(basetfilename)[0]
    PFT = CleanBaseStr.split('_',-1)[1]
    df = pd.read_excel(Name)

    # Calculate proportion of MSD basemap within tabulated area
    df.iloc[:,6:] = df.iloc[:,6:].div(df["TABULATED AREA"], axis="index")
    df.iloc[:,6:] = df.iloc[:,6:].mul(df['VALUE'], axis = "index")

    # Sum all Pixel Values
    df['VALUE'].iloc[-1] = df['VALUE'].sum()
    df.tail(1).iloc[:,6:] = df.iloc[:,6:].sum()
    df.tail(1).iloc[:,6:] = df.tail(1).iloc[:,6:].div(df['VALUE'].iloc[-1])

    #Dataframe to Excel
    out_xls = f"PFT_{PFT}_weighted_Tabulated_Proportion.xlsx"
    output_file = os.path.join(Proportion_Tables, out_xls)
    df.to_excel(output_file,index=False)

### Append all separate excel files into a master excel file for final weighted proportion ### 

os.chdir(Proportion_Tables)

Cell_Value_Files = sorted(glob.glob("*.xlsx"))

Appended_Table  = r"D:\\GCAM\\Landcover\\CLM\\PFT_78\\Excel Files\\Appended Tabulation\\"

# Create a list with all Cell Values
Cell_Value_Appended_List = []
for Name in Cell_Value_Files:
    basetfilename = os.path.basename(Name)
    CleanBaseStr = os.path.splitext(basetfilename)[0]
    PFT = CleanBaseStr.split('_',-1)[1]
    df = pd.read_excel(Name)

    if df['PIXEL AREA'].all(0):
        select_df = df.iloc[-1:,]
        Cell_Value_Appended_List.append(select_df)

# Merge Dataframe by PFT
Cell_Value_df = pd.DataFrame()
for PFT_file in Cell_Value_Appended_List:
    Cell_Value_df = Cell_Value_df.append(PFT_file, ignore_index=True)

#Sort Values by PFT
Cell_Value_df = Cell_Value_df.sort_values(by='PFT', ascending=True)
# Fill NA Value
Cell_Value_df = Cell_Value_df.loc[:, Cell_Value_df.columns.difference(['OID','VALUE','PIXEL COUNT','PIXEL AREA', 'TABULATED AREA'])].fillna(0)
# Sort Columns of Dataframe
Cell_Value_df = Cell_Value_df.reindex(natsorted(Cell_Value_df.columns), axis=1)
#Dataframe to Excel
out_xls = f"PFT_Appended_Weighted_Proportion.xlsx"
output_file = os.path.join(Appended_Table, out_xls)
Cell_Value_df.to_excel(output_file,index=False)
