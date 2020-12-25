# TODO: words are not always in order, will need stictching
import pandas as pd
import re
import numpy as np
import warnings


input_folder = "../Crop_Reports/Bengal Crop Reports OCR/"
output_folder = "../Crop_Reports/Bengal Crop Reports Data/"

df = pd.read_csv("../Crop_Reports/Bengal Crop Reports OCR/calcutta_5_10_1910.csv", delimiter=',')
df.set_index('sort', inplace=True)
df.word = df.word.astype(str)

#Finds date of crop report (WILL NEED LATER ADJUSTMENT)
# first_page_df = df[df["image"]==df.iloc[0].image]
# loc_for = first_page_df[first_page_df["word"] =="for"].iloc[0][["x1","x3","y1","y3"]]
# loc_week = first_page_df[first_page_df["word"] =="week"].iloc[0][["x1","x3","y1","y3"]]
# loc_ending = first_page_df[first_page_df["word"] =="ending"].iloc[0][["x1","x3","y1","y3"]]
#
# # Quick check
# if max([loc_for.y1, loc_week.y1, loc_ending.y1])-min([loc_for.y1, loc_week.y1, loc_ending.y1]) < 10:
#     print("Good Date Match")
#     match_df = first_page_df[(first_page_df.y1 < loc_ending.y1 + 5) & (first_page_df.y1 > loc_ending.y1 - 5) & (first_page_df.x1 > loc_ending.x1)]
#     # gets rid of extra the
#     match_df = match_df[1:]
#     day = match_df.iloc[0]["word"]
#     month = match_df.iloc[1]["word"]
#     year = match_df.iloc[2]["word"]
# else:
#     print("Bad Date Match")

# columns of csv we are creating
text_list= []
district_list = []
image_list = []

for imageName in df.image.unique():
    page_df = df[df["image"]==imageName]

    # Finds district x,y locations
    #finds divider in middle
    divider = (min(page_df.x1)+max(page_df.x3))/2


    # Subset on left of divider (slightly offset to fix page translation problems_
    left_df = page_df[page_df.x3 < (divider - divider/10)]

    # subset on right of divider
    right_df = page_df[page_df.x3 > (divider - divider/10)]


    # Subset for at least three letters
    left_df = left_df[[(sum(c.isalpha() for c in word) >= 3) for word in left_df.word]]

    # tries to find district y
    min_row = left_df[left_df.x1==min(left_df.x1)].iloc[0]

    district_df = left_df.loc[left_df.x1 < int((min_row.x1 + 150)),]


    # finds numbers to the right of text
    number_df = right_df[[(sum(c.isalpha() for c in word) == 0) for word in right_df.word]]
    min_number_row = number_df[min(number_df.x1)== number_df.x1]

    # Draws y boundaries MAKE ITERATIVE
    i = 0
    while i < district_df.shape[0]:

        # will need correction latet to deal with end of reports:
        if (i == (district_df.shape[0]-1)):
            text_df = right_df[(right_df.y3 > int(district_df.y1.iloc[i]))]
        else:
            text_df = right_df[(right_df.y3 < int(district_df.y1.iloc[i+1])) & (right_df.y3 > int(district_df.y1.iloc[i]))]


        # draws x boundaries
        text_df = text_df[text_df.x1 > int(min_number_row.x3)]

        text_list.append(text_df.word.str.cat(sep=" "))
        district_list.append(district_df.iloc[i].word)
        image_list.append(imageName)

        i = i + 1





# To write codE!
code_list = [0]*len(district_list)






# Writes to csv
# CHANGE THIS
output_path = "../Crop_Reports/Bengal Crop Reports Data/" + "data2.csv"
output_df = pd.DataFrame(
    {'district': district_list,
     'text': text_list,
     'Is Sufficient': code_list,
     'image': image_list,
    })
output_df.to_csv(output_path)








# group into parahraphs! then remove those without fodder?

#Example of what we write TO. District, code we assign, price of staple this week, price of last week, date

# Use 1,23,45,6 at top to mark top?