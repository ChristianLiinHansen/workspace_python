# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 16:20:45 2014

@author: christian
"""

import numpy as np
import cv2
import time

def takeImageFromVideo(cap):
    ret, frame = cap.read()
    cv2.imshow("Image taken", frame)

def main():

    # cap = cv2.VideoCapture('indoor4.mp4')  # In order to play a recorded video
    cap = cv2.VideoCapture(2)  # In order to play the video streamed from a USB webcamera on video2

    # Set the camera in 1080p resolution. So the height is 1080, p = progressive scan = not interlaced. = "Full HD" = 1920 x 1080.
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920) #the parameter is limited to 720 pixels
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080) # At 1024 the parameter is limited to 720 pixels

    print "Width is:", cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    print "Height is:", cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)

    startTime = time.clock()
    waitTime = 3
    flag = False

    while cap.isOpened():
        k = cv2.waitKey(30) & 0xff
        ret, frame = cap.read()
        cv2.imshow('Streaming video', frame)

        currentTime = time.clock()
        # print "The difference in time is", currentTime - startTime
        if currentTime - startTime > waitTime and flag is False:
            takeImageFromVideo(cap)
            flag = True

        # if we push "q" the program ececutes
        if k == 27:
            print("User closed the program...")
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    main()
