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
            thumbnail_image_url='https://example.com/dorm1.jpg',
            title='Dorm 1',
            text='Choose an option',
            actions=[
                MessageAction(label='Address', text='Dorm 1 Address'),
                MessageAction(label='Transportation', text='Dorm 1 Transportation'),
                MessageAction(label='Fees', text='Dorm 1 Fees'),
            ]
        ))

        # 第二個輪播樣板
        carousel_columns.append(CarouselColumn(
            thumbnail_image_url='https://example.com/dorm2.jpg',
            title='Dorm 2',
            text='Choose an option',
            actions=[
                MessageAction(label='Address', text='Dorm 2 Address'),
                MessageAction(label='Transportation', text='Dorm 2 Transportation'),
                MessageAction(label='Fees', text='Dorm 2 Fees'),
            ]
        ))

        # 第三個輪播樣板
        carousel_columns.append(CarouselColumn(
            thumbnail_image_url='https://example.com/dorm3.jpg',
            title='Dorm 3',
            text='Choose an option',
            actions=[
                MessageAction(label='Address', text='Dorm 3 Address'),
                MessageAction(label='Transportation', text='Dorm 3 Transportation'),
                MessageAction(label='Fees', text='Dorm 3 Fees'),
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

