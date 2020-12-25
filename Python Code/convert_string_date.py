import pandas as pd
from datetime import datetime

manual_df = pd.read_csv("../Crop_Reports/Manual Check Crop Reports/crop_reports_verified.csv")

# cleans
verified_df = manual_df.dropna()
verified_df = verified_df[verified_df.date != "unknown"]

my_list = []
for row in verified_df["date 2"]:
    row = str(row)
    temp_row = row.split(" ")
    my_list.append(temp_row)

# m d y
my_list_2 = []
for row in my_list:
    if len(row[1]) == 1:
        row[1] = str(0) + str(row[1])
    my_list_2.append(row)

my_list_3 = []
for row in my_list_2:
    row = row[0] + row[1] + row[2]
    my_list_3.append(row)

my_list_4 = []
i = 0
for row in my_list_3:
    i = i + 1
    print(i)
    date = datetime.strptime(row, '%m%d%Y').strftime('%m/%d/%Y')
    my_list_4.append(date)

cleaned_df = pd.DataFrame(list(verified_df.ocr_report_path),my_list_4)
cleaned_df.columns = ["Path"]

cleaned_df.to_csv("../Crop_Reports/Manual Check Crop Reports/crop_reports_verified_cleaned.csv")

#pd.read_csv("../Crop_Reports/Manual Check Crop Reports/crop_reports_verified_cleaned.csv", index_col=0)