import cv2
from cvzone.HandTrackingModule import HandDetector
import pydirectinput
import webbrowser

detector = HandDetector(detectionCon = 0.8, maxHands=2)
video = cv2.VideoCapture(0)


webbrowser.open_new_tab('https://tetris.com/play-tetris')
#window = webview.create_window("Tetris", 'https://tetris.com/play-tetris', width = 1000, height = 750)
#webview.start()


left = {
    tuple([0, 1, 0, 0, 0]): ('STATE: LEFT', 'left'),
    tuple([1, 1, 0, 0, 0]): ('STATE: ROTATE LEFT', 'z'),
    tuple([1, 1, 1, 1, 1]): ('STATE: HARD DROP', 'space'),
    tuple([1, 0, 0, 0, 0]): ('STATE: DOWN', 'down'),
}
right = {
    tuple([0, 1, 0, 0, 0]): ('STATE: RIGHT', 'right'),
    tuple([1, 1, 0, 0, 0]): ('STATE: ROTATE RIGHT', 'x'),
    tuple([1, 1, 1, 1, 1]): ('STATE: HARD DROP', 'space'),
    tuple([1, 0, 0, 0, 0]): ('STATE: DOWN', 'down'),
}
idle = ('STATE: IDLE', '')

currentInput = idle
framesBetweenInput = 20
while True:
    ret, frame = video.read()
    hands, image = detector.findHands(frame)
    framesBetweenInput -= 1

    if len(hands) == 2 and framesBetweenInput <= 0:
        framesBetweenInput = 10

        leftHand = next(filter(lambda hand: hand["type"] == "Left", hands), None)
        rightHand = next(filter(lambda hand: hand["type"] == "Right", hands), None)

        #not sure why this might happen len(hands) is two
        if leftHand == None or rightHand == None:
            continue

        leftFingerUp = tuple(detector.fingersUp(leftHand))
        rightFingerUp = tuple(detector.fingersUp(rightHand))

        print("left: {} right: {} ".format(leftFingerUp, rightFingerUp))

        leftInput = left.get(leftFingerUp)
        rightInput = right.get(rightFingerUp)

        if (leftInput != None):
            currentInput = leftInput
        elif (rightInput != None):
            currentInput = rightInput
        else:
            currentInput = idle

        pydirectinput.press(currentInput)

    cv2.putText(frame, currentInput[0], (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imshow("Frame", frame)

    #this is to quit out of the video frame
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
