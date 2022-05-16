#  L_Reports.py. (Modified 2022-05-15, 3:34 p.m. by Praxis)
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
from ..gui.L_Help_Page import L_Help_Page

class L_Reports:
    def __init__(self, tab_id: str):
        self.__tab_id = tab_id
        self.__add_help_page()
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.__build_content()

    def get_menu_buttons(self):
        return None

    def __add_help_page(self):
        help_page = L_Help_Page(tab_id=self.__tab_id)
        help_page.set_page_title(title="Reports")
        help_page.add_section_title(title="Subtitle", section=1)
        help_page.add_image(image_file="test.png", height=75, section=1)
        help_page.add_text(text="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", section=1)
        help_page.add_link(url="https://github.com/Peace-Robotics-Studio/report-manager/wiki/Obtaining-Data-From-MyEd", link_text="Instructions for exporting student data from MyEd",
                      alt_text="Report Manager Wiki", section=1)

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