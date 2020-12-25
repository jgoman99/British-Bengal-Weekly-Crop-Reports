# TODO: words are not always in order, will need stictching, add last page, fix little text at bottom adding to last row, remove namn (low prioriet)
# add more explict post fixing (e.g. removing bad reports)
# skips last page for now

# For last page? see if large block text and then remove above? for front page do the same?
import pandas as pd
import os
import re
import numpy as np
import warnings

input_folder = "../Crop_Reports/Bengal Crop Reports OCR/"
output_folder = "../Crop_Reports/Bengal Crop Reports Data/"




def report_to_data(file_name):
    # reading data
    path = os.path.join(input_folder, file_name)
    df = pd.read_csv(path, delimiter=',')
    df.set_index('sort', inplace=True)
    df.word = df.word.astype(str)


    # DOES NOTHING. WILL USE TO SCREEN LATER
    number_fodder = 100
    if (number_fodder > 1):

        # columns of csv we are creating
        text_list = []
        district_list = []
        image_list = []
        header_list = []

        for imageName in df.image.unique():
            page_df = df[df["image"] == imageName]


            # # find date
            # page_y1_min = page_df.y1.min()
            # page_y1_min_df = page_df[page_df.y1 < (page_y1_min+100)]
            # index = [idx for idx, word in enumerate(page_y1_min_df.word) if 'supple' in word][0]
            #
            # index_line = page_y1_min_df[page_y1_min_df.y1 < (page_y1_min_df.iloc[index].y1+5)].word
            # print(index_line)


            # Finds district x,y locations
            # finds divider in middle
            divider = (min(page_df.x1) + max(page_df.x3)) / 2

            # Subset on left of divider (slightly offset to fix page translation problems_
            left_df = page_df[page_df.x3 < (divider - divider / 10)]

            # subset on right of divider
            right_df = page_df[page_df.x3 > (divider - divider / 10)]

            # Subset for at least three letters
            left_df = left_df[[(sum(c.isalpha() for c in word) >= 3) for word in left_df.word]]

            # tries to find district y
            min_row = left_df[left_df.x1 == min(left_df.x1)].iloc[0]

            district_df = left_df.loc[left_df.x1 < int((min_row.x1 + 150)),]

            # merges names that are on next line
            # district_df.loc[district_df.index[i],"word"]
            to_keep = [True] * district_df.shape[0]
            i = 0
            while i < (district_df.shape[0] - 1):
                if district_df.iloc[i + 1].y1 < (district_df.iloc[i].y3 + 100):
                    to_keep[i + 1] = False
                    district_df.loc[district_df.index[i], "word"] = str(district_df.iloc[i].word) + " " + str(
                        district_df.iloc[i + 1].word)
                    i = i + 2
                else:
                    i = i + 1

            district_df = district_df[to_keep]

            # finds numbers to the right of text
            number_df = right_df[[(sum(c.isalpha() for c in word) == 0) for word in right_df.word]]
            min_number_row = number_df[min(number_df.x1) == number_df.x1].iloc[0]

            # Draws y boundaries MAKE ITERATIVE
            i = 0
            while i < district_df.shape[0]:

                # will need correction latet to deal with end of reports:
                if (i == (district_df.shape[0] - 1)):
                    text_df = right_df[(right_df.y3 > int(district_df.y1.iloc[i]))]
                else:
                    text_df = right_df[
                        (right_df.y3 < int(district_df.y1.iloc[i + 1])) & (right_df.y3 > int(district_df.y1.iloc[i]))]

                # draws x boundaries

                text_df = text_df[text_df.x1 > int(min_number_row.x1)]

                # finds header:
                header_list.append(page_df[page_df.y1 < page_df.y1.min() + 20].word.str.cat(sep=" "))
                text_list.append(text_df.word.str.cat(sep=" "))
                district_list.append(district_df.iloc[i].word)
                image_list.append(imageName)

                i = i + 1



        # Writes to csv
        # CHANGE THIS
        output_path = os.path.join(output_folder, file_name) + ".csv"

        if (os.path.exists(output_path)):
            main_results_df = pd.read_csv(output_path, delimiter=',')
            # this may be slow apparently? if it is you can fix
            new_results = pd.DataFrame(
                {'district': district_list,
                 'text': text_list,
                 'header': header_list,
                 'image': image_list,
                 })
            main_results_df = main_results_df.append(new_results)
            main_results_df.to_csv(output_path, index=False)
        else:
            output_df = pd.DataFrame(
                {'district': district_list,
                 'text': text_list,
                 'header': header_list,
                 'image': image_list,
                 })
            output_df.to_csv(output_path, index=False)


def all_reports_to_data():
    files = os.listdir(input_folder)
    print(files)
    for file in files:
        print(file)
        report_to_data(file)

if __name__ == '__main__':
    all_reports_to_data()