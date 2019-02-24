#!/usr/bin/env python
import subprocess
import requests
import sqlite3
import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import SimpleMFRC522
import array
import serial
import time
import math
usernum=0
UID=""
continue_reading = True
BuzzerPin = 11 # Raspberry Pi Pin 17-GPIO 17

connection = sqlite3.connect("svm_data.db")
crsr = connection.cursor()

# Raspberry Pi pin configuration:
lcd_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 18
lcd_d7        = 22
lcd_backlight = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)


class product:
    def __init__(self,name,weight,price):
        self.name = name
        self.weight = weight
        self.price = price

product1 = product("5Star",20,10)
product2 = product("Amul Bisuit",60,10)
product3 = product("Maggi",70,12)
product4 = product("Uncle chips",30,10)
p1=0
p2=0
p3=0
p4=0
class user:
    def __init__(self,name,uid,password,balance):
        self.name = name
        self.uid = uid
        self.password = password
        self.balance = balance
user1 =[]
user1.append(user("Keval","52b1661f","1234","1000"))
user1.append(user("Ishan","a77b3c27","1234","1000"))

def locks_to_open():
    locks =array.array('i')
    for i in range(4):
        lcd_print ("Do you want to open lock "+str(i+1))
        locks.append(input())
    # print ('ARRAY: ',locks_array) 
    # print(locks_array[0])
    
    return locks  
def lcd_print(data):
    if len(data)>30:
        lcd_print(data[:14])
        lcd_print(data[14:])
    else:
        if len(data)>16:data=data[:14]+"\n"+data[14:]
        print(data)
        lcd.message(data)
        time.sleep(3.0)
        lcd.clear()
    

def fetch_data(rfid):
    db = pymysql.connect(host='localhost', port=3306, user='username', database='mydb', password='password')
    cur = db.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM payment WHERE rfid ='%s'"
    cur.execute(sql % rfid)
    if(cur.fetchone() > 0):
      lcd_print('Found!')
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

def update_sales (UID,P1,P2,P3,P4,total):
    s = "A"+str(P1)+"B"+str(P2)+"C"+str(P3)+"D"+str(P4)
    Url="http://maker.ifttt.com/trigger/SVM_sales_data/with/key/iLPqP1nHEzbv3IGxm3aHfdlmO9rlBng9fSS3DN7RVR7?value1="+str(UID)+"&&value2="+s+"&&value3="+str(total)
    r=requests.get(Url)
    lcd_print(r)

def weightInput():
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
    return str(s)
##lcd.message("Welcome to \nSVM v1.0")
##time.sleep(3.0)
##lcd.clear()
##lcd.message("please scan your \nSVM debit card")
##time.sleep(3.0)
##lcd.clear()
lcd_print("Welcome to SVM \nv1.0")
lcd_print("please scan your SVM debit card")
##reader = SimpleMFRC522.SimpleMFRC522()
##
##try:
##        id, text = reader.read()
##        print("customer id   : "+str(id))
##        print("customer name : "+str(text))
##finally:
##        GPIO.cleanup()
##print("please enter your 4 digit pin")
##password = input()
##while password != 1234:
##      print("incorrect pin please re-enter your pin")
##      password = input()
try:
	#myLines=subprocess.check_output("/usr/bin/nfc-poll", stderr=open('/dev/null','w'))
	#buffer=[]
	#for line in myLines.splitlines():
	#    	line_content=line.split()
	#	if(not line_content[0] =='UID'):
	#		pass
	#    	else:
	#		buffer.append(line_content)
	#str=buffer[0]
	#id_str=str[2]+str[3]+str[4]+str[5]
	id_str= "52b1661f"
	UID=id_str
	lcd_print (id_str)
	#del buffer
	#del str
	usernum=0;
	for i in range(1):
            if (user1[i].uid==id_str):
                usernum=i
	del id_str
        lcd_print("name : "+str(user1[usernum].name))
        lcd_print("please enter your 4 digit pin")
        password = input()
        while password != int(user1[usernum].password):
              lcd_print("incorrect pin please re-enter your pin")
              password = input()
	lcd_print("login successfull")
	lcd_print("USER : "+user1[usernum].name)
	lcd_print("BALANCE : INR "+user1[usernum].balance)

except KeyboardInterrupt:
        pass

print("Today we have beverages for you!")
print("|--------------------------|")
print("|Lock|     item         | price  |")
print("| 01 |     5 Star       |   10   |")
print("| 02 |     Amul Biscuts |   10   |")
print("| 03 |     Maggi        |   12   |")
print("| 04 |     Uncle Chips  |   10   |")
print("|--------------------------|") 
print("Please enter locks you want to open!")



locks = locks_to_open()
# print(locks[0])
total_amount = 0
amount1 = 0
amount2 = 0
amount3 = 0
amount4 = 0
ledon(18)
ledon(23)
ledon(24)
ledon(7)
while continue_reading:

	if(locks[0] == 1): 
         		lcd_print("LOCK 1 OPENED")
         		ledoff(18)
         		initial_weight = float(weightInput())
         		# print (initial_weight)
         		lcd_print ('Please take the items you want! NOW! ')
         		time.sleep(7)
         		lcd_print ('Weight removed......')
         		ledon(18)
         		lcd_print("LOCK 1 CLOSED")
         		final_weight = float(weightInput())
         		# print (final_weight)
         		number_product1 = (initial_weight-final_weight)/product1.weight
         		# number_product2 = ((initial_weight-final_weight)%product1.weight)/product2_weight
         		p1=str(round(number_product1))
         		print ('You took '+str(round(number_product1))+' '+product1.name )
         		amount1 = round(number_product1)*product1.price

	if(locks[1] == 1): 
         		lcd_print("LOCK 2 OPENED")
         		ledoff(23)
         		initial_weight = float(weightInput())
         		# print (initial_weight)
         		lcd_print ('Please take the items you want! NOW! ')
         		time.sleep(7)
         		lcd_print ('Weight removed......')
         		lcd_print("LOCK 2 CLOSED")
         		ledon(23)
         		final_weight = float(weightInput())
         		# print (final_weight)
         		number_product2 = (initial_weight-final_weight)/product2.weight
         		# number_product2 = ((initial_weight-final_weight)%product1.weight)/product2_weight
         		p2=str(round(number_product2))
         		print ('You took '+str(round(number_product2))+' '+product2.name )
         		amount2 = round(number_product2)*product2.price

	if(locks[2] == 1): 
         		lcd_print("LOCK 3 OPENED")
         		ledoff(24)
         		initial_weight = float(weightInput())
         		# print (initial_weight)
         		lcd_print ('Please take the items you want! NOW! ')
         		time.sleep(7)
         		lcd_print ('Weight removed......')
         		lcd_print("LOCK 3 CLOSED")
         		ledon(24)
         		final_weight = float(weightInput())
         		# print (final_weight)
         		number_product3 = (initial_weight-final_weight)/product3.weight
         		# number_product2 = ((initial_weight-final_weight)%product1.weight)/product2_weight
         		p3=str(round(number_product3))
         		lcd_print ('You took '+str(round(number_product3))+' '+product3.name )
         		amount3 = round(number_product3)*product3.price

	if(locks[3] == 1): 
         		lcd_print("LOCK 4 OPENED")
         		ledoff(7)
         		initial_weight = float(weightInput())
         		# print (initial_weight)
         		lcd_print ('Please take the items you want! NOW! ')
         		time.sleep(7)
         		lcd_print ('Weight removed......')
         		lcd_print("LOCK 4 CLOSED")
         		ledon(7)
         		final_weight = float(weightInput())
         		# print (final_weight)
         		
         		number_product4 = (initial_weight-final_weight)/product4.weight
         		# number_product2 = ((initial_weight-final_weight)%product1.weight)/product2_weight
         		p4=str(round(number_product4))
         		lcd_print ('You took '+str(round(number_product4))+' '+product4.name )
         		amount4 = round(number_product4)*product4.price
            	
	# print("Do you want to continue purchase?")
	# continue_reading = input("True/False")
	continue_reading = False
	total_amount = amount1 + amount2 + amount3 + amount4
	crsr.execute("SELECT uid,balance FROM emp")
        ans= crsr.fetchall()
        for i in ans:
            # print(i)
            if i[0] == UID:
                print(i[1])
                balance = int(i[1])
            
        new_balance = balance - total_amount
	crsr.execute("UPDATE emp SET balance = balance where uid= UID")
	pa=int(float(p1))
	pb=int(float(p2))
	pc=int(float(p3))
	pd=int(float(p4))
	update_sales(UID,pa,pb,pc,pd,total_amount)
	lcd_print("Total amount :" + str(total_amount))
	lcd_print("Current BALANCE : "+str(int(user1[usernum].balance)-total_amount))
lcd_print("Thanks for the purchase:)")