from time import time

import cv2
from cvzone.HandTrackingModule import HandDetector
import pydirectinput
import webbrowser

# COMMAND SETUP
# Down = [1,1,1,1,1]
# Rotate Left = [1,1,0,0,0]
# Rotate Right = [1,0,0,0,1]
# Idle = [0,0,0,0,0]
# Right = [0,1,0,0,0]
# Left= [0,0,0,0,1]

detector = HandDetector(detectionCon=0.8, maxHands=2)
video = cv2.VideoCapture(0)

framesBetweenInput = 20
# webbrowser.open_new_tab('https://tetris.com/play-tetris')
# window = webview.create_window("Tetris", 'https://tetris.com/play-tetris', width = 1000, height = 750)
# webview.start()

left = {
    (0, 1, 0, 0, 1): ('STATE: ROTATE LEFT', 'z'),
    (1, 1, 0, 0, 0): ('STATE: LEFT', 'left'),
    (1, 0, 0, 0, 0): ('STATE: DOWN', 'down'),
}
right = {
    (0, 1, 0, 0, 0): ('STATE: ROTATE RIGHT', 'x'),
    (1, 1, 0, 0, 0): ('STATE: RIGHT', 'right'),
    (1, 1, 1, 1, 1): ('STATE: HARD DROP', 'space'),
}

def getInput(hands):
    rightHand = tuple(detector.fingersUp(hands[0]))[1:]
    leftHand = tuple(detector.fingersUp(hands[1]))[1:]

    currentInput = left.get(leftHand)
    if currentInput is None:
        currentInput = right.get(rightHand)

    if currentInput is None:
        currentInput = ("State: Idle", '')

    return currentInput


secSinceLastInput = 0
currentInput = ("", "")

while True:
    ret, frame = video.read()
    hands, image = detector.findHands(frame)

    if len(hands) == 2 and time() > secSinceLastInput + .5:
        secSinceLastInput = time()

        currentInput = getInput(hands)

        pydirectinput.press(currentInput[1])

    cv2.putText(frame, currentInput[0], (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow("Frame", frame)

    # this is to quit out of the video frame
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
