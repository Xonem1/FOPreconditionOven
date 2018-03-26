#!/usr/bin/env python3 -tt
"""
Autor: Jesus Alberto Esquer Inzunza
Company: Radiall
Alias: Xonem
"""

# Imports
import tkinter as tk
from tkinter import ttk as ttk
import platform


# Global variables
E = tk.E
W = tk.W
N = tk.N
S = tk.S

TEMP = 125
TIEMPO = 90
QTYCABLE = 0.0
TIPOCABLE = 500
FONT = "Consolas 20 bold"

#s = ttk.Style()
#s.configure('my.TButton', font=('Helvetica', 12))
# TIPOCABLE = ('490', '500')

# Platform.system devuelve el sistema operativo ejemplo:Windows, Linux'
PLATFORM = platform.system()

# Declaracion de clases


class App(tk.Frame):
    """
    La clase se encargara de crear una ventana que calculara el numero de
    ciclos de un horneado, con respecto a una formula y datos constantes.
    """
    def __init__(self, master):
        """
        Constructor
        """
        self.s = ttk.Style()
        self.s.configure('my.TButton', font=('Consolas', 20))
        qty = QTYCABLE
        tk.Frame.__init__(self)
        self.grid(sticky=N+S+E+W)
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.configurar_frame()
        self.maximizar()
        self.crear_interfaz()
        self.calculo_ciclo(qty)


# Declaracion de Funciones
    def maximizar(self):
        """
        El metodo maximiza la ventana dependiendo del sistema operativo
        por que el programa se testea en windows y linux.
        """
        try:
            if PLATFORM == "Linux":
                print("Detectando Sistema Operativo Linux")
                self.master.attributes('-zoomed', 1)
            else:
                print("Detectando Sistema Operativo Windows")
                self.master.wm_state('zoomed')
        except tk.TclError as error:
            print("Error Detectado: ", error)
            self.destroy()
            exit(1)

    def configurar_frame(self):
        """
        El metodo configura el frame, es parte del constructor
        """
        self.master.title("FO Precondicionado - Radiall OBR")
        self.master.tk_setPalette(background='#ececec')
        self.master.iconbitmap("radiall.ico")

    def crear_interfaz(self):
        """
        El metodo creara los botones, entrys y todos los widgets en general
        que se van a utilizar
        """
        self.campo1 = ttk.Entry(self, textvariable=QTYCABLE,
                                font=FONT, width=20)
        self.button1 = ttk.Button(self, text="Capturar y calcular",
                                  style='my.TButton', width=20)

        self.campo1.grid(row=0, column=0, padx=30, pady=30,)
        self.button1.grid(row=1, sticky = N, padx=30, pady=30)

    def calculo_ciclo(self, qty):
        """
        El metodo analizara el dato dato y aplicara la formula que se obtuvo
        de una regresion
        """
        print(qty)
        pass


if __name__ == '__main__':
    ROOT = tk.Tk()
    APP = App(ROOT)
    APP.mainloop()
