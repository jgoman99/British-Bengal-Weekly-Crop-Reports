# Python Imports
import io
import os
from os import path

# Gcloud imports
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf import json_format

input_folder = "../Crop_Reports/Bengal Gazettes/"
output_folder = "../Crop_Reports/Bengal Crop Reports PDF/"
bucket_name = "calcutta-gazette"

gcs_source_uri = "gs://calcutta-gazette/calcutta_excerpt_at_least_2_crop_reports/calcutta_excerpt_at_least_2_crop_reports.pdf_page_121.pdf"

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

        print(points)
        print("Has crop report: " + str(has_weather_and_crop_report))
        print("Has for the week: " + str(has_for_the_week))
        print("Has supplement: " + str(has_supplement))


        if (points > 5 & (has_supplement > 0)):
            return(True)
        #print(u"Full text: {}".format(temp_text))

def extract_from_all():
    storage_client = storage.Client.from_service_account_json('../API_Keys/Famine Research OCR-cdf9018b001d.json')
    blobs = storage_client.list_blobs(bucket_name)
    for blob in blobs:
        print(blob.name)

if __name__ == '__main__':
    async_detect_document(gcs_source_uri)
