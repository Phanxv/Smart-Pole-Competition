import cv2
import queue
import time
import threading
q=queue.Queue()

def Receive():
    print("start Reveive")
    cap = cv2.VideoCapture("rtsp://streaming.planetcloud.cloud:5541/1f9fc0c7-8e74-43fc-8758-dfeb8c09d8f0/0")
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