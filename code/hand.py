import time

from board import SCL, SDA
import busio

from adafruit_motor import servo
from adafruit_pca9685 import PCA9685 

class Hand():

    def __init__(self):
        self.i2c = busio.I2C(SCL, SDA)
        self.pca = PCA9685(self.i2c)
        self.pca.frequency = 50

        self.thumbBase = servo.Servo(self.pca.channels[0], min_pulse=500, max_pulse=2500)
        self.thumbEnd = servo.Servo(self.pca.channels[1], min_pulse=500, max_pulse=2500)
        self.pointerBase = servo.Servo(self.pca.channels[2], min_pulse=500, max_pulse=2500)
        self.pointerEnd = servo.Servo(self.pca.channels[3], min_pulse=500, max_pulse=2500)
        self.middleBase = servo.Servo(self.pca.channels[4], min_pulse=500, max_pulse=2500)
        self.middleEnd = servo.Servo(self.pca.channels[5], min_pulse=500, max_pulse=2500)
        self.ringBase = servo.Servo(self.pca.channels[6], min_pulse=500, max_pulse=2500)
        self.ringEnd = servo.Servo(self.pca.channels[7], min_pulse=500, max_pulse=2500)
        self.pinkyBase = servo.Servo(self.pca.channels[8], min_pulse=500, max_pulse=2500)
        self.pinkyEnd = servo.Servo(self.pca.channels[9], min_pulse=500, max_pulse=2500)

    def zeroServos(self):
        self.thumbBase.angle = 0
        self.thumbEnd.angle = 180
        self.pointerBase.angle = 180
        self.pointerEnd.angle = 0
        self.middleBase.angle = 0
        self.middleEnd.angle = 180
        self.ringBase.angle = 180
        self.ringEnd.angle = 0
        self.pinkyBase.angle = 180
        self.pinkyEnd.angle = 180


    def fist(self):
        self.thumbBase.angle = 120
        self.thumbEnd.angle = 0
        self.pointerBase.angle = 60
        self.pointerEnd.angle = 180
        self.middleBase.angle = 120
        self.middleEnd.angle = 0
        self.ringBase.angle = 60
        self.ringEnd.angle = 180
        self.pinkyBase.angle = 60
        self.pinkyEnd.angle = 0

    def middleFinger(self):
        self.thumbBase.angle = 120
        self.thumbEnd.angle = 0
        self.pointerBase.angle = 60
        self.pointerEnd.angle = 180
        self.ringBase.angle = 60
        self.ringEnd.angle = 180
        self.pinkyBase.angle = 60
        self.pinkyEnd.angle = 0

    def rockOn(self):
        self.middleBase.angle = 120
        self.middleEnd.angle = 0
        self.ringBase.angle = 60
        self.ringEnd.angle = 180

    def testMovements(self):

        self.zeroServos()
        time.sleep(1)

        #Finger by finger make a fist
        for i in range(5):
            for j in range(179):
                if j < 120:
                    if i == 0: self.pinkyBase.angle = (180-j)
                    elif i == 1: self.ringBase.angle = (180-j)
                    elif i == 2: self.middleBase.angle = j
                    elif i == 3: self.pointerBase.angle = (180-j)
                    elif i == 4: self.thumbBase.angle = j
                
                if i == 0: self.pinkyEnd.angle = (180-j)
                elif i == 1: self.ringEnd.angle = j
                elif i == 2: self.middleEnd.angle = (180-j)
                elif i == 3: self.pointerEnd.angle = j
                elif i == 4: self.thumbEnd.angle = (180-j)
                time.sleep(0.02)

        #Gradually release the fist
        for i in range(179):
            if i < 120:
                self.thumbBase.angle = (120-i)
                self.pointerBase.angle = (60+i)
                self.middleBase.angle = (120-i)
                self.ringBase.angle = (60+i)
                self.pinkyBase.angle = (60+i)
            self.thumbEnd.angle = i
            self.pointerEnd.angle = (180-i)
            self.middleEnd.angle = i
            self.ringEnd.angle = (180-i)
            self.pinkyEnd.angle = i
            time.sleep(0.02)

        #Make the fist quickly
        self.fist()
        time.sleep(1)

        self.zeroServos()

    def terminate(self):
        self.pca.deinit()


def main():
    hand = Hand()

    hand.zeroServos()
    time.sleep(1)

    #hand.testMovements()
    #time.sleep(1)

    for i in range(5):
        hand.fist()
        time.sleep(0.5)
        hand.zeroServos()
        time.sleep(0.5)

    #hand.middleFinger()
    #time.sleep(1)

    #hand.rockOn()
    #time.sleep(5)

    hand.zeroServos()

    hand.terminate()

if __name__ == "__main__":
    main()
