#  Settings.py. (Modified 2022-04-15, 7:55 p.m. by godvalve)
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

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
RES_FOLDER = str(Path(THIS_FOLDER).parents[0]) + "/data/"

res_dir = dict(
    ROOT=RES_FOLDER,
    CSS=RES_FOLDER + "css/",
    GUI=RES_FOLDER + "gui/"
)

default_css_class = 'content-area'

launcher_configuration_menu_labels = dict(
    MENU_1="Setup",
    MENU_2="Quick Reports",
    MENU_3="Feedback"
)
default_launcher_menu_tab = "MENU_1"

version_number = "v2022.04.15"
