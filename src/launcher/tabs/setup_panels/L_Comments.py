#  L_Comments.py. (Modified 2022-05-24, 9:27 p.m. by Praxis)
#  Copyright (c) 2022-2022 Peace Robotics Studio
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
from ..L_Help_Manager import L_Help_Manager


class L_Comments:
    def __init__(self, page_id: dict):
        self.__page_id = page_id
        L_Help_Manager.register_panel(panel_name="Comments", tab_id=page_id['TAB_ID'], panel_id=page_id['PANEL_ID'])
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        label = Gtk.Label()  # Add a label to the box
        label.set_text("Comments")  # Set the value of the label text
        label.get_style_context().add_class('label-notification')  # Connect a CSS class to the label
        self.__layout_container.add(label)

    def get_layout_container(self):
        """ Public Accessor: Returns the main Gtk.Container holding widgets for this class. """
        return self.__layout_container