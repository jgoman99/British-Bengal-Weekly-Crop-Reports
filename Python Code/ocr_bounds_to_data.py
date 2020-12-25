import os
import pandas as pd
in_folder = "../Crop_Reports/Bengal Crop Reports OCR Bounds/"
out_folder= "../Crop_Reports/Bengal Crop Reports Data/"
out_path = out_folder + "main.csv"

path_df = pd.read_csv("../Crop_Reports/Manual Check Crop Reports/crop_reports_verified_cleaned_is_good.csv")
path_df.Date = pd.to_datetime(path_df.Date)

sheets = os.listdir(in_folder)

master_df = pd.DataFrame()
for sheet in sheets:
    path = in_folder + sheet
    df = pd.read_csv(path)
    df["Path"] = ""

    if len(df.Date) > 0:
        df["Path"] = list(path_df[path_df.Date == df.Date.unique()[0]].Path)[0]
        print(path_df[path_df.Date == df.Date.unique()[0]].Path)


    master_df = master_df.append(df)


# cleaning
master_df.District = master_df.District.str.replace("-", " ")

master_df.to_csv(out_path,index=False)
