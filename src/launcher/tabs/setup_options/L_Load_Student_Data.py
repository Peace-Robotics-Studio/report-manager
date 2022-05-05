#  L_Student_Enrollment.py. (Modified 2022-05-01, 9:46 p.m. by Praxis)
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


class L_Load_Student_Data:
    FORMATTED_DATA = None
    RAW_DATA = defaultdict(list)

    def __init__(self):
        # self.FORMATTED_DATA = self.__format_data(raw_data)
        self.__student_roster_loaded = False

    def __format_data(self, data) -> dict:
        """ Private task:  """
        grade_groups = {}
        fields_in_data = list(data.keys())
        fields_in_data.remove("Grade")
        for item_number, grade in enumerate(data['Grade'], start=0):
            key = grade
            if key not in grade_groups:
                grade_groups[key] = []
            student_data = []
            for field in fields_in_data:
                student_data.append(data[field][item_number])
            grade_groups[key].append(student_data)
        return grade_groups


    def load_data(self, file_name):
        """ Private Initializer: Load the contents of the selected CSV file into a dictionary. """


        # Perform some basic checks on the data to ensure it is usable
        if all(field in self.RAW_DATA for field in ("Grade", "Name", "Gender")):  # Make sure the dictionary has these field names as keys
            # Display dictionary data in a Gtk.TreeView
            data_fields = list(self.RAW_DATA.keys())  # Get a list of all keys in the data dict
            data_fields.remove("Grade")  # Remove the 'Grade' field since it will be used as a top-level category

            # Format the data into a usable dictionary format
            # Here, usable means sorting the data by a chosen field key (in this case, 'Grade') in preparation for using the grade
            # value as a top-level row heading.
            formatted_data = self.__format_data(self.RAW_DATA)

            # Establish display order of top-level rows
            sorted_keys = sorted(formatted_data.keys())  # Sort grade keys in ascending order
            # The sorted() function places numerical values before alphabetical values, so move Kindergarten to the front of the list
            if 'KF' in sorted_keys:  # Make sure that Kindergarten ('KF') is in the list
                sorted_keys.remove('KF')  # Remove kindergarten from the sorted list of keys
                sorted_keys = ['KF'] + sorted_keys  # Add KF to the front of the sorted list

            # Create a label for each top-level row. Rows will be displayed in the order that they appear in the row_order list
            row_order = {}
            for key in sorted_keys:
                if key == 'KF':
                    row_order[key] = f"Kindergarten ({len(formatted_data[key])})"
                else:
                    row_order[key] = f"Grade {key[1] if key.startswith('0') else key} ({len(formatted_data[key])})"  # Strip any leading '0' from the key

            # Set the order of visible columns. Only columns in this dict will be visible
            column_properties = {"Name": {"renderer": "static-text", "searchable": True}}
            if 'Usual' in data_fields:
                column_properties["Usual"] = {"renderer": "editable-text", "searchable": False}
            column_properties["Gender"] = {"renderer": "static-text", "searchable": False}
            if 'Identity' in data_fields:
                column_properties["Identity"] = {"renderer": "selectable", "options": ["M", "F"], "searchable": False}
            if 'Status' in data_fields:
                column_properties["Status"] = {"renderer": "static-text", "searchable": True}

            # Keep track of whether a list has already been displayed
            if not self.__student_roster_loaded:
                self.__student_roster_loaded = True
            else:
                self.student_details_list.reset()
            self.student_details_list.update(data_fields=data_fields, column_properties=column_properties, row_order=row_order, data=formatted_data)
        else:
            # ToDo: display message to user in GUI
            print("Student CSV data file does not contain all required fields: 'Grade', 'Name', 'Gender'")