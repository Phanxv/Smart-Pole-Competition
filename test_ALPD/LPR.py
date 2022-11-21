from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import time
import cv2
from easyocr import Reader

rtsp_url = "rtsp://admin:TniENG406@192.168.1.64:554/Streaming/channels/1/"
vs = VideoStream(rtsp_url).start()
time.sleep(2.0)
fps = FPS().start()
nplateCascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")
minArea = 100
reader = Reader(["th"])
while True :
    frame = vs.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plate = nplateCascade.detectMultiScale(frame_gray, 1.1, 4)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    for (x,y,w,h) in plate :
        area = w*h
        if area > minArea :
            cv2.rectangle(frame,(x,y-30),(x+w+30,y+h),(0,255,0),2)
            cv2.imshow("Frame", frame)
            ROI = frame_gray[y-50:y+h, x:x+w+50]
            cv2.imshow("ROI", ROI)
            detected = reader.readtext(ROI)
            try :
                detected_len = len(detected[0][1])
                if detected_len > 6 and detected_len < 10 :
                    detected_num = detected[0][1]
                    print(detected_num.replace(" ", ""))
                elif detected_len < 4 :
                    detected_num = detected[0][1] + detected[1][1]
                    print(detected_num.replace(" ", ""))
                    break
                break
            except IndexError:
                pass
            #print(detected[0][1])
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
            break

    # update the FPS counter
    fps.update()

# stop the timer and display FPS information
fps.stop()