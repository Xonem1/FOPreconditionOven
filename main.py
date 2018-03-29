#!/usr/bin/env python3 -tt
"""
Autor: Jesus Alberto Esquer Inzunza
Company: Radiall
Alias: Xonem
"""

# Imports
import tkinter as tk
from tkinter import ttk as ttk
from tkinter import E, W, S, N, messagebox, StringVar
import platform


# Global variables


TEMP = 125
TIEMPO = 90
QTYCABLE = None
TIPOCABLE = 500
NUMPART = None
FONT = "Consolas 20"
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

        self.qty = StringVar(value=QTYCABLE)
        self.np = StringVar(value=NUMPART)

        self.estiloboton = ttk.Style()
        self.estiloboton.configure('my.TButton', font=('Consolas', 20))
        self.estilolabel = ttk.Style()
        self.estilolabel.configure('my.Label', font=('Consolas', 20))
        tk.Frame.__init__(self)
        self.grid(sticky=N+S+E+W)
        # self.grid()
        top = self.winfo_toplevel()
        # top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        # self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        try:
            self.configurar_frame()
            # self.maximizar()
            self.crear_interfaz()
        except Exception as error:
            print(error)
            self.destroy()

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
                self.margen_top = int(self.master.winfo_height()/4)
                print(self.margen_top)
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
        vcmd_peso = (self.register(self.onValidate_peso),
                     '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        vcmd_parte = (self.register(self.onValidate_parte),
                      '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.ventana_entradas = ttk.Frame(self, borderwidth=20,
                                          relief="groove")

        self.ent_parte = ttk.Entry(self.ventana_entradas,
                                   textvariable=self.np, font=FONT, width=20,
                                   validate="key", validatecommand=vcmd_parte)

        self.ent_peso = ttk.Entry(self.ventana_entradas,
                                  textvariable=self.qty, font=FONT, width=20,
                                  validate="key", validatecommand=vcmd_peso)

        self.lab_parte = ttk.Label(self.ventana_entradas, text="# Parte",
                                   font=FONT)

        self.lab_peso = ttk.Label(self.ventana_entradas, text="Peso",
                                  font=FONT)

        self.but_calcular = ttk.Button(self, text="Calcular",
                                       style="my.TButton",
                                       command= self.calculo_ciclo)

        self.ventana_entradas.grid(row=0, column=0, padx=20, pady=20)
        self.ent_parte.grid(row=0, column=1, pady=15)
        self.lab_parte.grid(row=0, column=0, padx=10, sticky=W)
        self.ent_peso.grid(row=1, column=1, pady=15)
        self.lab_peso.grid(row=1, column=0, padx=10, sticky=W)
        self.but_calcular.grid(row=1, column=0, padx=20, pady=20)
        self.ent_parte.bind('<Return>', self.focus_peso)
        self.ent_peso.bind('<Return>', self.bind_calcular)

    def calculo_ciclo(self):
        """
        El metodo analizara el dato dato y aplicara la formula que se obtuvo
        de una regresion
        """
        print("calcular ciclo")
        pass

    def capturar_calcular(self):
        """
        El metodo capturara los datos
        """
        pass

    def onValidate_peso(self, d, i, P, s, S, v, V, W):
        """
        Metodo evalua y valida si se lee numeros de un entry.
        """
        if S.isdigit():
            return True
        else:
            messagebox.showwarning("Warning", "Solo Numeros")
            self.bell()
            return False

    def onValidate_parte(self, d, i, P, s, S, v, V, W):
        """
        Metodo evalua y valida si se lee numeros y puntos de un entry.
        """
        if S.isdigit() or S == "." :
            print(S.encode('ascii'))
            return True
        else:
            print(S.encode('ascii'))
            messagebox.showwarning("Warning", "Solo numeros y puntos")
            self.bell()
            return False

    def focus_peso(self, event):
        print("return presionado")
        self.ent_peso.focus_set()
        pass

    def bind_calcular(self, event):
        print("return presionado")
        self.calculo_ciclo()
        pass


if __name__ == '__main__':
    ROOT = tk.Tk()
    APP = App(ROOT)
    APP.mainloop()
