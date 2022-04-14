# Settings.py
#
# Copyright 2022 Peace Robotics Studio


import os
from pathlib import Path

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
RES_FOLDER = str(Path(THIS_FOLDER).parents[0]) + "/data/"

res_dir = dict(
    ROOT=RES_FOLDER,
    CSS=RES_FOLDER + "css/",
    GUI=RES_FOLDER + "gui/"
)

default_css_class = 'content-area'

launcher_configuration_menu_labels = [
    "Setup",
    "Quick Reports",
    "Results"
]
default_launcher_configuration_menu = 0     # This number is an index value of launcher_configuration_menu_labels[]
