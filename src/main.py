import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, Gio
import sys, subprocess

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
        filedescriptor = Gtk.FileDialog

        ## elements & settings
        self.button_to_connect_vpn = Gtk.Button(label="Build Connection")
        self.button_to_disconnect_vpn = Gtk.Button(label="Disconnect")
        self.log_view = Gtk.TextView(editable=False, cursor_visible=True)
        self.log_buffer = self.log_view.get_buffer()
        sys.stdout = StdoutRedirector(self.log_buffer)
        #self.log_buffer.set_text("TEST LOG\n")
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_hexpand(True)


        page1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        notebook.append_page(page1, Gtk.Label(label="Main View"))
        page1.append(Gtk.Label(label="Connect to VPN"))
        page1.append(self.button_to_connect_vpn)
        self.button_to_connect_vpn.connect("clicked", self.build_up_vpn_connection)
        page1.append(Gtk.Label(label="Disconnect from VPN"))
        page1.append(self.button_to_disconnect_vpn)
        self.button_to_disconnect_vpn.connect("clicked", self.disconnect_vpn_connection)

        page1.props.margin_start = 24
        page1.props.margin_end = 24
        page1.props.margin_top = 24
        page1.props.margin_bottom = 24

        page2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        notebook.append_page(page2, Gtk.Label(label="Logs"))
        page2.append(Gtk.Label(label="Logging State"))
        scrolled.set_child(self.log_view)
        page2.append(scrolled)
        page2.props.margin_start = 24
        page2.props.margin_end = 24
        page2.props.margin_top = 24
        page2.props.margin_bottom = 24

    def build_up_vpn_connection(self, _widget):
        print("Connect to VPN")
        self.credentials_window_popup()

    def disconnect_vpn_connection(self, _widget):
        print("Disconnect from VPN")

    def open_file(self, button):
        dialog = Gtk.FileDialog()
        dialog.set_title("Open a file")

        dialog.open(self, None, self.on_file_selected)

    def on_file_selected(self, dialog, result):
        try:
            self.selected_file = dialog.open_finish(result)
            print("Selected file:", self.selected_file.get_path())
        except Exception as e:
            print("No file selected:", e)

    def credentials_window_popup(self, **kargs):
        self.credentials_window = Gtk.Window(title="Credentials")
        self.credentials_window.set_transient_for(self)
        self.credentials_window.set_modal(True)           
        self.credentials_window.set_default_size(300, 200)
        
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.credentials_window.set_child(page)
        
        self.textfield_user_entry = Gtk.Entry()
        self.textfield_user_entry.set_placeholder_text("Username")
        self.passfield_user_entry = Gtk.PasswordEntry()
        self.passfield_user_entry.props.placeholder_text = "Password Entry"
        self.passfield_user_entry.props.show_peek_icon = True
        self.textfield_conn_name_entry = Gtk.Entry()
        self.textfield_conn_name_entry.set_placeholder_text("Connection Name")

        page.append(Gtk.Label(label="User"))
        page.append(self.textfield_user_entry)
        page.append(Gtk.Label(label="Password"))
        page.append(self.passfield_user_entry)
        page.append(Gtk.Label(label="Connection Name"))
        page.append(self.textfield_conn_name_entry)

        # Buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        page.append(btn_box)
        
        btn_box.append(Gtk.Label(label="Select Config File"))
        file_dialog_btn = Gtk.Button(label="Config File")
        file_dialog_btn.connect("clicked", self.open_file)
        btn_box.append(file_dialog_btn)

        ok_btn = Gtk.Button(label="Save")
        ok_btn.connect("clicked", self.process_user_credentials_build_connection)
        btn_box.append(ok_btn)

        cancel_btn = Gtk.Button(label="Cancel")
        cancel_btn.connect("clicked", self.credentials_window.close)
        btn_box.append(cancel_btn)

        page.props.margin_start = 24
        page.props.margin_end = 24
        page.props.margin_top = 24
        page.props.margin_bottom = 24
        btn_box.props.margin_start = 24
        btn_box.props.margin_end = 24
        btn_box.props.margin_top = 24
        btn_box.props.margin_bottom = 24

        self.credentials_window.present()
    
    def process_user_credentials_build_connection(self, _widget):

        username = self.textfield_user_entry.get_text()
        password = self.passfield_user_entry.get_text()
        vpn_connection_name = self.textfield_conn_name_entry.get_text()
        ovpn_file_location = self.selected_file.get_path()

        # Debugging purposes only
        # print("Credentials entered")
        # print(f"Username: {username}")
        # print(f"Password: {password}")
        # print(f"File Path: {ovpn_file_location}")

        results = subprocess.run(['echo', ovpn_file_location, username, password, vpn_connection_name], capture_output=True, text=True)
        print(f'{results.stdout}')
        results = subprocess.run(['ip', 'route'], capture_output=True, text=True)
        print(f'{results.stdout}')

        # # 1. Import config
        # subprocess.run(
        #     ["openvpn3", "config-import", "--config", ovpn_file_location, "--name", vpn_connection_name],
        #     check=True
        # )

        # # 2. Allow compression
        # subprocess.run(
        #     ["openvpn3", "config-manage", "--config", vpn_connection_name, "--allow-compression", "yes"],
        #     check=True
        # )

        # # 3. Start session and provide credentials
        # proc = subprocess.run(
        #     ["openvpn3", "session-start", "--config", vpn_connection_name],
        #     input=f"{username}\n{password}\n",
        #     text=True,
        #     check=True
        # )

        # # 4. Check config list
        # subprocess.run(
        #     ["openvpn3", "configs-list", "-v"],
        #     capture_output=True,
        #     check=True
        # )

        self.credentials_window.close()
        self.credentials_window = None

def on_activate(app):
    # Create window
    win = OpenVPNConnector(application=app)
    win.present()

def main():
    app = Gtk.Application(application_id="com.OpenVPNConnector.Application")
    app.connect("activate", on_activate)
    app.run(None)

if __name__ == "__main__":
    main()