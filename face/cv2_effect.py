import cv2

class cv2_effect:
    def mosaic(src, ratio=0.1):
        small = cv2.resize(src, None, fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)
        return cv2.resize(small, src.shape[:2][::-1], interpolation=cv2.INTER_NEAREST)


    def mosaic_area(src, x, y, width, height, ratio=0.1):
        dst = src.copy()
        dst[y:y + height, x:x + width] = mosaic(dst[y:y + height, x:x + width], ratio)
        return dst
    


#モザイクを利用するときのプログラム
# for (x,y,w,h) in lists:
#         # cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), thickness=2)
#         dst_face = mosaic_area(frame,x,y,w,h)
    