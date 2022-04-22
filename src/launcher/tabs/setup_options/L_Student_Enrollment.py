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

        button = Gtk.Button("Filter")
        button.connect("clicked", self.filter_names)
        self.__layoutContainer.add(button)

        self.student_details_list = Table_List(callback=self.button_clicked)
        roster_file_dir = Combo_Picker(label="Student Roster:", css_class="enrollment-combo-picker", parent_window=self.__parent_window, callback=self.__load_student_data)
        self.__layoutContainer.pack_start(roster_file_dir.get_layout_container(), False, False, 0)

        self.__layoutContainer.pack_start(self.student_details_list.get_layout_container(), False, True, 0)
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
        # print(self.__student_data.items())
        # print(f"number of categories: {len(self.__student_data)}")
        # print(list(self.__student_data))
        grade_groups = {}
        for item_number, grade in enumerate(self.__student_data['Grade'], start=0):
            if grade not in grade_groups:
                grade_groups[grade] = []
            grade_groups[grade].append([self.__student_data['Name'][item_number], self.__student_data['Gender'][item_number], self.__student_data['EnrStatus'][item_number]])

        # print(sorted(grade_groups.keys()))
        # print(grade_groups['01'])

        # Create the ListStore model
        self.software_liststore = Gtk.ListStore(str, str, str)
        for student in grade_groups['01']:
            self.software_liststore.append(student)
        self.current_filter_language = None

        # Create the filter and set it to use the liststore model
        self.language_filter = self.software_liststore.filter_new()
        # setting the filter function, note that we're not using the
        self.language_filter.set_visible_func(self.language_filter_func)

        # Create the treeview, make it use the filter as a model, and add the columns
        self.treeview = Gtk.TreeView(model=self.language_filter)
        self.treeview.get_style_context().add_class('duh')
        self.treeview.set_headers_visible(False)
        for i in range(len(self.__student_data)-1):
            renderer = Gtk.CellRendererText()
            renderer.set_padding(0, 0)
            column = Gtk.TreeViewColumn(cell_renderer=renderer, text=i)
            self.treeview.append_column(column)

        self.student_details_list.add(self.treeview)

    def language_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if (
            self.current_filter_language is None
            or self.current_filter_language == "None"
        ):
            return True
        else:
            if "Kla" in model[iter][0]:
                return True
            else:
                return False
            # return model[iter][0] == self.current_filter_language

    def filter_names(self, button):
        print("Filter!")
        self.current_filter_language = "Klassen, Crystal"
        self.language_filter.refilter()

