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
    CarouselColumn, MessageAction
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
        # 建立三個輪播樣板
        carousel_columns = [
            CarouselColumn(
                thumbnail_image_url='https://example.com/image1.jpg',  # 替換成你的圖片URL
                title='學餐選項1',
                text='描述1',
                actions=[
                    MessageAction(label='餐點1', text='餐點1'),
                    MessageAction(label='餐點2', text='餐點2'),
                    MessageAction(label='餐點3', text='餐點3'),
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://example.com/image2.jpg',  # 替換成你的圖片URL
                title='學餐選項2',
                text='描述2',
                actions=[
                    MessageAction(label='餐點4', text='餐點4'),
                    MessageAction(label='餐點5', text='餐點5'),
                    MessageAction(label='餐點6', text='餐點6'),
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://example.com/image3.jpg',  # 替換成你的圖片URL
                title='學餐選項3',
                text='描述3',
                actions=[
                    MessageAction(label='餐點7', text='餐點7'),
                    MessageAction(label='餐點8', text='餐點8'),
                    MessageAction(label='餐點9', text='餐點9'),
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

    elif user_message.startswith("餐點"):
        # 從訊息中獲取餐點編號
        try:
            meal_index = int(user_message.split("餐點")[1])
            if 1 <= meal_index <= 9:
                # 根據餐點編號推薦一個隨機餐點
                recommended_food = random.choice(menu)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"推薦你今天的餐點是：{recommended_food}")
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="抱歉，無效的餐點編號。")
                )
        except ValueError:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="抱歉，無效的餐點編號。")
            )

if __name__ == "__main__":
    app.run()
