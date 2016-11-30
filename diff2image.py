import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import os 

os.chdir('C:\\Users\\lorky\\Desktop\\imageprocessing\\clus4')

cam = cv2.VideoCapture(1)
time.sleep(1)
grabbed, f1 = cam.read()
f1 = imutils.resize(f1, width=300)

dirlist = os.listdir('C:\\Users\\lorky\\Desktop\\imageprocessing\\cascades')

while(True):
    grabbed, f2 = cam.read()
    f2 = imutils.resize(f2, width=300)
    g1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
    g1 = cv2.GaussianBlur(g1, (11, 11), 0)
    g2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
    g2 = cv2.GaussianBlur(g2, (11, 11), 0)
    frameDelta = cv2.absdiff(g1, g2) 
    thresh = cv2.threshold(frameDelta, 100, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    thresh = cv2.erode(thresh, None,iterations=1)
    thresh = cv2.dilate(thresh, None, iterations=7)
    (_,cnts,_) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    f3 = f2.copy()
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.05 * peri, True)
        if len(approx)==4:
            continue
        if cv2.contourArea(c)<float(150):
            continue
        #(x, y, w, h) = cv2.boundingRect(c)
        #cv2.rectangle(f3, (x, y), (x + w, y + h), (0, 255, 0), 2)
        (x,y),radius = cv2.minEnclosingCircle(c)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(f3,center,radius,(0,255,0),2)
    cv2.putText(f3, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, f3.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)  
    cv2.imshow('f1', f1)
    cv2.imshow('f2', f2)
    cv2.imshow('f3',f3)
    cv2.imshow('thresh', thresh)
    cv2.imshow('delta', frameDelta)
    cv2.imwrite(datetime.datetime.now().strftime("%H%M%S")+"f1.jpg", f1)
    cv2.imwrite(datetime.datetime.now().strftime("%H%M%S")+"f2.jpg", f2)
    cv2.imwrite("f3.jpg", f3) 

    print round(float(np.sum(g1))/float(np.prod(g1.shape)),3)   
    f1 = f2.copy()
    time.sleep(0.25)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cam.destroyAllWindows()

    
