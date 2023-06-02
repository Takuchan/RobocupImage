# coding:utf-8

import dlib
from imutils import face_utils
import cv2



class front_force_face:
    def __init__(self):
        print("")
    def main():
        face_detector = dlib.get_frontal_face_detector()

        # 顔のランドマーク検出ツールの呼び出し
        predictor_path = 'shape_predictor_68_face_landmarks.dat'
        face_predictor = dlib.shape_predictor(predictor_path)

        # 検出対象の画像の呼び込み
        img = cv2.imread('sozai/arimura.jpg')
        img_gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_detector(img_gry, 1)

        # 検出した全顔に対して処理
        for face in faces:
            # 顔のランドマーク検出
            landmark = face_predictor(img_gry, face)
            # 処理高速化のためランドマーク群をNumPy配列に変換(必須)
            landmark = face_utils.shape_to_np(landmark)

            # ランドマーク描画
            for (i, (x, y)) in enumerate(landmark):
                cv2.circle(img, (x, y), 1, (255, 0, 0), -1)

        cv2.imshow('sample', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if __name__ ==  '__main__':
        main()

