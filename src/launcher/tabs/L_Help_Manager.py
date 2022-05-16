#  L_Help_Manager.py. (Modified 2022-05-15, 10:49 p.m. by Praxis)
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
from ..gui.widgets.Treestore_Frame import Treestore_Frame
from ..gui.L_Help_Page_Renderer import L_Help_Page_Renderer
from ..gui.L_Help_Page import L_Help_Page
from ...Config import res_dir

from gi.repository import Gtk,  GdkPixbuf

class L_Help_Manager:
    FORMATTED_DATA = {
        'MENU_0': [
            ['Enrollment', 'MENU_0.PANEL_0'],
            ['Pronouns', 'MENU_0.PANEL_1'],
        ],
        'MENU_1': [
        ],
        'MENU_2': [
            ['Recent Files', 'MENU_2.PANEL_0'],
            ['By Grade', 'MENU_2.PANEL_1'],
            ['By Teacher', 'MENU_2.PANEL_2'],
            ['By Class Code', 'MENU_2.PANEL_3'],
            ['By Date', 'MENU_2.PANEL_4']
        ]
    }
    ROW_ORDER = {
        'MENU_0': 'Setup', 'MENU_1': 'Quick Reports', 'MENU_2': 'Feedback'
    }

    DATA_FIELDS = ['Title', 'Breadcrumbs']

    COLUMN_PROPERTIES = {"Title": {"renderer": "static-text", "searchable": True}}

    def __init__(self, tab_id: str):
        self.__tab_id = tab_id
        self.__close_help_menu_callback = None
        self.__page_renderer = L_Help_Page_Renderer()
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.__navigation_button_css_class = 'launcher-feedback-navigation-button'

        # Create a box to hold the help topic directory
        help_directory = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        help_directory.get_style_context().add_class('launcher_help_directory')
        help_directory.set_hexpand(True)
        help_directory.set_vexpand(True)
        self.__layout_container.pack_start(help_directory, True, True, 0)
        # Add TreeView to hold a directory of help contents organized by menu tab and panel
        topic_treeview = Treestore_Frame(css_class="launcher_help_directory_treeview")
        topic_treeview.update(data_fields=self.__class__.DATA_FIELDS, column_properties=self.__class__.COLUMN_PROPERTIES, row_order=self.__class__.ROW_ORDER, data=self.__class__.FORMATTED_DATA)
        topic_treeview.set_treeview_expanded(is_expanded=True)
        topic_treeview.hide_column_titles(True)
        help_directory.add(topic_treeview.get_layout_container())
        # Add a box to hold the contents of the help file
        help_contents = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        help_contents.get_style_context().add_class('launcher_help_content')
        help_contents.set_hexpand(True)
        help_contents.set_vexpand(True)
        self.__layout_container.pack_start(help_contents, True, True, 0)

        help_contents.add(widget=self.__page_renderer.get_layout_container())

        action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        action_box.get_style_context().add_class('launcher_help_action_bar')
        help_contents.pack_end(child=action_box, expand=False, fill=False, padding=0)

        button_grid = Gtk.Grid(column_spacing=0, row_spacing=0)
        action_box.pack_end(button_grid, False, False, 0)

        help_close = Gtk.Button(label="Close")
        help_close.get_style_context().add_class(self.__navigation_button_css_class)
        help_close.connect("clicked", self.close_button_clicked)
        button_grid.attach(child=help_close, left=0, top=0, width=1, height=1)

    def get_layout_container(self):
        """ Public Convenience: Returns the layout container for this object. """
        return self.__layout_container

    def set_close_help_callback(self, callback: callable):
        """ Callback Reference: Allows two buttons to trigger the same action (help button and close button) """
        # This function is executed in L_Menu_Layer after the creation of the 'main_menu' navigation menu
        self.__close_help_menu_callback = callback

    def update(self):
        """ Get the page_renderer to display the help page registered to current combination of active tab and panel ids. """
        # Display page for the active tab_id and it's active panel (panel_id is stored in a dict indexed by tab_id
        self.__page_renderer.show_page(tab_id=L_Menu.ACTIVE_TAB, panel_id=L_Menu.ACTIVE_PANEL[L_Menu.ACTIVE_TAB])

    def close_button_clicked(self, button):
        """ Callback: Triggers the toggling logic connected with the help special button in the navigation menu """
        # This function points to L_Menu.help_button_clicked().
        self.__close_help_menu_callback()  # Call the function registered as the callback for the close button in the action bar


