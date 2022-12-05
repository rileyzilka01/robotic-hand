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

for i in range(0, 100):
    servo0.angle -= 1
    time.sleep(0.02)

for i in range(0, 180):
    servo1.angle += 1
    time.sleep(0.02)

while servo0.angle < 179:
    servo0.angle += 1
    time.sleep(0.02)

while servo1.angle > 1:
    servo1.angle -= 1
    time.sleep(0.02)

servo0.angle = 180
servo1.angle = 0

pca.deinit()
