#  L_Comments.py. (Modified 2022-05-25, 10:57 p.m. by Praxis)
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
        # Add a container to hold the properties menu
        self.__properties_menu_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.__properties_menu_container.get_style_context().add_class('test')
        self.__properties_menu_container.set_hexpand(True)
        self.add(self.__properties_menu_container)

        # self.menu_button_keys = dict(
        #     PROPERTY_0={"TYPE": "Text",
        #              "PACK": "Start",
        #              "LABEL": "Recent Files",
        #              "ACTIVE": True,
        #              "INFO": "Recent feedback summary files",
        #              "CONTENT_MANAGER": self}
        # )
        # self.__category_menu = L_Menu(id="comments_menu",
        #                               parent_id=self.__page_id['PANEL_ID'],
        #                               orientation="horizontal",
        #                               container_css_class="launcher-feedback-options-menu",
        #                               button_values=self.menu_button_keys,
        #                               align_button_labels="left",
        #                               button_css_class="launcher-feedback-options-button",
        #                               content_manager=self,
        #                               message_callback=self.property_clicked)
        # self.__properties_menu_container.add(self.__category_menu.get_layout_container())

        report_list = Action_Frame()
        report_list.register_button(name="add", id="gender-add", callback=self.button_clicked, tooltip="Add", active=True)
        report_list.register_button(name="remove", id="gender-remove", callback=self.button_clicked, tooltip="Remove", active=False)
        self.add(report_list.get_layout_container())

        # self.RAW_DATA = defaultdict(list)
        self.__load_student_data("/home/godvalve/Desktop/report243.csv")
        # print(self.RAW_DATA)

    def property_clicked(self, button):
        print("click")

    def button_clicked(self, button, id):
        print(f"Button Clicked: {id}")

    def __load_student_data(self, file_name):
        # self.RAW_DATA.clear()  # Reset the dictionary to an empty state
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

    # def add_layout_container(self, container: Gtk.Container, state=None) -> None:
    #     self.options_content_area.add(container)
    #     container.show_all()
    #
    # def remove_layout_container(self, container: Gtk.Container) -> None:
    #     self.options_content_area.remove(container)