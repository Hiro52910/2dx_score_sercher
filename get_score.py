from selenium import webdriver
from selenium.webdriver.common.by import By
import cv2
import numpy as np
import time

def get_score (music_name):
    SCAN_HEIGHT = 128  # 上方向に進む距離（ピクセル）
    SCAN_STEP = 172  # 横方向に進む距離（ピクセル）
    PAGE_LOAD_WAIT = 2 

    # URLの設定
    url = "https://textage.cc/score/12/_" + music_name + ".html?1AC00" 


    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(PAGE_LOAD_WAIT)

    # ウェブページのスクショを取得
    screenshot_path = "webpage_screenshot.png"
    driver.save_screenshot(screenshot_path)
    driver.quit()

    # 画像を読み込む
    image = cv2.imread(screenshot_path)

    # 画像のサイズを取得
    height, width, _ = image.shape

    # 左下から右に進むスキャンの開始位置
    y_start_pos = 548
    x_start_pos = 8
    x = x_start_pos
    y = y_start_pos

    pic_num = 0


    # スキャン結果を保存
    detected_positions = []

    while x < width:
        while y >= 50:  # 上にスキャン
            # スキャン範囲を切り出し
            crop = image[max(0, y - SCAN_HEIGHT):y, x+40:x + 137]

            # 画像を保存
            crop_path = f"scaned_pic/crop_{pic_num}.png"
            cv2.imwrite(crop_path, crop)
            
            pic_num += 1

            # 上に進む
            y -= SCAN_HEIGHT

        # 下に戻って右に進む
        y = y_start_pos
        x += SCAN_STEP

    # 結果を表示
    print("Detected positions:", detected_positions)

    # 結果を画像に描画して保存
    for (x, y) in detected_positions:
        cv2.rectangle(image, (x, max(0, y - SCAN_HEIGHT)), (x + SCAN_STEP, y), (0, 255, 0), 2)

    output_path = "scanned_result.png"
    cv2.imwrite(output_path, image)
    print(f"Result saved to {output_path}")   


if __name__ == "__main__":
   # music_name = input("楽曲名を入力してください(ローマ字)：")
    music_name = "mei"
    get_score("mei")