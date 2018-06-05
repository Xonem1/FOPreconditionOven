#!/usr/bin/env python3 -tt
"""
Autor: Jesus Alberto Esquer Inzunza
Company: Radiall
Alias: Xonem
"""

import datetime
import platform
import sqlite3
# Imports
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import _thread
import matplotlib as mpl
import matplotlib.lines as lines

from tkinter import ttk as ttk
from tkinter import (END, DoubleVar, E, IntVar, Menu, N, PhotoImage, S,
                     StringVar, W, messagebox, simpledialog)

import numpy
import numpy as np
from numpy import arange, sin, pi
from tkcalendar import Calendar

import fechayhora
import regresion
from bascula import bascula
from serial_temp import serial_temp

import time
import datetime as dt
import os
import sys

# Global variables


TEMP = 125
TIEMPO = 90
QTYCABLE = None
TIPOCABLE = 500
NUMPART = None
FONT = "Consolas 20"
FONT_TABLA = "Consolas 12"
COLOR_JULIAN = "#D0E3AB"
DEBUG = True
DPI = 100
DATA = 0
UPDATE_TIME=100
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
    # Variable StringVar IntVar Etc
        self.tanda_num = IntVar(value="00001")
        self.qty = StringVar(value=QTYCABLE)
        self.np = StringVar(value=NUMPART)
        self.ciclo_text = StringVar(
            value="Presione calcular para obtener peso y numero de ciclos")
        self.ciclo_value = DoubleVar(value=0.0)
        self.peso = StringVar(value="0 kg")
        self.contador_entry_enable = 0
        self.peso_lista = [0, 0]
        self.data= 0
        self.num_data = 0
        self.puerto_bascula_windows = "COM19"
        self.archivo_nombre = None
        '''
        try:
            #self.archivo_nombre = self.getdb_tanda()+1
            #self.archivo_nombre = "Grafico_Tanda_"+str(self.archivo_nombre)
            #self.archivo_nombre=self.nombre_grafica
            if PLATFORM == "Linux":
                file = open("./graficas/"+self.archivo_nombre+".csv", "a") #se crea un archivo con la fecha y el nombre
                if os.stat("./graficas/"+self.archivo_nombre+".csv").st_size == 0:
                    file.write("Fecha,Exterior,Interior,Sensor 2,Sensor 1\n")
                    file.close()
            else:
                file = open(os.getcwd()+"\\graficas\\"+self.archivo_nombre+".csv", "a") #se crea un archivo con la fecha y el nombre
                if os.stat(os.getcwd()+"\\graficas\\"+self.archivo_nombre+".csv").st_size == 0:
                    file.write("Fecha,Exterior,Interior,Sensor 2,Sensor 1\n")
                    file.close()
        except Exception as e:
            print(e)
        '''
        try:
            self.con = sqlite3.connect("testing.db",
                                       detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            print("Base de datos Iniciada")
            self.c = self.con.cursor()
            self.con.close()
        except Exception as e:
            print(e)

    # ESTILOS
        self.estiloframe = ttk.Style()
        self.estiloframe.configure('my.TFrame', background=COLOR_JULIAN)

        self.estiloframe_ent = ttk.Style()
        self.estiloframe_ent.configure('ent.TFrame', background="#4285F4")

        self.estiloboton = ttk.Style()
        self.estiloboton.configure('ent.TButton', font=('Consolas', 18),
                                   background="#4285F4",
                                   justify= tk.CENTER)

        self.estiloboton2 = ttk.Style()
        self.estiloboton2.configure('sal.TButton', font=('Consolas', 18),
                                    background="#34a853")
        
        self.estiloboton3 = ttk.Style()
        self.estiloboton3.configure('graf.TButton', font=('Consolas', 18),
                                    background="#f65314")

        self.estiloframe_ent = ttk.Style()
        self.estiloframe_ent.configure('sal.TFrame', background="#34a853")

        self.estiloboton3 = ttk.Style()
        self.estiloboton3.configure('calc.TButton', font=('Consolas', 15),
                                    background="#ff7373", relief="sunken")

        self.estilolabel = ttk.Style()
        self.estilolabel.configure('my.Label', font=('Consolas', 50),
                                   background="azure")

        self.estilolabel_ent = ttk.Style()
        self.estilolabel_ent.configure('ent.Label', font=('Consolas', 20),
                                       background="#4285F4")

        self.estilolabel_ent = ttk.Style()
        self.estilolabel_ent.configure('sal.Label', font=('Consolas', 20),
                                       background="#34a853")

        self.estilolabel_ent.configure('salsubt.Label', font=('Consolas', 15),
                                       background="#34a853")

        self.estiloentry = ttk.Style()
        self.estiloentry.configure('my.TEntry', fieldbackground='gray93')
        self.estiloentry.map('my.TEntry',
                             fieldbackground=[('disabled', 'gray75'),
                                              ('focus', 'white')],)

        self.estiloentry = ttk.Style()
        self.estiloentry.configure('myPeso.TEntry', fieldbackground='white')
        self.estiloentry.map('myPeso.TEntry',
                             fieldbackground=[('disabled', 'white'),
                                              ('focus', 'white')],
                             foreground=[('disabled', 'black')])

        self.estilolabel_ent = ttk.Style()
        self.estilolabel_ent.configure('ciclo.Label', font=('Consolas', 15),
                                       background="#4285F4")

        tk.Frame.__init__(self)
        # self.grid(sticky=N+S+E+W)
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
                self.master.bind("<Escape>",
                                lambda e: self.pass_cmd())
            else:
                print("Detectando Sistema Operativo Windows")
                self.master.wm_state('zoomed')
                #self.margen_top = int(self.master.winfo_height()/4)
                # print(self.margen_top)
                self.master.bind("<Escape>",
                                lambda e: self.pass_cmd())
                self.master.bind("<Alt-Key-F4>",
                                lambda e: self.askstring_close())
                self.master.protocol("WM_DELETE_WINDOW", self.pass_cmd)
        except tk.TclError as error:
            print("Error Detectado: ", error)
            self.destroy()
            exit(1)

    def configurar_frame(self):
        """
        El metodo configura el frame, es parte del constructor
        """
        self.master.title("FO Precondicionado - Radiall OBR")
        # self.master.tk_setPalette(background='#fbbc05')
        self.config(bg='azure')
        self.master.config(bg='azure')
        # self.master.resizable(False,False)
        # self.master.overrideredirect(1)
        if PLATFORM == "Linux":
            # self.master.iconbitmap("@/home/pi/fopreconditionoven/radiall.XBM")
            img = PhotoImage(file="./rsc/radiall.gif")
            self.master.call('wm', 'iconphoto', self.master._w, img)
        else:
            # self.master.iconbitmap(".\\rsc\\radiall.ico")
            pass

    def crear_interfaz(self):
        self.ventana_main = ttk.Frame(self, borderwidth=5,
                                      relief="groove", style='my.TFrame')

        self.boton_entradas = ttk.Button(self.ventana_main, style='ent.TButton',
                                         text="Nuevo Lote de \nPrecondicionado",
                                         command=self.interfaz_entradas)

        self.boton_salidas = ttk.Button(self.ventana_main, style='sal.TButton',
                                        text="Cargar Lote de \nPrecondicionado",
                                        command=self.interfaz_salidas)

        self.boton_grafica = ttk.Button(self.ventana_main, style='graf.TButton',
                                        text="Abrir Grafica \nde Temperatura",
                                        command=self.asktring_name)

        self.label_titulo = ttk.Label(self, style='my.Label',
                                      text="Control Precondicionado")

        self.ventana_main.grid(row=1, column=0, padx=20, pady=20,
                               sticky=N+S)
        self.ventana_main.grid_columnconfigure(0,weight=1)
       # self.boton_entradas.grid(row=0, column=0, padx=25, pady=45, ipadx=20, ipady=20,
       #                          sticky=N+S+W+E)
       # self.boton_salidas.grid(row=0, column=1, padx=25, pady=45, ipadx=20, ipady=20,
       #                         sticky=N+S+W+E)

        self.boton_grafica.grid(row=0, column=0, padx=45, pady=45, ipadx=20, ipady=20,
                                sticky=N+S+W+E)

        self.label_titulo.grid(row=0, column=0, pady=10, sticky=N)
        self.grid_rowconfigure(0, minsize=300)

    def interfaz_entradas(self):
        # Configuracion
        self.window_entradas = tk.Toplevel(self.master)
        self.window_entradas.title("Entradas de Proceso")
        self.window_entradas.focus_set()
        ent_top = self.window_entradas.winfo_toplevel()
        ent_top.rowconfigure(0, weight=1)
        ent_top.columnconfigure(0, weight=1)
        self.contador_entry_enable = 0

        self.window_entradas.rowconfigure(0, weight=1)
        self.window_entradas.columnconfigure(0, weight=1)

        self.window_entradas.configure(background="#4285F4")

        # Configurar ventana para maximizar, borrar barra y quitar opcion de cerrar.
        try:
            if PLATFORM == "Linux":
                print("Detectando Sistema Operativo Linux")
                w, h = self.winfo_screenwidth(), self.winfo_screenheight()
                self.window_entradas.overrideredirect(1)
                self.window_entradas.geometry("%dx%d+0+0" % (w, h))
                self.window_entradas.focus_set()  # <-- move focus to this widget
                self.window_entradas.bind("<Escape>",
                                          lambda e: self.window_entradas.destroy())
                #self.window_entradas.protocol("WM_DELETE_WINDOW", self.disable_event)
            else:
                w, h = self.winfo_screenwidth(), self.winfo_screenheight()
                w, h = 1366, 768
                self.window_entradas.overrideredirect(1)
                self.window_entradas.geometry("%dx%d+0+0" % (w, h))
                self.window_entradas.focus_set()  # <-- move focus to this widget
                self.window_entradas.bind("<Escape>",
                                          lambda e: self.window_entradas.destroy())
                self.window_entradas.protocol(
                    "WM_DELETE_WINDOW", self.disable_event)
        except tk.TclError as error:
            print("Error Detectado: ", error)
            self.window_entradas.destroy()
            exit(1)
    # INTERFAZ DE ENTRADAS PRIMERA PARTE
        # Interfaz
        # Primera linea
        self.tanda_num.set(self.getdb_tanda()+1)

        self.entradas_frame = ttk.Frame(self.window_entradas, borderwidth=5,
                                        relief="sunken", style='ent.TFrame')
        self.entrada_tanda_label = ttk.Label(self.entradas_frame,
                                             text="Tanda: ",
                                             style="ent.Label")
        self.entrada_tanda_entry = ttk.Entry(self.entradas_frame,
                                             font=FONT, width=8,
                                             textvariable=self.tanda_num,
                                             justify="center",
                                             state='disabled',
                                             style='myPeso.TEntry')
        self.entrada_peso_label = ttk.Label(self.entradas_frame, text="Peso: ",
                                            style="ent.Label")
        self.entrada_peso_entry = ttk.Entry(self.entradas_frame, font=FONT,
                                            width=14, textvariable=self.peso,
                                            justify="center", state='disabled',
                                            style='myPeso.TEntry')
        self.boton_peso = ttk.Button(self.entradas_frame, text="Calcular",
                                     style="calc.TButton",
                                     cursor="hand2",
                                     command=self.calcular_peso)

        self.boton_enviar = ttk.Button(self.entradas_frame, text="Enviar",
                                       style="calc.TButton",
                                       cursor="hand2",
                                       command=self.enviar_db)

        self.ciclo_label = ttk.Label(self.entradas_frame,
                                     textvariable=self.ciclo_text,
                                     style="ciclo.Label")

        self.entradas_frame.grid(row=0, column=0)
        self.entrada_tanda_label.grid(row=0, column=0, padx=2, pady=10,
                                      sticky=E)
        self.entrada_tanda_entry.grid(row=0, column=1, padx=2, pady=10,
                                      sticky=W)
        self.entrada_peso_label.grid(row=0, column=2, padx=2, pady=10,
                                     sticky=E)
        self.entrada_peso_entry.grid(row=0, column=3, padx=2, pady=10,
                                     sticky=W)
        self.boton_peso.grid(row=0, column=4, padx=2, pady=10)

        self.tabla_frame = ttk.Frame(self.entradas_frame, borderwidth=5,
                                     relief="sunken", style='ent.TFrame')

        self.tabla_frame.grid(row=1, column=0, columnspan=5, sticky=N)
        self.boton_enviar.grid(row=2, column=4, sticky=E, pady=10, padx=10)
        self.ciclo_label.grid(row=2, column=1, columnspan=3, pady=1, padx=15)

        vcmd_mo_parte = (self.register(self.onValidate_mo_parte),
                         '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        vcmd_longitud = (self.register(self.onValidate_longitud),
                         '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

    # TABLA DE ENTRADAS INTERFAZ
        height = 15
        width = 4
        self.tabla = {}
        self.tabla_titulos = ("MO", "Part Number",
                              "Long_Inicial 1", "Long_Inicial 2")
        counter = 0
        self.tabla_ent_valores = []
        self.mo_valor = []
        self.np_valor = []
        self.lini_valor = []
        self.lfin_valor = []
        for k in range(4):
            self.ltitulo_tabla = ttk.Label(self.tabla_frame,
                                           text=str(self.tabla_titulos[k]),
                                           style="ent.Label")
            self.ltitulo_tabla.grid(row=0, column=k+1)
        for i in range(height):  # Rows
            self.num_tabla = ttk.Label(self.tabla_frame, text=i+1,
                                       style="ent.Label")
            for j in range(width):  # Columns
                if i == 0 and j == 0:
                    self.tabla = ttk.Entry(self.tabla_frame, text="",
                                           width=25, font=FONT_TABLA,
                                           justify="center",
                                           state='enabled', style='my.TEntry')
                else:
                    self.tabla = ttk.Entry(self.tabla_frame, text="",
                                           width=25, font=FONT_TABLA,
                                           justify="center",
                                           state='disabled', style='my.TEntry')
                self.tabla.grid(row=i+1, column=j+1, padx=1, pady=2)
                if counter % 4 == 0:
                    self.tabla.configure(validate="key",
                                         validatecommand=vcmd_mo_parte)
                    self.mo_valor.append(self.tabla)
                if (counter-1) % 4 == 0:
                    self.tabla.configure(validate="key",
                                         validatecommand=vcmd_mo_parte)
                    self.np_valor.append(self.tabla)
                if (counter-2) % 4 == 0:
                    self.tabla.configure(validate="key",
                                         validatecommand=vcmd_longitud)
                    self.lini_valor.append(self.tabla)
                if (counter-3) % 4 == 0:
                    self.tabla.configure(validate="key",
                                         validatecommand=vcmd_longitud)
                    self.lfin_valor.append(self.tabla)
                counter += 1
                self.tabla_ent_valores.append(self.tabla)
            self.num_tabla.grid(row=i+1, column=0)
        total_entrys = len(self.tabla_ent_valores)
        for x in range(total_entrys):
            self.tabla_ent_valores[x].bind('<Return>', self.siguiente_entry)
        # self.mo_valor[0].configure(validate="key",validatecommand=vcmd_mo_parte)
        print("Se generaron {0} filas y {1} columnas".format(height, width))
        '''
        #Testing Getters l:278
        for i in range(15):
            self.lfin_valor[i].insert(0,"hola")
            '''

    def interfaz_salidas(self):
        # Configuracion
        if DEBUG == False or DEBUG == True:
            print("Desarrollo")
            self.ventana_main.lower(belowThis=None)
            messagebox.showwarning("Error",
                                    "Pagina en Desarrollo",
                                    parent=self.ventana_main)
            self.ventana_main.bell()
            self.ventana_main.lift(aboveThis=None)
            self.ventana_main.focus_set()
            return
        self.window_salidas = tk.Toplevel(self.master)
        self.window_salidas.title("Entradas de Proceso")
        self.window_salidas.focus_set()
        ent_top = self.window_salidas.winfo_toplevel()
        ent_top.rowconfigure(0, weight=1)
        ent_top.columnconfigure(0, weight=1)

        self.window_salidas.rowconfigure(0, weight=1)
        self.window_salidas.columnconfigure(0, weight=1)

        self.window_salidas.configure(background="#34a853")

        # Configurar ventana para maximizar, borrar barra y quitar opcion de cerrar.
        try:
            if PLATFORM == "Linux":
                print("Detectando Sistema Operativo Linux")
                w, h = self.winfo_screenwidth(), self.winfo_screenheight()
                self.window_salidas.overrideredirect(1)
                self.window_salidas.geometry("%dx%d+0+0" % (w, h))
                self.window_salidas.focus_set()  # <-- move focus to this widget
                self.window_salidas.bind("<Escape>",
                                          lambda e: self.window_salidas.destroy())
                self.window_salidas.protocol(
                    "WM_DELETE_WINDOW", self.disable_event)
            else:
                w, h = self.winfo_screenwidth(), self.winfo_screenheight()
                w, h = 1366, 768
                self.window_salidas.overrideredirect(1)
                self.window_salidas.geometry("%dx%d+0+0" % (w, h))
                self.window_salidas.focus_set()  # <-- move focus to this widget
                self.window_salidas.bind("<Escape>",
                                          lambda e: self.window_salidas.destroy())
                self.window_salidas.protocol(
                    "WM_DELETE_WINDOW", self.disable_event)
        except tk.TclError as error:
            print("Error Detectado: ", error)
            self.window_salidas.destroy()
            exit(1)

        # Interfaz
        # Primera linea
        self.tanda_num.set("hola")
        self.entradas_frame = ttk.Frame(self.window_salidas, borderwidth=5,
                                        relief="sunken", style='sal.TFrame')
        self.entrada_tanda_label = ttk.Label(self.entradas_frame,
                                             text="Tanda: ",
                                             style="sal.Label")
        self.entrada_tanda_entry = ttk.Entry(self.entradas_frame,
                                             font=FONT, width=8,
                                             textvariable=self.tanda_num,
                                             justify="center")
        self.entrada_peso_label = ttk.Label(self.entradas_frame, text="Peso: ",
                                            style="sal.Label")
        self.entrada_peso_entry = ttk.Entry(self.entradas_frame, font=FONT,
                                            width=8,
                                            textvariable=self.tanda_num,
                                            justify="center")
        self.boton_peso = ttk.Button(self.entradas_frame, text="Calcular",
                                     style="calc.TButton",
                                     cursor="hand2",
                                     command=self.disable_event)

        self.boton_enviar = ttk.Button(self.entradas_frame, text="Enviar",
                                       style="calc.TButton",
                                       cursor="hand2",
                                       command=self.disable_event)

        self.entradas_frame.grid(row=0, column=0)
        self.entrada_tanda_label.grid(row=0, column=0, padx=2, pady=10,
                                      sticky=E)
        self.entrada_tanda_entry.grid(row=0, column=1, padx=2, pady=10,
                                      sticky=W)
        self.entrada_peso_label.grid(row=0, column=2, padx=2, pady=10,
                                     sticky=E)
        self.entrada_peso_entry.grid(row=0, column=3, padx=2, pady=10,
                                     sticky=W)
        self.boton_peso.grid(row=0, column=4, padx=2, pady=10)

        self.tabla_frame = ttk.Frame(self.entradas_frame, borderwidth=5,
                                     relief="sunken", style='sal.TFrame')

        self.tabla_frame.grid(row=2, column=0, columnspan=5, sticky=N)
        self.boton_enviar.grid(row=3, column=4, sticky=E)

        self.tabla = {}
        self.tabla_titulos = ("Ciclo 1", "Ciclo 2", "Ciclo 3")
        self.tabla_subtitulos = ("Long_Final 1", "Long_Final 2", "Long_Final 1",
                                 "Long_Final 2", "Long_Final 1", "Long_Final 2")
        for k in range(6):
            self.subtitulo_tabla = ttk.Label(self.tabla_frame,
                                             text=str(
                                                 self.tabla_subtitulos[k]),
                                             style="salsubt.Label")
            self.subtitulo_tabla.grid(row=1, column=(k+1))

        self.ltitulo_tabla1 = ttk.Label(self.tabla_frame,
                                        text=str(self.tabla_titulos[0]),
                                        style="sal.Label")
        self.ltitulo_tabla2 = ttk.Label(self.tabla_frame,
                                        text=str(self.tabla_titulos[1]),
                                        style="sal.Label")
        self.ltitulo_tabla3 = ttk.Label(self.tabla_frame,
                                        text=str(self.tabla_titulos[2]),
                                        style="sal.Label")
        self.ltitulo_tabla1.grid(row=0, column=1, columnspan=2)
        # Cosa curiosa no me dejo hacerlo en for loop por que esta de abajo
        # Requeria instanciarse asi y no se por que pero funciono.
        self.ltitulo_tabla2.grid(row=0, column=2, columnspan=4)
        self.ltitulo_tabla3.grid(row=0, column=5, columnspan=6)

        counter = 0
        height = 15
        width = 6
        for i in range(height):  # Rows
            self.num_tabla = ttk.Label(self.tabla_frame, text=i+1,
                                       style="sal.Label")
            for j in range(width):  # Columns
                self.tabla[counter] = ttk.Entry(self.tabla_frame, text="",
                                                width=20, font=FONT_TABLA,
                                                justify="center")
                self.tabla[counter].grid(row=i+2, column=j+1, padx=1, pady=2)
                counter += 1
            self.num_tabla.grid(row=i+2, column=0)
        print("Se generaron {0} filas y {1} columnas".format(height, width))


    def interfaz_grafica(self):
        # Configuracion
        mpl.style.use("seaborn")
        #self.archivo_nombre = self.getdb_tanda()+1
        #self.archivo_nombre = "Grafico_Tanda_"+str(self.archivo_nombre)
        self.window_grafica = tk.Toplevel(self.master)
        self.window_grafica.title("Grafica de Control")
        self.window_grafica.focus_set()
        ent_top = self.window_grafica.winfo_toplevel()
        ent_top.rowconfigure(0, weight=1)
        ent_top.columnconfigure(0, weight=1)

        self.window_grafica.rowconfigure(0, weight=1)
        self.window_grafica.columnconfigure(0, weight=1)

        #self.window_grafica.configure(background="#f65314") #red
        self.window_grafica.configure(background="white") #white

        # Configurar ventana para maximizar, borrar barra y quitar opcion de cerrar.
        try:
            if PLATFORM == "Linux":
                print("Detectando Sistema Operativo Linux")
                w, h = self.winfo_screenwidth(), self.winfo_screenheight()
                self.window_grafica.overrideredirect(1)
                self.window_grafica.geometry("%dx%d+0+0" % (w, h))
                self.window_grafica.focus_set()  # <-- move focus to this widget
                #self.window_grafica.bind("<Escape>",
                #                          lambda e: self.window_grafica.destroy())
                self.window_grafica.bind("<Alt-Key-F4>",
                                lambda e: self.pass_cmd())
                self.window_grafica.protocol("WM_DELETE_WINDOW", self.pass_cmd)
            else:
                w, h = self.winfo_screenwidth(), self.winfo_screenheight()
                w, h = 1366, 768
                #self.window_entradas.overrideredirect(1)
                self.window_grafica.geometry("%dx%d+0+0" % (w, h))
                self.window_grafica.focus_set()  # <-- move focus to this widget
                #self.window_grafica.bind("<Escape>",
                #                          lambda e: self.window_grafica.destroy())
                self.window_grafica.bind("<Alt-Key-F4>",
                                lambda e: self.pass_cmd())
                self.window_grafica.protocol("WM_DELETE_WINDOW", self.pass_cmd)
        except tk.TclError as error:
            print("Error Detectado: ", error)
            self.window_grafica.destroy()
            exit(1)

        GW,GH = (w/DPI-2.5),(h/DPI-0.3)
        print(GW,GH)
        self.fig = plt.Figure(figsize=(GW,GH), dpi=DPI)

        canvas = FigureCanvasTkAgg(self.fig, master=self.window_grafica)
        canvas.get_tk_widget().config(relief=tk.FLAT,borderwidth=1)
        temp_frame =  tk.Frame(self.window_grafica)

        try:
            if PLATFORM == "Linux":
                self.temp=serial_temp("/dev/ttyUSB0")
            else:
                self.temp=serial_temp("COM20")
        except:
            self.window_grafica.lower(belowThis=None)
            messagebox.showwarning("Error", "Conectar puerto serie",
                                parent=self.window_grafica)
            self.window_grafica.bell()
            self.window_grafica.lift(aboveThis=None)
            self.window_grafica.focus_set()
            self.window_grafica.destroy()

        x = np.arange(1, 4601, 1)        # Primeros 100 datos
        y1 = [0] *4600				#Bando de Datos, y primeros 100 ceros
        y2 = [0] *4600
        y3 = [0] *4600
        y4 = [0] *4600					#Bando de Datos, y primeros 4600 ceros

        ax = self.fig.add_subplot(111,ylim=[20,131], xscale='linear', xticks=arange(0,4600,500), xlabel="Tiempo",ylabel="Temperatura Precondicionado", yticks=arange(20,131,10))

        ax.axis([0,4601,0,135])

        line1, = ax.plot(x, y1, 'blue', label='Exterior')
        line2, = ax.plot(x, y2, 'red', label='Interior')
        line3, = ax.plot(x, y3, 'green', label='Sensor 1')
        line4, = ax.plot(x, y4, 'brown', label='Sensor 2')

        ls = lines.Line2D([0,4000], [130,130],color='black')
        li = lines.Line2D([0,4000], [120,120],color='black')
        ax.add_line(ls)
        ax.add_line(li)
        ax.legend()

        self.temp_var_ext = StringVar()
        self.temp_var_int = StringVar()
        self.temp_var_s2 = StringVar()
        self.temp_var_s1 = StringVar()
        self.titulo_var =  StringVar()
        self.titulo_var.set(self.archivo_nombre)

        temp_frame.grid(column=0, row=1, sticky=N, pady=100)
        canvas.get_tk_widget().grid(column=1,padx=0,pady=0,row=1,sticky=N, rowspan = 20)

        label_temp_var_ext = tk.Label(temp_frame, text="", textvariable = self.temp_var_ext, font=("Consolas", 20), bg="white").grid(column=0, row=0, sticky = E)
        label_temp_var_ext = tk.Label(temp_frame, text="", textvariable = self.temp_var_int, font=("Consolas", 20), bg="white").grid(column=0, row=1, sticky = E)
        label_temp_var_ext = tk.Label(temp_frame, text="", textvariable = self.temp_var_s2, font=("Consolas", 20), bg="white").grid(column=0, row=2, sticky = E)
        label_temp_var_ext = tk.Label(temp_frame, text="", textvariable = self.temp_var_s1, font=("Consolas", 20), bg="white").grid(column=0, row=3, sticky = E)
        titulo = tk.Label(self.window_grafica,text="asdasdasd",textvariable= self.titulo_var, font=("Consolas", 20), bg="white").grid(column=0, row=0, columnspan=2, sticky=S)
        

        def animate(i):
            if self.data<4600:
                del y1[0]
                del y2[0]
                del y3[0]
                del y4[0]

                buffer=self.temp.get_data()
                try:
                    self.temp_ext=float(self.temp.get_data()[0])
                    self.temp_int=float(self.temp.get_data()[1])
                    self.temp_s2=float(self.temp.get_data()[2])
                    self.temp_s1=float(self.temp.get_data()[3])
                except Exception as e:
                    print(e)
                y1.append(self.temp_ext)
                y2.append(self.temp_int)
                y3.append(self.temp_s2)
                y4.append(self.temp_s1)
                line1.set_ydata(y1)
                line2.set_ydata(y2)
                line3.set_ydata(y3)
                line4.set_ydata(y4)
                self.temp_var_ext.set("Exterior: "+ str("{0:.2f}".format(self.temp_ext)))
                self.temp_var_int.set("Interior: "+ str("{0:.2f}".format(self.temp_int)))
                self.temp_var_s2.set( "Sensor 2: "+ str("{0:.2f}".format(self.temp_s2)))
                self.temp_var_s1.set( "Sensor 1: "+ str("{0:.2f}".format(self.temp_s1)))
                self.num_data +=1
                print("Archivo numero: {0:07d}  Nombre: {1}".format(self.num_data, self.archivo_nombre))

                if PLATFORM == "Linux":
                    file = open("./graficas/"+self.archivo_nombre+".csv", "a")
                    file.write(str(dt.datetime.now())+","+str(self.temp_ext)+","+str(self.temp_int)+","+str(self.temp_s2)+","+str(self.temp_s1)+"\n")
                    file.close()
                else:
                    file = open(os.getcwd()+"\\graficas\\"+self.archivo_nombre+".csv", "a")
                    file.write(str(dt.datetime.now())+","+str(self.temp_ext)+","+str(self.temp_int)+","+str(self.temp_s2)+","+str(self.temp_s1)+"\n")
                    file.close()

            return line1, line2, line3, line4,

        

        
            
        self.ani = animation.FuncAnimation(self.fig, animate, frames=None, interval=30000, blit=False)

    def close_grafica(self):
        self.window_grafica.lower(belowThis=None)
        messagebox.showwarning("Error", "Una vez iniciada no cerrarla",
                               parent=self.window_grafica)
        self.window_grafica.bell()
        self.window_grafica.lift(aboveThis=None)
        self.window_grafica.focus_set()

    def disable_event(self):
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

    def getdb_tanda(self):
        self.con = sqlite3.connect("precondicionado.db",
                                   detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        self.c = self.con.cursor()
        cmd = "SELECT COUNT(*) FROM TANDA"
        self.c.execute(cmd)
        dato = str(self.c.fetchone())
        s = int(0)
        for s in dato:
            if s.isdigit():
                s = int(s)
                print(type(s))
                return s

    def calcular_peso(self):
        if DEBUG != True:
            if PLATFORM == "Linux":
                self.pesa = bascula()
            else:
                self.pesa = bascula()
            
            self.peso_lista = self.pesa.get_peso()
            if (float(self.peso_lista[0]) > 0):
                self.peso.set(self.peso_lista[0]+" kg")
                ciclos = regresion.Regresion(
                    9514, 125, 90, float(self.peso_lista[0]), 9)
                ciclos = round(ciclos, 2)
                self.ciclo_value.set(ciclos)
                x = self.ciclo_value.get()
                texto = "Ciclos Requeridos :{0}".format(x)
                self.ciclo_text.set(str(texto))
                self.ciclo_label.configure(style='ent.Label')
            else:
                self.window_entradas.lower(belowThis=None)
                messagebox.showwarning("Error de Conexion",
                                       "Coloque material en la bascula",
                                       parent=self.window_entradas)
                self.window_entradas.bell()
                self.window_entradas.lift(aboveThis=None)
                self.window_entradas.focus_set()
        else:
            print("Modo Debug")
            self.peso_lista = ("1234", "kg")
            self.peso.set(self.peso_lista[0]+" kg")
            self.ciclo_value.set(1231.23)
            x = self.ciclo_value.get()
            texto = "Ciclos Requeridos :{0}".format(x)
            self.ciclo_text.set(str(texto))
            self.ciclo_label.configure(style='ent.Label')


    def onValidate_mo_parte(self, d, i, P, s, S, v, V, W):
        """
        Metodo evalua y valida si se lee numeros de un entry.
        """
        if S.isdigit() or S == "." or S == "-":
            return True
        else:
            self.window_entradas.lower(belowThis=None)
            messagebox.showwarning("Warning", "Solo Numeros flotantes",
                                   parent=self.window_entradas)
            self.window_entradas.bell()
            self.window_entradas.lift(aboveThis=None)
            self.window_entradas.focus_set()
            self.bell()
            return False

    def onValidate_longitud(self, d, i, P, s, S, v, V, W):
        """
        Metodo evalua y valida si se lee numeros y puntos de un entry.
        """
        if S.isdigit():
            return True
        else:
            self.window_entradas.lower(belowThis=None)
            messagebox.showwarning("Warning", "Solo numeros Enteros, sin decimales",
                                   parent=self.window_entradas)
            self.window_entradas.bell()
            self.window_entradas.lift(aboveThis=None)
            self.window_entradas.focus_set()
            self.bell()
            return False

    def siguiente_entry(self, event):
        x = len(self.tabla_ent_valores[self.contador_entry_enable].get())
        print(x)
        if self.contador_entry_enable != 59 and x > 0:
            self.contador_entry_enable += 1
            self.tabla_ent_valores[self.contador_entry_enable].configure(
                state='enabled')
            self.tabla_ent_valores[self.contador_entry_enable].focus_set()

    def enviar_db(self):
        x = 0
        if (float(self.peso_lista[0]) > 0):
            for i in range(15):
                if self.mo_valor[i].get() != "" and self.np_valor[i].get() != "" and self.lini_valor[i].get() != "" and self.lfin_valor[i].get() != "":
                    '''
                    print(self.mo_valor[i].get())
                    print(self.np_valor[i].get())
                    print(self.lini_valor[i].get())
                    print(self.lfin_valor[i].get())
                    '''
                    x += 1
            if x <= 0:
                self.window_entradas.lower(belowThis=None)
                messagebox.showerror("Error", "Ninguna Fila esta Completa",
                                     parent=self.window_entradas)
                self.window_entradas.bell()
                self.window_entradas.lift(aboveThis=None)
                self.window_entradas.focus_set()
                self.bell()
            else:
                self.window_entradas.lower(belowThis=None)
                if messagebox.askyesno("Base de datos", "Se van Agregar {} filas".format(x), parent=self.window_entradas):
                    print("enviar a la base de datos")
                    self.db_entrada_set(x)
                self.window_entradas.bell()
                self.window_entradas.lift(aboveThis=None)
                self.window_entradas.focus_set()
                self.bell()
        else:
            self.window_entradas.lower(belowThis=None)
            messagebox.showerror("Error", "Coloque las piezas y presione Calcular",
                                 parent=self.window_entradas)
            self.window_entradas.bell()
            self.window_entradas.lift(aboveThis=None)
            self.window_entradas.focus_set()
            self.bell()

    def pass_cmd(self):
        print("PASS")
        pass
    
    def askstring_close(self):
        self.contra = simpledialog.askstring("CONTRASEÑA", "DIGITE CONTRA", show='*',
                                        parent=self.master)
        if self.contra == "1945":
            self.master.destroy()
            quit()
        else:
            print("Error no escribio nada")
            return


    def asktring_name(self):
        self.archivo_nombre = simpledialog.askstring("NOMBRE DE LA GRAFICA", "PORFAVOR INSERTE EL NOMBRE DE LA GRAFICA",
                                        parent=self.master)
        if self.archivo_nombre != "":
            print("Nombre de la grafica ", self.archivo_nombre)
            self.interfaz_grafica()
        else:
            print("Error no escribio nada")
            return
        try:
            #self.archivo_nombre = self.getdb_tanda()+1
            #self.archivo_nombre = "Grafico_Tanda_"+str(self.archivo_nombre)
            #self.archivo_nombre=self.nombre_grafica
            if PLATFORM == "Linux":
                file = open("./graficas/"+self.archivo_nombre+".csv", "a") #se crea un archivo con la fecha y el nombre
                if os.stat("./graficas/"+self.archivo_nombre+".csv").st_size == 0:
                    file.write("Fecha,Exterior,Interior,Sensor 2,Sensor 1\n")
                    file.close()
            else:
                file = open(os.getcwd()+"\\graficas\\"+self.archivo_nombre+".csv", "a") #se crea un archivo con la fecha y el nombre
                if os.stat(os.getcwd()+"\\graficas\\"+self.archivo_nombre+".csv").st_size == 0:
                    file.write("Fecha,Exterior,Interior,Sensor 2,Sensor 1\n")
                    file.close()
        except Exception as e:
            print(e)

    def db_entrada_set(self, x):
        """[summary]
        
        Arguments:
            x {[type]} -- [description]
        """
        con = sqlite3.connect("precondicionado.db",
        detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        c = con.cursor()
        now = datetime.datetime.now()

        PESO = self.peso_lista[0]
        TANDA = self.tanda_num.get()
        print(type(TANDA))
        company_sql = "INSERT INTO TANDA(FECHA, PESO) VALUES (?,?)"  
        c.execute(company_sql, (now, PESO))
        con.commit()

        for i in range(15):
            if self.mo_valor[i].get() != "" and self.np_valor[i].get() != "" and self.lini_valor[i].get() != "" and self.lfin_valor[i].get() != "":
                MO = int(self.mo_valor[i].get())
                NP = str(self.np_valor[i].get())
                MEDIDA_INI1 = int(self.lini_valor[i].get())
                MEDIDA_INI2 = int(self.lfin_valor[i].get())
                company_sql = '''INSERT INTO CICLO(
                    MO,
                    NP,
                    MEDIDA_INI1,
                    MEDIDA_INI2,
                    MEDIDA_FINA1,
                    MEDIDA_FINA2,
                    MEDIDA_FINB1,
                    MEDIDA_FINB2,
                    RESULTADO_A1,
                    RESULTADO_A2,
                    RESULTADO_B1,
                    RESULTADO_B2,
                    ESTADO,
                    TANDA_ID
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
                c.execute(company_sql, (MO, NP, MEDIDA_INI1, MEDIDA_INI2,0,0,0,0,0,0,0,0,0, TANDA))
                con.commit()


        """
        MO=int(MO)
        NP=str(NP)
        PESO=float(PESO)
        MEDIDA_INI1=int(MEDIDA_INI1)
        MEDIDA_INI2=int(MEDIDA_INI2)
        self.con = sqlite3.connect("testing.db",
                                   detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.c = self.con.cursor()
        company_sql = "INSERT INTO PRECONDICIONADO(FECHA, MO, NP, PESO, MEDIDA_INI1, MEDIDA_INI2) VALUES (?,?,?,?,?,?)"  
        c.execute(company_sql, (now, MO, NP, PESO, MEDIDA_INI1, MEDIDA_INI2))
        con.commit()
        dato = str(self.c.fetchone())
        """


if __name__ == '__main__':
    ROOT = tk.Tk()
    s = ttk.Style(ROOT)
    print(str(s.theme_names()))
    themes = ('winnative', 'clam', 'alt', 'default',
              'classic', 'vista', 'xpnative')
    s.theme_use(themes[1])
    APP = App(ROOT)  
    APP.mainloop()