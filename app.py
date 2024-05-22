from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, BubbleContainer, BoxComponent, TextComponent, SeparatorComponent
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "0584d0fc476d78024afcd7cbbf8096b4"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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

@app.route("/")
def index():
    return "Hello, World!"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "交通":
        transit_message = get_transit_info()
        flex_message = FlexSendMessage(alt_text="交通資訊", contents=transit_message)
        line_bot_api.reply_message(event.reply_token, flex_message)

def get_transit_info():
    try:
        response = requests.get("https://transit.navitime.com/zh-tw/tw/transfer?start=00016389&goal=00022583")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            transit_element = soup.find(id="transit-1")
            
            if transit_element:
                # 查找class为'time display-inline text-frame'的元素，并获取其文本内容
                time_element = transit_element.find(class_="time display-inline text-frame")
                if time_element:
                    time_text = time_element.get_text(strip=True)
                    print("捷運士林站(中正)-東吳大學:(557)")
                    print(time_text)
            
            transit_element = soup.find(id="transit-2")

            if transit_element:
                # 查找class为'time display-inline text-frame'的元素，并获取其文本内容
                time_element = transit_element.find(class_="time display-inline text-frame")
                if time_element:
                    time_text = time_element.get_text(strip=True)
                    print("捷運士林站(中正)-東吳大學:(300)")
                    print(time_text)

                else:
                    print("未找到指定的class元素。")
            else:
                print("未找到指定的id元素。")
        else:
            print(f"无法获取页面内容。状态码: {response.status_code}")

    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    app.run()

https://transit.navitime.com/zh-tw/tw/transfer?start=00016389&goal=00022583
