#  L_Feedback.py. (Modified 2022-04-15, 8:37 p.m. by godvalve)
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
        self.__navigation_button_css_class = 'launcher-feedback-navigation-button'
        self.__build_content()

    def get_layout_container(self):
        return self.__layout_container

    def __build_content(self):
        content_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)  # Create a box to hold content data
        content_area.get_style_context().add_class(self.__content_container_css_class)  # Connect a CSS class to the box
        content_area.set_hexpand(True)  # Set the box to horizontally expand
        content_area.set_vexpand(True)  # Set the box to vertically expand and take up all remaining space
        self.__layout_container.attach(child=content_area, left=0, top=0, width=1, height=1)  # Attach box to position 0 of the layout grid
        navigation_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)  # Create a box to hold the navigation bar
        navigation_bar.get_style_context().add_class(self.__navigation_bar_css_class)  # Attach a CSS class
        navigation_bar.set_hexpand(True)  # Set the navigation box to horizontally expand
        self.__layout_container.attach(child=navigation_bar, left=0, top=1, width=1, height=1)  # Attach the box to position 1 of the layout grid
        editor_button = Gtk.Button(label="Open Editor")  # Create a button to open the editor
        editor_button.get_style_context().add_class(self.__navigation_button_css_class)  # Attach a CSS class
        load_button = Gtk.Button(label="Load")  # Create a button to load a selected file into the editor
        load_button.get_style_context().add_class(self.__navigation_button_css_class)  # Attach a CSS class
        navigation_bar.pack_end(child=editor_button, expand=False, fill=False, padding=0)  # Add the button to right side of the navigation bar's box
        navigation_bar.pack_end(child=load_button, expand=False, fill=False, padding=0)  # Add the button immediately to the left of the editor button
