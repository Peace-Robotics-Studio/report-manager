#  L_Comments.py. (Modified 2022-05-26, 10:54 p.m. by Praxis)
#  Copyright (c) 2022-2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.
import csv
from collections import defaultdict

import gi
import re
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from ...gui.ABS_Panel import Panel
from ...gui.widgets.Action_Frame import Action_Frame
from ...gui.L_Menu import L_Menu


class L_Comments(Panel):
    def __init__(self, page_id: dict, panel_name: str):
        super().__init__(panel_name=panel_name, page_id=page_id, layout_orientation=Gtk.Orientation.VERTICAL)
        self.__page_id = page_id
        self.__currently_loaded_property = None
        # Add a container to hold the properties menu
        self.__properties_menu_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__properties_menu_container.get_style_context().add_class('test')
        self.__properties_menu_container.set_hexpand(True)
        self.add(self.__properties_menu_container)

        self.menu_button_keys = dict(
            PROPERTY_0={"TYPE": "Text",  # This is a text-based menu
                     "PACK": "Start",  # Buttons are stacked from left to right
                     "LABEL": "Files",  # Name of the menu entry
                     "ACTIVE": True,  # This button is initialized with active styling
                     "INFO": "Recent feedback summary files",  # The tooltip
                     "CONTENT_MANAGER": self},  # The class responsible for loading content when a menu button is clicked
            PROPERTY_1={"TYPE": "Text",
                     "PACK": "Start",
                     "LABEL": "By Grade",
                     "ACTIVE": False,
                     "INFO": "Summary files by grade",
                     "CONTENT_MANAGER": self},
            PROPERTY_2={"TYPE": "Text",
                     "PACK": "Start",
                     "LABEL": "By Teacher",
                     "ACTIVE": False,
                     "INFO": "Summary files by teacher",
                     "CONTENT_MANAGER": self},
            PROPERTY_3={"TYPE": "Text",
                     "PACK": "Start",
                     "LABEL": "By Class",
                     "ACTIVE": False,
                     "INFO": "Summary files by class code",
                     "CONTENT_MANAGER": self},
            PROPERTY_4={"TYPE": "Text",
                     "PACK": "Start",
                     "LABEL": "By Period",
                     "ACTIVE": False,
                     "INFO": "Summary files by date",
                     "CONTENT_MANAGER": self}
        )
        self.__category_menu = L_Menu(id="comments_menu",  # The ID of this menu
                                      parent_id=self.__page_id['PANEL_ID'],  # The panel that this menu belongs to
                                      orientation="horizontal",  # This is a horizontal menu
                                      container_css_class="test",  # The CSS class for the menu container
                                      button_values=self.menu_button_keys,  # The dictionary of keys to be displayed in this menu
                                      align_button_labels="left",  # Aligns all buttons labels left
                                      button_css_class="properties-menu-button",  # CSS class for the menu buttons
                                      content_manager=self,  # This object (L_Comments) will manage content for this menu
                                      message_callback=self.property_clicked,  # Capture click events and coordinate loading widgets into the content area
                                      manage_content=False)  # L_Menu will not load widgets into the content area
        self.__category_menu.pad_menu(css_class="test2")  # Add a box with styling to the end of the menu to complete styling theme
        self.__properties_menu_container.add(self.__category_menu.get_layout_container())

        self.__properties_content_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.__properties_content_container.get_style_context().add_class('test1')
        self.__properties_content_container.set_vexpand(True)
        self.__properties_content_container.set_hexpand(True)
        self.add(self.__properties_content_container)
        self.__display_files()

        # self.__load_report_comments("/home/godvalve/Desktop/report243.csv")

    def property_clicked(self, key):
        match key:
            case "PROPERTY_0":  # Existing Files
                self.__display_files()
            case "PROPERTY_1":  # By Grade
                self.__display_by_grade()
            case "PROPERTY_2":  # By Teacher
                self.__display_by_teacher()
            case "PROPERTY_3":  # By Class
                self.__display_by_class()
            case "PROPERTY_4":  # By Date
                self.__display_by_period()

    def __display_files(self):
        """ PROPERTY_0 """
        files_list = Action_Frame(css_class="files-list-container")
        files_list.register_button(name="add", id="add_file", callback=self.__files_button_clicked, tooltip="Add", active=True)
        files_list.register_button(name="remove", id="remove_file", callback=self.__files_button_clicked, tooltip="Remove", active=False)
        self.display_content(files_list.get_layout_container())

    def __display_by_grade(self):
        """ PROPERTY_1 """
        self.display_content(Gtk.Label(label="Comments by grade."))

    def __display_by_teacher(self):
        """ PROPERTY_2 """
        self.display_content(Gtk.Label(label="Comments by teacher."))

    def __display_by_class(self):
        """ PROPERTY_3 """
        self.display_content(Gtk.Label(label="Comments by class."))

    def __display_by_period(self):
        """ PROPERTY_4 """
        self.display_content(Gtk.Label(label="Comments by period."))

    def __load_report_comments(self, file_name):
        count = 0
        try:
            with open(file_name, mode='r', encoding='utf-8-sig') as fp:  # Open file using utf-8 encoding
                Lines = fp.readlines()
                for line in Lines:
                    count += 1
                    line = re.sub(",,+", ",", line.strip(","))
                    # line = line.strip(",")
                    print("Line {}: {}".format(count, line))

        except Exception as e:
            print(e)
            # ToDo: display message to user in GUI
            print('\033[3;30;43m' + ' Unable to read CSV file! ' + '\033[0m')

    def display_content(self, container: Gtk.Container) -> None:
        if self.__currently_loaded_property is not None:
            self.__properties_content_container.remove(self.__currently_loaded_property)
        self.__properties_content_container.add(container)
        self.__currently_loaded_property = container
        self.__properties_content_container.show_all()

    def __files_button_clicked(self, button, id):
        print(f"{id} clicked")

