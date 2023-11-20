import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import cv2

capture = cv2.VideoCapture(0)

# MediaPipe Processing
# base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
# options = vision.GestureRecognizerOptions(base_options=base_options)
# recognizer = vision.GestureRecognizer.create_from_options(options)




while True:
    ret, frame = capture.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()