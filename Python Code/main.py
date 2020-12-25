# missing gazette splitter and a gsutil command bc of stuff. will fix?

import extract_crop_reports
import match_to_pdf
import pdf_to_png
import ocr_crop_report
import ocr_to_data


def pineapple():
    extract_crop_reports.extract_from_all()
    match_to_pdf.match_all_to_pdf()
    pdf_to_png.convert_all()
    ocr_crop_report.ocr_on_all_png()
    #ocr_to_data.all_reports_to_data()


if __name__ == '__main__':
    pineapple()
