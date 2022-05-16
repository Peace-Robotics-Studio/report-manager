#  L_Feedback_Files.py. (Modified 2022-05-15, 4:46 p.m. by Praxis)
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

from gi.repository import Gtk
from ...gui.L_Help_Page import L_Help_Page

class L_Feedback_Files:
    """ This class is called by """
    def __init__(self, tab_id: str, active_option: str):
        """ Constructor """
        self.__tab_id = tab_id
        self.__add_help_page()
        self.__layoutContainer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.__layoutContainer.set_hexpand(True)
        self.__layoutContainer.set_vexpand(True)
        self.page_label = Gtk.Label()
        self.page_label.set_xalign(0)  # Set the horizontal alignment for the label
        self.page_label.get_style_context().add_class('launcher-feedback-options-label')  # Connect a CSS class to the label
        self.__layoutContainer.add(self.page_label)
        self.set_state(active_option)

    def get_layout_container(self):
        return self.__layoutContainer

    def set_state(self, key):
        match key:
            case "PANEL_0":  # Existing Files
                self.display_recent_files()
            case "PANEL_1":  # By Grade
                self.display_by_grade()
            case "PANEL_2":  # By Teacher
                self.display_by_teacher()
            case "PANEL_3":  # By Class
                self.display_by_class()
            case "PANEL_4":  # By Date
                self.display_by_date()

    def __add_help_page(self):
        help_page_0 = L_Help_Page(tab_id=self.__tab_id, panel_id="PANEL_0")
        help_page_0.set_page_title(title="Display Recent Files")

        help_page_1 = L_Help_Page(tab_id=self.__tab_id, panel_id="PANEL_1")
        help_page_1.set_page_title(title="Feedback By Grade")

        help_page_2 = L_Help_Page(tab_id=self.__tab_id, panel_id="PANEL_2")
        help_page_2.set_page_title(title="Feedback By Teacher")

        help_page_3 = L_Help_Page(tab_id=self.__tab_id, panel_id="PANEL_3")
        help_page_3.set_page_title(title="Feedback By Class")

        help_page_4 = L_Help_Page(tab_id=self.__tab_id, panel_id="PANEL_4")
        help_page_4.set_page_title(title="Feedback By Date")


    def display_recent_files(self):
        self.page_label.set_text("Recent Feedback Summaries")  # Set the value of the label text

    def display_by_grade(self):
        self.page_label.set_text("Feedback By Grade")  # Set the value of the label text

    def display_by_teacher(self):
        self.page_label.set_text("Feedback By Teacher")  # Set the value of the label text

    def display_by_class(self):
        self.page_label.set_text("Feedback By Class")  # Set the value of the label text

    def display_by_date(self):
        self.page_label.set_text("Feedback By Date")  # Set the value of the label text