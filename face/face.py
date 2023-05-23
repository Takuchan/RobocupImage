import cv2
import pandas as pd
import dlib
from imutils import face_utils
import csv
import math
import numpy as np
#おれおりじなるデータいんぽーと
import faceModel


def fitting_rotated_image(img, angle):
    height,width = img.shape[:2]
    center = (int(width/2), int(height/2))
    radians = np.deg2rad(angle)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)

    new_width = int(abs(np.sin(radians)*height) + abs(np.cos(radians)*width))
    new_height = int(abs(np.sin(radians)*width) + abs(np.cos(radians)*height))

    M[0,2] += int((new_width-width)/2)
    M[1,2] += int((new_height-height)/2)

    return cv2.warpAffine(img, M, (new_width, new_height))



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
        rectWidth = face.width()
        rectHeight = face.height()
        rectCenter = face.center()
        x_start = rectCenter.x - rectWidth
        x_end = x_start + rectWidth*2
        y_start = rectCenter.y - rectHeight
        y_end = y_start + rectHeight*2
        face_im = img1[y_start:y_end, x_start:x_end]

        # 顔の角度を修正
        points = []
        for point in face_predictor(img1, face).parts():
            points.append([int(point.x), int(point.y)])
        x_diff = points[0][0] - points[36][0]
        y_diff = points[0][1] - points[36][1]
        angle = math.degrees(math.atan2(y_diff, x_diff))
        rotated_im = fitting_rotated_image(face_im, angle)

        cv2.imshow("cereter",rotated_im)

        # 回転後の画像で顔検出して画像保存
        rotated_rects = face_detector(rotated_im, 1)
        print(rotated_rects)
        if len(rotated_rects) == 0:
            print('顔が抽出されませんでした')
            continue

        rotated_rect = rotated_rects[0]
        x_start = rotated_rect.left()
        x_end = rotated_rect.right()
        y_start = rotated_rect.top()
        y_end = rotated_rect.bottom()
        cropped_im = rotated_im[y_start:y_end, x_start:x_end]



        landmark = face_predictor(cropped_im, face)
        landmark = face_utils.shape_to_np(landmark)

        # ランドマーク描画とデータを保存する
        # coordinate = []
        for (i, (x, y)) in enumerate(landmark):
            # print(i,(x,y))
            cv2.circle(cropped_im, (x, y), 1, (255, 0, 0), -1)
            tempCordinate = faceModel.singlePointFaceModel()
            tempCordinate.set_single_point(facePointNumber=i,x_p=x,y_p=y)
            # coordinate.append(tempCordinate)
    alldata = faceModel.faceAllDataModel()
    # alldata.set_value(list_data=coordinate)
    faceallData.append(alldata)


    # #画面表示
    # cv2.imshow("Realtime Screen",cropped_im)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break


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
