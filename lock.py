import RPi.GPIO as GPIO
import MFRC522
import signal
import pymysql
import time
import serial

def lock (int select):
   while(GPIO.input(6)==GPIO.HIGH)
   for(int i=0;i<4;i++)
    if(select%10==1)
      print("lock "+ i+1 + "opened")
      
   
