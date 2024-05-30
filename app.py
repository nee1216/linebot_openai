import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 設定 LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "0584d0fc476d78024afcd7cbbf8096b4"
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# LINE Bot 的 Webhook 路由
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 爬取捷運站信息的函式
def scrape_station_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # 發送 GET 請求
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 確認請求成功

    # 解析 HTML 內容
    soup = BeautifulSoup(response.content, "html.parser")

    # 尋找捷運士林站(中正)的元素
    station_element = soup.find("a", class_="default_cursor", title="捷運士林站(中正)")

    if station_element:
        # 獲取該元素對應的 tr 元素內容並返回
        return station_element.find_parent("tr").text.strip()
    else:
        return f"找不到捷運士林站(中正)的內容。"

# LINE Bot 接收文字訊息的處理函式
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "交通":
        url1 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=557#"
        url2 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=300"
        station_info1 = scrape_station_info(url1)
        station_info2 = scrape_station_info(url2)
        reply_message = f"第一個網站捷運士林站(中正)的內容：\n{station_info1}\n\n第二個網站捷運士林站(中正)的內容：\n{station_info2}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入「捷運士林站(中正)資訊」查詢相關資訊。"))

if __name__ == "__main__":
    app.run()
