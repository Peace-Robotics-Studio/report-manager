#  L_Reports.py. (Modified 2022-04-16, 1:34 p.m. by Praxis)
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

class L_Reports:
    def __init__(self):
        self.__layoutContainer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.__build_content()

    def get_layout_container(self):
        return self.__layoutContainer

    def __build_content(self):
        label = Gtk.Label()  # Add a label to the box
        label.set_text("Reports Area")  # Set the value of the label text
        label.get_style_context().add_class('label-notification')  # Connect a CSS class to the label
        self.__layoutContainer.add(label)
        button = Gtk.Button()
        button.set_label("Click Me Reports")
        self.__layoutContainer.add(button)