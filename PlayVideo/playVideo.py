#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 16:20:45 2014

@author: christian
"""

import numpy as np
import cv2
import cv
import time
import os

class CameraDriverCV:
    def __init__(self, cameraIndex):
        self.camera = cv.CaptureFromCAM(cameraIndex)
        self.setResolution()
        self.setFPS(30)

        # Storage for image processing.
        self.currentFrame = None

    def getImage(self):
        # Get image from camera.
        image =  cv.QueryFrame(self.camera)
        return image

    def setFPS(self, fps):
        pass

    def setResolution(self):
        cv.SetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_WIDTH, 1920)
        cv.SetCaptureProperty(self.camera, cv.CV_CAP_PROP_FRAME_HEIGHT, 1080)

    def setFocus(self):
        # Disable autofocus
        os.system('v4l2-ctl -d 1 -c focus_auto=0')

        # Set focus to a specific value. High values for nearby objects and
        # low values for distant objects.
        os.system('v4l2-ctl -d 1 -c focus_absolute=0')

        # sharpness (int)    : min=0 max=255 step=1 default=128 value=128
        os.system('v4l2-ctl -d 1 -c sharpness=200')

    def showImg(self, nameOfWindow, image):
        cv.ShowImage(nameOfWindow, image)

class CameraDriver:
    def __init__(self, cameraIndex):

        self.cameraIndex = cameraIndex
        self.cap = cv2.VideoCapture(cameraIndex)

        # Set the resolution
        self.setResolution()

        # Disable autofocus to begin with
        self.autoFocus = np.array(0, dtype=np.uint8)

        # Set focus to a specific value. High values for nearby objects and
        # low values for distant objects.
        self.absoluteFocus = np.array(0, dtype=np.uint8)

         # sharpness (int)    : min=0 max=255 step=1 default=128 value=128
        self.sharpness = np.array(128, dtype=np.uint8)

        # Take a picture bottom
        self.bottom = np.array(0, dtype=np.uint8)

    def setResolution(self):
        # Set the camera in 1080p resolution. So the height is 1080, p = progressive scan = not interlaced. = "Full HD" = 1920 x 1080.
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920)      # Slight delay with full HD in app. 1 sec.
        self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080)
        # self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280)      # Better with delay
        # self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720)
        # self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1024)
        # self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 576)
        # self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 848)
        # self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
        # self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 640)
        # self.cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

        print "Pixel width is:", self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
        print "Pixel height is:", self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)

    def setAutoFocus(self, autoFocus, absolutFocus, sharpness):

        # If the autoFocus is ON, we use the autofocus
        if autoFocus:
            os.system('v4l2-ctl -d ' + str(self.cameraIndex) + ' -c focus_auto=' + str(int(autoFocus)))

        # Else we set the autoFocus to OFF, and use manuel focus
        else:
            os.system('v4l2-ctl -d ' + str(self.cameraIndex) + ' -c focus_auto=' + str(int(autoFocus)))
            os.system('v4l2-ctl -d ' + str(self.cameraIndex) + ' -c focus_absolute=' + str(absolutFocus))
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

    def saveImg(self, nameOfWindow, image):
        cv2.imwrite("/home/christian/workspace_python/MasterThesis/SeedDetection/writefiles/" + str(nameOfWindow) + ".jpg", image)

    def scaleImg(self, image, scale):
        img_scale = cv2.resize(image, (0, 0), fx=scale, fy=scale)
        return img_scale

    def autoFocusTrackBar(self, nameOfWindow):
        self.autoFocus = self.trackbarListener("Autofocus", nameOfWindow)
        self.addTrackbar("Autofocus", nameOfWindow, self.autoFocus, 1)
        self.setAutoFocus(self.autoFocus, self.absoluteFocus, self.sharpness)

    def absolutFocusTrackBar(self, nameOfWindow):
        self.absoluteFocus = self.trackbarListener("Absolute focus", nameOfWindow)
        self.addTrackbar("Absolute focus", nameOfWindow, self.absoluteFocus, 255)

    def sharpnessTrackBar(self, nameOfWindow):
        self.sharpness = self.trackbarListener("Sharpness", nameOfWindow)
        self.addTrackbar("Sharpness", nameOfWindow, self.sharpness, 255)

    def takePictureTrackBar(self, nameOfWindow):
        self.bottom = self.trackbarListener("Take picture", nameOfWindow)
        self.addTrackbar("Take picture", nameOfWindow, self.bottom, 1)

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
        return croppedImg

    def closeDown(self):
        print("User closed the program...")
        cv2.destroyAllWindows()
        self.cap.release()

def main():

    # In order to play the video streamed from a USB webcamera the 0 parameter is used.
    # However if the cameraIndex is changed, change the argument.
    cd = CameraDriver(0)
    nameOfVideoWindow = "VideoStream"
    nameOfImgWindow = "ImageFromVideo"
    image_show_ratio = 0.5

    imgFlag = False

    # while cd.cap.isOpened():
    while True:
        # image = cd.getCroppedImg(nameOfWindow, cd.getImg())
        image = cd.getImg()

        # The trackbar settings.
        cd.autoFocusTrackBar(nameOfVideoWindow)
        cd.absolutFocusTrackBar(nameOfVideoWindow)
        cd.sharpnessTrackBar(nameOfVideoWindow)
        cd.takePictureTrackBar(nameOfVideoWindow)

        # Stream the video input
        cd.showImg(nameOfVideoWindow, image, image_show_ratio)

        # If the user takes a photo...
        if cd.bottom is 1 and imgFlag is False:
            cd.saveImg(nameOfImgWindow, image)
            croppedImg = cd.getCroppedImg(nameOfImgWindow, image)
            cd.saveImg("ImageCropped", croppedImg)

            imgFlag = True

        # If the user set the bottom back again...
        if cd.bottom is 0 and imgFlag is True:
            cv2.destroyWindow(nameOfImgWindow)
            imgFlag = False

        # If the user push "ESC" the program ececutes
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            cd.closeDown()
            break

if __name__ == '__main__':
    main()
