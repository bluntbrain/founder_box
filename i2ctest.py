import binascii
import time
import threading
from collections import deque #use as a fifo queue

queue = deque() #queue to pass information from thread to main process
queue_lock = threading.Lock() #prevent possible issues from 
txt_file = '50_shades_of_grey.txt' #don't ask ;)
running = True

def nfc_reader():
    #copied from adafruit example
    import Adafruit_PN532 as PN532
    CS   = 18
    MOSI = 23
    MISO = 24
    SCLK = 25

    pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
    pn532.begin()
    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {ver}.{rev}')
    pn532.SAM_configuration()

    # Main loop to detect cards and read a block.
    print('Waiting for MiFare card...')
    while True:
        if not running: #cheap way to kill a thread nicely (cheap ain't pretty)
            return
        #don't bother specifying a timeout, they forgot to support it in the library
        uid = pn532.read_passive_target() 
        # Try again if no card is available.
        if uid is None:
            continue
        print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))
        # Authenticate block 4 for reading with default key (0xFFFFFFFFFFFF).
        if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B,
                                                       [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
            print('Failed to authenticate block 4!')
            continue
        # Read block 4 data.
        data = pn532.mifare_classic_read_block(4)
        if data is None:
            print('Failed to read block 4!')
            continue
        # make sure our queue is free
        with queue_lock:
            # replaced print with deque.append
            queue.append('Read block 4: 0x{binascii.hexlify(data[:4])}')
        #optionally emit some sort of signal that data is ready. In our case the main loop will chech periodically on it's own

# Main program
nfc_thread = threading.Thread(target=nfc_reader)
nfc_thread.start()

with open(txt_file, 'r') as f:
    while True: #also cheap, but easy
        if queue: #bool(deque) works like bool(list)
            with queue_lock:
                print("we found a card!")
                print(queue.popleft())
                continue
        try:
            print(next(f)) #otherwise go back to more interesting matters
        except StopIteration:
            running = False
            nfc_thread.join()
            break
        time.sleep(.9) #notice loop time will be less than timeout on nfc read.
                       #  you could put the printing of the *book* into another thread
                       #  and use events to immediately call your return from your 
                       #  nfc reader