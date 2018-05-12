# -*- coding: utf-8 -*-
"""
Created on Sat Apr 21 07:44:40 2018

@author: ESQUER_J
"""

import sqlite3
import datetime

now = datetime.datetime.now()
print(now)
def connect():
    con = sqlite3.connect("precondicionado.db",
                          detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    print("Base de datos creada")
    c = con.cursor()
    return c, con

def create_db():
    db=connect()
    c=db[0]
    con=db[1]
    c.execute('''
              CREATE TABLE TANDA(
              ID INTEGER PRIMARY KEY AUTOINCREMENT,
              FECHA timestamp,
              PESO REAL
              )''')

    c.execute('''
              CREATE TABLE CICLO(
              ID INTEGER PRIMARY KEY AUTOINCREMENT,
              MO INT NOT NULL,
              NP TEXT NOT NULL,
              MEDIDA_INI1 INT NOT NULL,
              MEDIDA_INI2 INT NOT NULL,
              MEDIDA_FINA1 INT NOT NULL,
              MEDIDA_FINA2 INT NOT NULL,
              MEDIDA_FINB1 INT NOT NULL,
              MEDIDA_FINB2 INT NOT NULL,
              ESTADO INT NOT NULL,
              PRECON_ID INT NOT NULL,
              FOREIGN KEY(PRECON_ID) REFERENCES PRECONDICIONADO(ID) ON DELETE CASCADE
              )''')


    con.close()
    
    
def insert_dbt1(c,con):
    company_sql = "INSERT INTO PRECONDICIONADO(FECHA, MO, NP, PESO, MEDIDA_INI1, MEDIDA_INI2) VALUES (?,?,?,?,?,?)"  
    c.execute(company_sql, (now, 123123123, "PCHARMAN123", 15.05, 32123, 30004))
    con.commit()
    
def insert_dbt2(c,con):
    company_sql = "INSERT INTO CICLO1(MEDIDA_FIN1, MEDIDA_FIN2, ESTADO, PRECON_ID) VALUES (?,?,?,?)" 
    c.execute(company_sql, (123123,123123,1,1))
    con.commit()


def select_db(company_id,c):
    company_sel = "SELECT * FROM CICLO1 WHERE PRECON_ID=?"
    c.execute(company_sel, (company_id,))
    print(c.fetchall())
    return c.fetchall()

def select_db_all(c):
    company_sel = "SELECT * FROM TANDA"
    c.execute(company_sel)
    x =(c.fetchall())
    return x

def test():
    insert_dbt1()
    insert_dbt2()

def getdb_tanda():
    c=connect()
    c=c[0]
    print(c)
    cmd = "SELECT COUNT(*) FROM TANDA"
    c.execute(cmd)
    dato=str(c.fetchone())
    s = int(0)
    for s in dato:
        if s.isdigit():
            s = int(s)
            print(type(s))
            print(s)
    
#con.close()
create_db()
#x = select_db_all()
#print(x)
#test()
#select_db(1)
#getdb_tanda()