#!/usr/bin/env python3 -tt
"""
Module documentation.
"""

# Imports
import tkinter as tk
import platform

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
        tk.Label(self, text="Text label").pack()
        # self.master.resizable(False, False)

        self.master.tk_setPalette(background='#ececec')

        if platform == "Linux":
            self.master.attributes('-zoomed', 1)
        else:
            self.master.wm_state('zoomed')

        # self.master.wm_state('zoomed')
        # self.master.attributes('-zoomed',1)

        # self.master.geometry("{}x{}+{}+{}".format(w, h, 0, 0))

        self.master.config(menu=tk.Menu(self.master))


# Main body

if __name__ == '__main__':

    root = tk.Tk()
    app = App(root)
    app.mainloop()
