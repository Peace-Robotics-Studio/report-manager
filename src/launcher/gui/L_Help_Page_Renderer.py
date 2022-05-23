#  L_Help_Page_Renderer.py. (Modified 2022-05-22, 12:31 p.m. by Praxis)
#  Copyright (c) 2022-2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.
import os

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk,  GdkPixbuf
from ...Config import res_dir

class L_Help_Page_Renderer:
    CSS_FORMATTING = dict(
        H1='large-title',
        H2='medium-title',
        H3='small-title',
        TEXT='help-text',
        LINK='help-link'
    )
    HELP_PAGES = {}

    def __init__(self):
        self.__layout_container = Gtk.ScrolledWindow()
        self.__layout_container.set_vexpand(True)
        self.scrollable_window_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.__layout_container.add(self.scrollable_window_content)

    def get_layout_container(self):
        return self.__layout_container

    def view_page(self, tab_id: str, panel_id: str):
        print("updating")

    @classmethod
    def add_page(cls, tab_id: str, panel_id: str, page_object: list):
        if tab_id not in cls.HELP_PAGES:
            cls.HELP_PAGES[tab_id] = {}
        cls.HELP_PAGES[tab_id][panel_id] = page_object

    def show_page(self, tab_id: str, panel_id: str):
        # Empty out the scrollable window in preparation for the next help page rendering request
        contents = self.scrollable_window_content.get_children()  # Get all the widgets in the scrollable window
        for widget in contents:  # Loop through the widget list
            widget.destroy()

        if tab_id in self.__class__.HELP_PAGES:
            if panel_id in self.__class__.HELP_PAGES[tab_id]:
                page_data = self.__class__.HELP_PAGES[tab_id][panel_id].get_page_data()  # Returns a list
                for section in page_data:
                    new_section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
                    new_section.set_hexpand(True)
                    new_section.get_style_context().add_class('help-text-section')
                    self.scrollable_window_content.add(new_section)
                    for text_block in section:
                        new_label = Gtk.Label()
                        new_label.set_line_wrap(True)
                        if text_block[0] == 'LINK':
                            link_text = text_block[2]
                            link_href = text_block[1]
                            link_title = text_block[3]
                            new_label.set_markup(f"<a href=\"{link_href}\" title=\"{link_title}\">{link_text}</a>")
                            new_label.get_style_context().add_class(self.CSS_FORMATTING[text_block[0]])
                            new_label.set_xalign(0)
                        elif text_block[0] == 'IMAGE':
                            new_label = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
                            new_label.get_style_context().add_class('help-image-container')
                            new_label.set_hexpand(True)
                            label_image = Gtk.Image()
                            label_image.set_hexpand(True)
                            label_image.set_halign(Gtk.Align.CENTER)
                            new_label.add(label_image)
                            if os.path.isfile(res_dir[text_block[3]] + text_block[1]):
                                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                                    filename=res_dir[text_block[3]] + text_block[1],
                                    height=text_block[2],
                                    width=-1,
                                    preserve_aspect_ratio=True)
                            else:
                                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                                    filename=res_dir['IMAGES'] + "broken.png",
                                    height=30,
                                    width=-1,
                                    preserve_aspect_ratio=True)
                            label_image.set_from_pixbuf(pixbuf)
                        elif text_block[0] == 'H3':
                            new_label.set_label(text_block[1])
                            new_label.set_xalign(0)
                            new_label.get_style_context().add_class(self.CSS_FORMATTING[text_block[0]])
                        elif text_block[0] == 'H2':
                            new_label.set_label(text_block[1])
                            new_label.set_xalign(0.5)
                            new_label.get_style_context().add_class(self.CSS_FORMATTING[text_block[0]])
                        else:
                            new_label.set_label(text_block[1])
                            new_label.get_style_context().add_class(self.CSS_FORMATTING[text_block[0]])
                            new_label.set_xalign(0)
                        new_section.add(new_label)
            else:
                self.add_default_page("Unavailable")
        else:
            self.add_default_page("Unavailable")
        self.scrollable_window_content.show_all()

    def add_default_page(self, title):
        new_section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        new_section.set_hexpand(True)
        new_section.get_style_context().add_class('help-text-section')
        self.scrollable_window_content.add(new_section)
        new_label = Gtk.Label()
        new_label.set_line_wrap(True)
        new_label.set_label(title)
        new_label.set_xalign(0.5)
        new_label.get_style_context().add_class(self.CSS_FORMATTING['H2'])
        new_section.add(new_label)
