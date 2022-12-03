from imutils.video import VideoStream
from imutils.video import FPS
from imutils.video import FileVideoStream
import numpy as np
import time
import cv2
from easyocr import Reader
import requests
import json

rtsp_url1 = "rtsp://admin:TniENG406@192.168.1.64:554/Streaming/channels/1/"
rtsp_url2 = "rtsp://streaming.planetcloud.cloud:5541/2ae468e3-b55f-47ff-9f77-33644c741ebf/0"
allowchar = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ1234567890"
print("Start Loading Video Stream...")
#vs = VideoStream(src=1).start()
vs = FileVideoStream("Footage2.mp4").start()
time.sleep(2.0)
fps = FPS().start()
print("Load Video Stream Successfully")
nplateCascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
minArea = 100
th = 125
kernel = np.ones((2, 2), np.uint8)
print("Start Loading OCR...")
reader = Reader(["th"],gpu=False)
print("Load OCR Successfully")
while True :
    frame = vs.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plate = nplateCascade.detectMultiScale(frame_gray, 1.2, 2)
    #cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    for (x,y,w,h) in plate :
        area = w*h
        if area > minArea :
            #cv2.rectangle(frame,(x,y-30),(x+w+30,y+h),(0,255,0),2)
            #cv2.imshow("Frame", frame)
            ROI_process = frame_gray[y-30:y+h, x:x+w+30]
            #ROI_process = cv2.equalizeHist(ROI)
            #ROI_process[ROI_process>=th] = 255
            #ROI_process[ROI_process<th] = 0
            eroded = cv2.erode(ROI_process,kernel,iterations=1)
            equ = cv2.equalizeHist(ROI_process)
            blur = cv2.GaussianBlur(equ, (5, 5), 1)
            #thresh = cv2.adaptiveThreshold(ROI_process, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 4)
            cv2.imshow("ROI", blur)
            detected = reader.readtext(blur,allowlist=allowchar,detail=0)
            print(detected)
            try :
                if(len(detected[0]) > 4) :
                    print(detected[0])
                    requests.post('https://whole-adults-kneel-110-164-157-62.loca.lt/lpr', data = detected[0].encode('utf-8'), headers={'Content-Type' : 'text/plain; charset=utf-8'})
                else :
                    print(detected[0] + detected[1])
            except IndexError:
                pass
            #print(detected[0][1])
    # if the `q` key was pressed, break from the loop
            fps.update()
    if key == ord("q"):
           break

    # update the FPS counter


# stop the timer and display FPS information
fps.stop()