#!/usr/bin/env python3

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import tempfile
import subprocess


class PytkfmtApp:
    def __init__(self, master=None):
        # build ui
        self.MainWindow = tk.Tk() if master is None else tk.Toplevel(master)
        self.MainWindow.configure(height=800, width=600)
        self.MainWindow.resizable(True, True)
        self.MainWindow.title("PyTkFmt")

        main_frame = tk.Frame(self.MainWindow)
        main_frame.configure(height=800, width=600)

        self.text_input = ScrolledText(main_frame)
        self.text_input.configure(padx=8, pady=8, )
        self.text_input.pack(expand=True, fill="both", side="top")

        main_frame.pack(expand=True, fill="both", padx=2, pady=2, side="top")

        self.text_input.bind('<Control-Shift-Return>', self.fmt)
        self.text_input.bind('<Control-Shift-Key-S>', self.pg_format)
        self.text_input.focus()

        instruction = 'Paste text here then press \
Control-Shift-Return to format using fmt(1),\nor Control-Shift-S to format \
with pg_format(1)'

        self.text_input.insert('end', instruction)

        # Main widget
        self.mainwindow = self.MainWindow

    def run(self):
        self.mainwindow.mainloop()

    def get_text(self):
        return self.text_input.get('1.0', 'end-1c')

    def set_text(self, text):
        self.text_input.delete('1.0', 'end')
        self.text_input.insert('end', text)

    def execute_fmt(self, text):
        tmp = tempfile.NamedTemporaryFile(mode='w')
        tmp.write(text)
        tmp.seek(0)
        result = subprocess.run(['fmt', '-72', tmp.name], capture_output=True)
        result_text = result.stdout.decode('utf-8').strip()
        tmp.close()
        return result_text

    def execute_pg_format(self, text):
        tmp = tempfile.NamedTemporaryFile(mode='w')
        tmp.write(text)
        tmp.seek(0)
        result = subprocess.run(['pg_format', tmp.name], capture_output=True)
        result_text = result.stdout.decode('utf-8').strip()
        tmp.close()
        return result_text


    def fmt(self, _evt):
        text = self.get_text()
        result_text = self.execute_fmt(text)
        self.set_text(result_text)

    def pg_format(self, _evt):
        text = self.get_text()
        result_text = self.execute_pg_format(text)
        self.set_text(result_text)


if __name__ == "__main__":
    app = PytkfmtApp()
    app.run()
