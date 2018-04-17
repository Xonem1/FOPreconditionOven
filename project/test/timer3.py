# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 14:47:40 2018

@author: ESQUER_J
"""

from datetime import datetime, timedelta
import time
import tkinter as tk
from tkinter import StringVar



fdt = datetime.now()
ldt = 0

def temporizador(y):
    if isinstance(y,   int):
        x = timedelta(seconds = 0)
        timer=timedelta(seconds = y)
        while x<timer:
            ldt=datetime.now()
            x=ldt-fdt
            print(x)
            ltiempo.config(text = x)
    else:
        print("error")
        

root=tk.Tk()
root.after(100,temporizador(2))
ltiempo = tk.Label(root)
ltiempo.pack()


root.mainloop()