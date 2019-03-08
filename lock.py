import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
s=""
for i in range(4):
    print("do you want to open lock "+str(i+1))
    s=s+str(input())
if s[0]=='1':
    GPIO.output(17,GPIO.HIGH)
    print"lock 1 opened"
if s[0]=='0':
    GPIO.output(17,GPIO.LOW)
    print"lock 1 Closed"
if s[1]=='1':
    GPIO.output(19,GPIO.HIGH)
    print"lock 2 opened"
if s[1]=='0':
    GPIO.output(19,GPIO.LOW)
    print"lock 2 Closed"
if s[2]=='1':
    GPIO.output(20,GPIO.HIGH)
    print"lock 3 opened"
if s[2]=='0':
    GPIO.output(20,GPIO.LOW)
    print"lock 3 Closed"
if s[3]=='1':
    GPIO.output(21,GPIO.HIGH)
    print"lock 4 opened"
if s[3]=='0':
    GPIO.output(21,GPIO.LOW)
    print"lock 4 Closed"
time.sleep(10)
GPIO.cleanup()