import requests
from bs4 import BeautifulSoup

WEBBOOK_URL = "https://discord.com/api/webhooks/1496876347476410589/qdEV4geQmkg00PZct6bK5LtwCx1Noj-t8qdT_pcTEncNUW0kiHrMVD6WbDs2Pqv1BO_K"

# サイトのHTMLを取得する
url = "https://www.pokemoncenter-online.com/"
response = requests.get(url)

# HTMLを読みやすく解析する
soup = BeautifulSoup(response.text, "html.parser")

# テキスト取得
slides = soup.find_all("div", class_ ="swiper-slide")

lottery_found = False

for slide in slides:
    link = slide.find("a")
    if link:
        href = link.get("href")
        print(href)
        if href and "/lottery/" in href:
            lottery_found = True
            message = f"🎯ポケセン抽選開始！\nhttps://www.pokemoncenter-online.com{href}"
            requests.post(WEBBOOK_URL, json={"content": message})
            print(f"通知送信！: {href}")


if not lottery_found:
    print("現在抽選受付中のお知らせはありません")






















































































































