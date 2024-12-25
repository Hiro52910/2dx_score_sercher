import cv2
import numpy as np


def get_note_from_pic(image_path):
    # 画像を読み込む
    image = cv2.imread(image_path)

    # 画像サイズを取得
    height, width, _ = image.shape

    # レーンの数を設定
    num_lanes = 7  
    lane_width = width // num_lanes

    # 結果を保持するリスト（下から上へ保存）
    results = []

    # 下から上へスキャン
    y = height - 1
    while y >= 0:
        row_result = []
        for lane in range(num_lanes):
            # 各レーンの範囲を切り出し
            x_start = lane * lane_width
            x_end = x_start + lane_width
            crop = image[max(0, y-3):y+1, x_start:x_end]  # 厚さ4ピクセルの領域

            # HSV変換
            hsv_crop = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

            # 青色の範囲を定義
            blue_lower = np.array([100, 150, 50])
            blue_upper = np.array([140, 255, 255])
            blue_mask = cv2.inRange(hsv_crop, blue_lower, blue_upper)

            # 白色の範囲を定義
            white_lower = np.array([0, 0, 200])
            white_upper = np.array([180, 55, 255])
            white_mask = cv2.inRange(hsv_crop, white_lower, white_upper)

            # 青または白が検出された場合、レーン番号を記録
            if np.any(blue_mask) or np.any(white_mask):
                row_result.append(lane + 1)  # レーン番号を1から始める

        # この行の結果を保存（空でなければ）
        if row_result:
            results.append((y, row_result))
            y -= 4  # オブジェクトを検出した場合、4ピクセルジャンプ
        else:
            y -= 1  # 検出されなければ1ピクセル進む

    # 結果を表示
    for row in results:
        print(f"Row {row[0]}: Lanes {row[1]}")

    # 結果を画像に描画して保存
    for row in results:
        y = row[0]
        for lane in row[1]:
            x_start = (lane - 1) * lane_width
            x_end = x_start + lane_width
            cv2.rectangle(image, (x_start, max(0, y-3)), (x_end, y), (0, 255, 0), 1)

    output_path = "result/detected_lanes.png"
    cv2.imwrite(output_path, image)
    print(f"Annotated image saved to {output_path}")

if __name__ == "__main__":
    get_note_from_pic("scaned_pic/crop_0.png")