#  L_Reports.py. (Modified 2022-05-09, 10:39 p.m. by Praxis)
#  Copyright (c) 2021-2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from ...Config import *

class L_Reports:
    def __init__(self):
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.__build_content()

    def get_menu_buttons(self):
        return None

    def get_layout_container(self):
        return self.__layout_container

    def __build_content(self):
        label = Gtk.Label()  # Add a label to the box
        label.set_text("Reports Area")  # Set the value of the label text
        label.get_style_context().add_class('label-notification')  # Connect a CSS class to the label
        self.__layout_container.add(label)
        image = Gtk.Image()
        image.set_from_file(res_dir['IMAGES'] + 'test.png')
        self.__layout_container.add(image)