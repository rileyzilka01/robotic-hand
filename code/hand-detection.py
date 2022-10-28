import cv2 as cv
import mediapipe as mp
import time


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
        max_num_hands=1
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
                for id, coord in enumerate(handCoord.landmark):
                    if id == 0:
                        cy = int(h*coord.y)
                        cx = int(w*coord.x)
                        print(f"{id}: x={cx}, y={cy}")
                        cv.circle(img, (cx, cy), 10, (255, 0, 255), cv.FILLED)

                mpDraw.draw_landmarks(img, handCoord, mpHands.HAND_CONNECTIONS)


        cv.imshow("Camera", img)

        key = cv.waitKey(20)
        if key == 27:
            break


if __name__ == "__main__":
    main()