# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 17:19:46 2018

@author: ESQUER_J
"""

from datetime import datetime, timedelta

def float_to_hour(value = 0):
    if isinstance(value, float):
        print(value%1.0)
        print(timedelta(hours = 8.24))
        pass
    else:
        print("Error, valor ingresado no es flotante.")
    
if __name__ == '__main__':
    float_to_hour(1.23)