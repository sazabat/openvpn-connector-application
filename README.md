# OpenVPN Connector from a simple GUI Window
Connect & Authenticate to your OpenVPN Server with this little application. This open source program can be customized and rebuild for own appropriate usage. The deployed version from the main branch is a ready to use executable which can be installed on the OS.

## Prerequisites
- Ensure OpenVPN is installed on your system. This application uses the openvpn system utilities.

# Development
## Python Packages
- Install all required python packages from requirements.txt to get started.

## Build from source
Use the command below to build your own executable GUI application, if changes are made or customized.
- pyinstaller ./src/main.py --onefile --console --hidden-import=gi --hidden-import=gi.repository.Gtk --hidden-import=gi.repository.Gio --hidden-import=gi.repository.GLib
