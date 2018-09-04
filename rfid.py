import serial

def read_rfid ():
   ser = serial.Serial ("/dev/ttyAMA0")
   ser.baudrate = 9600
   data = ser.read(12)
   ser.close ()
   return data

id = read_rfid ()
print id