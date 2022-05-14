#  L_Help_Manager.py. (Modified 2022-05-11, 10:59 p.m. by Praxis)
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
from ..gui.L_Help_Page_Directory import L_Help_Page_Directory
from ...Config import res_dir

from gi.repository import Gtk,  GdkPixbuf

class L_Help_Manager:
    """ This class stores data for an inidividual page """
    RAW_DATA = {
        "MENU_0": {
            "PROPERTIES": {"TITLE": "Setup", "INDEX_TITLE": "Setup"},
            "PANELS": {
                "PANEL_0": {"PROPERTIES": {"TITLE": "Enrollment", "INDEX_TITLE": "Enrollment"}},
                "PANEL_1": {"PROPERTIES": {"TITLE": "Pronouns", "INDEX_TITLE": "Pronouns"}}
            }
        },
        "MENU_1": {
            "PROPERTIES": {"TITLE": "Quick Reports", "INDEX_TITLE": "Quick Reports"},
            "PANELS": {}
        },
        "MENU_2": {
            "PROPERTIES": {"TITLE": "Feedback", "INDEX_TITLE": "Feedback"},
            "PANELS": {
                "PANEL_0": {"PROPERTIES": {"TITLE": "Recent Files", "INDEX_TITLE": "Recent Files"}},
                "PANEL_1": {"PROPERTIES": {"TITLE": "By Grade", "INDEX_TITLE": "By Grade"}},
                "PANEL_2": {"PROPERTIES": {"TITLE": "By Teacher", "INDEX_TITLE": "By Teacher"}},
                "PANEL_3": {"PROPERTIES": {"TITLE": "By Class Code", "INDEX_TITLE": "By Class Code"}},
                "PANEL_4": {"PROPERTIES": {"TITLE": "By Date", "INDEX_TITLE": "By Date"}}
            }
        }
    }

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

    def __init__(self):
        self.__close_help_menu_callback = None
        self.__page_directory = L_Help_Page_Directory()
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

        help_contents.add(widget=self.__page_directory.get_layout_container())





        # test_label = Gtk.Label()
        # test_label.set_markup("<span color='red' size='large'>1</span> 22 \r <span font_family='monospace'>333</span>")



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
        return self.__layout_container

    def set_close_help_callback(self, callback: callable):
        self.__close_help_menu_callback = callback

    def update(self):
        # print(f"Tab: {L_Menu.ACTIVE_TAB}; Panel: {L_Menu.ACTIVE_PANEL}")
        self.__page_directory.show_page(tab_id=L_Menu.ACTIVE_TAB, panel_id=L_Menu.ACTIVE_PANEL)

    def close_button_clicked(self, button):
        self.__close_help_menu_callback()

    @classmethod
    def add_page(cls, ):

