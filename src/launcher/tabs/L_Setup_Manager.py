#  L_Setup_Manager.py. (Modified 2022-04-24, 9:50 p.m. by Praxis)
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
from ..gui.ABS_Content_Manager import Content_Manager
from ..gui.L_Menu import L_Menu
from .setup_options.L_Student_Enrollment import L_Student_Enrollment


class L_Setup_Manager(Content_Manager):
    def __init__(self, parent_window: Gtk.Window, message_callback):
        """ Constructor: Inherits from Content_Manager abstract class """
        super().__init__()
        self.__process_action = message_callback
        self.__content_container_css_class = 'launcher-feedback-content-container'
        self.__navigation_bar_css_class = 'launcher-feedback-navigation-bar'
        self.__navigation_button_css_class = 'launcher-feedback-navigation-button'
        self.__content_options_menu_css_class = 'launcher-feedback-options-menu-container'
        self.__content_options_container_css_class = 'launcher-feedback-options-container'
        self.options_content_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)  # Create a box to hold the options display data
        menu_button_keys = dict(
            MENU_0={"LABEL": "Enrollment", "ACTIVE": True, "CONTENT_MANAGER": L_Student_Enrollment(parent_window=parent_window)},
        )
        self.__category_menu = L_Menu(orientation="vertical",
                                      container_css_class="launcher-feedback-options-menu",
                                      button_values=menu_button_keys,
                                      align_button_labels="left",
                                      button_css_class="launcher-feedback-options-button",
                                      content_manager=self,
                                      message_callback=self.option_clicked)
        self.__build_content()

    def __build_content(self):
        """ Private Initializer: This function composes the feedback tab layout """
        # Create the content area
        content_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)  # Create a box to hold content data
        content_area.get_style_context().add_class(self.__content_container_css_class)  # Connect a CSS class to the box
        content_area.set_hexpand(True)  # Set the box to horizontally expand
        content_area.set_vexpand(True)  # Set the box to vertically expand and take up all remaining space
        super().attach_to_grid(child=content_area, left=0, top=0, width=1, height=1)  # Attach box to position 0 of the layout grid
        # Divide content area into options menu and display area
        # Create options menu area
        options_menu_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)  # Create a box to hold the options menu
        options_menu_area.get_style_context().add_class(self.__content_options_menu_css_class)  # Connect a CSS class to the box
        options_menu_area.set_vexpand(True)
        options_menu_area.add(self.__category_menu.get_layout_container())
        content_area.pack_start(options_menu_area, False, False, 0)
        # Update properties for options in the content area (created in the constructor)
        self.options_content_area.get_style_context().add_class(self.__content_options_container_css_class)  # Connect a CSS class to the box
        self.options_content_area.set_vexpand(True)
        self.options_content_area.set_hexpand(True)
        content_area.pack_start(self.options_content_area, False, True, 0)

    def navigation_pane_button_clicked(self, button) -> None:
        """ Public Processor: This function coordinates menu actions with the GUI_Manager. """
        self.__process_action("editor")

    def option_clicked(self, value):
        # self.__setup_manager.set_state(value)
        print(f"Setup_Manager: option_clicked()")
        # Check if button belongs to active option
        # Remove layout container for active option and load container for key value

    def add_layout_container(self, container: Gtk.Container, state=None) -> None:
        self.options_content_area.add(container)
        container.show_all()

    def remove_layout_container(self, container: Gtk.Container) -> None:
        self.options_content_area.remove(container)
