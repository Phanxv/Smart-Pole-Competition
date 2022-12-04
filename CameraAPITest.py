import cv2
import numpy as np 
import os

CAM = ["rtsp://streaming.planetcloud.cloud:5541/1f9fc0c7-8e74-43fc-8758-dfeb8c09d8f0/0",
       "rtsp://streaming.planetcloud.cloud:5541/7707ed09-0c72-4429-b2ea-a0cc521773ea/0",
       "rtsp://streaming.planetcloud.cloud:5541/7f6a5e94-60b4-4a0e-b564-cdabff325120/0",
       "rtsp://streaming.planetcloud.cloud:5541/2ae468e3-b55f-47ff-9f77-33644c741ebf/0"]

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
cap = cv2.VideoCapture(CAM[0], cv2.CAP_FFMPEG)
while(1):
    ret, frame = cap.read()
    if ret == False & 0xFF == ord('q'):
        print("Frame is empty")
        break
    else:
        cv2.imshow('VIDEO', frame)
        cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()
