import pigpio #importing GPIO library
import time
from spidev import SpiDev

class Motor():
    __dir = None
    __speed = None
    __pi = None
    __break = None
    __currSpeed = None

    def __init__(self, pi, sv, fr, brk):
        self.__pi = pi
        self.__speed = sv
        self.__dir = fr
        self.__break = brk
        self.__pi.set_mode(self.__dir, pigpio.OUTPUT)
        self.__pi.set_mode(self.__speed, pigpio.OUTPUT)
        self.__pi.set_mode(self.__break, pigpio.OUTPUT)
        self.__currSpeed = 0

    def setSpeed(self, speed):
        # sets PW duty cycle, and checks to see if within max-min range
        if speed > 400:
            self.__currSpeed = 400
        elif speed <= 0:
            self.__currSpeed = 0
        else:
            self.__currSpeed = speed
        print(f"speed was set: {(self.__currSpeed / 400)}")
        self.__pi.set_PWM_dutycycle(self.__speed, self.__currSpeed)

    def speedUp(self, amount):
        self.setSpeed(self.__currSpeed + amount)

    def slowDown(self, amount):
        self.setSpeed(self.__currSpeed - amount)

    def forward(self):
        self.__pi.write(self.__dir, 0) #may need to swap
        print(f"direction: {self.__pi.read(self.__dir)}")

    def reverse(self):
        self.__pi.write(self.__dir, 1) #may need to swap
        print(f"direction: {self.__pi.read(self.__dir)}")

    def hardStop(self):
        curr = self.__pi.read(self.__break)
        self.__pi.write(self.__break, curr ^ 1)
        print(f"hard stop: {self.__pi.read(self.__break)}")

class LeadScrew():
    __dir = None
    __speed = None
    __pi = None
    __enable = None

    def __init__(self, pi, direction_pin, step_pin, leadScrew_Enable):

        self.__pi = pi
        self.__speed = step_pin
        self.__enable = leadScrew_Enable


class HallEffectSensor():
    __pin = None
    __pi = None
    __revolutions = None
    __currRevs = None
    __rpms = None
    __startTime = None

    def __init__(self, pi, pin, revolutions):
        self.__pi = pi
        self.__pin = pin
        self.__pi.set_mode(pin, pigpio.INPUT)
        self.__revolutions = revolutions
        self.__rpms = 0
        self.__currRevs = 0
        self.__startTime = time.time()

    def read(self):
        return self.__pi.read(self.__pin)

    def measureRPMs(self):
        # Called if sensor output changes
        tempReading = self.read()
        if (tempReading == 0):
            self.__currRevs += 1
        #else:
            #print("no HE data!")

        if (self.__currRevs == self.__revolutions + 1): #plus 1 means it went full circle
            rpmEndTime = time.time()
            rpmDelta = (rpmEndTime - self.__startTime)
            self.__startTime = time.time()
            self.__rpms = 1.0 / ((rpmDelta) / 60.0)
            self.__currRevs = 0
            print(f"RPM: {self.__rpms}")
            while(self.read() == 0):
                x=0

        return tempReading # self.__rpms

class CurrentSensor():
    __channel = None
    __ZEROAMP = 810
    __HALFAMP = 10
    __spi = None

    def __init__(self, channel):
        self.__channel = channel
        # Start SPI connection
        self.__spi = SpiDev() # Created an object
        self.__spi.open(0, 0)
        self.__spi.max_speed_hz = 1000000

    # Read MCP3008 data
    def read(self):
      adc = self.__spi.xfer2([1,(8+self.__channel)<<4,0])
      data = ((adc[1]&3) << 8) + adc[2]
      return data

    def measureCurrent(self, samples):
        maxVal = 0
        for counter in range(samples):
            reading = self.read()
            if (reading > maxVal):
                maxVal = reading
        amps = ( (maxVal - self.__ZEROAMP) / self.__HALFAMP ) / 2.0
        return amps

