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
gantry_freq = 0
vms_freq = 0

pi.hardware_PWM(x_step, 40000, 500000)
pi.hardware_PWM(z_step, 40000, 500000)
print(pi.get_PWM_frequency(x_step))
print(pi.get_PWM_frequency(z_step))

pi.write(brk, 1)
pi.write(23, 1)



def accel_curve(value, motor):
    if motor == 'x':
        if value >= 800:
            gantry_freq = 8000
        else:
            gantry_freq = value*10 
        pi.set_PWM_frequency(x_step, gantry_freq)
    elif motor == 'z':
        if value >= 300:
            vms_freq = 3000
        else:
            vms_freq = value*10
        pi.set_PWM_frequency(z_step, vms_freq)

n = 0
i = 0

while True:

    if pi.read(x_plus) == 0: # drives the gantry clockwise
        i+=1
        accel_curve(i,'x')
        pi.write(x_motordrive_enable, 1)
        pi.write(x_direction, 1)
       
        print("x_plus" + str(i) + str(gantry_freq))
    elif pi.read(x_minus) == 0:# drives the gantry counterclockwise
        pi.write(x_motordrive_enable, 1)
        pi.write(x_direction, 0)
        
        print("x_minus")
    elif pi.read(z_plus) == 0: # runs the vms clockwise
        pi.write(z_motordrive_enable, 1)
        pi.write(z_direction, 1)
        
        print("z_plus")
    elif pi.read(z_minus) == 0: # runs the vms counterclockwise
        pi.write(z_motordrive_enable, 1)
        pi.write(z_direction, 0)
        
        print("z_minus")
    elif pi.read(t_plus) == 0:
        m.reverse()
        m.setSpeed(100)
        print("t_plus")
    elif pi.read(t_minus) == 0:
        m.forward()
        m.setSpeed(100)
        print("t_minus")
    else:
        m.setSpeed(0)
        pi.write(z_motordrive_enable, 0)
        pi.write(x_motordrive_enable, 0)
       
        i = 0

