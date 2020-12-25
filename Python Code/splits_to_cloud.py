from google.cloud import storage
import os

input_folder = "../Crop_Reports/Bengal Gazettes Chunks/"

bucket_name = "calcutta-gazette"


def explicit(bucket_name, source_name, path):

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json('../API_Keys/Famine Research OCR-cdf9018b001d.json')

    destination_name = source_name

    source_name2 = os.path.join(path, source_name)

    # Make an authenticated API request
    # buckets = list(storage_client.list_buckets())
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_name)
    if not blob.exists():
        blob.upload_from_filename(source_name2)



if __name__ == '__main__':
    folder_list = os.listdir(input_folder)

    for folder in folder_list:
        path = os.path.join(input_folder, folder)
        file_list = os.listdir(path)
        for file in file_list:
            print(file)
            explicit(bucket_name, file, path)
