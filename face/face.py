import cv2
import dlib
from imutils import face_utils


def mosaic(src, ratio=0.1):
    small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
    return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)


def mosaic_area(src, x, y, width, height, ratio=0.1):
    dst = src.copy()
    dst[y:y + height, x:x + width] = mosaic(dst[y:y + height, x:x + width], ratio)
    return dst

cap = cv2.VideoCapture(0)
xml_path = "haarcascade_frontalcatface.xml"
cascade = cv2.CascadeClassifier(xml_path)

face_detector = dlib.get_frontal_face_detector()
predictor_path = 'shape_predictor_68_face_landmarks.dat'
face_predictor = dlib.shape_predictor(predictor_path)

while(True):
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    lists = cascade.detectMultiScale(frame_gray, minSize=(50, 50))
    faces = face_detector(frame_gray,1)
    for (x,y,w,h) in lists:
        # cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), thickness=2)
        dst_face = mosaic_area(frame,x,y,w,h)
    
    for face in faces:
        # 顔のランドマーク検出
        landmark = face_predictor(frame_gray, face)
        # 処理高速化のためランドマーク群をNumPy配列に変換(必須)
        landmark = face_utils.shape_to_np(landmark)

        # ランドマーク描画
        for (i, (x, y)) in enumerate(landmark):
            print(i,(x,y))
            cv2.circle(frame, (x, y), 1, (255, 0, 0), -1)
    
    # cv2.imshow("camera",dst_face)
    cv2.imshow("camera",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()