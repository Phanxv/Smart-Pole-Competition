import cv2
import queue
import time
import threading
q=queue.Queue()

def Receive():
    print("start Reveive")
    cap = cv2.VideoCapture("rtsp://streaming.planetcloud.cloud:5541/2ae468e3-b55f-47ff-9f77-33644c741ebf/0")
    ret, frame = cap.read()
    q.put(frame)
    while ret:
        ret, frame = cap.read()
        q.put(frame)


def Display():
     print("Start Displaying")
     while True:
         if q.empty() !=True:
            frame=q.get()
            cv2.imshow("frame1", frame)
         if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
if __name__=='__main__':
    p1=threading.Thread(target=Receive)
    p2 = threading.Thread(target=Display)
    p1.start()
    p2.start()