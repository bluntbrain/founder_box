import RPi.GPIO as GPIO
import time
s="0"
x=1
GPIO.setmode(GPIO.BOARD)

MATRIX = [ [1,2,3,'A'],
           [4,5,6,'B'],
           [7,8,9,'C'],
           [0,'F','E','D'] ]

COL = [7, 29, 31, 33]
ROW = [32, 37, 3, 5]

for j in range (4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 1)

for i in range (4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

try:
    while(x):
        for j in range (4):
            GPIO.output(COL[j],0)

            for i in range (4):
                if GPIO.input (ROW[i]) == 0:
                    print (MATRIX[i][j])
                    s=s+str(MATRIX[i][j])
                    if(len(s)==5):
                        print(int(s))
                        x=0
                    while (GPIO.input(ROW[i]) == 0):
                        pass

            GPIO.output(COL[j],1)
except KeyboardInterrupt:
    GPIO.cleanup()