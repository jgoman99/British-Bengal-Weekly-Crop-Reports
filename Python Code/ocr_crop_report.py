# Python Imports
import io
import os
from os import path

# Gcloud imports
from google.cloud import vision
from google.cloud.vision import types


input_folder = "../Crop_Reports/Bengal Crop Reports PNG/"
output_folder = "../Crop_Reports/Bengal Crop Reports OCR/"


def ocr_on_pngs(file_paths, folder):
    # To change
    output_path = os.path.join("../Crop_Reports/Bengal Crop Reports OCR/",folder) + ".csv"

    # Checks if file already has been scanned
    if not os.path.exists(output_path):
        client = vision.ImageAnnotatorClient()

        f = open(output_path, "w")
        f.write("sort,image,word,x1,y1,x2,y2,x3,y3,x4,y4")
        f.close()

        for file_path in file_paths:
            # Tells us which file is being processed
            print(file_path)

            # Loads image
            with io.open(file_path, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)

            # Performs label detection on the image file
            response = client.text_detection(image=image)
            labels = response.text_annotations

            k = 1
            while (k < len(labels)):
                # print(label.description)

                # discards unicode

                # FIX this
                imageString = file_path + ","
                word = '{}'.format(labels[k].description)
                word = word.replace(",","")
                word = word.replace(",","")
                word = word.replace('"',"")
                word = word.replace("'","")
                # removes whitespace
                word = word.strip()
                word = word + ','
                word = (word.encode("ascii", "ignore")).decode("utf-8")

                vertices = (['{},{}'.format(vertex.x, vertex.y)
                             for vertex in labels[k].bounding_poly.vertices])

                toAlsowrite = ('{}'.format(','.join(vertices)))
                f = open(output_path, "a")

                f.write("\n" + str(k - 1) + ",")
                f.write(imageString)
                f.write(word.lower())
                f.write(toAlsowrite)
                f.close()
                k += 1


def ocr_on_all_png():
    folders = os.listdir(input_folder)

    for folder in folders:
        temp_path = os.path.join(input_folder,folder)
        files = os.listdir(temp_path)
        file_paths = [os.path.join(temp_path,file) for file in files]
        ocr_on_pngs(file_paths,folder)



if __name__ == '__main__':
    ocr_on_all_png()
