#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2017 Jesus Alberto Esquer Inzunza <beldom13@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
#---------
#---------End of 


#---------Imports
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as Tk
from tkinter import Text, BOTH, W, N, E, S
from tkinter.ttk import Frame, Button, Label, Style
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.lines as lines
import time
import datetime as dt
import os
import sys
from matplotlib import gridspec
import platform


#---------End of imports

#---------Constants

ON=True
OFF=False
RUN=False
LOGTIME=0
DPI=100
GW=0
GH=0
hola="Hola"
RUN=True
PLATFORM = platform.system()

#---------End of Constants


#---------Variables
#Definir Variables
inicio = time.time()
tinutil=0.0
ttotal=0.0
tlog=time.time()
Timex=0
Datos=0
tiempocuba = 0
data=100
segundo=1
varianza=0
promedio=0
z=[]
counter=0
muestra=10
cpkvar=0
cpvar=0


#---------End of Variables

#Menu de inicio parametros etc.
print(" El programa consiste en graficar el procentaje de metalizacion")
print(" de una cuba con la siguiente formula.")
print("  %Metl = T(vacio)/T(Total)")
print(" ")
try:
	NAME=str(input(" Porfavor Ingrese el nombre de la Cuba: ")) #Nombre
except:
	print("Limite Superior, inferior, muestras de capacidad")
	print("y numero de datos guardados deben ser numeros enteros")
	print("Presione cualquier tecla para salir")
	sys.exit()
try:
	LALTO=int(input(" Ingrese valor de limite superior: ")) #Limite1
except:
	print("Limite Superior, inferior, muestras de capacidad")
	print("y numero de datos guardados deben ser numeros enteros")
	print("Presione cualquier tecla para salir")
	sys.exit()
try:
	LBAJO=int(input(" Ingrese valor de limite inferior: ")) #Limite2
except:
	print("Limite Superior, inferior, muestras de capacidad")
	print("y numero de datos guardados deben ser numeros enteros")
	print("Presione cualquier tecla para salir")
	sys.exit()
try:
	LOGTIME=int(input(" Intervalo de Guardado(seg): "))
except:
	print("Limite Superior, inferior, muestras de capacidad")
	print("y numero de datos guardados deben ser numeros enteros")
	print("Presione cualquier tecla para salir")
	sys.exit()
try:
	muestra=int(input(" Numero de muestras para calculo de capacidad: "))
except:
	print("Limite Superior, inferior, muestras de capacidad")
	print("y numero de datos guardados deben ser numeros enteros")
	print("Presione cualquier tecla para salir")
	sys.exit()
print("	Cargando Datos..")



#Configurar entradas de sensores

#Crear Log
now=str(dt.datetime.now()) #obtenemos la fecha de creacion
now=now.replace(" ","-") #cambiamos los espacios por guiones
nombreprueba= "probe-" #nombre
namenow=str(NAME)
namenow=namenow.replace(" ","-") #cambiamos los espacios por guiones
if PLATFORM == "Linux":
	file = open("/home/pi/Desktop/LogsPlatinado/"+namenow+".csv", "a") #se crea un archivo con la fecha y el nombre
	print("Fecha de inicio: "+str(now))
	if os.stat("/home/pi/Desktop/LogsPlatinado/"+namenow+".csv").st_size == 0:
		file.write("Fecha,Tiempo Total,Tiempo activo,Porcentaje,Cpk,Cp\n")
		file.close()
else:
	file = open(os.getcwd()+"\\"+namenow+".csv", "a") #se crea un archivo con la fecha y el nombre
	print("Fecha de inicio: "+str(now))
	if os.stat(os.getcwd()+"\\"+namenow+".csv").st_size == 0:
		file.write("Fecha,Tiempo Total,Tiempo activo,Porcentaje,Cpk,Cp\n")
		file.close()

#Verificacion final

if LALTO>100 or LBAJO>100:
	print("")
	print("")
	print("	 ERROR = Los limites deben ser menores a 100")
	pass

elif LALTO<0 or LBAJO<0:
	print("")
	print("")
	print("	 ERROR = Los limites deben ser mayores a 0")
	pass

elif LBAJO>=LALTO:
	print("")
	print("")
	print("	 ERROR = El limite inferior, debe ser superior al limite superior.")
	pass

else:
	RUN=False
	tlog=time.time()
	# Empezar Ciclo Loop
	print("")
	print("")
	print("	Iniciando...")
	time.sleep(1)

if RUN:
	input("Presione cualquier tecla para salir")
	sys.exit()


def Cp(mylist, usl, lsl):
    arr = np.array(mylist)
    arr = arr.ravel()
    sigma = np.std(arr)
    Cp = float(usl - lsl) / (6*sigma)
    return Cp


def Cpk(mylist, usl, lsl):
    arr = np.array(mylist)
    arr = arr.ravel()
    sigma = np.std(arr)
    m = np.mean(arr)

    Cpu = float(usl - m) / (3*sigma)
    Cpl = float(m - lsl) / (3*sigma)
    Cpk = np.min([Cpu, Cpl])
    return Cpk


def animate(i):
	global tideal
	global inicio
	global ani
	global data
	global tinutil
	global tiempocuba
	global ttotal
	global tlog
	global Timex
	global Datos
	global LOGTIME
	global file
	global segundo
	global LALTO
	global LBAJO
	global varianza
	global promedio
	global x
	global counter
	global z
	global muestra
	global cpvar
	global cpkvar
	

	
	if((time.time()-inicio)>1): #Apartado para crear log
		ttotal=ttotal+1
		tinutil=ttotal
		tiempocuba=tinutil/ttotal
		#print(str(tiempocuba)+" "+str(tinutil)+" "+str(ttotal))
		data=(tiempocuba)*100
		inicio=time.time()
		#ax.text(50,50,"Datos Guardados: "+str(Datos),color='blue')
		ldatos.set("Datos: "+str(Datos))
		#print(counter<len(z))
		if(counter<muestra):
			z.insert(counter,data)
			#print(len(z))
			counter+=1
		else:
			cpvar=(Cp(z, LALTO, LBAJO))
			cpkvar=(Cpk(z, LALTO, LBAJO))
			#print("CPK: "+str(Cpk(z, LALTO, LBAJO)))
			#print("CP: "+str(Cp(z, LALTO, LBAJO)))
			lcp.set("CP: "+str(cpvar))
			lcpk.set("CPK: "+str(cpkvar))
			counter=0
			print("Datos en Z: "+str(z))
			z=[]
			print(z)
		
		
	del y[0]
	#y.append((1/(i+1))*100)
	y.append(data)
	line.set_ydata(y)  # update the data
	#print(y[99])
	

	
##
	if PLATFORM == "Linux":
		if (time.time()-tlog)>=LOGTIME:
			file = open("/home/pi/Desktop/LogsPlatinado/"+namenow+".csv", "a")
			file.write(str(dt.datetime.now())+","+str(ttotal/60)+","+str(tinutil/60)+","+str(tiempocuba)+","+str(cpkvar)+","+str(cpvar)+"\n")
			tlog=time.time()
			Datos = Datos + 1
			file.close()
	else:
		if (time.time()-tlog)>=LOGTIME:
			file = open(".\\"+namenow+".csv", "a")
			file.write(str(dt.datetime.now())+","+str(ttotal/60)+","+str(tinutil/60)+","+str(tiempocuba)+","+str(cpkvar)+","+str(cpvar)+"\n")
			tlog=time.time()
			Datos = Datos + 1
			file.close()
##
	#print((time.time()-inicio))
	return line,

root = Tk.Tk()  	    #Aqui creo mi ventana
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
print(w,h)
GW,GH = (w/DPI)-2,(h/DPI)-2
#root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
print(GW,GH)
#fig = plt.Figure()
#fig =plt
fig = plt.Figure(figsize=(GW,GH), dpi=DPI)
#fig.Figure(figsize=(GW,GH), dpi=DPI)
#fig = plt.Figure(figsize=(1,2), dpi=DPI)

x = np.arange(1, 101, 1)        # Primeros 100 datos
y = [0] *100					#Bando de Datos, y primeros 100 ceros
root.title("Proceso de Metalizacion")

ltitulo=Tk.StringVar()		#Creo una variable para el texto
lcp=Tk.StringVar()		#Creo una variable para el texto
lcpk=Tk.StringVar()
ldatos=Tk.StringVar()
llims=Tk.StringVar()
llimi=Tk.StringVar()

titulo = Tk.Label(root,text="",textvariable=ltitulo,font=("Monospace", 20)).grid(column=0, row=0, columnspan=2)
info = Tk.Label(root,text="Informacion",font=("Monospace", 12)).grid(column=0, row=1,padx=11,pady=5)
labelcp = Tk.Label(root,text="",textvariable=lcp).grid(column=0, row=2,sticky=W,padx=2)
labelcpk = Tk.Label(root,text="",textvariable=lcpk).grid(column=0, row=3,sticky=W,padx=2)
datos = Tk.Label(root,text="",textvariable=ldatos).grid(column=0, row=4,sticky=W,padx=2)
lims = Tk.Label(root,text="",textvariable=llims).grid(column=0, row=5,sticky=W,padx=2)
limi = Tk.Label(root,text="",textvariable=llimi).grid(column=0, row=6,sticky=W,padx=2)


ltitulo.set("Metalizacion: " +NAME)
lcp.set("CP: Espere")
lcpk.set("CPK: Espere")
ldatos.set("Datos: ")
llims.set("Lim Sup: "+str(LALTO))
llimi.set("Lim Inf: "+str(LBAJO))

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=1,padx=10,pady=0,row=1,rowspan=15,sticky=W)
canvas.get_tk_widget().config(relief=Tk.RIDGE,borderwidth=10)
#canvas.get_tk_widget().grid_propagate(True)



ax = fig.add_subplot(111,ylim=[0,1], xscale='linear', xticks=arange(0,101,10), xlabel="Tiempo",ylabel="Porcentaje de Metalizacion", yticks=arange(0,101,10))

ls = lines.Line2D([0,100], [LALTO,LALTO],color='red')
li = lines.Line2D([0,100], [LBAJO,LBAJO],color='red')
ax.text(2,LALTO+2,"Limite Superior",color='red')
ax.text(2,LBAJO+2,"Limite Inferior",color='red')
ax.add_line(ls)
ax.add_line(li)
ax.axis([0,100,0,105])
line, = ax.plot(x, y)

def main(args):
	Tk.mainloop()
ani = animation.FuncAnimation(fig, animate, frames=None, interval=1000, blit=False)

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
