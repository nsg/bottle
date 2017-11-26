#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import ui

win = ui.BottleWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
