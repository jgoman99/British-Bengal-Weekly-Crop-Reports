import os
from PyPDF2 import PdfFileReader, PdfFileWriter


input_folder = "../Crop_Reports/Bengal Gazettes/"
output_folder = "../Crop_Reports/Bengal Gazettes Chunks/"

# Wow was fast this time
def split_document(file_name,file_names_no_extension):

    write_folder = os.path.join(output_folder, file_names_no_extension) + "/"

    # Checks if the folder has already been converted
    if not os.path.exists(write_folder):
        os.makedirs(write_folder)

        #moved here to save on memory
        pdf_path = os.path.join(input_folder, file_name)
        pdf = PdfFileReader(pdf_path)

        for page in range(pdf.getNumPages()):
            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(page))

            output_filename = '{}_page_{}.pdf'.format(file_names_no_extension, page + 1)

            with open(os.path.join(write_folder, output_filename), 'wb') as out:
                pdf_writer.write(out)

            print('Created: {}'.format(output_filename))

def split_all_documents():
    file_list = os.listdir(input_folder)


    for file_name in file_list:
        file_names_no_extension = file_name.split(".")[0]
        split_document(file_name,file_names_no_extension)

if __name__ == '__main__':
    split_all_documents()