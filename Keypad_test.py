from pad4pi import rpi_gpio
import time

# Setup Keypad
KEYPAD = [
        ["1","2","3","A"],
        ["4","5","6","B"],
        ["7","8","9","C"],
        ["*","0","#","D"]
]

key_seq = []
# same as calling: factory.create_4_by_4_keypad, still we put here fyi:
ROW_PINS = [4, 5, 6, 13] # BCM numbering
COL_PINS = [12, 26, 2, 3] # BCM numbering

factory = rpi_gpio.KeypadFactory()

# Try factory.create_4_by_3_keypad
# and factory.create_4_by_4_keypad for reasonable defaults
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

#keypad.cleanup()
s=""
ss=""
def printKey(key):
    print(key)
    key_seq.append(key)
    print(key_seq)
    print(key_seq)
    if(len(key_seq) == 4):
        ss=""
        for i in range(4):
            ss = key_seq.pop() + ss
    print(key_seq)
    print(ss)
  
  #if (key=="1"):
  #  print("number")
  #elif (key=="A"):
  #  print("letter")

# printKey will be called each time a keypad button is pressed
keypad.registerKeyPressHandler(printKey)

try:
  while(True):
    time.sleep(0.2)
except:
 keypad.cleanup()