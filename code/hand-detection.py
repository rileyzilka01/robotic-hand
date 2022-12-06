import cv2 as cv
import mediapipe as mp
import time
import numpy as np
import math


def main():
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
                print(f'Pinky Base Angle: {angle}')
                #print(vec1)
                for id, coord in enumerate(handCoord.landmark):
                    if id == 0:
                        cy = int(h*coord.y)
                        cx = int(w*coord.x)
                        #print(f"{id}: x={cx}, y={cy}")
                        cv.circle(img, (cx, cy), 10, (255, 0, 255), cv.FILLED)

                mpDraw.draw_landmarks(img, handCoord, mpHands.HAND_CONNECTIONS)


        cv.imshow("Camera", img)

        key = cv.waitKey(20)
        if key == 27:
            break


if __name__ == "__main__":
    main()