from linebot import LineBotApi, WebhookHandler
from linebot.models import *

from flask import Flask, request, abort

app = Flask(__name__)

# 設定你的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0584d0fc476d78024afcd7cbbf8096b4')


@app.route("/callback", methods=['POST'])
def callback():
    # 確認請求頭中的 X-Line-Signature
    signature = request.headers['X-Line-Signature']

    # 取得原始內容
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 處理 LINE 通知
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 檢查訊息是否為 "住宿"
    if event.message.text.strip() == "住宿":
        # 建立三個輪播樣板
        carousel_columns = []

        # 第一個輪播樣板
        carousel_columns.append(CarouselColumn(
            thumbnail_image_url='https://github.com/nee1216/linebot_openai/blob/04c322993a6e7286568539958baffc5ba027b666/S__201318420_0.jpg',
            title='校外宿舍',
            text='有容學舍',
            actions=[
                MessageAction(label='地址', text='地址'),
                MessageAction(label='交通方式', text='交通方式'),
                MessageAction(label='住宿費用', text='住宿費用'),
            ]
        ))

        # 第二個輪播樣板
        carousel_columns.append(CarouselColumn(
            thumbnail_image_url='https://example.com/dorm2.jpg',
            title='校外宿舍',
            text='泉思學舍',
            actions=[
                MessageAction(label='地址', text='地址'),
                MessageAction(label='交通方式', text='交通方式'),
                MessageAction(label='住宿費用', text='住宿費用'),
            ]
        ))

        # 第三個輪播樣板
        carousel_columns.append(CarouselColumn(
            thumbnail_image_url='https://github.com/nee1216/linebot_openai/blob/d1c06d40e5ff5bedef45f5579f8677a98cad1034/S__201318422_0.jpg',
            title='校內宿舍',
            text='松勁樓，榕華樓，柚芳樓',
            actions=[
                MessageAction(label='地址', text='地址'),
                MessageAction(label='交通方式', text='交通方式'),
                MessageAction(label='住宿費用', text='住宿費用'),
            ]
        ))

        # 創建輪播模板訊息
        carousel_template = TemplateSendMessage(
            alt_text='Dormitory options',
            template=CarouselTemplate(columns=carousel_columns)
        )

        # 回覆輪播模板
        line_bot_api.reply_message(
            event.reply_token,
            carousel_template
        )

# 在本地端啟動 Flask 應用程序
if __name__ == "__main__":
    app.run()

