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
        self.master.resizable(False,False)
        
        self.master.tk_setPalette(background='#ececec')
        x= int((self.master.winfo_screenwidth()-self.master.winfo_reqwidth())/2)
        y= int((self.master.winfo_screenheight()-self.master.winfo_reqheight())/2)
        self.master.geometry("300x200+{}+{}".format(x,y))
        
        self.master.config(menu = tk.Menu(self.master))
        
# Main body
if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    app.mainloop()