import pigpio #importing GPIO Library
import time
from spidev import SpiDev #can probably omit this if we're not using spidev

#user_gpio:= 0-31
#frequency: >=0 Hz

class VMS()

  __directionPin = None
  __speedPin = None
  __enablePin = None
  __pi = None
  __isEnabled = None
  __currentSpeed = 0
  
  def __init__(self, pi, direction, step, enable) -> None
  
    self.__pi = pi #pin ids for direction, step, and enable pins in Main.py
    self.__directionPin = direction #pin id 12
    self.__speedPin = step #pin id 19
    self.__eanblePin = enable #pin id 24
    
    self.__pi.write(self.__enablePin, 0)
    
    self.__pi.set_PWM_frequency(self.__speedPin, 227)
    
  def setSpeed(self, step):
    if self.__currentSpeed >= 0
      if self.__currentSpeed < 20
        self.__currentSpeed = self.__currentSpeed + 1 #technically this isn't a curve, but it will call the motor to accelerate more slowly
        self.__pi.hardware_PWM(19, self.__currentSpeed, 500000)
        self.__sleep(.05)
      elif
        self.__pi.hardware_PWM(19, self.__currentSpeed, 500000)
   
    
    print(self.__pi.get_PWM_frequency(self.__speedPin))
    print(f"Set speed to: {self.__currentSpeed}")
    
  def increaseSpeed(self, amount):
    self.setSpeed(self.__currentSpeed + amount)
    
  def decreaseSpeed(self, amount):
    self.setSpeed(self.__currentSpeed - amount)
    
    def setDirection(self):
      
        gpio.setup(4, gpio.IN)
        gpio.setup(19, gpio.IN)
        gpio.setup(12, gpio.OUT)

         if self.__pi.read(19) == 0:
          if self.__pi.read(4) == 1:
            self.__pi.write(12, 1) #"1" is the same as GPIO.HIGH (forward)
            self.__pi.hardware_PWM(12, 40, 500000)
            print("Moving Up")
            return
          
        if self.__pi.read(4) == 0:
          if self.__pi.read(19) == 1:
            self.__pi.write(12, 0) #"0" is the same as GPIO.LOW (reverse)
            self.__pi.hardware_PWM(12, 40, 500000)
            print("Moving Down")
            return
    
    def getSpeed(self) -> int:
      return self.__currentSpeed
    
    def enable(self):
      print("VMS: Enabling")
      
      
      if self.__pi.read(self.__enablePin) == 1:
        print("Disabling")
        self.__pi.write(self.__enablePin, 0)
        self.__pi.hardware_PWM(24, 40, 500000)
        self.__targetSpeed = 40 
        self.__currentSpeed = 40
        return
      
      if self.__pi.read(self.__enablePin) == 0:
        print("enabling")
        self.__pi.write(self.enablePin, 1)
        self.pi.hardware_PWM(24, 40, 500000) #both enable + direction had the step pin, fixed on 3/2/2023
        self.__targetSpeed = 40
        self.__currentSpeed = 40
        return
  
  self.__pi.hardware_PWM(13, 40, 500000) #sets speed to 40 hz if loop fails

class LeadScrew()

  __directionPin = None
  __speedPin = None
  __enablePin = None
  __pi = None
  __isEnabled = None
  __currentSpeed = 0
  
  def __init__(self, pi, direction, step, enable) -> None
  
    self.__pi = pi #pin ids for direction, step, and enable pins in Main.py
    self.__directionPin = direction #pin id 17
    self.__speedPin = step #pin id 18
    self.__eanblePin = enable #pin id 24
    
    self.__pi.write(self.__enablePin, 0)
    
    self.__pi.set_PWM_frequency(self.__speedPin, 227)
    
  def setSpeed(self, step):
    if self.__currentSpeed >= 0
      if self.__currentSpeed < 20
        self.__currentSpeed = self.__currentSpeed + 1 #technically this isn't a curve, but it will call the motor to accelerate more slowly
        self.__pi.hardware_PWM(18, self.__currentSpeed, 500000)
        self.__sleep(.0125)
      elif
        self.__pi.hardware_PWM(18, self.__currentSpeed, 500000)
   
    
    print(self.__pi.get_PWM_frequency(self.__speedPin))
    print(f"Set speed to: {self.__currentSpeed}")
    
  def increaseSpeed(self, amount):
    self.setSpeed(self.__currentSpeed + amount)
    
  def decreaseSpeed(self, amount):
    self.setSpeed(self.__currentSpeed - amount)
    
    def setDirection(self):
      
        gpio.setup(4, gpio.IN)
        gpio.setup(19, gpio.IN)
        gpio.setup(12, gpio.OUT)

         if self.__pi.read(19) == 0:
          if self.__pi.read(4) == 1:
            self.__pi.write(17, 1) #"1" is the same as GPIO.HIGH (forward)
            self.__pi.hardware_PWM(17, 40, 500000)
            print("Moving Up")
            return
          
        if self.__pi.read(4) == 0:
          if self.__pi.read(19) == 1:
            self.__pi.write(17, 0) #"0" is the same as GPIO.LOW (reverse)
            self.__pi.hardware_PWM(17, 40, 500000)
            print("Moving Down")
            return
    
    def getSpeed(self) -> int:
      return self.__currentSpeed
    
    def enable(self):
      print("LC: Enabling")
      
      
      if self.__pi.read(self.__enablePin) == 1:
        print("Disabling")
        self.__pi.write(self.__enablePin, 0)
        self.__pi.hardware_PWM(24, 40, 500000)
        self.__targetSpeed = 40 
        self.__currentSpeed = 40
        return
      
      if self.__pi.read(self.__enablePin) == 0:
        print("enabling")
        self.__pi.write(self.enablePin, 1)
        self.pi.hardware_PWM(24, 40, 500000) #both enable + direction had the step pin, fixed on 3/2/2023
        self.__targetSpeed = 40
        self.__currentSpeed = 40
        return
  
  self.__pi.hardware_PWM(13, 40, 500000) #sets speed to 40 hz if loop fails  
      
class Motor()
  __dir = None
  __speed = None
  __pi = None
  __break = None
  currSpeed = None
  
  def __init__(self, pi, sv, fr, brk):
    self.__pi = pi
    self.__speed = sv
    self.__dir = fr
    self.__break = br
    self.__pi.set_mode(self.__dir, pigpio.OUTPUT)
    self.__pi.set_mode(self.__speed, pigpio.OUTPUT)
    self.__pi.set_mode(self.__break, pigpio.OUTPUT)
    self.__currSpeed = 0
    self.__pi.write(23,0)
    
  def setSpeed(self, speed)
    if speed > 25:
      self.__currSpeed = 25
    elif speed <= 0:
      self.__currSpeed = 0
    else:
      self.__currSpeed = speed
    #print(f"speed was set: {(self.__currSpeed / 25)}")
    self.__pi.set_PWM_frequency(self.__speed, self.__currSpeed)
    
  def speedUp(self, amount)
    self.setSpeed(self.__currSpeed + amount)
  
  def slowDown(self,amount)
    self.setSpeed(self.__currSpeed - amount)
    
  def forward(self):
    self.__pi.write(self.__dir, 0) #may need to swap
    print(f"direction: {self.__pi.read(self.__dir)}")
    
  def reverse(self):
    self.__pi.write(self.__dir, 1) #may need to swap
    print(f"direction: {self.__pi.read(self.__dir)}")
    
  def hardstop(self):
    curr = self.__pi.read(self.__break)
    self.__pi.write(self.__break, curr ^ 1)
    print(f"hard stop: {self.__pi.read(self.__break)}")
    
    self.__pi.write(23, cuur^1)
    
  
      
     
      
