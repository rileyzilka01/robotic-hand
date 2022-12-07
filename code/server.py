
import socket
import time
from queue import Queue
import cv2 as cv
import mediapipe as mp
import numpy as np
import math

# This class handles the Server side of the comunication between the laptop and the brick.
class Server:
    def __init__(self, host, port):
       # setup server socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        # We need to use the ip address that shows up in ipconfig for the usb ethernet adapter that handles the comunication between the PC and the brick
        print("Setting up Server\nAddress: " + host + "\nPort: " + str(port))
        
        serversocket.bind((host, port))
        # queue up to 5 requests
        serversocket.listen(1) 
        self.cs, addr = serversocket.accept()
        print ("Connected to: " + str(addr))

    # Sends set of angles to the brick via TCP.
    # Input: base_angle [Float]: The angle by which we want the base to move
    #        joint_angle [Float]: The angle by which we want to joint to move
    #        queue [Thread-safe Queue]: Mutable data structure to store (and return) the messages received from the client
    def sendAngle(self, base_angle, queue):
        # Format in which the client expects the data: "angle1,angle2"
        data = str(base_angle)
        print("Sending Data: (" + data + ") to robot.")
        self.cs.send(data.encode("UTF-8"))
        # Waiting for the client (ev3 brick) to let the server know that it is done moving
        reply = self.cs.recv(128).decode("UTF-8")
        queue.put(reply)

    # Sends set of angles to the brick via TCP.
    # Input: x [Int]: The x of the end effector
    #        y [Int]: The y of the end effector
    #        queue [Thread-safe Queue]: Mutable data structure to store (and return) the messages received from the client
    def sendPoint(self, x, y, queue):
        # Format in which the client expects the data: "x,y"
        data = str(x) + "," + str(y)
        print("Sending Data: (" + data + ") to robot.")
        self.cs.send(data.encode("UTF-8"))
        # Waiting for the client (ev3 brick) to let the server know that it is done moving
        reply = self.cs.recv(128).decode("UTF-8")
        queue.put(reply)

    # Sends a termination message to the client. This will cause the client to exit "cleanly", after stopping the motors.
    def sendTermination(self):
        self.cs.send("EXIT".encode("UTF-8"))

    # Lets the client know that it should enable safety mode on its end
    def sendEnableSafetyMode(self):
        self.cs.send("SAFETY_ON".encode("UTF-8"))
    
    # Lets the client know that it should disable safety mode on its end
    def sendDisableSafetyMode(self):
        self.cs.send("SAFETY_OFF".encode("UTF-8"))

def main():
    #Server
    host = "192.168.1.194"
    port = 9999
    server = Server(host, port)
    queue = Queue()


    #Camera
    cap = cv.VideoCapture(0)

    #mpDraw
    mpDraw = mp.solutions.drawing_utils

    #Initializing the hand model
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75,
        max_num_hands=2
    )

    while (True):
        #Get frame from webcam
        success, img = cap.read()
        h, w, c = img.shape

        #setRGB
        #img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        #Hands
        results = hands.process(img)
        if results.multi_hand_landmarks:
            for handCoord in results.multi_hand_landmarks:
                coords = handCoord.landmark
                print(coords[0].x*w)
                vec1 = [coords[17].x - coords[0].x, coords[17].y - coords[0].y, coords[17].z - coords[0].z]
                vec2 = [coords[18].x - coords[17].x, coords[18].y - coords[17].y, coords[18].z - coords[17].z]
                numer = np.dot(vec1, vec2)
                denom = np.linalg.norm(vec1) * np.linalg.norm(vec2)
                angle = math.acos(numer/denom)*(180/math.pi)
                if angle > 90:
                    angle = 90
                if angle < 0:
                    angle = 0
                
                ratio = angle/90
                conversion = 120*ratio

                #Send angle to the pi
                server.sendAngle(conversion, queue)

                print(f'Pinky Base Angle: {angle}')
                #print(vec1)
                #for id, coord in enumerate(handCoord.landmark):
                #    if id == 0:
                #         cy = int(h*coord.y)
                #         cx = int(w*coord.x)
                #         #print(f"{id}: x={cx}, y={cy}")
                #         cv.circle(img, (cx, cy), 10, (255, 0, 255), cv.FILLED)

                # mpDraw.draw_landmarks(img, handCoord, mpHands.HAND_CONNECTIONS)


        cv.imshow("Camera", img)

        key = cv.waitKey(20)
        if key == 27:
            break


if __name__ == "__main__":
    main()