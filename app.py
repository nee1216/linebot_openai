from flask import Flask, request, abort
import random
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselTemplate,
    CarouselColumn, MessageAction, URIAction
)

app = Flask(__name__)

# 設置你的 Line Bot 的 Channel Access Token 與 Channel Secret
line_bot_api = LineBotApi('tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0584d0fc476d78024afcd7cbbf8096b4')

# 定義餐點列表
menu = [
    "牛肉麵",
    "滷肉飯",
    "三杯雞",
    "炒麵",
    "燒臘飯",
    "義大利麵",
    # 可以自行擴充餐點列表
]

# Line Bot 的 Webhook 路由
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

# 處理文字訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 接收使用者的訊息
    user_message = event.message.text.strip()

    if user_message == "學餐":
        # 建立三個按鈕選項
        carousel_columns = [
            CarouselColumn(
                thumbnail_image_url='https://example.com/image1.jpg',  # 替換成你的圖片URL
                title='隨機推薦',
                text='隨機推薦一個餐點',
                actions=[
                    MessageAction(label='隨機推薦', text='隨機推薦'),
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://example.com/image2.jpg',  # 替換成你的圖片URL
                title='呈現菜單',
                text='呈現所有菜單',
                actions=[
                    URIAction(label='菜單', uri='https://example.com/menu'),
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://example.com/image3.jpg',  # 替換成你的圖片URL
                title='私人推薦',
                text='私人推薦一個餐點',
                actions=[
                    MessageAction(label='私人推薦', text='私人推薦'),
                ]
            )
        ]

        # 創建輪播模板訊息
        carousel_template = TemplateSendMessage(
            alt_text='學餐選項',
            template=CarouselTemplate(columns=carousel_columns)
        )

        # 回覆輪播模板
        line_bot_api.reply_message(
            event.reply_token,
            carousel_template
        )

    elif user_message == "隨機推薦":
        # 隨機推薦一個餐點
        recommended_food = random.choice(menu)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"今天推薦你吃 {recommended_food}！")
        )

    elif user_message == "私人推薦":
        # 私人推薦一個餐點
        # 在這裡你可以自己實現一些邏輯，例如根據使用者的個人喜好進行推薦
        recommended_food = "推薦的餐點"  # 這裡需要替換成你的推薦邏輯
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"我特別為你推薦 {recommended_food}！")
        )

if __name__ == "__main__":
    app.run()
