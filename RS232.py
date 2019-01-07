import serial
import time

x=1;
serialport = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.5)
s=""
while x:
    if serialport.inWaiting()>0:
        for i in range(7):
            s=s+serialport.read()
        if len(s) > 4:
            x=0;
        time.sleep(1)
print str(s)
