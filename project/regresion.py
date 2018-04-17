# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:29:34 2018

@author: ESQUER_J
"""

def Regresion(TIPO, TEMPERATURA, TIEMPO, QTY, SHRINK = 0):
    X1 = TEMPERATURA
    X2 = TIEMPO
    X3 = QTY
    if TIPO == 490:
        CICLOS = (-1*((-15.59)+(0.1934*X1)+(0.1273*X2)+(-0.405*X3)+(-0.001388*X1*X2)+(0.00392*X2*X3)) + SHRINK)/0.3007
        print(CICLOS)
        return(CICLOS)
        pass
    elif TIPO == 500:
        pass
    else:
        print("ERROR: No se encuentra en la base de datos")
        pass

if __name__ == '__main__':
    Regresion(490, 100, 90, 3.2, 4.9525)