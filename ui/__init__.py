import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

import re

import ui.snap as snap

class BottleWindow(Gtk.Window):

    start_welcome_text = ("Welcome to Bottle, this is a application "
                          "built to manage Snaps on your system with "
                          "a focus on security and ease of use. "
                          "To get started, type in a search query below.")

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

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        search_label = Gtk.Label(self.start_welcome_text)
        search_label.set_line_wrap(True)
        vbox.pack_start(search_label, False, True, 20)

        search = Gtk.Entry()
        search.set_icon_from_icon_name(0, "system-search")
        search.set_placeholder_text("Click here and search")
        search.connect("activate", self.enter_callback, search)
        vbox.pack_start(search, False, True, 0)

        self.liststore = Gtk.ListStore(str, str, str, str)
        treeview = Gtk.TreeView(model=self.liststore)

        renderer_text = Gtk.CellRendererPixbuf()
        column_text = Gtk.TreeViewColumn("-", renderer_text, icon_name=0)
        treeview.append_column(column_text)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Name", renderer_text, text=1)
        treeview.append_column(column_text)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Summary", renderer_text, text=2)
        treeview.append_column(column_text)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Installed", renderer_text, text=3)
        treeview.append_column(column_text)

        vbox.pack_start(treeview, False, True, 20)

    def search_result(self, rl):

        self.liststore.clear()

        for r in rl:

            if re.match(r".*-{}$".format(r.publisher), r.name):
                icon = "system-users-symbolic"
            else:
                icon = "face-wink-symbolic"

            self.liststore.append([
                icon,
                r.name,
                r.summary,
                ("{} (rev {})".format(
                    r.installed['version'],
                    r.installed['rev']
                    ) if r.installed else "No")
                ])

    def enter_callback(self, widget, entry):
        rl = snap.find(entry.get_text())
        self.search_result(rl)
