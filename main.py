#!/usr/bin/env python3 -tt
"""
Module documentation.
"""

# Imports
import tkinter as tk #tkpython3
#import os

# Global variables

# Class declarations

# Function declarations

class App(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        self.pack()
        self.master.title("Hello World")
        tk.Label(self, text="Text label").pack()

# Main body
if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()
