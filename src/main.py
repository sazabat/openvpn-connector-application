import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib
import sys

class StdoutRedirector:
    def __init__(self, textbuffer):
        self.textbuffer = textbuffer

    def write(self, text):
        GLib.idle_add(self._append_text, text)

    def flush(self):
        pass

    def _append_text(self, text):
        end_iter = self.textbuffer.get_end_iter()
        self.textbuffer.insert(end_iter, text)
        return False


class OpenVPNConnector(Gtk.ApplicationWindow):
    def __init__(self,**kargs):

        super().__init__(**kargs, default_height=500, default_width=500,title="Simple OpenVPN Connector")

        notebook = Gtk.Notebook()
        self.set_child(notebook)

        ## elements & settings
        self.connect_to_vpn = Gtk.Button(label="Build Connection")
        self.disconnect_from_vpn = Gtk.Button(label="Disconnect")
        self.user_entry_field = Gtk.Entry()

        self.log_view = Gtk.TextView(editable=False, cursor_visible=True)
        self.log_buffer = self.log_view.get_buffer()
        sys.stdout = StdoutRedirector(self.log_buffer)
        #self.log_buffer.set_text("TEST LOG\n")
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)

        
        self.user_pass_entry = Gtk.PasswordEntry()
        self.user_pass_entry.props.placeholder_text = "Password Entry"
        self.user_pass_entry.props.show_peek_icon = True
        

        page1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        notebook.append_page(page1, Gtk.Label(label="Main View"))
        page1.append(Gtk.Label(label="Connect to VPN"))
        page1.append(self.connect_to_vpn)
        self.connect_to_vpn.connect("clicked", self.build_up_vpn_connection)
        page1.append(Gtk.Label(label="Disconnect from VPN"))
        page1.append(self.disconnect_from_vpn)

        page1.props.margin_start = 24
        page1.props.margin_end = 24
        page1.props.margin_top = 24
        page1.props.margin_bottom = 24


        page2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        notebook.append_page(page2, Gtk.Label(label="Logs"))
        page2.append(Gtk.Label(label="Logging State"))
        scrolled.set_child(self.log_view)
        page2.append(scrolled)
        # stdout umleredirect
        print("Programm gestartet")
        print("Hallo aus stdout!")

        page3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)        
        notebook.append_page(page3, Gtk.Label(label="Enter Fields Test"))
        page3.append(Gtk.Label(label="User"))
        page3.append(self.user_entry_field)
        page3.append(Gtk.Label(label="Password"))
        page3.append(self.user_pass_entry)


    def build_up_vpn_connection(self, _widget):
        print("Test")
        #self.close()


def on_activate(app):
    # Create window
    win = OpenVPNConnector(application=app)
    win.present()


app = Gtk.Application(application_id="com.OpenVPNConnector.Application")
app.connect("activate", on_activate)
app.run(None)