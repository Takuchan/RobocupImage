import cv2
import os
import numpy as np

# load = cv2.imread('sakurei1.jpeg',0) #第２引数 -1=無変換 0=グレー 1=カラー 2=任意の震度 3=任意のカラー
cap_file = cv2.VideoCapture('3.mp4')

frame_count = int(cap_file.get(cv2.CAP_PROP_FRAME_COUNT))
print('フレーム',frame_count)

previous_frame = []


for i in range(frame_count):
    ch,frame=cap_file.read()
    if ch:
        frame = cv2.resize(frame,(480,720))
        orb = cv2.ORB_create()


        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        canny = cv2.Canny(gray,5,50)
        
        height = canny.shape[0]
        width = canny.shape[1]
        center = (int(width/2),int(height/2))
 
        angle = 0
        scale = 1.0
        trans = cv2.getRotationMatrix2D(center,angle,scale)
        image2 = cv2.warpAffine(frame,trans,(width,height))
        

        previous_frame.append(image2)
        
        #わかりやすい変数に置き換え
        img_src1 = image2
        img_src2 = previous_frame[i - 1]
        img_dst = img_src1


        keypoint1,descript1 = orb.detectAndCompute(img_src1,None) #現在のフレームの写真
        keypoint2,descript2 = orb.detectAndCompute(img_src2,None) #前のフレームの写真をゲット
        bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
        matches = bf.match(descript1,descript2)
        matches = sorted(matches,key=lambda x:x.distance)
        img3 = cv2.drawMatches(img_src1, keypoint1, img_src2, keypoint2, matches, img_dst, flags=2)


        cv2.imshow('movie',img3)
    k= cv2.waitKey(1)
    if k == 27:
        break



cv2.waitKey(0)

f = open('edited_movie.txt','w')
if f != None:
    f.write(str(previous_frame))
else:
    f.close()