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
                thumbnail_image_url='https://www.google.com/imgres?q=%E6%9C%89%E5%AE%B9%E5%AD%B8%E8%88%8D&imgurl=https%3A%2F%2Fpgw.udn.com.tw%2Fgw%2Fphoto.php%3Fu%3Dhttps%3A%2F%2Fuc.udn.com.tw%2Fphoto%2F2023%2F09%2F05%2Frealtime%2F24829906.jpg%26x%3D0%26y%3D0%26sw%3D0%26sh%3D0%26exp%3D3600&imgrefurl=https%3A%2F%2Fudn.com%2Fnews%2Fstory%2F6928%2F7418820&docid=r07SUWuxS_FcXM&tbnid=nF79q6TVz4cLpM&vet=12ahUKEwjKp7Wk1u6FAxUXcPUHHZxgCzoQM3oECGIQAA..i&w=2508&h=1672&hcb=2&ved=2ahUKEwjKp7Wk1u6FAxUXcPUHHZxgCzoQM3oECGIQAA',
                title='校外宿舍',
                text='有容學舍',
                actions=[
                    MessageAction(label='地址', text='校外宿舍有容學舍地址'),
                    MessageAction(label='交通方式', text='校外宿舍有容學舍交通方式'),
                    MessageAction(label='住宿費用', text='校外宿舍有容學舍住宿費用'),
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://www.google.com/url?sa=i&url=https%3A%2F%2F247chill.blogspot.com%2F2021%2F08%2Fchuanszu.html&psig=AOvVaw3CDxckcuzvwy0J2E6_8oUY&ust=1714729262489000&source=images&cd=vfe&opi=89978449&ved=0CBIQjRxqFwoTCLC04rjW7oUDFQAAAAAdAAAAABAE',
                title='校外宿舍',
                text='泉思學舍',
                actions=[
                    MessageAction(label='地址', text='校外宿舍泉思學舍地址'),
                    MessageAction(label='交通方式', text='校外宿舍泉思學舍交通方式'),
                    MessageAction(label='住宿費用', text='校外宿舍泉思學舍住宿費用'),
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://233ca8414a.cbaul-cdnwnd.com/5a4223ad91b3073522caa2d53bc72ce4/200000001-9017d9113a/%E6%9F%9A%E8%8A%B3%E6%A8%93.jpg?ph=233ca8414a',
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
    elif user_message == "校外宿舍有容學舍交通方式":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="捷運：搭乘板南線到捷運龍山寺站，步行約6分鐘即可抵達。")
        )
    elif user_message == "校外宿舍泉思學舍地址":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="台北市北投區北投路二段55號")
        )
    elif user_message == "校外宿舍泉思學舍交通方式":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="捷運：搭乘淡水信義線到捷運北投站，步行約3分鐘即可抵達。")
        )                    
    elif user_message == "校內宿舍地址":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="台北市士林區臨溪路70號")
        )
    elif user_message == "校內宿舍交通方式":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="一、自行駕車\n1、中山重慶北路交流道（往士林方向）匝道，經百齡橋直行中正路至雙溪公園，右轉至善路。\n2、北二高路線—由堤頂交流道下北二高，往左至內湖路（內湖/大直方向），過自強隧道，直行到至善路左轉。\n二、捷運\n1、搭乘淡水信義線至捷運士林站，1號出口出站，\n往中正路方向轉乘公車304、255、620、小18、小19、557至東吳大學站。\n2、搭乘文湖線至捷運劍南路站，往劍潭寺方向出口，轉乘公車620，至東吳大學站。\n三、公車\n請於台北車站後站之承德路上搭乘304公車至東吳大學站。\n請事先購買學生型悠遊卡（捷運公車兩用），\n學生公車每段分段點扣費12元；車上投幣每車分段點每人每段15元 。\n四、計程車\n1、台北車站至雙溪校區約250元。\n2、士林捷運站至雙溪校區約90元。\n3、松山機場至雙溪校區約200元。")
        )


# 在本地端啟動 Flask 應用程序
if __name__ == "__main__":
    app.run()

