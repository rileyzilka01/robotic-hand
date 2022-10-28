import cv2 as cv
import time



def main():
    #Camera
    cap = cv.VideoCapture(0)

    #Hand Detection
    
    while (True):
        #Get frame from webcam
        success, img = cap.read()

        #Hands
        imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(imgray, 127, 255, 0)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
                
        #Draw contours
        i = 1
        if (i == 1):
            cv.drawContours(img, contours, -1, (255,0,0), 3)
        else:
            #cnt = contours[1]
            for cnt in contours:
                cv.drawContours(img, [cnt], 0, (0,255,0), 3)
                cv.imshow("Camera", img)
                time.sleep(0.5)

        cv.imshow("Camera", img)

        key = cv.waitKey(20)
        if key == 27:
            break


if __name__ == "__main__":
    main()