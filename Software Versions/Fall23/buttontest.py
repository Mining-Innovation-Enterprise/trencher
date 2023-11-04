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

,,,
pi.set_mode(4, pigpio.INPUT) 
pi.set_mode(20, pigpio.INPUT)
pi.set_mode(25, pigpio.INPUT)
pi.set_mode(16, pigpio.INPUT) 
,,,

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

def set_motor_duty_cycle(motor, dc):
    # sets the motor duty cycle
    # takes the percentage and multiplies it to the full value
    
    if dc>= 0 | dc<= 1:
        duty_cycle = dc*1000000
        if motor =='vms':
            pi.hardware_PWM(motor, vms_freq, duty_cycle)
        elif motor =='gantry':
            pi.hardware_PWM(motor, gantry_freq, duty_cycle)
        else:
            print('Incorrect motor name. valid names are : vms, gantry')
    else:
        print("Incorrect duty cycle. Please enter a value between in the range of 0 and 1")

# adding a motor driver object and stepper controller object for both the vms and gantry
# sets the style of motor to be used and the respective step and direction pins

vms_driver = apis.DriverStepDirGeneric(step_pin=z_step, dir_pin=z_direction)
gantry_driver = apis.DriverStepDirGeneric(step_pin=x_step, dir_pin=x_direction)

vms_stepper = apis.AdvPiStepper(vms_driver)
gantry_stepper = apis.AdvPiStepper(gantry_driver)

    
m = Motor(pi, sv, fr, brk)

# sets the frequency and duty cycle for the gantry (x) and vms motors (z)
gantry_freq = 40000
vms_freq = 40000

pi.hardware_PWM(x_step, 40000, 500000)
pi.hardware_PWM(z_step, 40000, 500000)
print(pi.get_PWM_frequency(x_step))
print(pi.get_PWM_frequency(z_step))

pi.write(brk, 1)
pi.write(23, 1)

while True:

    if pi.read(x_plus) == 0: # drives the gantry clockwise
        # pi.write(x_motordrive_enable, 1)
        # pi.write(x_direction, 1)
        # uses the gantry_stepper object to tell the driver to accelerate the motor to the given speed in steps/sec
        gantry_stepper.run(1, 0.3) 
        print("x_plus")
    elif pi.read(x_minus) == 0:# drives the gantry counterclockwise
        # pi.write(x_motordrive_enable, 1)
        # pi.write(x_direction, 0)
        # uses the gantry_stepper object to tell the driver to accelerate the motor to the given speed in steps/sec
        gantry_stepper.run(-1, 0.3) 
        print("x_minus")
    elif pi.read(z_plus) == 0: # runs the vms clockwise
        # pi.write(z_motordrive_enable, 1)
        # pi.write(z_direction, 1)
        # uses the gantry_stepper object to tell the driver to accelerate the motor to the given speed in steps/sec
        vms_stepper.run(1, 0.3) 
        print("z_plus")
    elif pi.read(z_minus) == 0: # runs the vms counterclockwise
        # pi.write(z_motordrive_enable, 1)
        # pi.write(z_direction, 0)
        # uses the gantry_stepper object to tell the driver to accelerate the motor to the given speed in steps/sec
        vms_stepper.run(-1, 0.3)
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
        # pi.write(z_motordrive_enable, 0)
        # pi.write(x_motordrive_enable, 0)
        vms_stepper.stop()
        gantry_stepper.stop()

