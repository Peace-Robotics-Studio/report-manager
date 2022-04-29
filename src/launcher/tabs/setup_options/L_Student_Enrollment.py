#  L_Student_Enrollment.py. (Modified 2022-04-26, 10:37 p.m. by Praxis)
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
from ...gui.widgets.Tabular_Display import Tabular_Display



class L_Student_Enrollment:
    def __init__(self, parent_window: Gtk.Window):
        """ Constructor: """
        self.__student_roster_loaded = False
        self.__parent_window = parent_window  # Required by the Combo_Picker to obtain the updated window coordinates
        self.__student_data = defaultdict(list)  # Holds the contents of the student roster CSV file
        # Create a container to hold student enrollment data
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        # self.__layoutContainer.get_style_context().add_class('')
        self.__layout_container.set_hexpand(True)
        self.__layout_container.set_vexpand(True)
        # # Create a widget to hold tabular data. Must be created before the Combo_Picker
        self.student_details_list = Tabular_Display()
        # # Create a widget for selecting CSV files to be displayed in the Table_List
        roster_file_dir = Combo_Picker(label="Student Roster:", css_class="enrollment-combo-picker", parent_window=self.__parent_window, callback=self.__load_student_data)
        self.__layout_container.pack_start(roster_file_dir.get_layout_container(), False, False, 0)
        self.__layout_container.pack_start(self.student_details_list.get_layout_container(), False, True, 0)
        self.__layout_container.show_all()

    def get_layout_container(self):
        """ Public Accessor: Returns the main Gtk.Container holding widgets for this class. """
        return self.__layout_container

    def __load_student_data(self, file_name):
        """ Private Initializer: Load the contents of the selected CSV file into a dictionary. """
        self.__student_data.clear()  # Reset the dictionary to an empty state
        try:
            with open(file_name, mode='r', encoding='utf-8-sig') as csv_file:  # Open file
                csv_reader = csv.DictReader(csv_file)  # Read contents of CSV file
                for line in csv_reader:  # Parse data into dictionary format
                    for key, value in line.items():
                        self.__student_data[key].append(value)
        except:
            # ToDo: display message to user in GUI
            print("Unable to read CSV file.")

        # Perform some basic checks on the data to ensure it is useable
        if all (field in self.__student_data for field in ("Grade", "Name", "Gender")):  # Make sure the dictionary has these field names as keys
            # Display dictionary data in a Gtk.TreeView
            if not self.__student_roster_loaded:
                self.student_details_list.update(self.__student_data)
                self.__student_roster_loaded = True
            else:
                self.student_details_list.empty()
                self.student_details_list.update(self.__student_data)
        else:
            # ToDo: display message to user in GUI
            print("Student CSV data file does not contain all required fields: 'Grade', 'Name', 'Gender'")

