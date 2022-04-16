#  L_Feedback.py. (Modified 2022-04-15, 3:03 p.m. by Praxis)
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

class L_Feedback:
    def __init__(self):
        self.__layout_container = Gtk.Grid(column_spacing=0, row_spacing=0)
        self.__content_container_css_class = 'launcher-feedback-content-container'
        self.__navigation_bar_css_class = 'launcher-feedback-navigation-bar'
        self.__build_content()

    def get_layout_container(self):
        return self.__layout_container

    def __build_content(self):
        content_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        content_area.get_style_context().add_class(self.__content_container_css_class)  # Connect a CSS class to the box
        content_area.set_hexpand(True)
        content_area.set_vexpand(True)
        self.__layout_container.attach(child=content_area, left=0, top=0, width=1, height=1)
        navigation_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        navigation_bar.get_style_context().add_class(self.__navigation_bar_css_class)
        # navigation_bar.set_halign(Gtk.Align.END)
        navigation_bar.set_hexpand(True)
        self.__layout_container.attach(child=navigation_bar, left=0, top=1, width=1, height=1)
        editor_button = Gtk.Button(label="Open Editor")
        load_button = Gtk.Button(label="Load")
        navigation_bar.pack_end(child=editor_button, expand=False, fill=False, padding=0)
        navigation_bar.pack_end(child=load_button, expand=False, fill=False, padding=0)

