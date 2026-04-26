import requests
from bs4 import BeautifulSoup
import schedule
import time
import os
from dotenv import load_dotenv

WEBHOOK_URL = "ここに先ほどコピーしたURLを貼る"

load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

def check_lottery():
    print("チェック中...")
    
    try:
        url = "https://www.pokemoncenter-online.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        slides = soup.find_all("div", class_="swiper-slide")

        lottery_found = False

        for slide in slides:
            link = slide.find("a")
            if link:
                href = link.get("href")
                if href and "/lottery/" in href:
                    lottery_found = True
                    message = f"🎯 ポケセン抽選受付中！\nhttps://www.pokemoncenter-online.com{href}"
                    requests.post(WEBHOOK_URL, json={"content": message})
                    print(f"通知送信！: {href}")

        if not lottery_found:
            print("現在抽選受付中のお知らせはありません")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

# 10分ごとに実行
schedule.every(10).minutes.do(check_lottery)

# 起動時に1回すぐ実行
check_lottery()

print("監視開始！止めるにはCtrl+Cを押してください")

while True:
    schedule.run_pending()
    time.sleep(1)