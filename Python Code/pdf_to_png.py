# TODO: Add measure of progress (e.g. how many converted)

input_folder = "../Crop_Reports/Bengal Crop Reports PDF/"
output_folder = "../Crop_Reports/Bengal Crop Reports PNG/"

import os
from pdf2image import convert_from_path

def page_to_png(page_path, write_folder):
    pdf = convert_from_path(page_path, 500)
    write_file_name = page_path.split(".pdf")[0] + ".png"
    #may cause issues in the long run
    write_file_name = write_file_name.split("\\")[-1]
    write_path = os.path.join(write_folder, write_file_name)
    print(write_file_name)
    pdf[0].save(write_path, 'PNG')


def report_to_png(report_folder_path, write_folder):
    pages = os.listdir(report_folder_path)
    for page in pages:
        page_to_png(os.path.join(report_folder_path, page),write_folder)



def folder_to_png(folder_path):
    sub_folders = os.listdir(folder_path)

    for sub_folder in sub_folders:
        write_folder = os.path.join(output_folder, sub_folder)
        if not os.path.exists(write_folder):
            os.makedirs(write_folder)
            report_to_png(os.path.join(folder_path,sub_folder), write_folder)


def convert_all():
    folders = os.listdir(input_folder)
    for folder in folders:
        folder_to_png(os.path.join(input_folder,folder))
    #file_names = [".".join(f.split(".")[:-1]) for f in file_list]


if __name__ == '__main__':
    convert_all()

