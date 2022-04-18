#  L_Content_Manager.py. (Modified 2022-04-17, 12:14 p.m. by Praxis)
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
from .ABS_Content_Manager import Content_Manager


class L_Content_Manager(Content_Manager):

    def __init__(self, launcher_properties):
        """ Constructor: Inherits from Content_Manager abstract class
            launcher_properties: dictionary including width, height, banner_height """
        super().__init__()
        self.__launcher_properties = launcher_properties
        self.__content_container_css_class = 'launcher-content-container'
        self.__build_layer()

    # Private Methods

    def __build_layer(self) -> None:
        """ Initialization: composes layout of content area """
        self.__content_area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.__content_area.get_style_context().add_class(self.__content_container_css_class)
        self.__content_area.set_margin_top(self.__launcher_properties['BANNER_HEIGHT'] + self.__launcher_properties['MENU_BUTTON_HEIGHT'])  # Set the top margin to the height of the banner + menu bar
        self.__content_area.set_hexpand(True)
        self.__content_area.set_vexpand(True)
        super().attach_to_grid(child=self.__content_area, left=0, top=0, width=1, height=1)

    # Public Methods

    def add_layout_container(self, container: Gtk.Container) -> None:
        self.__content_area.add(container)
        container.show_all()

    def remove_layout_container(self, container: Gtk.Container) -> None:
        self.__content_area.remove(container)
