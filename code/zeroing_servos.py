import time

from board import SCL, SDA
import busio

from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)

pca = PCA9685(i2c)

pca.frequency = 50

thumbBase = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500)
thumbEnd = servo.Servo(pca.channels[1], min_pulse=500, max_pulse=2500)
pointerBase = servo.Servo(pca.channels[2], min_pulse=500, max_pulse=2500)
pointerEnd = servo.Servo(pca.channels[3], min_pulse=500, max_pulse=2500)
middleBase = servo.Servo(pca.channels[4], min_pulse=500, max_pulse=2500)
middleEnd = servo.Servo(pca.channels[5], min_pulse=500, max_pulse=2500)
ringBase = servo.Servo(pca.channels[6], min_pulse=500, max_pulse=2500)
ringEnd = servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2500)
pinkyBase = servo.Servo(pca.channels[8], min_pulse=500, max_pulse=2500)
pinkyEnd = servo.Servo(pca.channels[9], min_pulse=500, max_pulse=2500)



pca.deinit()
