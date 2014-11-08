# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 14:29:05 2014

@author: christian
"""
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 16:31:37 2014

@author: christian
"""

##########################################
# References
##########################################
# Trackbar
# http://docs.opencv.org/trunk/doc/py_tutorials/py_gui/py_trackbar/py_trackbar.html

# Tracking the circles
#http://stackoverflow.com/questions/21612258/filled-circle-detection-using-cv2-in-python

##########################################
# Libraries
##########################################
import numpy as np
import cv2
import cv

##########################################
# Functions
##########################################

#For the trackbar
def nothing(x):
    pass


##########################################
# Main
##########################################

video = 'DSC_0015.MOV'
#cap = cv2.VideoCapture('DSC_0005.MOV')     # 
#cap = cv2.VideoCapture('DSC_0006.MOV')     # 
#cap = cv2.VideoCapture('DSC_0007.MOV')     # 
#cap = cv2.VideoCapture('DSC_0008.MOV')     # 
#cap = cv2.VideoCapture('DSC_0009.MOV')     # 
#cap = cv2.VideoCapture('DSC_00010.MOV')    # Blue bricks only
#cap = cv2.VideoCapture('DSC_0013.MOV')      # Green and blue bricks
cap = cv2.VideoCapture(video)      # Test video loop

maxValue_trackbar = 255
threshold_trackbar = 20

while(1):
    
    #Read each image and store it in "frame"
    sucessfully_read, frame = cap.read()
   # width = cap.get(cv.CV_CAP_PROP_FPS)    
    #print("width is:", width)
    if not sucessfully_read:
        print("Video ended. Reloading video...")
        #cap = cv2.VideoCapture(video)   # works but is slow
        #frame = cap.read()
        #cap.set(cv.CV_CAP_PROP_POS_MSEC, 0)
        #cap.set(cv.CV_CAP_PROP_POS_FRAMES, 0)
        cap.set(cv.CV_CAP_PROP_POS_AVI_RATIO, 0)        
        continue; 
    
    # Resize each frame
    factor = 0.5
    smallImg = cv2.resize(frame, (0,0), fx=factor, fy=factor)
    
    # Get the grayscale image
    grayImg = cv2.cvtColor(smallImg, cv2.COLOR_BGR2GRAY)    
    
    # Create a black image, a window. Otherwise the trackbar would not work...
    cv2.namedWindow('image')  
    
    # create trackbars for color change
    cv2.createTrackbar('Threshold','Thresholded video',100,maxValue_trackbar,nothing)
   
    # Do the thresholding with trackbar
    ret, threshold_img = cv2.threshold(grayImg,threshold_trackbar,maxValue_trackbar,cv2.THRESH_BINARY_INV)
    cv2.imshow('Thresholded video',threshold_img)
    
    # get current positions of four trackbars
    threshold_trackbar = cv2.getTrackbarPos('Threshold','Thresholded video')
    
    #Do a little morphology - Do some closing, i.e. erode and then dialate
    kernel = np.ones((5,5),np.uint8)
    erosion = cv2.erode(threshold_img,kernel,iterations = 2)
    #cv2.imshow('Erosion video',erosion)
    #Do a little morphology - then dialate
    dilation = cv2.dilate(erosion,kernel,iterations = 2)
    cv2.imshow('Dilation video',dilation)
    
    # Finding the countours
    contours, hierarchy = cv2.findContours(erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    # Draw the countours on the input images, -1 is draw all countours
    #cv2.drawContours(smallImg, contours, -1, (0,255,0), 3)

    #Do the raw moments to find the x,y coordinates
    centers = []
    radii = [] 
    print("Next image ...\n")
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area < 50:
            #print("Area is too small")
            continue
        #else:
           # print("Area is:")
           # print(area)
           
        br = cv2.boundingRect(contour)
        radii.append(br[2])
              
        #Calculate the moments 
        m = cv2.moments(contour)
        center = center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
        centers.append(center)
    
#    if (len(centers) ==0):
#        continue
#        print("hmm")
    
    print("There are {} circles".format(len(centers)))
    
    if (len(centers) > 0):
        radius = int(np.average(radii)) + 5
    
    for center in centers:
        cv2.circle(smallImg, center, 3, (255, 0, 0), -1)
        cv2.circle(smallImg, center, radius, (0, 255, 0), 1)    

    # Execute if user hit Esc key
    cv2.imshow('Input video',smallImg)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break 

cap.release()
cv2.destroyAllWindows()