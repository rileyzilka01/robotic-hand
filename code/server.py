
import socket
from queue import Queue
import cv2 as cv
import mediapipe as mp
import numpy as np
import math

class Server:
    def __init__(self, host, port):
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        print("Setting up Server\nAddress: " + host + "\nPort: " + str(port))
        serversocket.bind((host, port))

        #5 items in the queue
        serversocket.listen(5) 
        self.cs, addr = serversocket.accept()
        print ("Connected to: " + str(addr))

    def sendAngle(self, angles, queue):
        thumb = str(angles[0])
        pointer = str(angles[1])
        middle = str(angles[2])
        ring = str(angles[3])
        pinky = str(angles[4])
        #print(f"Sending Data: [{thumb}, {pointer}, {middle}, {ring}, {pinky}] to robot.")
        self.cs.send(thumb.encode("UTF-8"))
        # Waiting for the client to send a response to the server
        reply = self.cs.recv(128).decode("UTF-8")
        queue.put(reply)
        self.cs.send(pointer.encode("UTF-8"))
        # Waiting for the client to send a response to the server
        reply = self.cs.recv(128).decode("UTF-8")
        queue.put(reply)
        self.cs.send(middle.encode("UTF-8"))
        # Waiting for the client to send a response to the server
        reply = self.cs.recv(128).decode("UTF-8")
        queue.put(reply)
        self.cs.send(ring.encode("UTF-8"))
        # Waiting for the client to send a response to the server
        reply = self.cs.recv(128).decode("UTF-8")
        queue.put(reply)
        self.cs.send(pinky.encode("UTF-8"))
        # Waiting for the client to send a response to the server
        reply = self.cs.recv(128).decode("UTF-8")
        queue.put(reply)

def getAngles(coords, fingerBase, fingerEnd):
    #This function calculates the angles between the joints provided

    #Calculate Base Angle
    vec1 = [coords[fingerBase[1]].x - coords[fingerBase[0]].x, coords[fingerBase[1]].y - coords[fingerBase[0]].y, coords[fingerBase[1]].z - coords[fingerBase[0]].z]
    vec2 = [coords[fingerBase[2]].x - coords[fingerBase[1]].x, coords[fingerBase[2]].y - coords[fingerBase[1]].y, coords[fingerBase[2]].z - coords[fingerBase[1]].z]
    numer = np.dot(vec1, vec2)
    denom = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    angle = math.acos(numer/denom)*(180/math.pi)
    if angle > 90:
        angle = 90
    if angle < 0:
        angle = 0
    
    ratio = angle/90
    baseAngle = 120*ratio

    #Calculate End Angle
    vec1 = [coords[fingerEnd[1]].x - coords[fingerEnd[0]].x, coords[fingerEnd[1]].y - coords[fingerEnd[0]].y, coords[fingerEnd[1]].z - coords[fingerEnd[0]].z]
    vec2 = [coords[fingerEnd[2]].x - coords[fingerEnd[1]].x, coords[fingerEnd[2]].y - coords[fingerEnd[1]].y, coords[fingerEnd[2]].z - coords[fingerEnd[1]].z]
    numer = np.dot(vec1, vec2)
    denom = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    angle = math.acos(numer/denom)*(180/math.pi)
    if angle > 90:
        angle = 90
    if angle < 0:
        angle = 0
    
    ratio = angle/90
    endAngle = 180*ratio

    return baseAngle, endAngle

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
        max_num_hands=1
    )

    #The point sets for each finger (to get the angles)
    pointSets = [[[1, 2, 3], [2, 3, 4]],        #Thumb
                 [[0, 5, 6], [5, 6, 7]],        #Pointer
                 [[0, 9, 10], [9, 10, 11]],     #Middle
                 [[0, 13, 14], [13, 14, 15]],   #Ring
                 [[0, 17, 18], [17, 18, 19]]]   #Pinky

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
                angles = []
                for i in range(0, len(pointSets)):
                    baseAngle, endAngle = getAngles(coords, pointSets[i][0], pointSets[i][1])
                    angles.append([baseAngle, endAngle])

                #Send the list of angles to the pi
                server.sendAngle(angles, queue)

                print(f'Angles: {angles}')


        cv.imshow("Camera", img)

        key = cv.waitKey(20)
        if key == 27:
            break


if __name__ == "__main__":
    main()