#  L_Menu.py. (Modified 2022-05-15, 10:44 p.m. by Praxis)
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
from .L_Menu_Text_Button import L_Menu_Text_Button
from .L_Menu_Special_Button import L_Menu_Special_Button

class L_Menu:
    ACTIVE_TAB = None  # Active tab in the main navigation menu
    ACTIVE_PANEL = {}  # Active panel in an options menu
    def __init__(self, id: str, orientation: str, container_css_class: str, button_values: dict, button_css_class: str, content_manager: object, message_callback: callable, align_button_labels: str ="default", parent_id: str = None, content_container: Gtk.Container = None):
        """ Constructor """
        self.id = id  # Keep track of the instance of L_Menu. This allows for logic for specific menu instances
        self.parent_id = parent_id
        self.__content_container = content_container
        self.message_callback = message_callback  # Dialog OK | CANCEL messages - Open the editor or quit the application
        self.button_action_callbacks = {}
        self.__content_manager = content_manager
        if orientation.lower() == "horizontal":
            self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            self.__layout_container.set_hexpand(True)
        else:
            self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            self.__layout_container.set_vexpand(True)
        self.__layout_container.get_style_context().add_class(container_css_class)
        self.__menu_button_css_active = 'active-menu-button'
        self.__menu_button_css_inactive = 'inactive-menu-button'
        self.__menu_buttons = {}
        self.__active_tab_key = None

        # Create button objects for all registered buttons
        for id_key in button_values:  # id_key -> Menu_0; Menu_1; etc
            # Create text-label buttons
            if button_values[id_key]["TYPE"] == "Text":  # Regular buttons with a text label that have CSS styling that changes based on active state
                # Create a menu button object and store a reference to the object
                self.__menu_buttons[id_key] = {"BUTTON_OBJECT": L_Menu_Text_Button(key=id_key,
                                                                                   label=button_values[id_key]["LABEL"],
                                                                                   label_alignment=align_button_labels,
                                                                                   style_class=button_css_class,
                                                                                   callback=self.load_menu_request),  # track active menu; sytle buttons; swap display containers; pass event messages; load help pages
                                                # Store a reference to the object that manages content for that button
                                                "CONTENT_MANAGER": button_values[id_key]["CONTENT_MANAGER"]}  # The class instance for displaying content
                # If the button is starts as the active selection after initialization, then style it as the active button
                if button_values[id_key]["ACTIVE"] is True:  # Check to see if the button is set as the default active button after initialization
                    self.track_active_menu(id_key)
                    self.__menu_buttons[id_key]["BUTTON_OBJECT"].set_style_name(self.__menu_button_css_active)
                    self.__load_tab_content(id_key)
                else:
                    self.__menu_buttons[id_key]["BUTTON_OBJECT"].set_style_name(self.__menu_button_css_inactive)
            # Create special buttons
            elif button_values[id_key]["TYPE"] == "Special":  # 'Special' because it does not function like the other navigation buttons
                self.__menu_buttons[id_key] = {"BUTTON_OBJECT": L_Menu_Special_Button(key=id_key,
                                                                                      label=button_values[id_key]["LABEL"],
                                                                                      style_class=button_values[id_key]["STYLE_CLASS"],
                                                                                      active_state=button_values[id_key]["ACTIVE"],
                                                                                      active_class=button_values[id_key]["ACTIVE_CLASS"],
                                                                                      tooltip=button_values[id_key]["TOOLTIP"],
                                                                                      callback=self.load_menu_request),  # track active menu; sytle buttons; swap display containers; pass event messages; load help pages
                                                "CONTENT_MANAGER": button_values[id_key]["CONTENT_MANAGER"]}  # The class instance for the content manager

            # Store the button either at the right or left of the menu bar
            if button_values[id_key]["PACK"] == "Start":  # The default packing order (left) for text-based navigation buttons
                self.__layout_container.pack_start(child=self.__menu_buttons[id_key]["BUTTON_OBJECT"].get_button(), expand=False, fill=False, padding=0)
            else:  # A mechanism for packing special buttons at the end (right) of the navigation bar
                self.__layout_container.pack_end(child=self.__menu_buttons[id_key]["BUTTON_OBJECT"].get_button(), expand=False, fill=False, padding=0)

            # Special button is the only one with an 'ACTION_CALLBACK' key. Button is defined in L_Menu_Layer()
            if "ACTION_CALLBACK" in button_values[id_key]:  # This is used by the special help button ('MENU_3') to call update() in L_HELP_Manager to display a help page
                # Currently the only callback stored in this dict
                self.button_action_callbacks[id_key] = button_values[id_key]["ACTION_CALLBACK"]  # Store the function reference in a local dict

    def get_layout_container(self):
        """ Public Accessor: This function returns the Gtk layout container """
        return self.__layout_container

    def __activate_menu_button(self, key: str):
        """ Private Initializer: This function modifies CSS style attributes for active and inactive menu buttons. """
        if self.__active_tab_key != key:  # Don't style a button that is already active
            self.__menu_buttons[key]["BUTTON_OBJECT"].set_style_name(self.__menu_button_css_active)
            self.__menu_buttons[self.__active_tab_key]["BUTTON_OBJECT"].set_style_name(self.__menu_button_css_inactive)

    def __load_tab_content(self, key: str):
        """ Private Task: Swaps out layout containers in the content layer based on the key of the active menu. """
        if self.__active_tab_key is not None:  # It is only 'None' when first initialized
            # Obtain a reference to the content manager object  for this tab_id and get the Gtk.Container object with content widgets.
            # Remove the container.
            if self.__content_container is None:
                self.__content_manager.remove_layout_container(self.__menu_buttons[self.__active_tab_key]["CONTENT_MANAGER"].get_layout_container())

        # Check to see if the last container to be loaded was the help page container. Display last loaded page instead.
        if self.__active_tab_key == "MENU_3" and self.id == "main_menu":  # Is this is the 'help' button (MENU_3) on the navigation menu (main_menu)
            self.__active_tab_key = self.__class__.ACTIVE_TAB  # Sets the currently active tab_id key to the previously stored tab_id
        else:
            self.__active_tab_key = key  # Help page was not previously shown. Select content using this key.

        # Get the content container connected with this key.
        if self.__content_container is None:
            self.__content_manager.add_layout_container(self.__menu_buttons[self.__active_tab_key]["CONTENT_MANAGER"].get_layout_container())

    def track_active_menu(self, key):
        """ Public Task: Store information about the currently active menus. """
        # Register the current active tab in a class variable.
        if self.id == "main_menu":  # This is a tab menu. 'main_menu' is the id of the navigation menu. Menu items in it are given 'tab_id' values of 'MENU_#'
            if key != "MENU_3":  # Exclude the 'help' menu tab ('Menu_3')
                self.__class__.ACTIVE_TAB = key  # Save the current tab_id key as the active tab
                panel_buttons = self.__menu_buttons[key]["CONTENT_MANAGER"].get_menu_buttons()  # Get a list of any buttons in a secondary menu
                if panel_buttons is None:  # Tabs that don't have a secondary menu
                    self.__class__.ACTIVE_PANEL[self.__class__.ACTIVE_TAB] = 'ROOT'  # Assign a default of 'ROOT' to the active panel for tabs without secondary menus
        else:  # Then this is a secondary panel menu and its IDs follow a 'PANEL_#' naming convention
            # Due to execution order, the panel menus get created before the tab menus. As a consequence, there is no active tab_id at initialization time.
            # The parent_id (this is the tab_id that this panel belongs to) is used as the active_tab value
            self.__class__.ACTIVE_PANEL[self.parent_id] = key

    def help_button_clicked(self):
        """ Callback: Used by the special help button in the 'main_menu' navigation menu. """
        # Either close the help area or show a page. The contents to be loaded is determined by self.__load_tab_content()
        self.load_menu_request("MENU_3")  # 'MENU_3' is the id assigned to the help button

    def load_menu_request(self, key) -> None:
        """ Public Processor: This function coordinates menu actions with the GUI_Manager. """
        self.track_active_menu(key)  # Store values for the currently active id (MENU_# or PANEL_#)
        self.__activate_menu_button(key)  # Set CSS class attributes for active / inactive menu buttons
        self.__load_tab_content(key)  # Swaps out layout containers in the content layer based on the key of the active menu
        self.message_callback(key)  # Passes Dialog OK | CANCEL messages to the top-level window

        # Loads a menu help page if key is MENU_3
        if key in self.button_action_callbacks:  # True if key == MENU_3
            self.button_action_callbacks[key]()  # Calls L_Help_Manager.update()

