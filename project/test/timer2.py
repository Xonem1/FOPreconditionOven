# -*- coding: utf-8 -*-
"""
Created on Wed Apr  4 14:31:31 2018

@author: ESQUER_J
"""

from tkinter import *
from datetime import datetime, timedelta
import time
tk=Tk()
INICIO =datetime.now()
FIN = timedelta(seconds = 5)

def clock():
    AHORA = datetime.now() - INICIO
    label1.config(text = AHORA)
    if AHORA<FIN:
        tk.after(700,clock)
    else:
        pass
    
label1=Label(tk,justify='center')
label1.pack()
clock()
tk.mainloop()