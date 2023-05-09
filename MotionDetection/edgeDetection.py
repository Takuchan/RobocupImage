import cv2
import numpy as np

capture = cv2.VideoCapture(1)

while True:
    ref, frame = capture.read()
    rawFrame = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #thresh = 輪郭　
    ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
    print(hierarchy)
    output = cv2.drawContours(frame, contours, -1, (0,255,0), 3)
    
    cv2.imshow('now screen',gray)
    cv2.imshow('now scree3n',output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
capture.release()
cv2.destoryAllWindows()