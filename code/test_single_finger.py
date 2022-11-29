import time

from board import SCL, SDA
import busio

from adafruit_motor import servo
from adafruit_pca9685 import PCA9685

i2c = busio.I2C(SCL, SDA)

pca = PCA9685(i2c)

pca.frequency = 50

servo0 = servo.Servo(pca.channels[0], min_pulse=500, max_pulse=2500)
servo1 = servo.Servo(pca.channels[1], min_pulse=500, max_pulse=2500)

servo0.angle = 150
servo1.angle = 30

time.sleep(2)

servo0.angle = 90
servo1.angle = 90

time.sleep(2)

servo0.angle = 135
servo1.angle = 25

time.sleep(2)

servo0.angle = 180
servo1.angle = 0

time.sleep(1)

servo0.angle = 0
servo1.angle = 180

time.sleep(2)

servo0.angle = 180
servo1.angle = 0

pca.deinit()
