#  L_Help_Page_Directory.py. (Modified 2022-05-09, 10:39 p.m. by Praxis)
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

from gi.repository import Gtk, GdkPixbuf
from ...Config import *

class L_Help_Page:
    def __init__(self, tab_id: str, panel_id: str = "ROOT"):
        CSS_FORMATTING = dict(
            H1='large-title',
            H2='medium-title',
            H3='small-title',
            TEXT='help-text',
            LINK='help-link'
        )
        self.__help_pages = {}
        self.__layout_container = Gtk.ScrolledWindow()
        self.__layout_container.set_vexpand(True)
        self.scrollable_window_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.__layout_container.add(self.scrollable_window_content)
        label = Gtk.Label()  # Add a label to the box
        label.set_text("Reports Area")  # Set the value of the label text
        label.get_style_context().add_class('label-notification')  # Connect a CSS class to the label
        self.scrollable_window_content.add(label)

        self.simulation()

    def get_menu_buttons(self):
        return None

    def get_layout_container(self):
        return self.__layout_container

    def show_page(self, tab_id: str, panel_id: str):
        # for section in test:
        #     new_section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        #     new_section.set_hexpand(True)
        #     new_section.get_style_context().add_class('help-text-section')
        #     scrollable_window_content.add(new_section)
        #     for text_block in section:
        #         new_label = Gtk.Label()
        #         new_label.set_line_wrap(True)
        #         if text_block[0] == 'LINK':
        #             link_text = text_block[2]
        #             link_href = text_block[1]
        #             link_title = text_block[3]
        #             new_label.set_markup(f"<a href=\"{link_href}\" title=\"{link_title}\">{link_text}</a>")
        #             new_label.get_style_context().add_class(conversion[text_block[0]])
        #             new_label.set_xalign(0)
        #         elif text_block[0] == 'IMAGE':
        #             new_label = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        #             new_label.get_style_context().add_class('help-image-container')
        #             new_label.set_hexpand(True)
        #             label_image = Gtk.Image()
        #             label_image.set_hexpand(True)
        #             label_image.set_halign(Gtk.Align.CENTER)
        #             new_label.add(label_image)
        #             pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
        #                 filename=res_dir['IMAGES'] + text_block[1],
        #                 height=text_block[2],
        #                 width=-1,
        #                 preserve_aspect_ratio=True)
        #             label_image.set_from_pixbuf(pixbuf)
        #         elif text_block[0] == 'H3':
        #             new_label.set_label(text_block[1])
        #             new_label.set_xalign(0)
        #             new_label.get_style_context().add_class(conversion[text_block[0]])
        #         else:
        #             new_label.set_label(text_block[1])
        #             new_label.get_style_context().add_class(conversion[text_block[0]])
        #         new_section.add(new_label)
        pass

    def simulation(self):
        test = [
            [("H2", "Title")],
            [
                ("H3", "Subtitle"),
                ("IMAGE", "test.png", 75),
                ("TEXT",
                 "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                ("LINK", "https://github.com/Peace-Robotics-Studio/report-manager/wiki/Obtaining-Data-From-MyEd", "Instructions for exporting student data from MyEd", "Report Manager Wiki")
            ],
            [
                ("TEXT",
                 "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                ("LINK", "https://github.com/Peace-Robotics-Studio/report-manager/wiki/Obtaining-Data-From-MyEd", "Instructions for exporting student data from MyEd", "Report Manager Wiki")
            ],
            [
                ("TEXT",
                 "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                ("LINK", "https://github.com/Peace-Robotics-Studio/report-manager/wiki/Obtaining-Data-From-MyEd", "Instructions for exporting student data from MyEd", "Report Manager Wiki")
            ]
        ]
        self.add_help_page("MENU_0", "PANEL_0")

    def add_help_page(self, tab_id: str, panel_id: str = "ROOT"):
        self.__help_pages[tab_id] = {panel_id: []}


