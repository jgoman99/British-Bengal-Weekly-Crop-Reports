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


def page_to_data(page_df):
    try:
        y1_min = int(min(page_df.y1))
        y3_max = int(max(page_df.y3))
        x1_min = int(min(page_df.x1))
        x3_max = int(max(page_df.x3))
        middle_divider = int((y1_min + y3_max) / 2)
        # center_divider = (x1_min + x3_max) / 2

        # finds top anchor
        top_anchor = page_df[page_df.word.str.contains("inch")]
        top_anchor_x3 = int(top_anchor.x3)
        top_anchor_y1 = int(top_anchor.y1)

        # finds rightmost word between .4 .6 page: temp_df WILL be recycled
        temp_df = page_df[(page_df.x3 > top_anchor_x3)]
        temp_df = temp_df[(temp_df.y3 > middle_divider * .8)]
        temp_df = temp_df[(temp_df.y1 < middle_divider * 1.25)]
        is_alpha = [word.isalpha() for word in temp_df.word]
        temp_df = temp_df[is_alpha]
        paragraph_anchor_x1 = int(min(temp_df.x1))
        paragraph_anchor_x3 = int(max(temp_df.x3))

        text_df = page_df[(page_df.x3 > int(top_anchor_x3))]
        text_df = text_df[text_df.y3 < int(top_anchor_y1)]

        return y1_min, y3_max, x1_min, x3_max, middle_divider, top_anchor_x3, top_anchor_y1, paragraph_anchor_x1, paragraph_anchor_x3
    except:
        return None

def report_to_data(path):
    data_path = input_folder + path + ".csv"
    df = pd.read_csv(data_path, delimiter=',')
    df.set_index('sort', inplace=True)
    df.word = df.word.fillna("")
    df.word = df.word.str.lower()

    page_list = []
    pages = list(df.image.unique())
    sort_nicely(pages)
    for imageName in pages:
        page_df = df[df["image"] == imageName]
        page_list.append(page_df)

    return page_list

def sort_nicely( l ):
  """ Sort the given list in the way that humans expect.
  """
  convert = lambda text: int(text) if text.isdigit() else text
  alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
  l.sort( key=alphanum_key )

