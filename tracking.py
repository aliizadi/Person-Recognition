from imutils.video import VideoStream
import argparse
import imutils
import cv2
import time


firstFrame = None
initBB2 = None
fps = None
differ = None
now = ''
frame_counter = 0
tracker_on = 0

video = cv2.VideoCapture('/home/aliiz/Desktop/Bsc project/codes/video.mp4')


while video.isOpened():

    ret, frame = video.read()

    frame = imutils.resize(frame, width=500)

    frame_counter = frame_counter + 1
    if frame_counter > 1:

        (H, W) = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if firstFrame is None:
            firstFrame = gray
            continue

        frameDelta = cv2.absdiff(firstFrame, gray)

        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=2)

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        cnts = cnts[0]

        contour_count = 0
        for c in cnts:
            contour_count = contour_count + 1

            if cv2.contourArea(c) < 500:
                continue

            (x, y, w, h) = cv2.boundingRect(c)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # cv2.draw('frame', frame)
            cv2.imshow('image', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        time.sleep(0.1)



        # time.sleep(5)
