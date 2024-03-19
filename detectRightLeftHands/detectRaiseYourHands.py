import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, smooth_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results_hands = hands.process(rgb_frame)
    results_pose = pose.process(rgb_frame)

    if results_hands.multi_hand_landmarks:
        for hand_landmarks in results_hands.multi_hand_landmarks:
            # 手の座標を取得
            x_max = 0
            y_max = 0
            x_min = float('inf')
            y_min = float('inf')

            for landmark in hand_landmarks.landmark:
                x = min(int(landmark.x * frame.shape[1]), frame.shape[1] - 1)
                y = min(int(landmark.y * frame.shape[0]), frame.shape[0] - 1)
                x_max = max(x_max, x)
                y_max = max(y_max, y)
                x_min = min(x_min, x)
                y_min = min(y_min, y)

            # 手の中心座標を計算
            center_x = int((x_max + x_min) / 2)
            center_y = int((y_max + y_min) / 2)

            # 手が画面の左側にあるか右側にあるかを判定
            hand_side = "Right" if center_x < frame.shape[1] // 2 else "Left"

            # 手の矩形と中心位置をフレーム上に描画
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
            cv2.putText(frame, hand_side, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    if results_pose.pose_landmarks:
        landmarks = results_pose.pose_landmarks.landmark
        right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
        right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

        left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

        # 肩と手首の座標を使用して角度を計算
        right_angle = np.arctan2(right_wrist[1] - right_shoulder[1], right_wrist[0] - right_shoulder[0]) * 180 / np.pi
        left_angle = np.arctan2(left_wrist[1] - left_shoulder[1], left_wrist[0] - left_shoulder[0]) * 180 / np.pi

        # 角度が30度以上であるかどうかを判定
        if right_angle < 30:
            cv2.putText(frame, "Right arm is raised", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if left_angle < 30:
            cv2.putText(frame, "Left arm is raised", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # 結果を表示
    cv2.imshow('Hand Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
