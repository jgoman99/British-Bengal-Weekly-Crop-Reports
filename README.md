This repository stores the digitization of weekly crop reports in British Bengal 1894-1936. The directory 
`Crop Reports` contains 293 weeks of crop reports with date and report text by district. `Raw OCR Crop Reports` contains the digitization of 3,474 reports. `File Dates` contains
a crosswalk to add the date to each file in `Raw Ocr Crop Reports`.

The data uploaded is in an unfinished state, as I stopped working on it in October 2020 to work on other projects. This repository is a dump of my data in csv form, while the code used
to construct these datasets is in my private repository. If you would like access to my code, please message me.

Here is what weekly crop reports look like:
![]("Images/crop_report_example_1900")
![]("Images/crop_report_example_1930")

Digitization Pipeline (Note: This was written two months after I stopped working on the project, so it may be slightly off):

1) Download Calcutta Gazette from internet archive e.g. https://archive.org/details/in.ernet.dli.2015.23322
2) I split each gazette (generally a few thousand pages) into several thousand images in pdf form using python
3) I uploaded the several thousand images into a google cloud bucket. Note: Google Cloud buckets do not have folders, so I accounted for that in my code. (I used gsutil for this, as the
pythonic way was not multi-threaded)
4) I then used google cloud vision text recognitions for pdfs on every fourth page to check if that page was a crop report. (I used the pdf version of google text recognition,
as I believed at the time that it was faster than the png version, which I have no idea if this is correct as the documentation was fairly black box at the time) (Every fourth page is not
the most efficient, but I had $220 worth of Google credit to spend in a few weeks, so credit was not the issue)
5) After identifying crop reports, I extracted them, and converted them to png form. Each page was one image.
6) I then ran Google Cloud Vision text recognition for png/other image files on the reports, creating what is in `Raw OCR Crop Reports`.
7) I then used a PyQt GUI to manually verify that each crop report was correct, as well as add the date. The resulting crosswalks are in `File Dates`
8) I then used a PyQt Gui to select blocks of text for each district. The results are seen in `Crop Reports`.

This project was fairly easy to do. Google Cloud Vision's documentation can be a bit hard to decipher, but once you do, it works well. I also wrote several PyQt GUIs to aid in the digitization
process, which was not bad, but did require me to read documentation in Java where Qt is better documented.



