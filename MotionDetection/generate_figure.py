import cv2
import numpy as np

img = np.full((1080,1920,3),128,dtype=np.uint8)

pic = cv2.rectangle(img,(100,300),(300,60),(255,0,0),-1) #左上頂点の座標、右下頂点の座標、色、太さ
cv2.imshow("完成",pic)
cv2.waitKey()
cv2.imwrite('./ractangle.png',img)