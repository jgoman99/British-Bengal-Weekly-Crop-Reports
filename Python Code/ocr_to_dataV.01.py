# TODO Rough code written to show proof of concept. will need rewrite?
# Cleaning will be neccessary
import pandas as pd

input_folder = "../Crop_Reports/Bengal Crop Reports OCR/"
output_folder = "../Crop_Reports/Bengal Crop Reports Data/"

df = pd.read_csv("../Crop_Reports/Bengal Crop Reports OCR/calcutta_5_10_1910.csv", delimiter=',')

#Finds date of crop report (WILL NEED LATER ADJUSTMENT)
first_page_df = df[df["image"]==df.iloc[0].image]
loc_for = first_page_df[first_page_df["word"] =="for"].iloc[0][["x1","x3","y1","y3"]]
loc_week = first_page_df[first_page_df["word"] =="week"].iloc[0][["x1","x3","y1","y3"]]
loc_ending = first_page_df[first_page_df["word"] =="ending"].iloc[0][["x1","x3","y1","y3"]]

# Quick check
if max([loc_for.y1, loc_week.y1, loc_ending.y1])-min([loc_for.y1, loc_week.y1, loc_ending.y1]) < 10:
    print("Good Date Match")
    match_df = first_page_df[(first_page_df.y1 < loc_ending.y1 + 5) & (first_page_df.y1 > loc_ending.y1 - 5) & (first_page_df.x1 > loc_ending.x1)]
    # gets rid of extra the
    match_df = match_df[1:]
    day = match_df.iloc[0]["word"]
    month = match_df.iloc[1]["word"]
    year = match_df.iloc[2]["word"]
else:
    print("Bad Date Match")

# columns of csv we are creating
text = []
district = []
image_list = []

for imageName in df.image.unique():
    page_df = df[df["image"]==imageName]
    fodder_df = page_df[page_df["word"] == "fodder"]
    index = 0

    #sets image_list
    # This is probably bad practice
    k = 0
    while k < fodder_df.shape[0]:
        image_list.append(imageName)
        k = k +1

    while index < fodder_df.shape[0]:
        start_word = fodder_df.iloc[index]

        index = index + 1

        # bounds
        bound = 100
        bound_side = 200

        # Below bounds
        multiple_below = 1
        while True:
            bool_exists = page_df[(page_df.y3 > start_word.y3 + bound * (multiple_below - 1)) & (
                        page_df.y3 < start_word.y3 + bound * multiple_below) & (page_df.x1 > start_word.x1 - bound_side)
                                  & (page_df.x3 < start_word.x1 + bound_side)].word
            if (len(bool_exists) < 1):
                break
            multiple_below = multiple_below + 1

        # Above bounds
        multiple_above = 1
        while True:
            bool_exists = page_df[(page_df.y1 > start_word.y1 - bound * (multiple_above)) &
                                  (page_df.y1 < start_word.y1 - bound * (multiple_above - 1)) & (
                                              page_df.x1 > start_word.x1 - bound_side)
                                  & (page_df.x3 < start_word.x3 + bound_side)].word
            if (len(bool_exists) < 1):
                break
            multiple_above = multiple_above + 1

        # Right Bounds
        multiple_right = 1
        while True:
            bool_exists = page_df[(page_df.y1 > start_word.y1 - bound) & (page_df.y3 < start_word.y3 + bound) &
                                  (page_df.x3 < start_word.x3 + bound_side * (multiple_right)) &
                                  (page_df.x3 > start_word.x3 + bound_side * (multiple_right - 1))]
            if (len(bool_exists) < 1):
                break
            multiple_right = multiple_right + 1

        # Left Bounds
        multiple_left = 1
        while True:
            bool_exists = page_df[(page_df.y1 > start_word.y1 - bound) & (page_df.y3 < start_word.y3 + bound) &
                                  (page_df.x1 < start_word.x1 - bound_side * (multiple_left - 1)) &
                                  (page_df.x1 > start_word.x1 - bound_side * (multiple_left))]
            if (len(bool_exists) < 1):
                break
            multiple_left = multiple_left + 1

        # Result Text
        result_text = page_df[(page_df.y1 > start_word.y1 - bound * multiple_above) & (
                    page_df.y3 < start_word.y3 + bound * multiple_below) &
                              (page_df.x1 > start_word.x1 - bound_side * multiple_left) & (
                                          page_df.x3 < start_word.x3 + bound_side * multiple_right)]

        # Finds district (definitely needs improvement)
        dist_name_df = page_df[(page_df.y1 > start_word.y1 - bound * multiple_above) & (
                    page_df.y3 < start_word.y3 + bound * multiple_below)]
        while True:
            dist_name = dist_name_df[dist_name_df.x1==min(dist_name_df.x1)].iloc[0].word
            if (len(dist_name) < 4):
                # This is a bit sloppy, since it could remove multiple words. However, since thats fine in this case. yay!
                dist_name_df = dist_name_df[dist_name_df.word!=dist_name_df[dist_name_df.x1==min(dist_name_df.x1)].iloc[0].word]
            else:
                break




        # Saves result text
        text.append(result_text.word.str.cat(sep = " "))
        district.append(dist_name)

# Here we look for the code:
code = ["sufficient" in x for x in text]


# Writes to csv
# CHANGE THIS
output_path = "../Crop_Reports/Bengal Crop Reports Data/" + "data2.csv"
output_df = pd.DataFrame(
    {'district': district,
     'text': text,
     'Is Sufficient': code,
     'image': image_list,
    })
output_df.to_csv(output_path)








# group into parahraphs! then remove those without fodder?

#Example of what we write TO. District, code we assign, price of staple this week, price of last week, date

# Use 1,23,45,6 at top to mark top?