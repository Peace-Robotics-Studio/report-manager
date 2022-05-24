#  L_Setup_Manager.py. (Modified 2022-05-23, 8:12 p.m. by Praxis)
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
from .setup_panels.L_Student_Enrollment import L_Student_Enrollment
from .setup_panels.L_Pronouns import L_Pronouns
from .L_Help_Manager import L_Help_Manager


class L_Setup_Manager(Content_Manager):
    """ As per "The Quick Python Book": class doc strings list the available methods along with usage information. """
    def __init__(self, tab_id: str, parent_window: Gtk.Window, message_callback):
        """ Constructor: Inherits from Content_Manager abstract class """
        super().__init__()
        self.__tab_id = tab_id
        L_Help_Manager.register_tab(tab_name='Setup', tab_id=tab_id)
        self.__process_action = message_callback
        self.__content_container_css_class = 'launcher-feedback-content-container'
        self.__navigation_bar_css_class = 'launcher-feedback-navigation-bar'
        self.__navigation_button_css_class = 'launcher-feedback-navigation-button'
        self.__content_options_menu_css_class = 'launcher-feedback-options-menu-container'
        self.__content_options_container_css_class = 'launcher-feedback-options-container'
        self.options_content_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)  # Create a box to hold the options display data
        self.menu_button_keys = dict(
            PANEL_0={"TYPE": "Text",
                    "PACK": "Start",
                    "LABEL": "Enrollment",
                    "ACTIVE": True,
                    "INFO": "Load a CSV file containing student data",
                    "CONTENT_MANAGER": L_Student_Enrollment(page_id={"TAB_ID": self.__tab_id, "PANEL_ID": "PANEL_0"}, parent_window=parent_window)},
            PANEL_1={"TYPE": "Text",
                    "PACK": "Start",
                    "LABEL": "Pronouns",
                    "ACTIVE": False,
                    "INFO": "Manage custom pronouns",
                    "CONTENT_MANAGER": L_Pronouns(page_id={"TAB_ID": self.__tab_id, "PANEL_ID": "PANEL_1"})}
        )
        self.__category_menu = L_Menu(id="setup_menu",
                                      parent_id=tab_id,
                                      orientation="vertical",
                                      container_css_class="launcher-feedback-options-menu",
                                      button_values=self.menu_button_keys,
                                      align_button_labels="left",
                                      button_css_class="launcher-feedback-options-button",
                                      content_manager=self,
                                      message_callback=self.option_clicked)
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

    def get_menu_buttons(self):
        menu_keys = {}
        for key, values in self.menu_button_keys.items():
            menu_keys[key] = values['INFO']
        return menu_keys

    def navigation_pane_button_clicked(self, button) -> None:
        """ Public Processor: This function coordinates menu actions with the GUI_Manager. """
        self.__process_action("editor")

    def option_clicked(self, value):
        pass
        # self.__setup_manager.set_state(value)
        # print(f"Setup_Manager: option_clicked()")
        # Check if button belongs to active option
        # Remove layout container for active option and load container for key value

    def add_layout_container(self, container: Gtk.Container, state=None) -> None:
        self.options_content_area.add(container)
        container.show_all()

    def remove_layout_container(self, container: Gtk.Container) -> None:
        self.options_content_area.remove(container)
