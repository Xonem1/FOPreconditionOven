#!/usr/bin/env python3 -tt
"""
Module documentation.
"""

# Imports
import tkinter as tk
import platform
import sys

# Global variables

# Platform.system devuelve el sistema operativo ejemplo:Windows, Linux'

platform = platform.system()

# Class declarations

# Function declarations


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("Hello World")
        label1 = tk.Label(self, text="Soy el titulo 1")
        label1.pack()
        # tk.Label(self, text="Text label").pack()
        # self.master.resizable(False, False)

        self.master.tk_setPalette(background='#ececec')

        if platform == "Linux":
            self.master.attributes('-zoomed', 1)
        else:
            self.master.wm_state('zoomed')

        self.mainMenu(),
        # self.master.wm_state('zoomed')
        # self.master.attributes('-zoomed',1)

        # self.master.geometry("{}x{}+{}+{}".format(w, h, 0, 0))

    def mainMenu(self):
        self.master.title("FO Precondition")
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        file = tk.Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)
        edit = tk.Menu(menu)
        edit.add_command(label="Undo", command=self.undoTest)
        menu.add_cascade(label="Edit", menu=edit)

    def client_exit(self):
        self.master.destroy()

    def undoTest(self):
        
# Main body

if __name__ == '__main__':

    root = tk.Tk()
    app = App(root)
    app.mainloop()

