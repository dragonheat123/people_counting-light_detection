import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import os 

os.chdir('C:\\Users\\lorky\\Desktop\\imageprocessing\\test')

dirlist = os.listdir('C:\\Users\\lorky\\Desktop\\imageprocessing\\cascades')
filelist = os.listdir('C:\\Users\\lorky\\Desktop\\imageprocessing\\test')

for j in filelist:
    f1 = cv2.imread('C:\\Users\\lorky\\Desktop\\imageprocessing\\test\\'+j)
    tic= time.clock()
    f1 = imutils.resize(f1, width=300) 
    gray = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
    
    for flit in dirlist:
        path = ('C:\\Users\\lorky\\Desktop\\imageprocessing\\cascades\\'+flit).replace('/','//')
        print path
        classifier = cv2.CascadeClassifier(path)
        faces = classifier.detectMultiScale(gray,scaleFactor=1.03,minNeighbors=5,minSize=(10, 10))
        for (x,y,w,h) in faces:
            #cv2.rectangle(f1,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.circle(f1,(x+w/2,y+h/2),w/2,(255,0,0),2)        
    toc = time.clock()
    speed = toc-tic
    print speed
    #cv2.imshow(str(speed)+'_'+j, f1)     
    cv2.imwrite(j.replace('.jpg','_')+str(speed)+'.jpg',f1)
