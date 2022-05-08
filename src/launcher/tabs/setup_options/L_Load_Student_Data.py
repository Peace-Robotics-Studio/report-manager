#  L_Load_Student_Data.py. (Modified 2022-05-07, 2:14 p.m. by Praxis)
#  Copyright (c) 2021-2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.


class L_Load_Student_Data:
    FORMATTED_DATA = None
    RAW_DATA = None
    ROW_ORDER = None
    COLUMN_PROPERTIES = None
    DATA_FIELDS = None
    REGISTERED_CALLBACKS = []

    @classmethod
    def format_data(cls, data) -> dict:
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

    @classmethod
    def register_callback(cls, callback: callable):
        cls.REGISTERED_CALLBACKS.append(callback)

    @classmethod
    def broadcast_update(cls):
        for callback in cls.REGISTERED_CALLBACKS:
            callback()

    @classmethod
    def load_data(cls, raw_data) -> bool:
        """ Private Initializer: Load the contents of the selected CSV file into a dictionary. """
        cls.RAW_DATA = raw_data

        # Perform some basic checks on the data to ensure it is usable
        if all(field in cls.RAW_DATA for field in ("Grade", "Name", "Gender")):  # Make sure the dictionary has these field names as keys

            # Display dictionary data in a Gtk.TreeView
            cls.DATA_FIELDS = list(cls.RAW_DATA.keys())  # Get a list of all keys in the data dict
            cls.DATA_FIELDS.remove("Grade")  # Remove the 'Grade' field since it will be used as a top-level category

            # Format the data into a usable dictionary format
            # Here, usable means sorting the data by a chosen field key (in this case, 'Grade') in preparation for using the grade
            # value as a top-level row heading.
            cls.FORMATTED_DATA = cls.format_data(cls.RAW_DATA)

            # Establish display order of top-level rows
            sorted_keys = sorted(cls.FORMATTED_DATA.keys())  # Sort grade keys in ascending order
            # The sorted() function places numerical values before alphabetical values, so move Kindergarten to the front of the list
            if 'KF' in sorted_keys:  # Make sure that Kindergarten ('KF') is in the list
                sorted_keys.remove('KF')  # Remove kindergarten from the sorted list of keys
                sorted_keys = ['KF'] + sorted_keys  # Add KF to the front of the sorted list

            # Create a label for each top-level row. Rows will be displayed in the order that they appear in the row_order list
            cls.ROW_ORDER = {}
            for key in sorted_keys:
                if key == 'KF':
                    cls.ROW_ORDER[key] = f"Kindergarten ({len(cls.FORMATTED_DATA[key])})"
                else:
                    cls.ROW_ORDER[key] = f"Grade {key[1] if key.startswith('0') else key} ({len(cls.FORMATTED_DATA[key])})"  # Strip any leading '0' from the key

            # Set the order of visible columns. Only columns in this dict will be visible
            cls.COLUMN_PROPERTIES = {"Name": {"renderer": "static-text", "searchable": True}}
            if 'Usual' in cls.DATA_FIELDS:
                cls.COLUMN_PROPERTIES["Usual"] = {"renderer": "editable-text", "searchable": False}
            cls.COLUMN_PROPERTIES["Gender"] = {"renderer": "static-text", "searchable": False}
            if 'Identity' in cls.DATA_FIELDS:
                cls.COLUMN_PROPERTIES["Identity"] = {"renderer": "selectable", "options": ["M", "F"], "searchable": False}
            if 'Status' in cls.DATA_FIELDS:
                cls.COLUMN_PROPERTIES["Status"] = {"renderer": "static-text", "searchable": True}

            cls.broadcast_update()
            return True
        else:
            # ToDo: display message to user in GUI
            print("Student CSV data file does not contain all required fields: 'Grade', 'Name', 'Gender'")
            return False
