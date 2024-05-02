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
    # 回應輪播模板
    columns = [
        CarouselColumn(
            thumbnail_image_url='https://example.com/image1.jpg',
            title='Option 1',
            text='This is option 1',
            actions=[
                MessageAction(label='Choose 1', text='You chose option 1'),
            ]
        ),
        CarouselColumn(
            thumbnail_image_url='https://example.com/image2.jpg',
            title='Option 2',
            text='This is option 2',
            actions=[
                MessageAction(label='Choose 2', text='You chose option 2'),
            ]
        )
    ]

    carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(columns=columns)
    )

    line_bot_api.reply_message(
        event.reply_token,
        carousel_template
    )

# 在本地端啟動 Flask 應用程序
if __name__ == "__main__":
    app.run()

