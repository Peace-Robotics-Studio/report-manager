#  Table_List.py. (Modified 2022-04-19, 11:05 p.m. by Praxis)
#  Copyright (c) 2022-2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.

import gi
import cairo

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from ....Config import *


class Table_List:
    def __init__(self):
        """ Constructor:  """
        self.layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.__action_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__action_bar.get_style_context().add_class('context-box-container')
        self.__action_bar.set_hexpand(True)

        self.layout_container.add(self.__action_bar)
        list_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        list_container.set_hexpand(True)
        list_container.set_vexpand(True)

    def get_layout_container(self) -> Gtk.Container:
        """ Public Accessor: Returns Gtk.Container object. """
        return self.__layoutContainer

    def add_action_items(self):
        """ Accepts a list of button items to be added to the action bar """
        self.__action_bar