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
