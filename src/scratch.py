#  scratch.py. (Modified 2022-05-07, 10:40 p.m. by Praxis)
#  Copyright (c) 2022 Peace Robotics Studio
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


class ExpanderExample(Gtk.Window):
    def __init__(self):
        super().__init__(title="Expander Demo")

        self.set_size_request(350, 100)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        text_expander = Gtk.Expander(
                label="This expander displays additional information"
        )
        text_expander.set_expanded(True)
        vbox.add(text_expander)

        msg = """
This message is quite long, complicated even:
    - It has a list with a sublist:
        - of 3 elements;
        
        - taking several lines;
        - with indentation.
"""
        details = Gtk.Label(label=msg)
        text_expander.add(details)

        widget_expander = Gtk.Expander(label="Expand for more controls")
        vbox.add(widget_expander)

        expander_hbox = Gtk.HBox()
        widget_expander.add(expander_hbox)

        expander_hbox.add(Gtk.Label(label="Text message"))
        expander_hbox.add(Gtk.Button(label="Click me"))

        self.show_all()


win = ExpanderExample()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()