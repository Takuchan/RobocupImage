from insightface.app import FaceAnalysis
import numpy as np
import cv2
InsightFaceLandmarksDetector = FaceAnalysis(name='landmarks')
InsightFaceLandmarksDetector.prepare(ctx_id=0, det_size=(640, 640))

def rotate(coordinates, theta_rad,h,w):
    x = coordinates[1]
    y = coordinates[0]
    x = x - w/2
    y = y - h/2
    x_new = x * np.cos(theta_rad) - y * np.sin(theta_rad)
    y_new = x * np.sin(theta_rad) + y * np.cos(theta_rad)
    x_new = x_new + w/2
    y_new = y_new + h/2
    return np.array([y_new,x_new])


# Open the default camera (index 0)
cap = cv2.VideoCapture(0)

while True:
        # Read frame from the camera
    ret, frame = cap.read()
    face_landmarks = InsightFaceLandmarksDetector.get(frame)
    lm = np.fliplr(np.array(face_landmarks)) # w, h の順を入れ替える
    lm_eye_left      = lm[0]
    lm_eye_right     = lm[1]
    lm_nose          = lm[2]
    lm_mouse         = lm[3:]

    # 各パーツの位置の平均を算出
    eye_left     = lm_eye_left
    eye_right    = lm_eye_right
    eye_avg      = (eye_left + eye_right) * 0.5
    eye_to_eye   = eye_right - eye_left
    nose         = lm_nose
    mouse        = np.mean(lm_mouse, axis=0)

    w = img.shape[1]
    h = img.shape[0]

    # 目の傾き補正
    w_ = eye_to_eye[1]
    h_ = eye_to_eye[0]
    tan_rad = np.arctan(h_ / w_)
    tan_deg = np.rad2deg(tan_rad)

    center = (int(img.shape[1]/2), int(img.shape[0]/2))
    trans = cv2.getRotationMatrix2D(center, tan_deg, 1)
    img = cv2.warpAffine(img, trans, (img.shape[1],img.shape[0]))

    eye_left = rotate(eye_left, tan_rad, h, w)
    eye_right = rotate(eye_right, tan_rad, h, w)
    mouth_avg = rotate(mouth_avg, tan_rad, h, w)

    y_center_face, x_center_face = np.mean([eye_left, eye_right, mouth_avg], axis=0)
    crop_width = (eye_right - eye_left)[1] * 4.1
    h_adjast = - 0.05 * crop_width

    img_crop = img[
        int(y_center_face-crop_width/2+h_adjast) : int(y_center_face+crop_width/2+h_adjast),
        int(x_center_face-crop_width/2) : int(x_center_face+crop_width/2)
    ]

    img_crop = cv2.resize(img_crop, dsize=(500,500))

    # Display the frame
    cv2.imshow('Camera', img_crop)

        # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
