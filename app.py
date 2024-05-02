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
    # 接收使用者的訊息
    user_message = event.message.text.strip()

    # 檢查使用者訊息是否為 "住宿"
    if user_message == "住宿":
        # 建立三個輪播樣板
        carousel_columns = [
            CarouselColumn(
                thumbnail_image_url='https://github.com/nee1216/linebot_openai/blob/04c322993a6e7286568539958baffc5ba027b666/S__201318420_0.jpg',
                title='校外宿舍',
                text='有容學舍',
                actions=[
                    MessageAction(label='地址', text='校外宿舍有容學舍地址'),
                    MessageAction(label='交通方式', text='校外宿舍有容學舍交通方式'),
                    MessageAction(label='住宿費用', text='校外宿舍有容學舍住宿費用'),
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://example.com/dorm2.jpg',
                title='校外宿舍',
                text='泉思學舍',
                actions=[
                    MessageAction(label='地址', text='校外宿舍泉思學舍地址'),
                    MessageAction(label='交通方式', text='校外宿舍泉思學舍交通方式'),
                    MessageAction(label='住宿費用', text='校外宿舍泉思學舍住宿費用'),
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://github.com/nee1216/linebot_openai/blob/d1c06d40e5ff5bedef45f5579f8677a98cad1034/S__201318422_0.jpg',
                title='校內宿舍',
                text='松勁樓，榕華樓，柚芳樓',
                actions=[
                    MessageAction(label='地址', text='校內宿舍地址'),
                    MessageAction(label='交通方式', text='校內宿舍交通方式'),
                    MessageAction(label='住宿費用', text='校內宿舍住宿費用'),
                ]
            )
        ]

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

    # 根據選擇的地址選項回覆不同訊息
    elif user_message == "校外宿舍有容學舍地址":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="台北市萬華區大理街140號")
        )
    elif user_message == "校外宿舍泉思學舍地址":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="台北市北投區北投路二段55號")
        )
    elif user_message == "校內宿舍地址":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="台北市士林區臨溪路70號")
        )
    elif user_message == "校內宿舍交通方式":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="一、自行駕車

1、中山重慶北路交流道（往士林方向）匝道，經百齡橋直行中正路至雙溪公園，右轉至善路。
2、北二高路線—由堤頂交流道下北二高，往左至內湖路（內湖/大直方向），過自強隧道，直行到至
善路左轉。
二、捷運

1、搭乘淡水信義線至捷運士林站，1號出口出站，
     往中正路方向轉乘公車304、255、620、小18、小19、557至東吳大學站。
2、搭乘文湖線至捷運劍南路站，往劍潭寺方向出口，轉乘公車620，至東吳大學站。
三、公車

請於台北車站後站之承德路上搭乘304公車至東吳大學站。
請事先購買學生型悠遊卡（捷運公車兩用），
學生公車每段分段點扣費12元；車上投幣每車分段點每人每段15元 。
四、計程車

1、台北車站至雙溪校區約250元。
2、士林捷運站至雙溪校區約90元。
3、松山機場至雙溪校區約200元。")
        )


# 在本地端啟動 Flask 應用程序
if __name__ == "__main__":
    app.run()

