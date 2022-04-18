#  ABS_Content_Layer.py. (Modified 2022-04-17, 11:46 a.m. by Praxis)
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
from abc import ABC, abstractmethod


class Content_Layer(ABC):

    def __init__(self):
        """ Constructor """
        super().__init__()
        self.__layout_container = Gtk.Grid(column_spacing=0, row_spacing=0)


    def get_layout_container(self) -> Gtk.Container:
        """ Accessor function: returns Gtk layout container """
        return self.__layout_container

    def attach_to_grid(self, child: Gtk.Container, left: int, top: int, width: int, height: int) -> None:
        self.__layout_container.attach(child=child, left=left, top=top, width=width, height=height)
