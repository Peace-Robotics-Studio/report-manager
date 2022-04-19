#  scratch.py. (Modified 2022-04-18, 9:55 p.m. by Praxis)
#  Copyright (c) 2022-2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class SecondDialog(Gtk.Dialog):
    def __init__(self, message):
        super().__init__(title="Second Dialog", flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label=message)

        box = self.get_content_area()
        box.add(label)
        self.show_all()


class FirstDialog(Gtk.Dialog):
    def __init__(self, message):
        super().__init__(title="First Dialog", flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label=message)

        box = self.get_content_area()
        button = Gtk.Button(label="launcher another dialog")
        button.connect("clicked", self.dialog_button_clicked)

        box.add(button)
        box.add(label)

        self.show_all()

    def dialog_button_clicked(self, widget):
        dialog = SecondDialog("This is the second dialog's message.")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")
        dialog.destroy()


class DialogWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Dialog Example")

        self.set_border_width(6)

        button = Gtk.Button(label="Open dialog")
        button.connect("clicked", self.on_button_clicked)

        self.add(button)

    def on_button_clicked(self, widget):
        dialog = FirstDialog("This is the first dialog's message.")
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("The OK button was clicked")
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog.destroy()


win = DialogWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()