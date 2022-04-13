def on_button_toggled(self, button, name, parent):
    if button.get_active():
        parent.monitor_num_for_display = name

def button_clicked(self, button):

    if button.get_label() == "Run":
        self.response(Gtk.ResponseType.OK)
    elif button.get_label() == "Quit":
        self.response(Gtk.ResponseType.CANCEL)

def on_fullscreen_toggled(self, button, name, parent):
    if button.get_active():
        parent.is_fullscreen = True
    else:
        parent.is_fullscreen = False

# Obtain handle to the drawable area of the window and set a container to manage content
area = self.get_content_area()
grid = Gtk.Grid(column_homogeneous=False, column_spacing=0, row_spacing=0)
area.add(grid)

# Create a button
RUN_Button = Gtk.Button(label="Run")
RUN_Button.connect("clicked", self.button_clicked)
RUN_Button.get_style_context().add_class('button-background')
RUN_Button.set_name("myButton_green")

QUIT_Button = Gtk.Button(label="Quit")
QUIT_Button.connect("clicked", self.button_clicked)
QUIT_Button.get_style_context().add_class('button-background')
QUIT_Button.set_name("myButton_red")

# Create a list
vbox_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
vbox_list.set_hexpand(True)
vbox_list.set_vexpand(True)
vbox_list.set_valign(Gtk.Align.END)

group = Gtk.RadioButton.new(None)

display = Gdk.Display.get_default()
num_of_monitors = display.get_n_monitors()

for i in range(num_of_monitors):
    monitor = display.get_monitor(i)
    geometry = monitor.get_geometry()
    scale_factor = monitor.get_scale_factor()
    width = scale_factor * geometry.width
    height = scale_factor * geometry.height

    if monitor.is_primary():
        label = "Monitor #" + repr(i + 1) + " - " + repr(width) + " X " + repr(height) + " (PRIMARY)"

        button = Gtk.RadioButton.new_with_label_from_widget(group, label)
        button.get_style_context().add_class('blue-text')
        button.connect("toggled", self.on_button_toggled, i, parent)
        button.set_active(True)
    else:
        label = "Monitor #" + repr(i + 1) + " - " + repr(width) + " X " + repr(height)

        button = Gtk.RadioButton.new_with_label_from_widget(group, label)
        button.get_style_context().add_class('blue-text')
        button.connect("toggled", self.on_button_toggled, i, parent)

    vbox_list.add(button)

checkbutton = Gtk.CheckButton.new_with_label("Fullscreen Window")
checkbutton.get_style_context().add_class('blue-text')
checkbutton.connect("toggled", self.on_fullscreen_toggled, "fullscreen", parent)
checkbutton.set_active(True)
vbox_list.add(checkbutton)

grid.attach(vbox_list, 1, 2, 1, 1)
grid.attach(RUN_Button, 2, 0, 1, 1)
grid.attach(QUIT_Button, 2, 1, 1, 1)
grid.get_style_context().add_class('main-grid')



CSS UnicodeError
.button-background {
    background-image: url("../gui/button-default.png");
    border-image: none;
    color: gray;
    font-weight: bold;
    font-size: 18px;
    margin: 0;
    padding: 0;
    padding-top: 2px;
    border: 0;
    min-width: 110px;
    min-height: 41px;
    box-shadow: none;
}

#myButton_green.button-background {
    color: green;
}

#myButton_green.button-background:hover {
    background-image: url("../gui/button-bright-green.png");
}

#myButton_red.button-background {
    color: red;
}

#myButton_red.button-background:hover {
    background-image: url("../gui/button-bright-red.png");
}

.blue-text:focus {
    color: green;
}

.blue-text:hover {
    color: orange;
}

.blue-text {
    color: #197cc3;
}

.main-grid {
    margin-left: 3px;
    margin-bottom: 3px;
    margin-top: 189px;
    margin-right:3px;
    background-color: #353535;
}

.content-area {
    background-color: #353535;
}