#  L_Help_Page.py. (Modified 2022-05-15, 3:30 p.m. by Praxis)
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
from .L_Help_Page_Renderer import L_Help_Page_Renderer

class L_Help_Page:
    def __init__(self, tab_id: str, panel_id: str = "ROOT"):
        self.tab_id = tab_id
        self.panel_id = panel_id
        self.section_index = {}
        L_Help_Page_Renderer.add_page(tab_id=tab_id, panel_id=panel_id, page_object=self)
        self.page_title = None

    def get_page_data(self):
        help_page = []
        if self.page_title is not None:
            help_page.append(self.page_title)
        for key in sorted(self.section_index.keys()):
            help_page.append(self.section_index[key])
        return help_page

    def set_page_title(self, title: str, size: str = "H2"):
        self.page_title = [(size, title)]

    def add_text(self, text: str, section: int = 1):
        if section not in self.section_index:
            self.section_index[section] = []
        self.section_index[section].append(("TEXT", text))

    def add_section_title(self, title: str, section: int = 1, size: str = "H3"):
        # 'H3' is set as a left-aligned subtitle
        # 'H2' is set as a center aligned title
        if section not in self.section_index:
            self.section_index[section] = []
        self.section_index[section].append((size, title))

    def add_image(self, image_file: str, height: int, section: int = 1):
        if section not in self.section_index:
            self.section_index[section] = []
        self.section_index[section].append(("IMAGE", "test.png", 75))

    def add_link(self, url: str, link_text: str, alt_text: str, section: int = 1):
        if section not in self.section_index:
            self.section_index[section] = []
        self.section_index[section].append(("LINK", url, link_text, alt_text))






