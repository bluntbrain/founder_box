#!/usr/bin/env python

import time
import RPi.GPIO as GPIO
import SimpleMFRC522
import array

continue_reading = True
BuzzerPin = 11 # Raspberry Pi Pin 17-GPIO 17

class product:
    def __init__(self,name,weight,price):
        self.name = name
        self.weight = weight
        self.price = price

product1 = product("300ml",50,30)
product2 = product("750ml",100,60)
product3 = product("1.25L",200,120)
product4 = product("2.25L",400,240)


def locks_to_open():
    locks =array.array('i')
    x=int(input())
    for i in range(4):
        locks.append(x%10)
        x=x/10
    # print ('ARRAY: ',locks_array) 
    # print(locks_array[0])
    locks.reverse()
    return locks  

def fetch_data(rfid):
    db = pymysql.connect(host='localhost', port=3306, user='username', database='mydb', password='password')
    cur = db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM payment WHERE rfid ='%s'"
    cur.execute(sql % rfid)
    if(cur.fetchone() > 0):
      print('Found!')
    for row in cur:
        return row

def ledon(number):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(number,GPIO.OUT)
    GPIO.output(number,GPIO.HIGH)

def ledoff(number):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(number,GPIO.OUT)
    GPIO.output(number,GPIO.LOW)


def weightInput():
    return input("weight input:")

print("Welcome to SVM v1.0")
print("please scan your SVM debit card")
reader = SimpleMFRC522.SimpleMFRC522()

try:
        id, text = reader.read()
        print("customer id   : "+str(id))
        print("customer name : "+str(text))
finally:
        GPIO.cleanup()
print("please enter your 4 digit pin")
password = input()
while password != 1234:
      print("incorrect pin please re-enter your pin")
      password = input()

print("Today we have beverages for you!")
print("|--------------------------|")
print("|Lock|     item   | price  |")
print("| 01 |     300 ml |   30   |")
print("| 02 |     750 ml |   60   |")
print("| 03 |     1.25 L |  120   |")
print("| 04 |     2.25 L |  240   |")
print("|--------------------------|") 
print("Please enter locks you want to open!")



locks = locks_to_open()
# print(locks[0])
total_amount = 0
amount1 = 0
amount2 = 0
amount3 = 0
amount4 = 0
ledoff(18)
ledoff(23)
ledoff(24)
ledoff(7)
while continue_reading:

	if(locks[0] == 1): 
         		print("LOCK 1 OPENED")
         		ledon(18)
         		initial_weight = float(weightInput())
         		# print (initial_weight)
         		print ('Please take the items you want! NOW! ')
         		time.sleep(7)
         		print ('Weight removed......')
         		print("LOCK 1 CLOSED")
         		ledoff(18)
         		final_weight = float(weightInput())
         		# print (final_weight)
         		number_product1 = (initial_weight-final_weight)/product1.weight
         		# number_product2 = ((initial_weight-final_weight)%product1.weight)/product2_weight
         		print ('You took '+str(round(number_product1))+' '+product1.name )
         		amount1 = number_product1*product1.price

	if(locks[1] == 1): 
         		print("LOCK 2 OPENED")
         		ledon(23)
         		initial_weight = float(weightInput())
         		# print (initial_weight)
         		print ('Please take the items you want! NOW! ')
         		time.sleep(7)
         		print ('Weight removed......')
         		print("LOCK 2 CLOSED")
         		ledoff(23)
         		final_weight = float(weightInput())
         		# print (final_weight)
         		number_product2 = (initial_weight-final_weight)/product2.weight
         		# number_product2 = ((initial_weight-final_weight)%product1.weight)/product2_weight
         		print ('You took '+str(round(number_product2))+' '+product2.name )
         		amount2 = number_product2*product2.price

	if(locks[2] == 1): 
         		print("LOCK 3 OPENED")
         		ledon(24)
         		initial_weight = float(weightInput())
         		# print (initial_weight)
         		print ('Please take the items you want! NOW! ')
         		time.sleep(7)
         		print ('Weight removed......')
         		print("LOCK 3 CLOSED")
         		ledoff(24)
         		final_weight = float(weightInput())
         		# print (final_weight)
         		number_product3 = (initial_weight-final_weight)/product3.weight
         		# number_product2 = ((initial_weight-final_weight)%product1.weight)/product2_weight
         		print ('You took '+str(round(number_product3))+' '+product3.name )
         		amount3 = number_product3*product3.price

	if(locks[3] == 1): 
         		print("LOCK 4 OPENED")
         		ledon(7)
         		initial_weight = float(weightInput())
         		# print (initial_weight)
         		print ('Please take the items you want! NOW! ')
         		time.sleep(7)
         		print ('Weight removed......')
         		print("LOCK 4 CLOSED")
         		ledoff(7)
         		final_weight = float(weightInput())
         		# print (final_weight)
         		number_product4 = (initial_weight-final_weight)/product4.weight
         		# number_product2 = ((initial_weight-final_weight)%product1.weight)/product2_weight
         		print ('You took '+str(round(number_product4))+' '+product4.name )
         		amount4 = number_product4*product4.price
            	
	# print("Do you want to continue purchase?")
	# continue_reading = input("True/False")
	continue_reading = False
	total_amount = amount1 + amount2 + amount3 + amount4
	print("Total amount :" + str(total_amount))
print("Thanks for the purchase:)")