#!/usr/bin/env python3 -tt
"""
Autor: Jesus Alberto Esquer Inzunza
Company: Radiall
Alias: Xonem
"""

# Imports
import tkinter as tk
from tkinter import ttk as ttk
from tkinter import E, W, S, N, messagebox, StringVar, END, PhotoImage, Menu
import platform
from tkcalendar import Calendar
import fechayhora
import regresion
import numpy

# Global variables


TEMP = 125
TIEMPO = 90
QTYCABLE = None
TIPOCABLE = 500
NUMPART = None
FONT = "Consolas 20"
FONT_TABLA = "Consolas 12"
COLOR_JULIAN = "#D0E3AB"
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
        self.tanda_num = StringVar(value="000001")
        self.qty = StringVar(value=QTYCABLE)
        self.np = StringVar(value=NUMPART)
        self.ciclo = StringVar(value=0.0)

        self.estiloframe = ttk.Style()
        self.estiloframe.configure('my.TFrame', background=COLOR_JULIAN)

        self.estiloframe_ent = ttk.Style()
        self.estiloframe_ent.configure('ent.TFrame', background="#4285F4")

        self.estiloboton = ttk.Style()
        self.estiloboton.configure('ent.TButton', font=('Consolas', 50),
                                   background="#4285F4")

        self.estiloboton2 = ttk.Style()
        self.estiloboton2.configure('sal.TButton', font=('Consolas', 50),
                                   background="#34a853")

        self.estiloboton3 = ttk.Style()
        self.estiloboton3.configure('calc.TButton', font=('Consolas', 15),
                                   background="#ff7373", relief="sunken")

        self.estilolabel = ttk.Style()
        self.estilolabel.configure('my.Label', font=('Consolas', 50),
                                   background="azure")

        self.estilolabel_ent = ttk.Style()
        self.estilolabel_ent.configure('ent.Label', font=('Consolas', 20),
                                   background="#4285F4")

        tk.Frame.__init__(self)
        #self.grid(sticky=N+S+E+W)
        self.grid()
        
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        '''
        self.configurar_frame()
        # self.maximizar()
        self.crear_interfaz()
        '''
        try:
            self.configurar_frame()
            self.maximizar()
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
                self.master.attributes('-fullscreen', True)
            else:
                print("Detectando Sistema Operativo Windows")
                self.master.wm_state('zoomed')
                #self.margen_top = int(self.master.winfo_height()/4)
                #print(self.margen_top)
        except tk.TclError as error:
            print("Error Detectado: ", error)
            self.destroy()
            exit(1)

    def configurar_frame(self):
        """
        El metodo configura el frame, es parte del constructor
        """
        self.master.title("FO Precondicionado - Radiall OBR")
        #self.master.tk_setPalette(background='#fbbc05')
        self.config(bg='azure')
        self.master.config(bg='azure')
        #self.master.resizable(False,False)
        if PLATFORM == "Linux":
            # self.master.iconbitmap("@/home/pi/fopreconditionoven/radiall.XBM")
            img = PhotoImage(file="./rsc/radiall.gif")
            self.master.call('wm','iconphoto',self.master._w, img)
        else:
            self.master.iconbitmap(".\\rsc\\radiall.ico")

    def crear_interfaz(self):
        self.ventana_main = ttk.Frame(self, borderwidth=5,
                                          relief="groove", style='my.TFrame')

        self.boton_entradas = ttk.Button(self.ventana_main, style='ent.TButton',
                                         text="Entradas",
                                         command=self.interfaz_entradas)

        self.boton_salidas = ttk.Button(self.ventana_main, style='sal.TButton',
                                         text="Salidas")
        
        self.label_titulo = ttk.Label(self, style='my.Label',
                                      text="Control Precondicionado")

        self.ventana_main.grid(row=1, column=0, padx=20, pady=20,
                               sticky=N+S+W+E)
        self.boton_entradas.grid(row=0, column=0, padx=75, pady=75,
                                 sticky=N+S+W+E)
        self.boton_salidas.grid(row=0, column=1, padx=75, pady=75,
                                 sticky=N+S+W+E)
        self.label_titulo.grid(row=0, column=0, pady=10, sticky=N)
        self.grid_rowconfigure(0,minsize=300)

    def interfaz_entradas(self):
        #Configuracion
        self.window_entradas =  tk.Toplevel(self.master)
        self.window_entradas.title("Entradas de Proceso")
        self.window_entradas.focus_set()
        ent_top = self.window_entradas.winfo_toplevel()
        ent_top.rowconfigure(0, weight=1)
        ent_top.columnconfigure(0, weight=1)
        
        self.window_entradas.rowconfigure(0, weight=1)
        self.window_entradas.columnconfigure(0, weight=1)

        self.window_entradas.configure(background="#4285F4")

        #Configurar ventana para maximizar, borrar barra y quitar opcion de cerrar.
        try:
            if PLATFORM == "Linux":
                print("Detectando Sistema Operativo Linux")
                w, h = self.winfo_screenwidth(), self.winfo_screenheight()
                self.window_entradas.overrideredirect(1)
                self.window_entradas.geometry("%dx%d+0+0" % (w, h))
                self.window_entradas.focus_set() # <-- move focus to this widget
                self.window_entradas.bind("<Escape>",
                                     lambda e: self.window_entradas.destroy())
                self.window_entradas.protocol("WM_DELETE_WINDOW", self.disable_event)
            else:
                w, h = self.winfo_screenwidth(), self.winfo_screenheight()
                w, h= 1366,768
                self.window_entradas.overrideredirect(1)
                self.window_entradas.geometry("%dx%d+0+0" % (w, h))
                self.window_entradas.focus_set() # <-- move focus to this widget
                self.window_entradas.bind("<Escape>",
                                     lambda e: self.window_entradas.destroy())
                self.window_entradas.protocol("WM_DELETE_WINDOW", self.disable_event)
        except tk.TclError as error:
            print("Error Detectado: ", error)
            self.window_entradas.destroy()
            exit(1)

        #Interfaz
        #Primera linea
        self.entradas_frame = ttk.Frame(self.window_entradas, borderwidth=5,
                                        relief="sunken", style='ent.TFrame')
        self.entrada_tanda_label = ttk.Label(self.entradas_frame,
                                             text="Tanda: ",
                                             style="ent.Label")
        self.entrada_tanda_entry = ttk.Entry(self.entradas_frame,
                                             font=FONT,
                                             width=6, 
                                             textvariable=self.tanda_num)
        self.entrada_peso_label = ttk.Label(self.entradas_frame, text="Peso: ",
                                     style="ent.Label")
        self.entrada_peso_entry = ttk.Entry(self.entradas_frame, font=FONT,
                                     width=6, textvariable=self.tanda_num)
        self.boton_peso = ttk.Button(self.entradas_frame, text="Calcular",
                                     style="calc.TButton",
                                     cursor="hand2",
                                     command= self.disable_event)
        
        self.entradas_frame.grid(row=0, column=0)
        self.entrada_tanda_label.grid(row=0, column=0, padx=10, pady=10)
        self.entrada_tanda_entry.grid(row=0, column=1, padx=10, pady=10)
        self.entrada_peso_label.grid(row=0, column=2, padx=10, pady=10)
        self.entrada_peso_entry.grid(row=0, column=3, padx=10, pady=10)
        self.boton_peso.grid(row=0, column=4, padx=10, pady=10)

        self.tabla_frame = ttk.Frame(self.entradas_frame, borderwidth=5,
                                     relief="sunken", style='ent.TFrame')

        self.tabla_frame.grid(row=1, column=0, columnspan=5, sticky=N)

        height = 15
        width = 4
        self.tabla = {}
        self.tabla_titulo = ("MO","Part Number", "Long_1", "Long_2")
        counter = 0
        for k in range(4):
            self.titulo_tabla = ttk.Label(self.tabla_frame,
                                          text=str(self.tabla_titulo[k]),
                                          style="ent.Label")
            self.titulo_tabla.grid(row=0, column=k+1)
            print(self.tabla_titulo[k])
        for i in range(height): #Rows
            self.num_tabla = ttk.Label(self.tabla_frame, text=i+1,
                                       style="ent.Label")
            for j in range(width): #Columns
                self.tabla[counter] = ttk.Entry(self.tabla_frame, text="", width=25,
                              font=FONT_TABLA)
                self.tabla[counter].grid(row=i+1, column=j+1, padx=1, pady=2)
                counter+=1
            self.num_tabla.grid(row=i+1, column=0)
        print(counter)
        

    def disable_event(self):
        print("testing")
        self.window_entradas.lower(belowThis=None)
        messagebox.showwarning("Error", "Termine para poder cerrar",
                               parent=self.window_entradas)
        self.window_entradas.bell()
        self.window_entradas.lift(aboveThis=None)
        self.window_entradas.focus_set()
        pass

    def Hora_Fecha(self):
        def print_sel():  
            print(cal.selection_get())

        date_window = tk.Toplevel(self.master)
        date_window.title('Configurar Hora y Fecha')
        date_window.focus_set()
        actual_year = int(fechayhora.getdatetime("year"))
        actual_month = int(fechayhora.getdatetime("month"))
        actual_day = int(fechayhora.getdatetime("day"))
        
        cal = Calendar(date_window,
                       font="Arial 14", selectmode='day',
                       cursor="hand2", year=actual_year, month=actual_month,
                       day=actual_day)
        cal.pack(fill="both", expand=True)
        ttk.Button(date_window, text="ok", command=print_sel).pack()

if __name__ == '__main__':
    ROOT = tk.Tk()
    s = ttk.Style(ROOT)
    print(str(s.theme_names()))
    themes=('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    s.theme_use(themes[1])
    APP = App(ROOT)
    APP.mainloop()
