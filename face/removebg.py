import cv2
import numpy as np
import time
from ultralytics import YOLO

cap = cv2.VideoCapture(0)
count = 0

model = YOLO("yolov8n-seg.pt")

while (True):
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = model(frame,save=False,task='segment')
    
    for result in results:
        cv2.imshow("result",result)

    count +=1 
    print(count)
cap.release()
cv2.destroyAllWindows()