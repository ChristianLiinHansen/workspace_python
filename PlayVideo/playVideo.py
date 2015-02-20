#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 16:20:45 2014

@author: christian
"""

import numpy as np
import cv2
import time
import os

class CameraDriver:


    def __init__(self, cameraIndex):
        self.cameraIndex = cameraIndex
        self.cap = cv2.VideoCapture(cameraIndex)

        # Set the resolution
        self.setResolution()

        #Set the fokus
        self.setFocus(True, 100, 200)

        # Disable autofocus to begin with
        self.autoFocus = np.array(0, dtype=np.uint8)

        # Set focus to a specific value. High values for nearby objects and
        # low values for distant objects.
        self.absoluteFocus = np.array(0, dtype=np.uint8)

         # sharpness (int)    : min=0 max=255 step=1 default=128 value=128
        self.sharpness = np.array(128, dtype=np.uint8)

    def setResolution(self):
        # Set the camera in 1080p resolution. So the height is 1080, p = progressive scan = not interlaced. = "Full HD" = 1920 x 1080.
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080)
        print "Pixel width is:", self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
        print "Pixel height is:", self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)

    def setFocus(self, autoFocus, absolutFocus, sharpness):

        if autoFocus:
            # Set autofocus ON
            os.system('v4l2-ctl -d ' + str(self.cameraIndex) + ' -c focus_auto=' + str(int(autoFocus)))
        else:
            # Set autofocus OFF
            os.system('v4l2-ctl -d ' + str(self.cameraIndex) + ' -c focus_auto=' + str(int(autoFocus)))

            # Set focus to a specific value. High values for nearby objects and
            # low values for distant objects.
            os.system('v4l2-ctl -d ' + str(self.cameraIndex) + ' -c focus_absolute=' + str(absolutFocus))

            # sharpness (int)    : min=0 max=255 step=1 default=128 value=128
            os.system('v4l2-ctl -d ' + str(self.cameraIndex) + ' -c sharpness=' + str(sharpness))

    def getImg(self):
        if self.cap.isOpened():
            ret, img = self.cap.read()
            return img
        else:
            print 'Cant open video at cameraindex:', self.cameraIndex

    def showImg(self, nameOfWindow, image, scale):
        imgCopy = image.copy()
        image_show = self.scaleImg(imgCopy, scale)
        cv2.imshow(nameOfWindow, image_show)
        cv2.imwrite("/home/christian/workspace_python/MasterThesis/SeedDetection/writefiles/" + str(nameOfWindow) + ".jpg", image_show)

    def scaleImg(self, image, scale):
        img_scale = cv2.resize(image, (0, 0), fx=scale, fy=scale)
        return img_scale

    def autoFocusTrackBar(self, nameOfWindow):
        self.autoFocus = self.trackbarListener("Autofocus", nameOfWindow)
        self.addTrackbar("Autofocus", nameOfWindow, self.autoFocus, 1)

        print "The autofocus is:", self.autoFocus
        self.setFocus(self.autoFocus, 100, 128)

    def absolutFocusTrackBar(self, nameOfWindow):
        self.absoluteFocus = self.trackbarListener("Absolute focus", nameOfWindow)
        self.addTrackbar("Absolute focus", nameOfWindow, self.absoluteFocus, 100)

        # if self.autoFocus:
        #     self.setFocus(self.autoFocus, self.absoluteFocus, self.sharpness)

    def sharpnessTrackBar(self, nameOfWindow):
        self.sharpness = self.trackbarListener("Sharpness", nameOfWindow)
        self.addTrackbar("Sharpness", nameOfWindow, self.sharpness, 255)

        # if self.autoFocus:
        #     self.setFocus(self.autoFocus, self.absoluteFocus, self.sharpness)


    def addTrackbar(self, nameOfTrackbar, nameOfWindow, value, maxValue):
        cv2.namedWindow(nameOfWindow)
        cv2.createTrackbar(nameOfTrackbar, nameOfWindow, value, maxValue, self.nothing)

    def trackbarListener(self, nameOfTrackbar, nameOfWindow):
        value = cv2.getTrackbarPos(nameOfTrackbar, nameOfWindow)
        return value

    def nothing(self, x):
        pass

    def getCroppedImg(self, nameOfWindow, img):
        offset_x = 400
        offset_y = 200
        croppedImg = img.copy()
        croppedImg = croppedImg[offset_y:img.shape[0]-offset_y, offset_x:img.shape[1]-offset_x]
        cv2.imshow(nameOfWindow, croppedImg)
        cv2.imwrite("/home/christian/workspace_python/MasterThesis/SeedDetection/writefiles/" + str(nameOfWindow) + ".jpg", croppedImg)
        return croppedImg

    def closeDown(self):
        print("User closed the program...")
        cv2.destroyAllWindows()
        self.cap.release()

def main():

    # In order to play the video streamed from a USB webcamera the 0 parameter is used.
    # However if the cameraIndex is changed, change the argument.
    cd = CameraDriver(0)

    startTime = time.clock()
    waitTime = 1
    flag = True

    nameOfWindow = "Streaming video"
    image_ratio = 0.5

    while cd.cap.isOpened():
        k = cv2.waitKey(30) & 0xff
        image = cd.getImg()

        # The autofocus setting.
        cd.autoFocusTrackBar(nameOfWindow)
        # cd.absolutFocusTrackBar(nameOfWindow)
        # cd.sharpnessTrackBar(nameOfWindow)

        cd.showImg(nameOfWindow, image, image_ratio)
        currentTime = time.clock()
        # print "The difference in time is", currentTime - startTime
        if currentTime - startTime > waitTime and flag is False:
            takeImageFromVideo(cap, "ImageFromVideo")
            flag = True

        # if we push "q" the program ececutes
        if k == 27:
            cd.closeDown()
            break

if __name__ == '__main__':
    main()
