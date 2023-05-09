from curses import KEY_OPTIONS
import cv2
import numpy as np



WIDTH = 480
HEIGHT = 600
FPS = 30

VIDEO_TARGET = 2 #カメラID
VIDEO_TARGET2 = 1
cap_file = cv2.VideoCapture(VIDEO_TARGET)
cap_file2 = cv2.VideoCapture(VIDEO_TARGET2)
count = 1
cap_file.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
cap_file.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap_file.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap_file.set(cv2.CAP_PROP_FPS, FPS)
cap_file.set(cv2.CAP_PROP_BRIGHTNESS,300)
print(cap_file.get(cv2.CAP_PROP_FRAME_HEIGHT))


cap_file2.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
cap_file2.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap_file2.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap_file2.set(cv2.CAP_PROP_FPS, FPS)



#前のフレーム
previous_frame = []



#繰り返しのためのwhile文
# while True:
print('あの一瞬（とき）は戻ってこない...',count)
#カメラからの画像取得
ret, frame = cap_file.read()
#スマホカメラからの画像取得
ret2,frame2 = cap_file2.read()

orb = cv2.ORB_create()
gray = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
canny = cv2.Canny(gray,5,50)

height = canny.shape[0]
width = canny.shape[1]
center = (int(width/2),int(height/2))
print(canny.shape)
angle = 0
scale = 1.0
trans = cv2.getRotationMatrix2D(center,angle,scale)
smartphonecamera = cv2.warpAffine(frame,trans,(width,height))
smartphonecamera2 = cv2.warpAffine(frame2,trans,(width,height))

# previous_frame.append(smartphonecamera2)

img_src1 = smartphonecamera
img_src2 = smartphonecamera2
img_dst = img_src1


keypoint1,descript1 = orb.detectAndCompute(img_src1,None) #現在のフレームの写真
keypoint2,descript2 = orb.detectAndCompute(img_src2,None) #前のフレームの写真をゲット

coordinate =[] #x,y座標のリストタプル
for a in keypoint1:
    coordinate.append(a.pt)
bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)
matches = bf.match(descript1,descript2)
matches = sorted(matches,key=lambda x:x.distance)
img3 = cv2.drawMatches(img_src1, keypoint1, img_src2, keypoint2, matches, img_dst, flags=2)


for parent in coordinate:
    print('parent:{}'.format(parent))
    for children in parent:
        print('children:{}'.format(children))
        
    # cv2.putText(img3, "sample", (coordinate[i][0],coordinate[i][1]), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 5, cv2.LINE_AA)

#カメラの画像の出力
cv2.imshow('camera' , img3)

#繰り返し分から抜けるためのif文
cv2.waitKey(0)

count +=1
#メモリを解放して終了するためのコマンド
