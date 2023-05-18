import cv2
import dlib
from imutils import face_utils


cap = cv2.VideoCapture('hatsuon.mp4')
xml_path = "haarcascade_frontalcatface.xml"
cascade = cv2.CascadeClassifier(xml_path)

face_detector = dlib.get_frontal_face_detector()
predictor_path = 'shape_predictor_68_face_landmarks.dat'
face_predictor = dlib.shape_predictor(predictor_path)

frame_count = 0
while(True):
    print("今のフレーム数は{}".format(frame_count))
    frame_count += 1
    ret, frame = cap.read()
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    resize_frame = cv2.resize(frame_gray,dsize=None,fx=0.5, fy=0.5)
    #顔検出
    lists = cascade.detectMultiScale(resize_frame, minSize=(50, 50))
    for (x,y,w,h) in lists:
        img1 = resize_frame[y:y+h,x:x+w]
        img1 = cv2.resize(img1,dsize=(200,200))
        
    #顔検出して、特徴点をマークする初歩段階   
    faces = face_detector(img1,1)
    
    for face in faces:
        landmark = face_predictor(img1, face)
        landmark = face_utils.shape_to_np(landmark)

        # ランドマーク描画
        for (i, (x, y)) in enumerate(landmark):
            print(i,(x,y))
            cv2.circle(img1, (x, y), 1, (255, 0, 0), -1)
    
    # cv2.imshow("camera",dst_face)
    # cv2.imshow("camera",resize_frame)

    #Test
    cv2.imshow("test",img1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
