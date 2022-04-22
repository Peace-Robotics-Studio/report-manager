#  Table_List.py. (Modified 2022-04-21, 11:03 p.m. by Praxis)
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
from .Form_Button import Form_Button


class Table_List:
    def __init__(self, callback: callable):
        """ Constructor:  """
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.__layout_container.set_vexpand(True)
        self.__layout_container.get_style_context().add_class('table-list-container')
        self.__action_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__action_bar.get_style_context().add_class('action-bar')
        self.__action_bar.set_hexpand(True)
        plus_button = Form_Button(name="plus", callback=callback)
        self.__action_bar.add(plus_button.add())
        minus_button = Form_Button(name="minus", active=False, callback=callback)
        self.__action_bar.add(minus_button.add())
        edit_button = Form_Button(name="edit", active=False, callback=callback)
        self.__action_bar.add(edit_button.add())
        self.__layout_container.add(self.__action_bar)

        list_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        list_container.get_style_context().add_class('table-list-data')
        self.__layout_container.add(list_container)
        list_container.set_hexpand(True)
        list_container.set_vexpand(True)
        instructions = Gtk.Label()
        instructions.set_xalign(0)
        instructions.set_markup("<a href=\"https://github.com/Peace-Robotics-Studio/report-manager/wiki/Feature-Guide\" "
                   "title=\"Report Manager Wiki\">Instructions for exporting student data from MyEd BC</a>")
        instructions.get_style_context().add_class('instructions-link')
        self.__layout_container.add(instructions)

    def get_layout_container(self) -> Gtk.Container:
        """ Public Accessor: Returns Gtk.Container object. """
        return self.__layout_container

    def add_action_items(self):
        """ Accepts a list of button items to be added to the action bar """
        pass