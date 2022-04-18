#  ABS_Content_Manager.py. (Modified 2022-04-17, 11:46 a.m. by Praxis)
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
from .ABS_Content_Layer import Content_Layer


class Content_Manager(Content_Layer):

    def __init__(self):
        """ Constructor """
        super().__init__()

    @abstractmethod
    def add_layout_container(self, container: Gtk.Container) -> None:
        pass

    @abstractmethod
    def remove_layout_container(self, container: Gtk.Container) -> None:
        pass