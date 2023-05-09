import cv2
import numpy as np

def image_info(img,winname,action):
    print('---{}:{}---'.format(winname,action))
    print(' shape:{}'.format(img.shape[1],img.shape[0]))
    if img.ndim > 2:
        print('channels:{}'.format(img.shape[2]))
    print('ndim:{},type:{}'.format(img.ndim,img.dtype))

    cv2.imshow(winname,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


shape = (300,400,3)
img_1 = np.empty(shape,np.uint8)
