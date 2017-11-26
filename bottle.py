#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GObject

class BottleWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Bottle")
        self.set_border_width(10)
        self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "Manage applications"
        self.set_titlebar(hb)

        hbox = Gtk.Box(spacing=10)
        hb.pack_start(hbox)

        menu = Gtk.Button()
        icon = Gio.ThemedIcon(name="system-run")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        menu.add(image)
        hbox.pack_start(menu, True, True, 0)

        button = Gtk.ToggleButton("Search")
        button.connect("toggled", self.on_button_toggled, "1")
        hbox.pack_start(button, True, True, 0)

        button = Gtk.ToggleButton("Remove")
        button.connect("toggled", self.on_button_toggled, "1")
        hbox.pack_start(button, True, True, 0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        search_label = Gtk.Label("Bottle is a simple application to manage "
                                 "snaps and flatpacks on your system with "
                                 "a focus on security and ease to use.")
        search_label.set_line_wrap(True)
        vbox.pack_start(search_label, False, True, 20)

        search = Gtk.Entry()
        search.set_icon_from_icon_name(0, "system-search")
        search.set_placeholder_text("Click here and search")
        search.connect("activate", self.enter_callback, search)
        vbox.pack_start(search, False, True, 0)

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
        else:
            state = "off"
        print("Button", name, "was turned", state)

    def enter_callback(self, widget, entry):
        print("Enter!")


win = BottleWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
