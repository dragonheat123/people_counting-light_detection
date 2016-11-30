import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import os 
from time import time
import httplib
lastcapimage = 0
lastsenddata = 0

os.chdir('C:\\Users\\lorky\\Desktop\\imageprocessing\\testimages')

camera = cv2.VideoCapture(1)

def sendData(motion,illu):
    headers = {"Host": "api.thingspeak.com","User-Agent": "Mozilla/5.0", "Connection": "close"}
    motion = int(1);
    conn = httplib.HTTPConnection('www.thingspeak.com',80)
    conn.request("GET", "/update?api_key=UJKZYC2PGQSEPXLC&field1="+str(motion)
        +"&field2="+str(illu),'',headers)
    conn.close()

def capimage():
    global f1
    (grabbed, f1) = camera.read()       
    cv2.imwrite(datetime.datetime.now().strftime("%H%M%S")+'.jpg',f1)
    global lastcapimage 
    lastcapimage = time()  
    return

while True:
    if (time()-lastcapimage)>30:
        capimage()
        
        
        
        
        
        
        
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break    
         