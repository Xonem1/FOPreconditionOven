import serial
ser = serial.Serial('COM7', 9600)
x = 0
while x < 70:
    print(ser.readline())
    x = x + 1
ser.close()
print("fin")
