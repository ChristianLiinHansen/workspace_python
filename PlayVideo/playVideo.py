# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 16:20:45 2014

@author: christian
"""

import numpy as np
import cv2

cap = cv2.VideoCapture('indoor4.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)
    
    # Add some extra delay..
    cv2.waitKey(10)
    
    # if we push "q" the program ececutes
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cap.release()
