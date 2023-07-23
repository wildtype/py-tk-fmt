#!/usr/bin/python3
import tkinter as tk
from tkinter.scrolledtext import ScrolledText


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
        self.text_input.configure(padx=8, pady=8)
        self.text_input.pack(expand=True, fill="both", side="top")
        main_frame.pack(expand=True, fill="both", padx=8, pady=8, side="top")

        # Main widget
        self.mainwindow = self.MainWindow

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = PytkfmtApp()
    app.run()
