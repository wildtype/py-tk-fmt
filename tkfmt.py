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

        fmt_key = '<Control-Shift-Return>'
        fmt_command = ['fmt', '-72']
        self.text_input.bind(fmt_key, self.do_format(fmt_command))

        pgformat_key = '<Control-Shift-Key-S>'
        pgformat_command = ['pg_format']
        self.text_input.bind(pgformat_key, self.do_format(pgformat_command))

        md_dokuwiki_key = '<Control-Shift-Key-D>'
        md_dokuwiki_command = ['pandoc', '-f', 'markdown', '-t', 'dokuwiki']
        self.text_input.bind(md_dokuwiki_key, self.do_format(md_dokuwiki_command))

        jq_key = '<Control-Shift-Key-J>'
        jq_command = ['jq', '.']
        self.text_input.bind(jq_key, self.do_format(jq_command))

        self.text_input.focus()

        instruction = ''' Paste text here then press:

  * Control-Shift-Return to format with fmt(1)
  * Control-Shift-S to format SQL with pg_format(1)
  * Control-Shift-D to convert markdown to dokuwiki with pandoc(1)
  * Control-Shift-J to format JSON with jq(1)'''
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

    def do_format(self, command):
        def execute_formatter(command, text):
            tmp = tempfile.NamedTemporaryFile(mode='w')
            tmp.write(text)
            tmp.seek(0)
            complete_command = command + [tmp.name]
            result = subprocess.run(complete_command, capture_output=True)
            result_text = result.stdout.decode('utf-8').strip()
            tmp.close()
            return result_text

        def perform_formatting(_evt):
            text = self.get_text()
            result_text = execute_formatter(command, text)
            self.set_text(result_text)

        return perform_formatting


if __name__ == "__main__":
    app = PytkfmtApp()
    app.run()
