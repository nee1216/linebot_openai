from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
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
        news_message = latest_news()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=news_message))

def latest_news():
    try:
        response = requests.get("https://transit.navitime.com/zh-tw/tw/transfer?start=00016389&goal=00022583")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Assuming the transit information is in an element with id="transit-1"
            transit_1_element = soup.find(id="transit-1")
            if transit_1_element:
                transit_1_text = transit_1_element.get_text(strip=True)
                message = "捷運士林站(中正)-東吳大學:\n" + transit_1_text
            
            # Assuming the second part of transit information is in an element with id="transit-2"
            transit_2_element = soup.find(id="transit-2")
            if transit_2_element:
                transit_2_text = transit_2_element.get_text(strip=True)
                message += "\n\n" + transit_2_text
            
            message += "\n---------------------------------------------------------------------------------------"
            return message.strip()
        else:
            return f"Failed to retrieve the page. Status code: {response.status_code}"
    
    except Exception as e:
        return '無法取得最新消息，請稍後再試：{}'.format(str(e))

if __name__ == "__main__":
    app.run()
