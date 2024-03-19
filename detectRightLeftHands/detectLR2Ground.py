import cv2
import mediapipe as mp
import math
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("カメラから映像を取得できませんでした。")
            break

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # 直線aの計算 (ID 12と24の座標から) 右手の肩と右胴体
            a_x1 = landmarks[12].x
            a_y1 = landmarks[12].y
            a_x2 = landmarks[24].x
            a_y2 = landmarks[24].y
            
            # 直線bの計算 (ID 12と14の座標から)　右手の肩と右肘
            b_x1 = landmarks[12].x
            b_y1 = landmarks[12].y
            b_x2 = landmarks[14].x
            b_y2 = landmarks[14].y

            # 直線cの計算 (ID 11と23の座標から)　左手の肩と左胴体
            c_x1 = landmarks[11].x
            c_y1 = landmarks[11].y
            c_x2 = landmarks[23].x
            c_y2 = landmarks[23].y

            # 直線dの計算 (ID 11と13の座標から)　左手の肩と左肘
            d_x1 = landmarks[11].x
            d_y1 = landmarks[11].y
            d_x2 = landmarks[13].x
            d_y2 = landmarks[13].y



            
            # 2つの直線のなす角度を計算
            angle1 = math.acos((a_x2 - a_x1) * (b_x2 - b_x1) + (a_y2 - a_y1) * (b_y2 - b_y1) / (math.sqrt((a_x2 - a_x1)**2 + (a_y2 - a_y1)**2) * math.sqrt((b_x2 - b_x1)**2 + (b_y2 - b_y1)**2)))
            angle1 = math.degrees(angle1)

            # # 2つの直線のなす角度を計算
            angle2 = math.acos((c_x2 - c_x1) * (d_x2 - d_x1) + (c_y2 - c_y1) * (d_y2 - d_y1) / (math.sqrt((c_x2 - c_x1)**2 + (c_y2 - c_y1)**2) * math.sqrt((d_x2 - d_x1)**2 + (d_y2 - d_y1)**2)))
            angle2 = math.degrees(angle2)

            # 角度が30度を超えた場合にプリント
            if angle1 > 30:
                print(f"角度: {angle1:.2f}度 (30度を超えました) 右手")

            if angle2 > 30:
                print(f"角度: {angle2:.2f}度 (30度を超えました) 左手")

        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()