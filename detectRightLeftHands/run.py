import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

while True:
# フレームを取得
    ret, frame = cap.read()

    # RGBに変換
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ハンド検出を実行
    results = hands.process(rgb_frame)

    # 検出された手がある場合
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
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

    # 結果を表示
    cv2.imshow('Hand Tracking', frame)

    # 'q'が押されたら終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースを開放
cap.release()
cv2.destroyAllWindows()