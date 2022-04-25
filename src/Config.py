#  Config.py. (Modified 2022-04-23, 11:57 a.m. by Praxis)
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

version_number = "v2022.04.18"
config_file_name = "configuration.json"
config_file_path = res_dir["ROOT"] + "/" + config_file_name
config_data = {}

def load_json_from_file(file_path):
    """ Read in the contents of JSON file """
    with open(file_path) as file:
        return json.load(file)

def save_json_to_file(file_path, json_data):
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

if os.path.isfile(config_file_path):
    config_data = load_json_from_file(config_file_path)
else:
    config_data = {}

