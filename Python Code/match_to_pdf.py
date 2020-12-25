import pandas as pd
import os
from shutil import copyfile
import re

match_folder = "../Crop_Reports/Chunks Match List/"
chunks_folder = "../Crop_Reports/Bengal Gazettes Chunks/"
output_folder = "../Crop_Reports/Bengal Crop Reports PDF/"


def sort_nicely(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    l.sort(key=alphanum_key)

# Throws out singles
def groupSequence(x):
    it = iter(x)
    prev, res = next(it), []

    while prev is not None:
        start = next(it, None)

        if prev + 1 == start:
            res.append(prev)
        elif res:
            yield list(res + [prev])
            res = []
        prev = start

    # Driver program


def match_to_pdf(file_name):
    file_path = os.path.join(match_folder, file_name) + ".csv"
    print(file_path)
    matches = pd.read_csv(file_path)
    matches = matches.matches.to_list()
    sort_nicely(matches)

    # Possible source of future errors if we switch syntax (already sorted from above code)
    indices = [item.split("_")[-1] for item in matches]
    indices = [item.split(".")[0] for item in indices]
    indices = map(int, indices)
    indices = list(map(int, indices))
    if (len(indices)!=0):
        groups = list(groupSequence(indices))

        write_folder = os.path.join(output_folder, file_name) + "/"
        if not os.path.exists(write_folder):
            os.makedirs(write_folder)
            for group in groups:
                sub_folder_number = len(os.listdir(write_folder))
                sub_folder = file_name + "_folder_" + str(sub_folder_number)
                sub_folder_path = os.path.join(write_folder, sub_folder)
                os.makedirs(sub_folder_path)
                for person in group:
                    path = file_name + "_page_" + str(person) + ".pdf"
                    src = os.path.join(chunks_folder, file_name, path)
                    dst = os.path.join(sub_folder_path, path)
                    copyfile(src, dst)

def match_all_to_pdf():
    match_csvs = os.listdir(match_folder)
    match_csvs = [item.split(".")[0] for item in match_csvs]
    for match_csv in match_csvs:
        match_to_pdf(match_csv)


if __name__ == '__main__':
    match_all_to_pdf()
