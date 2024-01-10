import os
import cv2
import numpy as np
import insightface

# 画像パスの取得
img_path = os.path.abspath("meeting_image.jpg")
# 画像の読み込み
img =cv2.imread(img_path)

#  読み込んだ画像の確認
print(type(img))
print(img.shape)
print(img.dtype)

# オブジェクトの生成
app = insightface.app.FaceAnalysis()

# app.prepare(ctx_id=0) は、GPU を使用するか CPU を使用するかの指定です。 
# GPU を使用する場合は ctx_id=0、CPU を使用する場合は ctx_id=-1 を指定します。
app.prepare(ctx_id=0)

# 顔の検出
faces = app.get(img)

# 顔を四角形で囲む
for face in faces:
    x1, y1, x2, y2 = face.bbox.astype(np.int32)
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(img.shape[1] - 1, x2)
    y2 = min(img.shape[0] - 1, y2)
    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 7)

# 検出結果を保存
cv2.imwrite("output.jpg", img)
