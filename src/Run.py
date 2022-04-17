#  Run.py. (Modified 2022-04-16, 1:34 p.m. by Praxis)
#  Copyright (c) 2021-2022 Peace Robotics Studio
#  Licensed under the MIT License.
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so.

import gi
import sys

gi.require_version('Gtk', '3.0')

# Resolves error: "attempted relative import with no known parent package"
# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
if __name__ == '__main__':
    from editor.Editor_Interface import ReportEditor
else:
    from .editor.Editor_Interface import ReportEditor

# Create an instance of the Report Editor window
editor_window = ReportEditor()

# Run the program launcher and check for a progress signal (True: the user wants to view and edit reports; False: the user wants to exit)
if editor_window.popup_run_dialog():
    exit_status = editor_window.run(sys.argv)  # Capture any window destruction signals
    sys.exit(exit_status)  # Send window destruction signals (status) to the OS for processing
