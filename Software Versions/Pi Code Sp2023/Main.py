#g|*****************************************************************************|
#| Trencher BLDC Motor controls and sensor output
#| Author: Conor Porter
#| Last Modified: 04/12/2021
#|*****************************************************************************|

import os
#os.system("sudo killall pigpiod")
os.system ("sudo pigpiod") #Launching GPIO library
from Peripherals import *
from Connections import *
import time
import threading
#from ina260.controller import Controller


def ControlMotor(command):# check if the switch is on and button is not pressed. If so, accelerate motor to max speed
    #start recording clock for tracking RPM data
    if command.contents() == 'up':
        m.speedUp(2.55)
    elif command.contents() == 'down':
        m.slowDown(2.55)
    elif command.contents() == 'w':
        m.forward()
    elif command.contents() == 's':
        m.reverse()
    elif command.contents() == 'space':
        m.setSpeed(0)
    elif command.contents() == 'esc':
        m.hardStop()

def ControlLeadScrew(command, __pi):
    if command.contents() == '0':
        print("enabling leadscrew")
        leadScrew.enable()
    elif command.contents() == '=':
        leadScrew.increaseSpeed(100)
    elif command.contents() == '-':
        leadScrew.decreaseSpeed(100)
    elif command.contents() == '1':
        leadScrew.setDirection()
    elif command.contents() == '2':

        #sets direction to forward
        __pi.write(25, 1)
        #enables motor
        __pi.write(24, 1)

        m.setSpeed(153)
        leadScrew.setSpeed(0)
        leadScrew.setSpeed(840)




#****************************
# Trencher motor controller pinout
sv = 12 #PWM pin
fr = 27 #non-PWM pin
brk = 22 #non-PWM pin
rpm = 17 #non-PWM pin
trencher_Enable = 23
#****************************
#Lead Screw motor controller pinout
leadScrew_Enable = 24
step_pin = 13
direction_pin = 25
#****************************

#****************************
#

#****************************


pi = pigpio.pi()
speed = 0
m = Motor(pi, sv, fr, brk)

leadScrew = LeadScrew(pi, direction_pin, step_pin, leadScrew_Enable)

port = 3000
c = None
r = None
message = None
foundPort = False
closing = False
while not foundPort:
    try:
        c = ClientConnection(port)
        print(f"listening on port {port}")
        c.listenAndAccept(10)
        r = SocketReader(c.client())
        message = r.receive()
        if (message.type() == 'init' and message.contents() == 'hello'):
            foundPort = True
    except:
        port += 1


print(f"message received: {message.contents()}")
w = SocketWriter(c.client())
w.send(message)


while True:

    message = r.receive()
    # print(message)
    if (message != None):

        print(message.contents())

        if (message.type() == "m"):
            ControlMotor(message)

        if(message.type() == "l"):
            print("lead Screw")
            ControlLeadScrew(message, pi)

        if (message.type() == 's' and message.contents() == "Shutdown"):
            c.close()
            closing = True
            exit(0)
