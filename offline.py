import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import os 
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pylab


dirlist = os.listdir('C:\\Users\\lorky\\Desktop\\imageprocessing\\clus4')

global xlist 
global ylist 
global rlist 
xlist=[]
ylist=[]
rlist=[]
global f3

f3 = cv2.imread('C:\\Users\\lorky\\Desktop\\imageprocessing\\clus4\\194555f2.jpg')


tic = time.clock()

for i in range(1,3):
    if i > 0:
        f2 = cv2.imread('C:\\Users\\lorky\\Desktop\\imageprocessing\\clus4\\'+dirlist[i])
        f1 = cv2.imread('C:\\Users\\lorky\\Desktop\\imageprocessing\\clus4\\'+dirlist[i-1])
        g1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
        g1 = cv2.GaussianBlur(g1, (11, 11), 0)
        g2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
        g2 = cv2.GaussianBlur(g2, (11, 11), 0)
        frameDelta = cv2.absdiff(g1, g2) 
        thresh = cv2.threshold(frameDelta, 100, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        thresh = cv2.erode(thresh, None,iterations=1)
        thresh = cv2.dilate(thresh, None, iterations=7)
        (_,cnts,_) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.03 * peri, True)
            if len(approx)==4:
                continue
            if cv2.contourArea(c)<float(150):
                continue
            (x,y),radius = cv2.minEnclosingCircle(c)
            center = (int(x),int(y))
            radius = int(radius)
            xlist.append(x)
            ylist.append(y)
            rlist.append(radius) 
            cv2.circle(f3,center,1,(0,0,255),2)
            
cv2.imshow("results",f3)  
cv2.imwrite('raw.jpg',f3)     
cv2.imshow("g2",g2)
cv2.imshow("g1",g1)
cv2.imshow('thresh',thresh)
          
        
print time.clock()-tic