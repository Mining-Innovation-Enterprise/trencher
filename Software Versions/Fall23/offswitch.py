import os
import time
import pigpio
from Peripherals import *

pi = pigpio.pi()

if not pi.connected:
    print("not connected")
    os.system("sudo pigpiod")
    time.sleep(1)
    pi = pigpio.pi()
    
 
offbutton = 12
 
pi.set_pull_up_down(12, pigpio.PUD_UP)
 
pi.set_mode(12, pigpio.INPUT) 
pi.set_mode(offbutton, pigpio.INPUT)
pi.write(12,1)
while True:
     if pi.read(12) == 1:
         print("pudup")
     elif pi.read(12) == 0:
         print("puddown")
     else:
         print("cringefail")

  
