#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522
#from pad4pi import rpi_gpio
import time
s="0"
x=1
###KEYPAD SETUP ####

import time

GPIO.setmode(GPIO.BOARD)

MATRIX = [ ['1','2','3','A'],
           ['4','5','6','B'],
           ['7','8','9','C'],
           ['*','0','#','D'] ]

COL = [7, 29, 31, 33]
ROW = [32, 37, 3, 5]

reader = SimpleMFRC522.SimpleMFRC522()
for j in range (4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 1)

for i in range (4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

#### DEFINE USERS ####
class user:
    def __init__(self,name,uid,password,balance):
        self.name = name
        self.uid = uid
        self.password = password
        self.balance = balance

user1= (user("Keval","355163578266","1234","1000"))
user2= (user("Ishan","719327078343","1234","1000"))
 
def keypad():
    x=1
    s="0"
    try:
        while(x):
            for j in range (4):
                GPIO.output(COL[j],0)

                for i in range (4):
                    if GPIO.input (ROW[i]) == 0:
                        #print (MATRIX[i][j])
                        s=s+str(MATRIX[i][j])
                        if(len(s)==5):
                            print(int(s))
                            x=0
                        while (GPIO.input(ROW[i]) == 0):
                            pass
        
                GPIO.output(COL[j],1)
    
    except KeyboardInterrupt:
        GPIO.cleanup()
    return int(s)    
#keypad.registerKeyPressHandler(printKey)


#### MAIN LOOP ####
try:
        print(" Welcome to SVM 1.0")
        print("Scan your card!")
        continue_reading = True
        while continue_reading:
            id, text = reader.read()
            print(id)
            if (id == 355163578266):
                print("Name : Keval")
                password = keypad()
                
                continue_reading = False
            elif (id == 719327078343):
                print("Name : Ishan")
                password = keypad()
                continue_reading = False
            else:
                print("not found")
        
finally:
        GPIO.cleanup()