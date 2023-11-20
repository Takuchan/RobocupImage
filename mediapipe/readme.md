# What is this project?
このプロジェクトは指差す方向の物体を検知して、そのオブジェクトをマークし続けるプログラムを作ります。
GoogleのMediaPipeのAPIを使ってプログラムを書いていきます。
[公式ドキュメント](https://developers.google.com/mediapipe/solutions/vision/gesture_recognizer/python)

# canned_gestures_classifier_options
引用
Options for configuring the canned gestures classifier behavior. The canned gestures are ["None", "Closed_Fist", "Open_Palm", "Pointing_Up", "Thumb_Down", "Thumb_Up", "Victory", "ILoveYou"]
Display names locale: the locale to use for display names specified through the TFLite Model Metadata, if any.
Max results: the maximum number of top-scored classification results to return. If < 0, all available results will be returned.
Score threshold: the score below which results are rejected. If set to 0, all available results will be returned.
Category allowlist: the allowlist of category names. If non-empty, classification results whose category is not in this set will be filtered out. Mutually exclusive with denylist.
Category denylist: the denylist of category names. If non-empty, classification results whose category is in this set will be filtered out. Mutually exclusive with allowlist.

## Point!
- Display names locale: any string
- Max results: any integers
- Score threshold: 0.0 ~ 1.0
- Category allowlist: vector of strings
- Category denylist: vector of strings

## Display values
- Display names locale "en"
- max Result: -1
- Score threshold : 0
- category allowlist empty
- category denylist: empty
