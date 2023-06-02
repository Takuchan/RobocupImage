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


        # 各顔について処理を行う
        for face in faces:
            # 顔のランドマーク（特徴点）を検出
            landmarks =face_predictor(img_gry, face)

            # 目の座標を取得
            left_eye = (landmarks.part(36).x, landmarks.part(36).y)
            right_eye = (landmarks.part(45).x, landmarks.part(45).y)

            # 目の中心座標を計算
            center_x = int((left_eye[0] + right_eye[0]) / 2)
            center_y = int((left_eye[1] + right_eye[1]) / 2)

            # 顔の向きを計算
            angle = -cv2.fastAtan2(right_eye[1] - left_eye[1], right_eye[0] - left_eye[0])

            # 画像の中心座標を計算
            image_height, image_width = img_gry.shape[:2]
            image_center = (image_width // 2, image_height // 2)

            # アフィン変換行列を作成して顔を正面に向ける
            rotation_matrix = cv2.getRotationMatrix2D(image_center, angle, 1.0)
            rotated_image = cv2.warpAffine(img_gry, rotation_matrix, (image_width, image_height), flags=cv2.INTER_LINEAR)

            # 顔を正面に向けた画像を表示
            cv2.imshow('Rotated Image', rotated_image)
            cv2.waitKey(0)

        # ウィンドウを閉じる
        cv2.destroyAllWindows()


        # 検出した全顔に対して処理
        for face in faces:
            # 顔のランドマーク検出
            landmark = face_predictor(img_gry, face)
            # 処理高速化のためランドマーク群をNumPy配列に変換(必須)
            landmark = face_utils.shape_to_np(landmark)

            # ランドマーク描画
            for (i, (x, y)) in enumerate(landmark):
                cv2.circle(img, (x, y), 1, (255, 0, 0), -1)
            
        img1 = cv2.imread('sozai/arimura_yoko1.jpg')
        img1_gry = cv2.cvtColor()

        cv2.imshow('sample', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if __name__ ==  '__main__':
        main()

