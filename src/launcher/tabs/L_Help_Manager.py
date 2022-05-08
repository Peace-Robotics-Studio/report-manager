#  L_Help_Manager.py. (Modified 2022-05-07, 11:18 p.m. by Praxis)
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
from ..gui.L_Menu import L_Menu

from gi.repository import Gtk

class L_Help_Manager:
    def __init__(self):
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)




    def get_layout_container(self):
        return self.__layout_container

    def update(self):
        print(f"Tab: {L_Menu.ACTIVE_TAB}; Panel: {L_Menu.ACTIVE_PANEL}")

