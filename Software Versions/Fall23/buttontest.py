import os
import time
import pigpio
from Peripherals import *
import advpistepper as apis


pi = pigpio.pi()

if not pi.connected:
    print("not connected")
    os.system("sudo pigpiod")
    time.sleep(1)
    pi = pigpio.pi()

#****************************
# Trencher motor controller pinout
sv = 12 #PWM pin
fr = 27 #non-PWM pin
brk = 22 #non-PWM pin
rpm = 17 #non-PWM pin
trencher_Enable = 23
#****************************

led_green = 10 
led_yellow = 9

# gantry buttons
x_plus = 6
x_minus = 5

# vms buttons
z_plus = 4
z_minus = 25

# bucket ladder directions
t_plus = 16 #forward
t_minus = 20 #backward

x_motordrive_enable = 23
z_motordrive_enable = 24

# step is speed pin
x_step = 18
x_direction = 17

# step = speed pin
z_step = 19
z_direction = 21

#pull-up pull down sets buttons to output/input, PUD up tells the program to check when the circuit going through the buttons is broken.

pi.set_pull_up_down(20, pigpio.PUD_UP) #backwards bucket ladder
pi.set_pull_up_down(16, pigpio.PUD_UP) #forwards bucket ladder

pi.set_pull_up_down(z_minus, pigpio.PUD_UP) #VMS down
pi.set_pull_up_down(z_plus, pigpio.PUD_UP) #VMS up


pi.set_pull_up_down(x_plus, pigpio.PUD_UP) #gantry right
pi.set_pull_up_down(x_minus, pigpio.PUD_UP) #gantry left

#pi.set_mode(4, pigpio.INPUT) 
#pi.set_mode(20, pigpio.INPUT)
#pi.set_mode(25, pigpio.INPUT)
#pi.set_mode(16, pigpio.INPUT) 

#pigpio.INPUT sets the program to read an input

pi.set_mode(x_plus, pigpio.INPUT)
pi.set_mode(x_minus, pigpio.INPUT)

pi.set_mode(z_plus, pigpio.INPUT)
pi.set_mode(z_minus, pigpio.INPUT)

pi.set_mode(t_plus, pigpio.INPUT)
pi.set_mode(t_minus, pigpio.INPUT)

#pigpio.OUTPUT sets the program to output a signal

pi.set_mode(x_motordrive_enable, pigpio.OUTPUT)
pi.set_mode(z_motordrive_enable, pigpio.OUTPUT)

pi.set_mode(x_step, pigpio.OUTPUT)
pi.set_mode(x_direction, pigpio.OUTPUT)
pi.set_mode(z_step, pigpio.OUTPUT)
pi.set_mode(z_direction, pigpio.OUTPUT)

pi.set_mode(led_green, pigpio.OUTPUT)
pi.set_mode(led_yellow, pigpio.OUTPUT)

# sets no output, akin to setting defaults. 0 is no output

pi.write(x_motordrive_enable, 0)
pi.write(z_motordrive_enable, 0)

# sets default to output. 1 is positive output

pi.write(x_direction, 1)
pi.write(z_plus, 1)
pi.write(z_minus, 1)

pi.write(led_green, 1)
pi.write(led_yellow, 0)
    
m = Motor(pi, sv, fr, brk)

# sets the frequency and duty cycle for the gantry (x) and vms motors (z)

pi.write(brk, 1)
pi.write(23, 1)

avail_freq = [100, 160, 200, 250, 320, 400, 500, 800, 1000, 1600, 2000, 4000, 8000]

pi.set_PWM_dutycycle(z_step, 500000)

c = 0
while c<12:
    pi.set_PWM_frequency(z_step, avail_freq[c])
    print(pi.get_PWM_frequency(z_step))
    time.sleep(.1)
    c+=1

pi.set_PWM_frequency(step, 8000)
print(pi.get_PWM_frequency(step))
        

while True:

    if pi.read(x_plus) == 0: # drives the gantry clockwise
        pi.write(x_motordrive_enable, 1)
        pi.write(x_direction, 1)
       
        #print(f"x_plus: {i} gantry frequency: {pi.get_PWM_frequency(x_step)}")
        
    elif pi.read(x_minus) == 0:# drives the gantry counterclockwise
        pi.write(x_motordrive_enable, 1)
        pi.write(x_direction, 0)
        
        #print(f"x_minus: {i} gantry frequency: {pi.get_PWM_frequency(x_step)}")
    elif pi.read(z_plus) == 0: # runs the vms clockwise
        pi.write(z_motordrive_enable, 1)
        pi.write(z_direction, 1)
        
        #print(f"z_plus: {i} vms frequency: {pi.get_PWM_frequency(z_step)}")
    elif pi.read(z_minus) == 0: # runs the vms counterclockwise
        pi.write(z_motordrive_enable, 1)
        pi.write(z_direction, 0)
        
        #print(f"z_minus: {i} vms frequency: {pi.get_PWM_frequency(z_step)}")
    elif pi.read(t_plus) == 0:
        m.reverse()
        m.setSpeed(100)
        #print("t_plus")
    elif pi.read(t_minus) == 0:
        m.forward()
        m.setSpeed(100)
        #print("t_minus")
    else:
        m.setSpeed(0)
        pi.write(z_motordrive_enable, 0)
        pi.write(x_motordrive_enable, 0)
       
    

