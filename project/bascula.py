# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 10:11:55 2018

@author: ESQUER_J
"""
import sys
import glob
import serial

class bascula:
    '''
    Programa se encarga de la comunicacion de la bascula con el programa principal
    Primeramente se le proporcionara un Puerto
    Retornara 1 lista de peso y unidad
    Ejemplo:
        x.set_com(com)
        value =x.get_peso()
    '''
    def __init__(self):
        print("Puertos Seriales Disponibles: " + str(self.serial_ports()))
        com = str(self.serial_ports())
        com = com[2:-2]
        print(com)
        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.port = None
        self.ser.timeout = 10
        self.last_peso = None
        self.unidad = None
        self.set_com(com)
        
    def serial_ports(self):
        """ Lists serial port names
    
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
                https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        elif sys.platform.startswith ('linux'):
            ports = glob.glob ('/dev/tty[A-Za-z]*')
        else:
            raise EnvironmentError('Unsupported platform')
    
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def set_com(self, COM):
        self.ser.port = COM

    def open(self):
        FAIL = "NOCOMPORT"
        COM = str(self.ser.port)
        try:
            if COM != FAIL:
                try:
                    self.ser.open()
                    if self.ser.is_open:
                        #time.sleep(1)
                        print("Puerto Conectado: "+ str(self.ser.port))
                    else:
                        print("Error: El siguiente peurto no se encontro "+ str(self.ser.port))
                except Exception as error:
                    print("error de conexion l81")
                    print(error)
            else:
                print("Inicialice un puerto con self.ser.port = PUERTO")
        except Exception as error:
            print(error)

    def get_peso(self):
        try:
            self.open()
        except Exception as e:
            print("El puerto esta cerrado" +str(e))
        if self.ser.is_open:
            print("Obteniendo datos")
            self.ser.write(b'P\r\n')
            msg = self.ser.readline()
            #print(msg)
            msg = str(msg.decode("utf-8"))
            #print(msg)
            try:
                msg = msg.strip().split(" ")
                #print(msg)
                self.last_peso = msg[0]
                self.unidad = msg[1]
            except Exception as e:
                print("No es una lista la entrada del COM: "+str(e))
            self.ser.close()
            return msg


if __name__ == '__main__':
    x = bascula()
    value =x.get_peso()
    print(value)
    print(x.last_peso)
    print(x.unidad)
    