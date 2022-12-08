# robotic-hand

This project uses OpenCV and mediapipe to allow a real human to guide the movements of a robotic hand using a camera. The design for the robot is entirely authentic besides the model for the SG90 micro servo.

The code file contains all code required for the base operations of the hand, when running, you must change or add new iPv4 addresses for the server and client to connect. 

The model file contains the servo model and hand part models for design and development.

The project is free to use and develop by anyone, so long as I am mentioned.

# requirements

If you are using an Apple Silicon chip make sure you use a bash terminal to install the following requirements. 

pip3 install mediapipe-silicon
pip3 install opencv-python
pip3 install adafruit-circuitpython-pca9685
pip3 install adafruit-circuitpython-servokit
pip3 install adafruit-circuitpython

If you are using any other chip please use the following mediapipe library instead

pip3 install mediapipe
