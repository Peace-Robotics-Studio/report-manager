#  Settings.py. (Modified 2022-04-16, 4:33 p.m. by Praxis)
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

version_number = "v2022.04.15"
