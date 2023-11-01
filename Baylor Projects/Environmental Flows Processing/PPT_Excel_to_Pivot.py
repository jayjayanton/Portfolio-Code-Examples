import pandas as pd
import os
import glob
import numpy as np

#############
### Paths ###
#############

# Path for yearly average files
yearly_path =  r'D:\\Prism\\ppt files\\ppt_Yearly'

###################
### Excel Files ###
###################

Excel_files = sorted(glob.glob("*.xlsx"))

for excel in Excel_files:

    # Split name of File
    basefilename = os.path.basename(excel)
    CleanBaseStr = os.path.splitext(basefilename)[0]
    # Gage Number
    Gage = CleanBaseStr.split('_',1)[1]
    # CLimate Variable Name
    Climate_Var = CleanBaseStr.split('_',-1)[0]

    df = pd.read_excel(excel)
    Zonal_Dat = ['MEAN']
    Year_table = pd.pivot_table(df, values=Zonal_Dat, index=['FEATUREID','Year'])

    ##################
    ### Path names ###
    ##################

    # Monthly Averages
    Month_name =(f"{Climate_Var}_{Gage}_Monthly.csv")
    output_file_month = os.path.join(monthly_path,Month_name)
    Month_table.to_csv(output_file_month)

    # Yearly Averages
    Year_name =(f"{Climate_Var}_{Gage}_Yearly.csv")
    output_file_month = os.path.join(yearly_path,Year_name)
    Year_table.to_csv(output_file_month)
