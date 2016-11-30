import httplib
import cv2
import time
import random

headers = {"Host": "api.thingspeak.com","User-Agent": "Mozilla/5.0", "Connection": "close"}

while True:
    conn = httplib.HTTPConnection('www.thingspeak.com',80)
    conn.request("GET", "/update?api_key=UJKZYC2PGQSEPXLC&field1="+str(random.randint(1, 10))
        +"&field2="+str(random.randint(1, 10)),'',headers)
    r1 = conn.getresponse()
    print(r1.status, r1.reason)
    conn.close()
    time.sleep(30)
