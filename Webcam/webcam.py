# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 08:33:07 2014

@author: christian
"""

import numpy as np
import cv2

class ImageProcessing(object):
    def __init__(self, cameraIndex):
        self.cap = cv2.VideoCapture(cameraIndex)

    def getFrameFromVideo(self):
        ret, inputImg = self.cap.read()
        return inputImg

    def getRGBchannels(self, inputImg):

        # In OpenCV the channels are defied as img[:,:,0] = blue, img[:,:,1] = green, img[:,:,2] = red
        imgRed = inputImg.copy()
        imgGreen = inputImg.copy()
        imgBlue = inputImg.copy()

        # Get the red channel only, by setting zeropad the green and blue channel
        imgRed[:, :, 0] = 0     # Zeropad blue channel
        imgRed[:, :, 1] = 0     # Zeropad green channel

        # Get the green channel only, by setting zeropad the red and blue channel
        imgGreen[:, :, 0] = 0   # Zeropad blue channel
        imgGreen[:, :, 2] = 0   # Zeropad red channel

        # Get the blue channel only, by setting zeropad the red and green channel
        imgBlue[:, :, 1] = 0    # Zeropad green channel
        imgBlue[:, :, 2] = 0    # Zeropad red channel

        return imgRed, imgGreen, imgBlue

def main():

    # The camera index needs to be fixed to the USB webcamera. Sometimes the cameraIndex = 1 is is the inbuilt webcamera in the PC
    ip = ImageProcessing(1)

    while(True):

        # Capture frame-by-frame
        inputImg = ip.getFrameFromVideo()

        # Read the input instead
        # inputImg = cv2.imread("/home/christian/workspace_python/Webcam/ImageCropped2.png", cv2.CV_LOAD_IMAGE_COLOR)
        cv2.imshow("InputImg", inputImg)

        # Our operations on the frame come here
        # gray = cv2.cvtColor(inputImg, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Grayscale", gray)

        # Show the result
        R, G, B = ip.getRGBchannels(inputImg)
        cv2.imshow("The red channel", R)
        cv2.imshow("The green channel", G)
        cv2.imshow("The blue channel", B)

        # Save the inputImg channel
        # cv2.imwrite("/home/christian/workspace_python/Webcam/writefiles/inputImg.png", inputImg)

        # Break if we hit "ESC"
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            print "User has closed the program..."
            break

    # When everything done, release the capture
    ip.cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

