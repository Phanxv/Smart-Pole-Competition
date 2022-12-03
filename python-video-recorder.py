import cv2

cap= cv2.VideoCapture('rtsp://streaming.planetcloud.cloud:5541/2ae468e3-b55f-47ff-9f77-33644c741ebf/0')

width= int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

writer= cv2.VideoWriter('footage2.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))


while True:
    ret,frame= cap.read()

    writer.write(frame)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break


cap.release()
writer.release()
cv2.destroyAllWindows()