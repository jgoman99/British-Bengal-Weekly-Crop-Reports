import pandas as pd
import os
in_folder = "C:/Users/jgfri/OneDrive/Desktop/Famine Research Project/Crop_Reports/Bengal Crop Reports OCR/"
out_path = "C:/Users/jgfri/OneDrive/Desktop/Famine Research Project/Crop_Reports/Slate/ocr_combined.csv"

words = []
imageNames = []
for filename in os.listdir(in_folder):
    path = in_folder + filename
    data = pd.read_csv(path)
    print(path)
    words.append(data.word.to_list())
    imageNames.append(data.image.to_list())



flat_words = [item for sublist in words for item in sublist]
flat_image = [item for sublist in imageNames for item in sublist]

[i for i, j in enumerate(flat_words) if j == 'small-pox']