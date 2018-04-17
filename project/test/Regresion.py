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
        CICLOS =  (+15.46 + (-0.2027*X1) + (-0.1161*X2) + (0.809*X3) + (0.001388*X1*X2) + (-0.00740*X2*X3) + (SHRINK))/0.3074
        print(CICLOS)
        pass
    elif TIPO == 500:
        pass
    else:
        print("ERROR: No se encuentra en la base de datos")
        pass

if __name__ == '__main__':
    Regresion(490, 125, 90, 15.8, 7)