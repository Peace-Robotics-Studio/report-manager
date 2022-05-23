#  scratch2.py. (Modified 2022-05-22, 8:02 p.m. by Praxis)
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


class ListDemo(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="List Demo")
        self.set_default_size(200, 200)

    def make_highlight_tag(self):
        tag = Gtk.TextTag(name='search_highlight')
        tag.set_property('background', 'yellow')
        tag.set_property('foreground', 'black')
        return tag

win = ListDemo()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
