#  L_Menu_Layer.py. (Modified 2022-04-17, 9:51 a.m. by Praxis)
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
from .L_Menu import L_Menu
from ..tabs.L_Setup import L_Setup
from ..tabs.L_Reports import L_Reports
from ..tabs.L_Feedback import L_Feedback
from ...Settings import *


class L_Menu_Layer:

    def __init__(self, launcher_properties, content_manager: object):
        """ Constructor
            h_gui_manager: Handle to GUI_Manager instance,
            launcher_properties: dictionary including width, height, banner_height """
        self.__launcher_properties = launcher_properties
        self.__layout_container = Gtk.Grid(column_spacing=0, row_spacing=0)
        self.__menu_container_css_class = "launcher-menu-container"
        menu_buttons = dict(
            MENU_0={"LABEL": "Setup", "ACTIVE": True, "CONTENT_MANAGER": L_Setup()},
            MENU_1={"LABEL": "Quick Reports", "ACTIVE": False, "CONTENT_MANAGER": L_Reports()},
            MENU_2={"LABEL": "Feedback", "ACTIVE": False, "CONTENT_MANAGER": L_Feedback()}
        )
        self.__category_menu = L_Menu(orientation="horizontal",
                                      container_css_class="launcher-menu-container",
                                      button_values=menu_buttons,
                                      button_css_class="launcher-menu-button",
                                      content_manager=content_manager,
                                      message_callback=self.message_callback)
        self.__build_layer()  # Initialize layout containers

    # Private Methods

    def __build_layer(self) -> None:
        """ Private Initializer: This function composes the menu layout """
        self.__menu_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__menu_container.add(self.__category_menu.get_layout_container())
        self.__layout_container.attach(child=self.__menu_container, left=0, top=0, width=1, height=1)
        self.__menu_container.set_hexpand(True)
        self.__menu_container.set_vexpand(True)
        self.__menu_container.set_margin_top(self.__launcher_properties['BANNER_HEIGHT'])  # Set the top margin to the height of the banner
        # Set the bottom margin to (window_height - banner_height - button_height)
        self.__menu_container.set_margin_bottom(
            self.__launcher_properties['LAUNCHER_HEIGHT'] - self.__launcher_properties['BANNER_HEIGHT'] -
            self.__launcher_properties['MENU_BUTTON_HEIGHT'])

    # Public Methods

    def get_layout_container(self) -> Gtk.Grid:
        """ Public Accessor: This function returns the Gtk layout container """
        return self.__layout_container

    def message_callback(self, data) -> None:
        """ Public Processor: """
        print(data)





