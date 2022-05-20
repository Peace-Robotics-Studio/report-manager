#  Config.py. (Modified 2022-05-09, 10:36 p.m. by Praxis)
#  Copyright (c) 2021-2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.

import os
from pathlib import Path
import json
import xml.etree.ElementTree as ET

import PyPDF2 as PyPDF2

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
RES_FOLDER = str(Path(THIS_FOLDER).parents[0]) + "/data/"

res_dir = dict(
    ROOT=RES_FOLDER,
    CSS=RES_FOLDER + "css/",
    GUI=RES_FOLDER + "gui/",
    ICONS=RES_FOLDER + "icons/",
    IMAGES=RES_FOLDER + "images/",
    T0P0_IMAGES=RES_FOLDER + "images/tab_0/panel_0/"
)

version_number = "v2022.5.16"
config_file_name = "configuration.json"
config_file_path = res_dir["ROOT"] + "/" + config_file_name
config_data = {}

launcher_help_xml_name = "L_help_pages.xml"
launcher_help_xml_file = res_dir["ROOT"] + "/" + launcher_help_xml_name
help_pages = {}

config_file_locked = False

def load_json_from_file(file_path):
    """ Read in the contents of JSON file """
    with open(file_path) as file:
        return json.load(file)

def save_json_to_file(file_path, json_data):
    if not config_file_locked:
        with open(file_path, 'w') as json_file:
            json.dump(json_data, json_file)

def update_configuration_data():
    save_json_to_file(file_path=config_file_path, json_data=config_data)

def pdf_to_text(filename):
    """ Scraped from https://stackoverflow.blog/2022/04/21/the-robots-are-coming-for-the-boring-parts-of-your-job/?cb=1 """
    pdf = PyPDF2.PdfFileReader(open(filename, "rb"))
    text = ""
    for i in range(pdf.getNumPages()):
        text += pdf.getPage(i).extractText()
    return text

def load_help_xml_file():
    with open(launcher_help_xml_file) as file:
        tree = ET.parse(file)
    root = tree.getroot()  # Get the root element

    """ Parse the contents of XML document and save as dict """
    for tab in root.findall('tab'):  # Generate a list of tabs.
        help_pages[tab.get("id")] = {}  # Create a new dict and set it to the tab's id
        for page in tab.findall('page'):  # Generate a list of pages linked to this tab
            help_pages[tab.get("id")][page.get('id')] = {}  # Create a new dict and set it to the panel's id
            for count, element in enumerate(page):
                # Add element values contained at the 'page_title' level inside the 'page' element
                if element.tag == "section":  # Sections have CSS styling similar to <p></p>
                    # Check to see if the 'section' key has been added for this panel
                    if "section" not in help_pages[tab.get("id")][page.get('id')]:
                        help_pages[tab.get("id")][page.get('id')][element.tag] = {}  # Add the 'section' key and set it to an empty dict
                    # Pages may have more than one section. Differentiate using the count value
                    # Create a new empty dict and set to the count key
                    help_pages[tab.get("id")][page.get('id')][element.tag][count] = {}
                    # Add all elements from the 'section' element to a dict
                    for child_element in element:  # Loop through all elements in 'section'
                        # Clean text of all whitespace characters
                        text = child_element.text  # Grab the text from this child_element element
                        if text is not None:  # Make sure that the element contained text
                            text = " ".join(str(text).split())  # Remove any leading \n, \t, or multiple spaces
                        # Add to the dict
                        help_pages[tab.get("id")][page.get('id')][element.tag][count][child_element.tag] = {"attrib": child_element.attrib, "text": text}
                else:
                    # Create a dict with 'attribute' key and set to the dict of element attributes
                    help_pages[tab.get("id")][page.get('id')][element.tag] = dict(attribute=element.attrib)
                    # Add a 'text' key to this dict and set it to the string contained by the element
                    help_pages[tab.get("id")][page.get('id')][element.tag]["text"] = element.text

# Load the configuration data
if os.path.isfile(config_file_path):  # Make sure the file exists
    file_size = os.stat(config_file_path).st_size
    if file_size != 0:  # Make sure the file is not empty
        try:
            config_data = load_json_from_file(config_file_path)  # Load the contents of the file into a dictionary
        except:
            # ToDo: Present message to user in GUI
            print("Invalid json formatting in config file. Locking file to prevent over-writing contents.")
            config_file_locked = True
            config_data = {}
    else:
        config_data = {}
else:
    config_data = {}

if os.path.isfile(launcher_help_xml_file):  # Make sure the file exists
    file_size = os.stat(launcher_help_xml_file).st_size
    if file_size != 0:  # Make sure the file is not empty
        try:
            load_help_xml_file()  # Load the contents of the file into a dictionary
        except:
            # ToDo: Present message to user in GUI
            print("Unable to load help_pages XML file.")
else:
    print("No XML file (Config.py)")



