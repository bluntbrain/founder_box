import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BOARD)
mypin = 8
product1_weight=20
product2_weight=30
product3_weight=40
product4_weight=50
output=""
GPIO.setup(mypin, GPIO.OUT, initial = 1)
try:
print"please enter input pattern"
pattern=int(input(lockers you want to open:),8);

if(pattern%10==1)
  initial_weight = float(weightInput())
  print"opening locker 1"
  GPIO.output(mypin,GPIO.LOW)
  time.sleep(8)
  GPIO.output(mypin,GPIO.HIGH)
  final_weight = float(weightInput())
  output=output+(initial_weight-final_weight)/product1_weight+' '

  
pattern=pattern/10
if(pattern%10==1)
  initial_weight = float(weightInput())
  print"opening locker 2"
  GPIO.output(mypin,GPIO.LOW)
  time.sleep(8)
  GPIO.output(mypin,GPIO.HIGH)
  final_weight = float(weightInput())
  output=output+(initial_weight-final_weight)/product2_weight+' '


pattern=pattern/10
if(pattern%10==1)
  initial_weight = float(weightInput())
  print"opening locker 3"
  GPIO.output(mypin,GPIO.LOW)
  time.sleep(8)
  GPIO.output(mypin,GPIO.HIGH)
  final_weight = float(weightInput())
  output=output+(initial_weight-final_weight)/product3_weight+' '

pattern=pattern/10
if(pattern%10==1)
  initial_weight = float(weightInput())
  print"opening locker 4"
  GPIO.output(mypin,GPIO.LOW)
  time.sleep(8)
  GPIO.output(mypin,GPIO.HIGH)
  final_weight = float(weightInput())
  output=output+(initial_weight-final_weight)/product4_weight+' '
 
      
   
