# Python Imports
import io
import os
import pandas as pd
import re
from os import path

# Gcloud imports
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf import json_format

# TODO Add that it uses _page, so that may cause errors later on?
# Errors may arise from local vs google storage. should look into later
from google.cloud import storage

input_folder = "../Crop_Reports/Bengal Gazettes Chunks/"
match_folder = "../Crop_Reports/Chunks Match List/"
output_folder = "../Crop_Reports/Bengal Crop Reports PDF/"
bucket_name = "calcutta-gazette"


def async_detect_document(gcs_source_uri):
    # imports
    from google.cloud.vision_v1 import enums

    # Set up Vision API
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()
    features = [{"type": enums.Feature.Type.DOCUMENT_TEXT_DETECTION}]
    mime_type = 'application/pdf'

    # from GCP
    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    input_gcp = vision.types.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

    # send the api request
    pages = [1]  # list of page#s, 5max for online / 2000max for offline/async
    requests = [{"input_config": input_gcp, "features": features, "pages": pages}]
    response = client.batch_annotate_files(requests)
    for image_response in response.responses[0].responses:
        temp_text = image_response.full_text_annotation.text.lower()
        points = 0
        points = points + temp_text.count("weather")
        points = points + temp_text.count("seers")
        has_weather_and_crop_report = temp_text.count("weather and crop report")
        has_for_the_week = temp_text.count("for the week ending")
        has_supplement = temp_text.count("supplement")
        # will replace with better screener
        #number_of_fodder = sum(["fodder" in item for item in temp_text.split(" ")])

        print(points)
        print("Has crop report: " + str(has_weather_and_crop_report))
        print("Has for the week: " + str(has_for_the_week))
        print("Has supplement: " + str(has_supplement))
        #print(u"Has matches for fodder", number_of_fodder)

        if (points > 5 & (has_supplement > 0)):
            return (True)
        # print(u"Full text: {}".format(temp_text))


def extract_from_folder(folder):
    write_path = os.path.join(match_folder, folder) + ".csv"
    if not (os.path.exists(write_path)):
        files = os.listdir(os.path.join(input_folder, folder))
        #Puts files in human order
        sort_nicely(files)

        i = 0
        matches = []

        while i < (len(files) - 1):
            file = files[i]
            if not (file in matches):
                link = 'gs://' + bucket_name + "/" + folder + "/" + file
                has_report = async_detect_document(link)

                if has_report:
                    matches.append(files[i])

                    j = i - 1
                    check_left = True
                    while check_left:
                        if ((j < 0) | (files[j] in matches)):
                            check_left = False

                        else:
                            file = files[j]
                            link = 'gs://' + bucket_name + "/" + folder + "/" + file
                            has_report = async_detect_document(link)

                            if has_report:
                                matches.append(files[j])
                                j = j - 1
                            else:
                                check_left = False

                    j = i + 1
                    check_right = True
                    while check_right:
                        if j > (len(files) - 1) | (files[j] in matches):
                            check_right = False

                        else:
                            file = files[j]
                            link = 'gs://' + bucket_name + "/" + folder + "/" + file
                            has_report = async_detect_document(link)

                            if has_report:
                                matches.append(files[j])
                                j = j + 1
                            else:
                                check_right = False

            print(u"matches: ", matches)
            print(u"index: ", i)
            i = i + 4

        output_df = pd.DataFrame({'matches': matches})
        output_df.to_csv(write_path, index=False)



def sort_nicely(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    l.sort(key=alphanum_key)


def extract_from_all():
    folders = os.listdir(input_folder)
    for folder in folders:
        print(u"folder is ", folder)
        extract_from_folder(folder)


if __name__ == '__main__':
    extract_from_all()
