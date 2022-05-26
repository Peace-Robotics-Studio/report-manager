#  L_Comments.py. (Modified 2022-05-24, 9:27 p.m. by Praxis)
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
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from ...gui.ABS_Panel import Panel
from ...gui.widgets.Action_Frame import Action_Frame


class L_Comments(Panel):
    def __init__(self, page_id: dict, panel_name: str):
        super().__init__(panel_name=panel_name, page_id=page_id, layout_orientation=Gtk.Orientation.VERTICAL)

        report_list = Action_Frame()
        report_list.register_button(name="add", id="gender-add", callback=self.button_clicked, tooltip="Add", active=True)
        report_list.register_button(name="remove", id="gender-remove", callback=self.button_clicked, tooltip="Remove", active=False)
        self.add(report_list.get_layout_container())

        self.RAW_DATA = defaultdict(list)
        self.__load_student_data("/home/godvalve/Downloads/report243.csv")
        print(self.RAW_DATA)

    def button_clicked(self, button, id):
        print(f"Button Clicked: {id}")

    def __load_student_data(self, file_name):
        self.RAW_DATA.clear()  # Reset the dictionary to an empty state
        try:
            with open(file_name, mode='r', encoding='utf-8-sig') as csv_file:  # Open file using utf-8 encoding
                csv_reader = csv.DictReader(csv_file)  # Read contents of CSV file
                for line in csv_reader:  # Parse data into dictionary format
                    for key, value in line.items():
                        self.RAW_DATA[key].append(value)
        except Exception as e:
            print(e)
            # ToDo: display message to user in GUI
            print('\033[3;30;43m' + ' Unable to read CSV file! ' + '\033[0m')