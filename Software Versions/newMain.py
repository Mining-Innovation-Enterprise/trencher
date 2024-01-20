import os
import time
import pigpio
from peripherals import *

# motor pin assignments

# where does 'brake' pin go? is it used? is it x_motordrive_enable?
sv, fr = 12, 27 # sv is PWM
led_green, led_yellow = 10, 9
x_plus, x_minus, x_step, x_direction = 6, 5, 18, 17 # gantry pins
z_plus, z_minus, z_step, z_direction = 4, 25, 19, 21 # VMS pins
t_plus, t_minus = 16, 20 # bucket ladder direction pins
x_motordrive_enable, z_motordrive_enable = 23, 24 # double check that x is correct pin -- could be brake pin

# groupings to help readability later
x_motor_pins = [x_plus, x_minus]
z_motor_pins = [z_plus, z_minus]
t_motor_pins = [t_plus, t_minus]

# constants
# should be gantry and vms freq/duty instead? use these in doc commented code?
MAX_FREQUENCY = 8000 # VMS and gantry have different max freqs
DUTY_CYCLE = 500000 # 128 instead of 500k? if 500k, is that because of the advpistepper library?

# connect to pigpio
pi = pigpio.pi()

if not pi.connected:
    print("not connected")
    os.system("sudo pigpiod") # need to include "-s2 -t0"? '-s2' is 5 micro second sampling rate and '-t0' is seeding time origin at 0?
    time.sleep(1)
    pi = pigpio.pi()

# set buttons to pull-up
# should we pull-up or down? is down safer?
button_pins = [6, 5, 4, 25, 16, 20]
for pin in button_pins:
    pi.set_pull_up_down(pin, pigpio.PUD_UP)

# set input pins
input_pins = [x_motor_pins, z_motor_pins, t_motor_pins]
for pin in input_pins:
    pi.set_mode(pin, pigpio.INPUT)

# set output pins
output_pins = [x_motordrive_enable, z_motordrive_enable, x_step, x_direction, z_step, z_direction, led_green, led_yellow]
for pin in output_pins:
    pi.set_mode(pin, pigpio.OUTPUT)

# set initial states. 0 is no output, 1 is positive output
initial_states = {
    x_motordrive_enable: 0, # double check that this and z should be low
    z_motordrive_enable: 0,
    x_direction: 1,
    z_plus: 1, # this line and the line below are in the functional code but they tell VMS to go both up and down at the same time. why? why functional?
    z_minus: 1, # should these be deleted? should they be replaced with z_direction?
    led_green: 1,
    led_yellow: 0 # LEDs for what? not used in code. green always on and yellow always off?
}
for pin, state in initial_states.items():
    pi.write(pin, state)

# accelerates motor using predefined frequencies in GPIO library. 5 microsecond sampling rate
# still a 5 micro second sampling rate? "-s2" flag in line 32: "sudo pigpiod"?
# only accelerates for VMS, not gantry?
avail_freq = [100, 160, 200, 250, 320, 400, 500, 800, 1000, 1600, 2000, 4000, 8000]
for frequency in avail_freq:
    pi.set_PWM_frequency(z_step, frequency)
    print(pi.get_PWM_frequency(z_step))
    time.sleep(0.1) # is this the best delay between loops? does it matter?

''' 
# set PWM frequency and duty cycle for x_step and z_step
pi.set_PWM_frequency(x_step, MAX_FREQUENCY)
pi.set_PWM_dutycycle(x_step, DUTY_CYCLE)
pi.set_PWM_frequency(z_step, MAX_FREQUENCY)
pi.set_PWM_dutycycle(z_step, DUTY_CYCLE)
'''

class Motor:
    def __init__(self, pi, sv, fr, brk):
        self.__pi = pi
        self.__speed = sv
        self.__dir = fr # does this need to be set to pull up?
        self.__brake = brk # is brake even needed? isn't this techincally the gantry enable pin?
        self.__pi.set_mode(self.__dir, pigpio.OUTPUT)
        self.__pi.set_mode(self.__speed, pigpio.OUTPUT)
        self.__pi.set_mode(self.__brake, pigpio.OUTPUT) # including this line
        self.__curr_speed = 0

    def set_speed(self, speed):
        if speed > 400: # why 400? is this a cap? why cap at 400?
            self.__curr_speed = 400
        elif speed <= 0:
            self.__curr_speed = 0
        else:
            self.__curr_speed = speed
        self.__pi.set_PWM_dutycycle(self.__speed, self.__curr_speed) # "self.__speed" as first arg? should this not just be self?

    def speed_up(self, amount): # not used; planning to?
        self.set_speed(self.__curr_speed + amount)

    def slow_down(self, amount): # not used; planning to?
        self.set_speed(self.__curr_speed - amount)

    def forward(self):
        self.__pi.write(self.__dir, 0)

    def reverse(self):
        self.__pi.write(self.__dir, 1)

    def hard_stop(self): # not used; planning to?
        curr = self.__pi.read(self.__brake)
        self.__pi.write(self.__brake, curr ^ 1)

# main loop
while True:
    m = Motor(pi, sv, fr) # motor initialization

    if pi.read(x_plus) == 0: # drives gantry clockwise
        pi.write(x_motordrive_enable, 1)
        pi.write(x_direction, 1)
        pi.set_PWM_dutycycle(x_step, 128) # 50%?
        pi.set_PWM_frequency(x_step, 10000) # 10k value from datasheet? equates to ~300rpm?
    elif pi.read(x_minus) == 0: # drives gantry counterclockwise
        pi.write(x_motordrive_enable, 1)
        pi.write(x_direction, 0)
        pi.set_PWM_dutycycle(x_step, 128)
        pi.set_PWM_frequency(x_step, 10000)
    elif pi.read(z_plus) == 0: # drives VMS clockwise
        pi.write(z_motordrive_enable, 1)
        pi.write(z_direction, 1)
        pi.set_PWM_dutycycle(x_step, 128)
        pi.set_PWM_frequency(x_step, 2500) # same as gantry freq, equates to ~300 rpm? is 300 what we want?
    elif pi.read(z_minus) == 0: # drives VMS counterclockwise
        pi.write(z_motordrive_enable, 1)
        pi.write(z_direction, 0)
        pi.set_PWM_dutycycle(x_step, 128)
        pi.set_PWM_frequency(x_step, 2500)
    elif pi.read(t_plus) == 0: # drives bucket ladder clockwise
        m.reverse()
        m.set_speed(100) # why 100? seems arbitrary
    elif pi.read(t_minus) == 0: # drives bucket ladder counterclockwise
        m.forward()
        m.set_speed(100)
    else: # sets all speeds to 0
        m.set_speed(0)
        pi.write(z_motordrive_enable, 0)
        pi.write(x_motordrive_enable, 0)
        # need to exit loop and close? off button code to be included in main file -- checking with Mary about off button file operation

    # for BLDC (t_plus and t_minus), in new code it is being treated like a stepper. why? how work? what are lines 225-228?
    # 500Hz @ 50% duty? adds to prev value after each iteration of the loop? 500Hz -> 1000Hz -> 1500Hz -> ...
