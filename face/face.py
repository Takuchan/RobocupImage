import cv2
import pandas as pd
import dlib
from imutils import face_utils
import csv
#おれおりじなるデータいんぽーと
import faceModel



#すべてのデータを初期化していきやしょう
cap = cv2.VideoCapture("hatsuon.mp4")
xml_path = "haarcascade_frontalcatface.xml"
cascade = cv2.CascadeClassifier(xml_path)

face_detector = dlib.get_frontal_face_detector()
predictor_path = 'shape_predictor_68_face_landmarks.dat'
face_predictor = dlib.shape_predictor(predictor_path)

frame_count = 0
faceallData = []


while(True):
    print("今のフレーム数は{}".format(frame_count))
    frame_count += 1
    ret, frame = cap.read()
    if not ret:
        break
    frame_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    resize_frame = cv2.resize(frame_gray,dsize=None,fx=0.5, fy=0.5)
    #顔検出
    lists = cascade.detectMultiScale(resize_frame, minSize=(50, 50))
    for (x,y,w,h) in lists:
        img1 = resize_frame[y:y+h,x:x+w]
        img1 = cv2.resize(img1,dsize=(200,200))
    img2 = img1
    #顔検出して、特徴点をマークする初歩段階   
    faces = face_detector(img2,1)
    
    for face in faces:
        landmark = face_predictor(img2, face)
        landmark = face_utils.shape_to_np(landmark)

        # ランドマーク描画とデータを保存する
        coordinate = []
        for (i, (x, y)) in enumerate(landmark):
            # print(i,(x,y))
            cv2.circle(img2, (x, y), 1, (255, 0, 0), -1)
            tempCordinate = faceModel.singlePointFaceModel()
            tempCordinate.set_single_point(facePointNumber=i,x_p=x,y_p=y)
            coordinate.append(tempCordinate)
    alldata = faceModel.faceAllDataModel()
    alldata.set_value(list_data=coordinate)
    faceallData.append(alldata)
    #画面表示
    cv2.imshow("Realtime Screen",img2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


with open("finish_data.csv","w") as f:
    writer = csv.writer(f)
    for a in faceallData:
        hairetsu = []
        for b in a.get_value():
            list_data1 = b.get_single_point()[1]
            list_data2 = b.get_single_point()[2]
            hairetsu.append(str(list_data1) + ":" + str(list_data2))
        writer.writerow(hairetsu)
        hairetsu = []
cap.release()
cv2.destroyAllWindows()
