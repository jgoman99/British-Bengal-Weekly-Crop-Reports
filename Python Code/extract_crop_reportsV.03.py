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

def async_detect_document():
    # imports
    from google.cloud.vision_v1 import enums


    # Set up Vision API
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()
    features = [{"type": enums.Feature.Type.DOCUMENT_TEXT_DETECTION}]
    mime_type = 'application/pdf'

    # from GCP
    gcs_source_uri = "gs://cloud-samples-data/vision/pdf_tiff/census2010.pdf"
    #gcs_source_uri = "../Crop_Reports/Bengal Gazettes/test.pdf"
    #gcs_source_uri = "gs://output_bucket-1/calcutta-may-dec1909.pdf"
    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    input_gcp = vision.types.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

    # send the api request
    pages = [1]  # list of page#s, 5max for online / 2000max for offline/async
    requests = [{"input_config": input_gcp, "features": features, "pages": pages}]
    response = client.batch_annotate_files(requests)
    first_page_response = response.responses[0]
    print(first_page_response.responses[0].full_text_annotation.text)
    print(type(first_page_response))


if __name__ == '__main__':
    async_detect_document()
