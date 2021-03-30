import cv2
import numpy as np


def nothing(x):
    pass


path = '/Users/shysliannykovdenys/Desktop/MWR/Task1/F1_r1.MOV'

video = cv2.VideoCapture(path)

frame_grabbed, frame = video.read()
cv2.namedWindow("Controls")
cv2.createTrackbar("1.LowH", "Controls", 175, 180, nothing)
cv2.createTrackbar("2.HighH", "Controls", 180, 180, nothing)
cv2.createTrackbar("3.LowS", "Controls", 70, 255, nothing)
cv2.createTrackbar("4.HighS", "Controls", 255, 255, nothing)
cv2.createTrackbar("5.LowV", "Controls", 0, 255, nothing)
cv2.createTrackbar("6.HighV", "Controls", 255, 255, nothing)
cv2.createTrackbar("7.cR", "Controls", 5, 20, nothing)

while frame_grabbed:
    imHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    low_r = np.array([cv2.getTrackbarPos("1.LowH", "Controls"),
                      cv2.getTrackbarPos("3.LowS", "Controls"),
                      cv2.getTrackbarPos("5.LowV", "Controls")])
    high_r = np.array([cv2.getTrackbarPos("2.HighH", "Controls"),
                       cv2.getTrackbarPos("4.HighS", "Controls"),
                       cv2.getTrackbarPos("6.HighV", "Controls")])

    cR = cv2.getTrackbarPos("7.cR", "Controls")
    if cR == 0:
        cR = 1
    imInRange = cv2.inRange(imHSV, low_r, high_r)

    imInRange = cv2.erode(imInRange, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (cR, cR)))
    imInRange = cv2.dilate(imInRange, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (cR, cR)))
    imInRange = cv2.dilate(imInRange, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (cR, cR)))
    imInRange = cv2.erode(imInRange, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (cR, cR)))
    oMoments = cv2.moments(imInRange)
    dM10 = oMoments['m10']
    dArea = oMoments['m00']
    if dArea > 0:
        posX = int(dM10 / dArea)
        height, width, channels = frame.shape
        global error
        error = round((posX - width / 2) / width)
        if error > 0:
            cv2.line(frame, (round(width / 2), 16), (posX, 16), (0, 0, 0), 10)
        else:
            cv2.line(frame, (posX, 16), (round(width / 2), 16), (0, 0, 0), 10)
    else:
        error = None

    cv2.imshow('Source', frame)
    cv2.imshow('Transformed', imInRange)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    frame_grabbed, frame = video.read()

video.release()
cv2.destroyAllWindows()
