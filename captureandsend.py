import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import os 
import httplib

lastcapimage = 0
lastsenddata = 0

os.chdir('C:\\Users\\lorky\\Desktop\\imageprocessing\\testillu')

camera = cv2.VideoCapture(1)

def sendData(motion,illu):
    headers = {"Host": "api.thingspeak.com","User-Agent": "Mozilla/5.0", "Connection": "close"}
    conn = httplib.HTTPConnection('www.thingspeak.com',80)
    conn.request("GET", "/update?api_key=UJKZYC2PGQSEPXLC&field1="+str(motion)
        +"&field2="+str(illu),'',headers)
    conn.close()
    return

def capimage():
    global f3, lastcapimage, motion, illu, thresh
    (grabbed, f1) = camera.read() 
    f1 = imutils.resize(f1, width=300)      
    #cv2.imwrite(datetime.datetime.now().strftime("%H%M%S")+'f1.jpg',f1)
    time.sleep(1)
    (grabbed, f2) = camera.read() 
    f2 = imutils.resize(f2, width=300)      
    #cv2.imwrite(datetime.datetime.now().strftime("%H%M%S")+'f2.jpg',f2)
    g1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
    g1 = cv2.GaussianBlur(g1, (5, 5), 0)
    g2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
    g2 = cv2.GaussianBlur(g2, (5, 5), 0)
    frameDelta = cv2.absdiff(g1, g2) 
    thresh = cv2.threshold(frameDelta, 100, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    thresh = cv2.erode(thresh, None,iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)
    (_,cnts,_) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    f3 = f2.copy()
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.05 * peri, True)
        if len(approx)==4:
            continue
        #if cv2.contourArea(c)<float(150):
            #continue
        (x,y),radius = cv2.minEnclosingCircle(c)
        center = (int(x),int(y))
        radius = int(radius)
        cv2.circle(f3,center,radius,(0,255,0),2)
    cv2.putText(f3, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),(10, f3.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1) 
    illu = round(float(np.sum(g2))/2/float(np.prod(g2.shape))+float(np.sum(g2))/2/float(np.prod(g2.shape)),3)
    lastcapimage = time.time()  
    motion = int(3)
    return

while True:
    if (time.time()-lastcapimage)>5:
        capimage()
        #sendData(motion,illu)
        cv2.imshow("results",f3)
        cv2.imshow("thresh",thresh)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break    
         