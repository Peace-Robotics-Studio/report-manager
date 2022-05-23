#  L_Student_Enrollment.py. (Modified 2022-05-22, 10:43 a.m. by Praxis)
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
from ...gui.widgets.Treestore_Frame import Treestore_Frame
from .L_Load_Student_Data import L_Load_Student_Data
from ..L_Help_Manager import L_Help_Manager


class L_Student_Enrollment:
    def __init__(self, page_id: dict, parent_window: Gtk.Window):
        """ Constructor: """

        self.__page_id = page_id  # page_id = {tab_id, panel_id}
        L_Help_Manager.register_panel(panel_name="Enrollment", tab_id=page_id['TAB_ID'], panel_id=page_id['PANEL_ID'])
        self.RAW_DATA = defaultdict(list)
        self.__student_roster_loaded = False
        # Create a container to hold student enrollment data
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.__layout_container.set_hexpand(True)
        self.__layout_container.set_vexpand(True)

        # Create a widget to hold tabular data. Must be created before the Combo_Picker
        self.student_details_list = Treestore_Frame()

        # Add buttons to the action bar of the Display widget
        self.student_details_list.register_button(name="restore", id="TF-restore", callback=self.__button_clicked, tooltip="Restore Defaults", active=False)
        self.student_details_list.register_button(name="save", id="TF-save", callback=self.__button_clicked, tooltip="Save Changes", active=False)

        # Create a widget for selecting CSV files to be displayed in the Table_List
        roster_file_dir = Combo_Picker(label="Student Roster:", css_class="enrollment-combo-picker", parent_window=parent_window, callback=self.__load_student_data)
        self.__layout_container.pack_start(roster_file_dir.get_layout_container(), False, False, 0)
        self.__layout_container.pack_start(self.student_details_list.get_layout_container(), False, True, 0)
        self.__layout_container.show_all()

    def __button_clicked(self, button, id):
        print(f"{id} clicked (Student Enrollment)")

    def get_layout_container(self):
        """ Public Accessor: Returns the main Gtk.Container holding widgets for this class. """
        return self.__layout_container

    def __load_student_data(self, file_name):
        self.RAW_DATA.clear()  # Reset the dictionary to an empty state
        try:
            with open(file_name, mode='r', encoding='utf-8-sig') as csv_file:  # Open file using utf-8 encoding
                csv_reader = csv.DictReader(csv_file)  # Read contents of CSV file
                for line in csv_reader:  # Parse data into dictionary format
                    for key, value in line.items():
                        self.RAW_DATA[key].append(value)
            if L_Load_Student_Data.load_data(self.RAW_DATA):
                # Keep track of whether a list has already been displayed
                if not self.__student_roster_loaded:
                    self.__student_roster_loaded = True
                else:
                    self.student_details_list.reset()
                self.student_details_list.update(data_fields=L_Load_Student_Data.DATA_FIELDS, column_properties=L_Load_Student_Data.COLUMN_PROPERTIES, row_order=L_Load_Student_Data.ROW_ORDER, data=L_Load_Student_Data.FORMATTED_DATA)
            else:
                print("Error loading student data")
        except Exception as e:
            print(e)
            # ToDo: display message to user in GUI
            print('\033[3;30;43m' + ' Unable to read CSV file! ' + '\033[0m')
