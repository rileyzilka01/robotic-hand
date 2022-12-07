import time
from client import *
import ast

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
        self.thumbEnd.angle = 120
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
        self.middleBase.angle = 0
        self.middleEnd.angle = 180
        self.ringBase.angle = 60
        self.ringEnd.angle = 180
        self.pinkyBase.angle = 60
        self.pinkyEnd.angle = 0

    def rockOn(self):
        self.thumbBase.angle = 0
        self.thumbEnd.angle = 120
        self.pointerBase.angle = 180
        self.pointerEnd.angle = 0
        self.middleBase.angle = 120
        self.middleEnd.angle = 0
        self.ringBase.angle = 60
        self.ringEnd.angle = 180
        self.pinkyBase.angle = 180
        self.pinkyEnd.angle = 180

    def singleFingersToFist(self):
        self.thumbBase.angle = 120
        time.sleep(0.25)
        self.thumbEnd.angle = 0
        time.sleep(0.25)
        self.pointerBase.angle = 60
        time.sleep(0.25)
        self.pointerEnd.angle = 180
        time.sleep(0.25)
        self.middleBase.angle = 120
        time.sleep(0.25)
        self.middleEnd.angle = 0
        time.sleep(0.25)
        self.ringBase.angle = 60
        time.sleep(0.25)
        self.ringEnd.angle = 180
        time.sleep(0.25)
        self.pinkyBase.angle = 60
        time.sleep(0.25)
        self.pinkyEnd.angle = 0
        time.sleep(0.25)

    def setHandAngles(self, thumb, pointer, middle, ring, pinky):
        self.thumbBase.angle = int(float(thumb[1]))
        self.thumbEnd.angle = 120-(120*(int(float(thumb[1]))/180))
        self.pointerBase.angle = 180-int(float(pointer[0]))
        self.pointerEnd.angle = int(float(pointer[1])) 
        self.middleBase.angle = int(float(middle[1]))
        self.middleEnd.angle = 180-int(float(middle[1]))
        self.ringBase.angle = 180-int(float(ring[0]))
        self.ringEnd.angle = int(float(ring[1]))
        self.pinkyBase.angle = 180-int(float(pinky[0]))
        self.pinkyEnd.angle = 180-int(float(pinky[1]))


    def runWithCamera(self):
        ans = input("Home Network (1)\nLocal Network (2)\nChoose Option: ")
        while ans not in ['1', '2']:
            ans = input("Home Network (1)\nLocal Network (2)\nChoose Option: ")

        if ans == '1':
            host = "192.168.1.194"
        elif ans == '2':
            host = "169.254.58.57"
            
        port = 9999
        client = Client(host, port)

        #Get the initial angles for getting the estimtion of jacobian
        while (1):
            thumb = client.pollData()
            client.sendDone()
            pointer = client.pollData()
            client.sendDone()
            middle = client.pollData()
            client.sendDone()
            ring = client.pollData()
            client.sendDone()
            pinky = client.pollData()
            client.sendDone()
            thumb = ast.literal_eval(thumb)
            pointer = ast.literal_eval(pointer)
            middle = ast.literal_eval(middle)
            ring = ast.literal_eval(ring)
            pinky = ast.literal_eval(pinky)

            print(f"DATA RECEIVED: {thumb}, {pointer}, {middle}, {ring}, {pinky}")

            self.setHandAngles(thumb, pointer, middle, ring, pinky)
            time.sleep(0.1)

    def terminate(self):
        self.pca.deinit()


def main():
    hand = Hand()

    hand.zeroServos()
    time.sleep(1)

    ans = ''
    while ans != 'stop' or ans in ['1', '2', '3', '4', '5', '0']:
        ans = input("Please enter an input\n\t1: Fist\n\t2: Rock On\n\t3: Middle Finger\n\t4: Finger by Finger to Fist\n\t5: Run With Camera\n\t0: Zero Servos\n")
        if ans == '1': hand.fist()
        elif ans == '2': hand.rockOn()
        elif ans == '3': hand.middleFinger()
        elif ans == '4': hand.singleFingersToFist()
        elif ans == '5': hand.runWithCamera()

        elif ans == '0': hand.zeroServos()
        time.sleep(0.5)

    hand.zeroServos()

    hand.terminate()

if __name__ == "__main__":
    main()
