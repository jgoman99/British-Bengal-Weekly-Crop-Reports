import pandas as pd

main_data = pd.read_csv("../Crop_Reports/Bengal Crop Reports Data/main.csv")

unique_paths = main_data.Path.unique()

master_df = pd.DataFrame()
for path in unique_paths:
    data = main_data[main_data.Path == path]

    raw_ocr_data = pd.read_csv("../Crop_Reports/Bengal Crop Reports OCR/" + path + ".csv")

    cleaned_text = []
    i = 0
    while i < len(data.District):
        bound_text = raw_ocr_data[(raw_ocr_data.x1 > data.x1[i]) & (raw_ocr_data.y1 > data.y1[i]) & (raw_ocr_data.x3 < data.x3[i]) & (raw_ocr_data.y3 < data.y3[i])]
        raw_ocr_data[(raw_ocr_data.x1 > data.x1[i]) & (raw_ocr_data.x3 < data.x3[i]) & (raw_ocr_data.y1 > data.y1[i]) & (raw_ocr_data.y3 < data.y3[i])]
        min_x1 = min(bound_text.x1)
        min_y1 = min(bound_text.y1)





        i += 1
