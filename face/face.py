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


def doExecute(importFrame):
    face_detector = dlib.get_frontal_face_detector()

    # 顔のランドマーク検出ツールの呼び出し
    predictor_path = 'shape_predictor_68_face_landmarks.dat'
    face_predictor = dlib.shape_predictor(predictor_path)

    faces = face_detector(importFrame, 1)


    # 各顔について処理を行う
    for face in faces:
        # 顔のランドマーク（特徴点）を検出
        landmarks =face_predictor(importFrame, face)

        # 目の座標を取得
        left_eye = (landmarks.part(36).x, landmarks.part(36).y)
        right_eye = (landmarks.part(45).x, landmarks.part(45).y)

        # 目の中心座標を計算
        center_x = int((left_eye[0] + right_eye[0]) / 2)
        center_y = int((left_eye[1] + right_eye[1]) / 2)

        # 顔の向きを計算
        angle = -cv2.fastAtan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0])

        # 画像の中心座標を計算
        image_height, image_width = importFrame.shape[:2]
        image_center = (image_width // 2, image_height // 2)

        # アフィン変換行列を作成して顔を正面に向ける
        rotation_matrix = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        rotated_image = cv2.warpAffine(importFrame, rotation_matrix, (image_width, image_height), flags=cv2.INTER_LINEAR)

    
    return rotated_image

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
    img2 = doExecute(img1)
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
