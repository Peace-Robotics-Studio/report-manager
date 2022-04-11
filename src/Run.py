# run.py
#
# Copyright 2022 Peace Robotics Studio
#
# This is the main entry point for the Report Manager application. A dialog window is created as a child
# of the main editor window and the user is prompted to load data into the application for processing and
# analysis. The ReportEditor() class is required to handle the construction and destruction of the launcher
# dialog window since the inputted data is acted upon by the editor later on.

import gi
import sys
gi.require_version('Gtk', '3.0')

# Resolves error: "attempted relative import with no known parent package"
# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
if __name__ == '__main__':
    from editor.Report_Manager_Editor import ReportEditor
else:
    from .editor.Report_Manager_Editor import ReportEditor

# Create an instance of the Report Editor window
editor_window = ReportEditor()

# Run the program launcher and check for a progress signal (True: the user wants to view and edit reports; False: the user wants to exit)
if editor_window.popup_run_dialog():
    exit_status = editor_window.run(sys.argv)   # Capture any window destruction signals
    sys.exit(exit_status)   # Send window destruction signals (status) to the OS for processing