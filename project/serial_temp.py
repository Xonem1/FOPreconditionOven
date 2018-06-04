import sys
import glob
import serial
import platform

PLATFORM = platform.system()

class serial_temp:
    def __init__(self,comport):
        self.ser = serial.Serial()
        self.ser.port = comport
        self.ser.baudrate = 115200
        self.ser.timeout = 10
        self.ser.open()
    

    
    def get_data(self):
        #CHECAR EL LUNES
        msg_token= "0\r\n"
        if self.ser.is_open:
            self.ser.flush()
            buffer=self.ser.readline()
            self.ser.write(b'P\r\n')
            msg = self.ser.readline()
            msg = str(msg.decode("utf-8"))
            while msg == msg_token or msg == "":
                self.ser.write(b'P\r\n')
                msg = self.ser.readline()
                msg = str(msg.decode("utf-8"))
            msg = msg.split(",")
            return msg

        #self.ser.close()

    def get_serial_ports(self):
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
                #print(result)
            except (OSError, serial.SerialException):
                pass
        return result

if __name__ == '__main__':
    x = serial_temp("COM20")
    while True:
        print(x.get_data())