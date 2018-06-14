#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import pymysql
import time
import serial


continue_reading = True
product1_name = 'perfume'
product1_weight = 0.181
product1_price = 70
product2_name = 'pens'
product2_weight = 0.010
product2_price = 5
BuzzerPin = 11 # Raspberry Pi Pin 17-GPIO 17


def fetch_data(rfid):
    db = pymysql.connect(host='localhost', port=3306, user='username', database='mydb', password='password')
    cur = db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM payment WHERE rfid ='%s'"
    cur.execute(sql % rfid)
    #if(cur.fetchone() > 0):
    #   print('Found!')
    for row in cur:
        return row

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()
    GPIO.output(BuzzerPin, GPIO.LOW)
    GPIO.output(BuzzerPin, GPIO.HIGH)

def buzzer(number_of_times, buzzer_frequency):
    global BuzzerPin
    GPIO.setmode(GPIO.BOARD) # Set GPIO Pin As Numbering
    GPIO.setup(BuzzerPin, GPIO.OUT)
    for i in range(number_of_times):
        GPIO.output(BuzzerPin, GPIO.LOW)
        time.sleep(buzzer_frequency)
        GPIO.output(BuzzerPin, GPIO.HIGH)
        time.sleep(buzzer_frequency)
    GPIO.output(BuzzerPin, GPIO.HIGH)
    GPIO.cleanup() # Release resource    
                
    
def weightInput():
    #print "Starting program"

    ser = serial.Serial('/dev/ttyUSB0', baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                    )
    time.sleep(1)
    try:
            ser.write('Hello World\r\n')
            ser.write('Serial Communication Using Raspberry Pi\r\n')
            print 'Processing....'
            alist = ['']
            while True:
                if ser.inWaiting() > 0:
                        for i in range(13):
                                data = ser.read()
                                if i > 3 and i < 11:
                                    alist.append(data)
                        return ''.join(alist)

    except KeyboardInterrupt:
            print "Exiting Program"

    except:
            print "Error Occurs, Exiting Program"

    finally:
            ser.close()
            pass


signal.signal(signal.SIGINT, end_read)

MIFAREReader = MFRC522.MFRC522()

print "Welcome to the founder_box"
print "Please scan your card!"

while continue_reading:    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print "Card detected"
             
    
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    
    if status == MIFAREReader.MI_OK:

        
        print "Card read UID: %s-%s-%s-%s" % (uid[0], uid[1], uid[2], uid[3])
        user = fetch_data(str(uid[0]) + '-' + str(uid[1]) + '-' + str(uid[2]) + '-' + str(uid[3]))
        user_pwd = raw_input('What is your password?: ')
        if(int(user['password']) == int(user_pwd)):
            print 'Correct'
            print 'Balance : '+str(user['amount'])
            a = input('How many perfume you want: ')
            b = input('How many pens you want: ')
            initial_weight = float(weightInput())
            print initial_weight
            print 'Please take the items you want! NOW! '
            time.sleep(7)
            #print 'weight removed'
            final_weight = float(weightInput())
            #print final_weight
            number_product1 = (initial_weight-final_weight)/product1_weight
            number_product2 = ((initial_weight-final_weight)%product1_weight)/product2_weight
            print 'You took '+str(round(number_product1))+' '+product1_name +' and '+str(round(number_product2))+' '+product2_name
            print 'Total amount = ' + str(round(number_product1)*product1_price+round(number_product2)*product2_price)

            if (round(number_product1) != a or round(number_product2)!= b):
                buzzer(10,0.3)
           
                            
        else:
            print 'Incorrect'
            buzzer(4,0.3)
