import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import pydirectinput

#COMMAND SETUP
# Down = [1,1,1,1,1]
# Rotate = [1,0,0,0,0]
# Idle = [0,0,0,0,0]
# Right = [0,1,0,0,0]
# Left= [0,0,0,0,1]

detector = HandDetector(detectionCon = 0.8, maxHands=1)
video = cv2.VideoCapture(0)

framesBetweenInput = 20

while True:
    ret, frame = video.read()
    hands, image = detector.findHands(frame)
    framesBetweenInput -= 1
    if hands and framesBetweenInput <= 0:
        framesBetweenInput = 20
        lmlist = hands[0]
        fingerUp = detector.fingersUp(lmlist)
        print(fingerUp);
        if fingerUp==[1,1,1,1,1]:
            cv2.putText(frame, 'STATE: DOWN', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            pydirectinput.press('down')
        if fingerUp==[0,0,0,0,0]:
            cv2.putText(frame, 'STATE: IDLE', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        if fingerUp==[1,0,0,0,0]:
            cv2.putText(frame, 'STATE: ROTATE', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            pydirectinput.press('up')
        if fingerUp==[0,1,0,0,0]:
            cv2.putText(frame, 'STATE: RIGHT', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            pydirectinput.press('right')
        if fingerUp==[0,0,0,0,1]:
            cv2.putText(frame, 'STATE: LEFT', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            pydirectinput.press('left')
    cv2.imshow("Frame", frame)
    #this is to quit out of the video frame
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
