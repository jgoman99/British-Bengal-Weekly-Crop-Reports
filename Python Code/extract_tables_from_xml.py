from xml.etree import ElementTree as ET
import pandas as pd

def write_table(in_path, top_anchor,bottom_anchor,year,image):
    tree = ET.parse(in_path)
    root = tree.getroot()

    NSMAP = {
        'mw': 'http://www.loc.gov/standards/alto/v3/alto.xsd'
    }
    pass
    all_name_elements = tree.findall('.//mw:TextLine', NSMAP)

    def get_content(element):
        dict_temp = element.getchildren()[0].attrib
        res = {key: dict_temp[key] for key in dict_temp.keys()
               & {'CONTENT'}}

        content = [x for x in res.values()][0]
        return content

    contents = [get_content(x) for x in all_name_elements]

    top_anchors = top_anchor
    bottom_anchors = bottom_anchor

    headers = ["Districts", "Population among which vaccinations were performed", "estimated births",
               "Mortality infants under one year", "Surviving population under one year",
               "Number succesfully vaccinated",
               "Proportion Successfully Vaccinated per 1,000 surviving population",
               "Proportion Successfully Vaccinated per 1,000 surviving population previous year"]

    master_df = pd.DataFrame()
    for i in range(0, len(top_anchors)):
        anchor_top = top_anchors[i]
        anchor_bottom = bottom_anchors[i]

        top_index = contents.index(anchor_top)
        bottom_index = contents.index(anchor_bottom)
        series = pd.Series(contents[top_index:(bottom_index + 1)])
        master_df[headers[i]] = series

    master_df["year"] = year
    master_df["image"] = image

    out_path = "../Other Data/Generated Data/vaccination_bengal_" + year + ".csv"
    master_df.to_csv(out_path)


def get_content(element):
    dict_temp = element.getchildren()[0].attrib
    res = {key: dict_temp[key] for key in dict_temp.keys()
           & {'CONTENT'}}

    content = [x for x in res.values()][0]
    return content

def john_xml(in_path):
    tree = ET.parse(in_path)
    root = tree.getroot()

    NSMAP = {
        'mw': 'http://www.loc.gov/standards/alto/v3/alto.xsd'
    }
    pass
    all_name_elements = tree.findall('.//mw:TextLine', NSMAP)

    contents = [get_content(x) for x in all_name_elements]
    return contents

def subset_xml(contents,anchor):
    start = contents.index(anchor) + 1
    end = len(contents)
    return contents[start:end]

import time
#num = 29
def grab_elements(contents, number):
    out_path = "C:/Users/jgfri/OneDrive/Desktop/Famine Research Project/Other Data/Generated Data/temp/" + str(time.time()) + ".csv"
    my_ser = pd.Series(contents[0:(number-1)])
    my_ser.to_csv(out_path)
    return contents[number:len(contents)]


# "../Other Data/Medical Data/nls-data-indiaPapers/91541450/alto/91541823.34.xml"
#
# contents = john_xml("../Other Data/Medical Data/nls-data-indiaPapers/91541450/alto/91542045.34.xml")
# contents = subset_xml(contents,"Total.")
# contents = subset_xml(contents,"Rs.")
# grab_elements(contents,50)

def extract_funding(path,year):
    num = 52-11
    contents = john_xml(path)
    contents = subset_xml(contents, "Total.")
    contents = subset_xml(contents, "Rs.")

    out_path = "C:/Users/jgfri/OneDrive/Desktop/Famine Research Project/Other Data/Generated Data/district_vaccination_costs_total/" + str(year) + ".csv"
    my_data = pd.DataFrame({'Rs': pd.Series(contents[0:num])})
    image = path
    image_path = image.split("alto")[0] + "image/" + image.split("alto/")[1].split(".")[0] + ".3.jpg"
    my_data["start_year"] = [year]*num
    my_data["Image"] = [image_path] * num

    districts_data = pd.read_csv("../Other Data/Generated Data/district_vaccination_costs_total/1908.csv")
    districts = districts_data["Districts"]
    my_data["Districts"] = districts
    my_data.to_csv(out_path, index = False)

# list_to_extract = ["1006"]
# years = [1906]
# list_full = ["../Other Data/Medical Data/nls-data-indiaPapers/91539671/alto/9154" + x + ".34.xml" for x in list_to_extract]
#
#
# i =0
# while i < len(years):
#     extract_funding(list_full[i],years[i])
#     i = i + 1


#
#

# contents= john_xml("../Other Data/Medical Data/nls-data-indiaPapers/91541450/alto/91543709.34.xml")
# for x in range(2,22):
#     contents = subset_xml(contents, str(x))
#     contents = grab_elements(contents, 29)

