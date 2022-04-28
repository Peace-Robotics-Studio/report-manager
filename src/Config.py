#  Config.py. (Modified 2022-04-26, 11:19 p.m. by Praxis)
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

import PyPDF2 as PyPDF2

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
RES_FOLDER = str(Path(THIS_FOLDER).parents[0]) + "/data/"

res_dir = dict(
    ROOT=RES_FOLDER,
    CSS=RES_FOLDER + "css/",
    GUI=RES_FOLDER + "gui/",
    ICONS=RES_FOLDER + "icons/",
)

version_number = "v2022.04.26"
config_file_name = "configuration.json"
config_file_path = res_dir["ROOT"] + "/" + config_file_name
config_data = {}

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

# Load the configuration data
if os.path.isfile(config_file_path):  # Make sure the file exists
    file_size = os.stat(config_file_path).st_size
    if file_size != 0:  # Make sure the file is not empty
        try:
            config_data = load_json_from_file(config_file_path)  # Load the contents of the file into anto a dictionary
        except:
            # ToDo: Present message to user in GUI
            print("Invalid json formatting in config file. Locking file to prevent over-writing contents.")
            config_file_locked = True
            config_data = {}
    else:
        config_data = {}
else:
    config_data = {}

