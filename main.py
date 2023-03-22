import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import pydirectinput
import webbrowser

#COMMAND SETUP
# Down = [1,1,1,1,1]
# Rotate Left = [1,1,0,0,0]
# Rotate Right = [1,0,0,0,1]
# Idle = [0,0,0,0,0]
# Right = [0,1,0,0,0]
# Left= [0,0,0,0,1]

detector = HandDetector(detectionCon = 0.8, maxHands=1)
video = cv2.VideoCapture(0)

framesBetweenInput = 20
webbrowser.open_new_tab('https://tetris.com/play-tetris')
#window = webview.create_window("Tetris", 'https://tetris.com/play-tetris', width = 1000, height = 750) 
#webview.start()

inputs = {
    #Note: changed the gesture for moving piece down
    tuple([1,0,0,0,0]) : ('STATE: DOWN', 'down'),
    tuple([1,1,0,0,0]) : ('STATE: ROTATE LEFT', 'z'),
    tuple([1,0,0,0,1]) : ('STATE: ROTATE RIGHT', 'x'),
    tuple([0,0,0,0,0]) : ('STATE: IDLE', ''),
    tuple([0,1,0,0,0]) : ('STATE: LEFT', 'left'),
    tuple([0,0,0,0,1]) : ('STATE: RIGHT', 'right'),
    #I felt holding all fingers up is more natural for hard drop, if you disagree feel free to change the gestures
    tuple([1,1,1,1,1]) : ('STATE: HARD DROP', 'space'),
}

while True:
    ret, frame = video.read()
    hands, image = detector.findHands(frame)
    framesBetweenInput -= 1
    if hands and framesBetweenInput <= 0:
        framesBetweenInput = 10
        lmlist = hands[0]
        fingerUp = detector.fingersUp(lmlist)
        print(fingerUp);
        currentInput = inputs.get(tuple(fingerUp))

        if currentInput != None:
            cv2.putText(frame, currentInput[0], (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            pydirectinput.press(currentInput[1])


    cv2.imshow("Frame", frame)
    #this is to quit out of the video frame
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
