# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 16:20:45 2014

@author: christian
"""

import numpy as np
import cv2
import time

def takeImageFromVideo(cap, nameOfWindow):
    ret, frame = cap.read()
    offset_x = 400
    offset_y = 200
    imgCrop = cropImage(frame, offset_x, offset_y)
    cv2.imshow(nameOfWindow, imgCrop)
    cv2.imwrite("/home/christian/workspace_python/MasterThesis/SeedDetection/writefiles/" + str(nameOfWindow) + ".jpg", imgCrop)

def cropImage(img, offset_x, offset_y):
    crop_img = img.copy()
    # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
    return crop_img[offset_y:img.shape[0]-offset_y, offset_x:img.shape[1]-offset_x]

def main():

    # cap = cv2.VideoCapture('indoor4.mp4')  # In order to play a recorded video
    cap = cv2.VideoCapture(2)  # In order to play the video streamed from a USB webcamera on video2

    # Set the camera in 1080p resolution. So the height is 1080, p = progressive scan = not interlaced. = "Full HD" = 1920 x 1080.
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080)


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
            takeImageFromVideo(cap, "ImageFromVideo")
            flag = True

        # if we push "q" the program ececutes
        if k == 27:
            print("User closed the program...")
            break

    cv2.destroyAllWindows()
    cap.release()

if __name__ == '__main__':
    main()
