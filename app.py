from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, TextSendMessage
import requests
from bs4 import BeautifulSoup
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# 設定 LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "0584d0fc476d78024afcd7cbbf8096b4"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 設置日誌
if __name__ == "__main__":
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)

# Flex message JSON template
flex_message_json = {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#ACD6FF",
                "cornerRadius": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": "公車到站時間",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "xs",
                        "gravity": "center",
                        "align": "center",
                        "color": "#333333",
                        "decoration": "none"
                    }
                ]
            },
            {
                "type": "separator",
                "margin": "md"
            },
            {
                "type": "text",
                "text": "回學校",
                "margin": "md",
                "decoration": "none",
                "align": "center",
                "gravity": "center",
                "size": "lg",
                "color": "#333333",
                "weight": "bold"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "士林站→東吳大學",
                    "text": "捷運士林站→東吳大學"
                },
                "color": "#1E90FF",
                "margin": "xs"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "士林站→東吳大學(錢穆故居)",
                    "text": "捷運士林站→東吳大學(錢穆故居)"
                },
                "color": "#1E90FF",
                "margin": "xs"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "劍南路→東吳大學(錢穆故居)",
                    "text": "捷運劍南路→東吳大學(錢穆故居)"
                },
                "color": "#1E90FF",
                "margin": "xs"
            },
            {
                "type": "separator",
                "margin": "xxl"
            },
            {
                "type": "text",
                "text": "離開學校",
                "margin": "md",
                "align": "center",
                "gravity": "center",
                "size": "lg",
                "color": "#333333",
                "weight": "bold"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "東吳大學→士林站",
                    "text": "東吳大學→捷運士林站"
                },
                "color": "#1E90FF",
                "margin": "xs"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "東吳大學(錢穆故居)→士林站",
                    "text": "東吳大學(錢穆故居)→捷運士林站"
                },
                "color": "#1E90FF",
                "margin": "xs"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "東吳大學(錢穆故居)→劍南路",
                    "text": "東吳大學(錢穆故居)→捷運劍南路"
                },
                "color": "#1E90FF",
                "margin": "xs"
            }
        ]
    },
    "styles": {
        "footer": {
            "separator": True
        }
    }
}

@app.route("/callback", methods=['POST'])
def callback():
    try:
        # get X-Line-Signature header value
        signature = request.headers['X-Line-Signature']

        # get request body as text
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            app.logger.error("Invalid signature. Check your channel access token/channel secret.")
            abort(400)

        return 'OK'
    except Exception as e:
        app.logger.error(f"Exception in /callback: {e}")
        abort(500)

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
    station_element = soup.find("a", class_="default_cursor", title="東吳大學")

    if station_element:
        # 獲取該元素對應的 tr 元素內容並返回
        return station_element.find_parent("tr").text.strip()
    else:
        return f"找不到東吳大學的內容。"

def scrape_station_info1(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # 發送 GET 請求
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 確認請求成功

    # 解析 HTML 內容
    soup = BeautifulSoup(response.content, "html.parser")

    # 尋找捷運士林站(中正)的元素
    station_element = soup.find("a", class_="default_cursor", title="東吳大學(錢穆故居)")

    if station_element:
        # 獲取該元素對應的 tr 元素內容並返回
        return station_element.find_parent("tr").text.strip()
    else:
        return f"找不到東吳大學(錢穆故居)的內容。"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        if event.message.text == "交通":
            flex_message = FlexSendMessage(alt_text="公車到站時間", contents=flex_message_json)
            line_bot_api.reply_message(event.reply_token, flex_message)
        elif event.message.text == "東吳大學→捷運士林站":
            url1 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=557#"
            url2 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=300"
            station_info1 = scrape_station_info(url1)
            station_info2 = scrape_station_info(url2)
            reply_message = f"557公車：\n{station_info1}\n\n300公車：\n{station_info2}"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        elif event.message.text == "東吳大學(錢穆故居)→捷運士林站":
            url1 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=557#"
            url2 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=300"
            station_info3 = scrape_station_info1(url1)
            station_info4 = scrape_station_info1(url2)
            reply_message = f"557公車：\n{station_info3}\n\n300公車：\n{station_info4}"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入正確的關鍵字查詢相關資訊。"))
    except Exception as e:
        app.logger.error(f"Exception in handle_message: {e}")
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="發生錯誤，請稍後再試。"))

if __name__ == "__main__":
    app.run(debug=True)
