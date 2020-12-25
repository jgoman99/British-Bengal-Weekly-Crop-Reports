# #fills district for blanks
import os
import pandas as pd
in_folder = "../Crop_Reports/Bengal Crop Reports OCR Bounds/"

sheets = os.listdir(in_folder)
main_path = in_folder + "calcgzette1912_folder_12.csv"
districts_ordered = pd.read_csv(main_path)

for sheet in sheets:
    path = in_folder + sheet
    df = pd.read_csv(path)

    sum_nan = sum(pd.isna(df.District))
    if (sum_nan > 0) & (sum_nan < len(df)):
        print(u"Path is screwd up:",path)
    elif (sum_nan > 0):
        #print(u"Path is being modified",path)
        df.District = districts_ordered.District[0:len(df.District)]
        df.to_csv(path, index = False)
    else:
        #print(u"path has already been done",path)