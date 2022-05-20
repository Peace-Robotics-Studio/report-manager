#  L_Pronouns.py. (Modified 2022-05-15, 3:30 p.m. by Praxis)
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

from gi.repository import Gtk
from ...gui.widgets.Treestore_Frame import Treestore_Frame
from ...gui.widgets.Liststore_Frame import Liststore_Frame
from .L_Load_Student_Data import L_Load_Student_Data


class L_Pronouns:
    GENDER_PRONOUNS = [{"Gender": "Male", "Symbol": "M", "Pronouns": ["he", "him", "his"]},
                       {"Gender": "Female", "Symbol": "F", "Pronouns": ["she", "her", "hers"]},
                       {"Gender": "Non-Binary", "Symbol": "NB", "Pronouns": ["they", "<name>", "theirs"]}]

    def __init__(self, page_id: dict):
        self.__page_id = page_id
        self.__layout_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.__showing_student_list = False
        gender_list = Liststore_Frame(css_name="gender-frame")
        gender_list.register_button(name="add", id="gender-add", callback=self.button_clicked, tooltip="Add", active=True)
        gender_list.register_button(name="remove", id="gender-remove", callback=self.button_clicked, tooltip="Remove", active=False)
        self.__layout_container.add(gender_list.get_layout_container())
        self.__populate_gender_liststore(gender_list)

        right_side = Gtk.Grid(column_spacing=0, row_spacing=0)
        right_side.set_vexpand(True)
        self.__layout_container.add(right_side)
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        right_side.attach(child=box, left=0, top=0, width=2, height=1)


        identity_label = Gtk.Label(label="Identity:")
        identity_label.set_xalign(1)
        identity_label.get_style_context().add_class('entry-label')
        box.add(identity_label)

        self.identity_entry = Gtk.Entry(width_chars=20, xalign=0)
        self.identity_entry.set_placeholder_text(text="Label")
        self.identity_entry.connect("changed", self.added_gender_label)
        self.identity_entry.get_style_context().add_class('entry-with-label')
        box.add(self.identity_entry)
        symbol_label = Gtk.Label(label="Symbol:")
        symbol_label.set_xalign(1)
        symbol_label.get_style_context().add_class('entry-label')
        symbol_label.set_name("symbol-label")
        box.add(symbol_label)

        self.symbol_entry = Gtk.Entry(width_chars=9, xalign=0)
        self.symbol_entry.connect("changed", self.added_gender_label)
        self.symbol_entry.get_style_context().add_class('entry-with-label')
        box.add(self.symbol_entry)


        pronouns_label = Gtk.Label(label="Pronouns:")
        pronouns_label.set_xalign(1)
        pronouns_label.get_style_context().add_class('entry-label')
        right_side.attach(child=pronouns_label, left=0, top=1, width=1, height=1)

        self.pronouns_entry = Gtk.Entry()
        self.pronouns_entry.set_placeholder_text(text="Space-separated list")
        self.pronouns_entry.connect("changed", self.added_gender_label)
        self.pronouns_entry.get_style_context().add_class('entry-with-label')
        self.pronouns_entry.set_hexpand(True)
        right_side.attach(child=self.pronouns_entry, left=1, top=1, width=1, height=1)

        self.student_list = Treestore_Frame(css_name="student-frame", active_toggle="COLLAPSE")
        self.student_list.register_button(name="add", id="student-add", callback=self.button_clicked, tooltip="Add", active=True, pack_order="START")
        self.student_list.register_button(name="remove", id="student-remove", callback=self.button_clicked, tooltip="Remove", active=False, pack_order="START")
        self.show_student_data()
        L_Load_Student_Data.register_callback(self.show_student_data)  # Register callback function to be triggered when data set changes
        right_side.attach(child=self.student_list.get_layout_container(), left=0, top=2, width=2, height=1)
        gender_list.select_row(row=0)

    def show_student_data(self):
        if self.__showing_student_list:
            self.student_list.reset()
        if L_Load_Student_Data.FORMATTED_DATA is not None:
            self.student_list.update(data_fields=L_Load_Student_Data.DATA_FIELDS, column_properties=L_Load_Student_Data.COLUMN_PROPERTIES, row_order=L_Load_Student_Data.ROW_ORDER, data=L_Load_Student_Data.FORMATTED_DATA)
            self.student_list.set_column_visibility("Usual", False)
            self.student_list.set_column_visibility("Status", False)
            self.__showing_student_list = True

    def get_layout_container(self) -> Gtk.Container:
        """ Public Accessor: Returns the main Gtk.Container holding widgets for this class. """
        return self.__layout_container

    def button_clicked(self, button, id):
        print(f"Button Clicked: {id}")

    def added_gender_label(self, entry):
        # print(f"entry_changed: {entry}")
        pass

    def __populate_gender_liststore(self, gender_listview: Liststore_Frame):
        # Column_field -> (Label, Expand-Column)
        column_fields = [("Gender", True), ("Symbol", False)]
        gender_listview.update(data=self.GENDER_PRONOUNS, column_fields=column_fields, selection_callback=self.__gender_selected)

    def __gender_selected(self, gender_identifier):
        """ Callbackk for Liststore_Frame's Gtk.TreeView ::cursor-changed signal """
        self.__display_gender_properties(gender_label=gender_identifier['Gender'])

    def __display_gender_properties(self, gender_label: str):
        # if self.__showing_student_list is False:
        #     self.show_student_data()
        self.identity_entry.set_text(gender_label)
        for gender in self.GENDER_PRONOUNS:
            if gender['Gender'] == gender_label:
                self.symbol_entry.set_text(gender['Symbol'])
                self.student_list.filter_list(string_to_match=gender['Symbol'], fields_to_search=['Gender'])
                pronouns = ""
                for pronoun in gender['Pronouns']:
                    pronouns += f"{pronoun} "
                self.pronouns_entry.set_text(pronouns)
