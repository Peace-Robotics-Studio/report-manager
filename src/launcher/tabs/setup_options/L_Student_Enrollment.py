#  L_Student_Enrollment.py. (Modified 2022-04-21, 11:03 p.m. by Praxis)
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
import csv
from collections import defaultdict

from gi.repository import Gtk
from ...gui.widgets.Combo_Picker import Combo_Picker
from ...gui.widgets.Table_List import Table_List

class L_Student_Enrollment:
    def __init__(self, parent_window: Gtk.Window):
        self.__student_data = defaultdict(list)
        self.__parent_window = parent_window
        self.__layoutContainer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # self.__layoutContainer.get_style_context().add_class('test')
        self.__layoutContainer.set_hexpand(True)
        self.__layoutContainer.set_vexpand(True)

        roster_file_dir = Combo_Picker(label="Student Roster:", css_class="enrollment-combo-picker", parent_window=self.__parent_window, callback=self.__load_student_data)
        self.__layoutContainer.pack_start(roster_file_dir.get_layout_container(), False, False, 0)
        student_details_list = Table_List(callback=self.button_clicked)
        self.__layoutContainer.pack_start(student_details_list.get_layout_container(), False, True, 0)
        self.__layoutContainer.show_all()

    def get_layout_container(self):
        return self.__layoutContainer

    def button_clicked(self, button, name):
        print(name)

    def __load_student_data(self, file_name):
        print(f"Valid file: {file_name}")
        with open(file_name, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                for key, value in line.items():
                    self.__student_data[key].append(value)
        print(self.__student_data.items())
        print(f"number of categories: {len(self.__student_data)}")
        print(list(self.__student_data))
        print(f"list of all students: {self.__student_data['Name']}")
        print(f"Number of students: {len(self.__student_data['Name'])}")



