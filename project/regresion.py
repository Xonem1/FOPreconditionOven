# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:29:34 2018

@author: ESQUER_J
"""

def Regresion(LONGITUD, TEMPERATURA, TIEMPO, QTY, SHRINK = 0):
    X1 = LONGITUD
    X2 = TEMPERATURA
    X3 = TIEMPO
    X4 = QTY
    TIPO = 490
    SHRINK = (SHRINK*100)+200
    if TIPO == 490:
        #CICLOS = (-1*((-15.59)+(0.1934*X1)+(0.1273*X2)+(-0.405*X3)+(-0.001388*X1*X2)+(0.00392*X2*X3)) + SHRINK)/0.3007
        CICLOS=(-1*((-1526)+(0.03052*X1)+(18.84*X2)+(10.76*X3)-(91.4*X4)-(0.000001*X1*X1)+(0.000736*X1*X4)-(0.1344*X2*X3)+(0.8197*X3*X4))+SHRINK)/30.34
        print(CICLOS)
        return(CICLOS)
        pass
    elif TIPO == 500:
        pass
    else:
        print("ERROR: No se encuentra en la base de datos")
        pass

if __name__ == '__main__':

    Regresion(9514, 125, 90, 15.05, 9)
    
    