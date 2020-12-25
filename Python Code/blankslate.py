import pandas as pd
import os
import re
import numpy as np
import warnings


### as y increase towwards top of page
### x to right

input_folder = "../Crop_Reports/Bengal Crop Reports OCR/"
output_folder = "../Crop_Reports/Bengal Crop Reports Data/"
manual_df = pd.read_csv("../Crop_Reports/Manual Check Crop Reports/crop_reports_verified_cleaned.csv", index_col=0)

path = "calcgazette1912julysept_folder_13"
data_path = input_folder + path + ".csv"
if not os.path.exists(path):
    # reading data
    df = pd.read_csv(data_path, delimiter=',')
    df.set_index('sort', inplace=True)
    df.word = df.word.fillna("")
    df.word = df.word.str.lower()

    # columns of csv we are creating
    text_list = []
    district_list = []
    image_list = []
    header_list = []

    for imageName in df.image.unique():
        page_df = df[df["image"] == imageName]

        y1_min = min(page_df.y1)
        y3_max = max(page_df.y3)
        x1_min = min(page_df.x1)
        x3_max = max(page_df.x3)
        middle_divider = (y1_min + y3_max) / 2
        # center_divider = (x1_min + x3_max) / 2

        # finds top anchor
        top_anchor = page_df[page_df.word.str.contains("inch")]

        # finds rightmost word between .4 .6 page: temp_df WILL be recycled
        temp_df = page_df[(page_df.x3 > int(top_anchor.x3))]
        temp_df = temp_df[(temp_df.y3 > middle_divider * .8)]
        temp_df = temp_df[(temp_df.y1 < middle_divider * 1.25)]
        is_alpha = [word.isalpha() for word in temp_df.word]
        temp_df = temp_df[is_alpha]
        paragraph_anchor_x1 = min(temp_df.x1)
        paragraph_anchor_x3 = max(temp_df.x3)

        text_df = page_df[(page_df.x3 > int(top_anchor.x3))]
        text_df = text_df[text_df.y3 < int(top_anchor.y1)]

        print(text_df.word)
