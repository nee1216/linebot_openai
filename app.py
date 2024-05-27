from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, BubbleContainer, BoxComponent, TextComponent, SeparatorComponent
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

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
        bus_557_text = get_element_text('https://yunbus.tw/lite/route.php?id=TPE17333', 'https://yunbus.tw/#!stop/TPE171189')
        bus_300_text = get_elements_text('https://yunbus.tw/lite/route.php?id=TPE15532', 'https://yunbus.tw/#!stop/TPE29089')
        
        # 建立 BubbleContainer 作為 FlexMessage
        transit_bubble = BubbleContainer(
            body=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(text="捷運士林站(中正) - 東吳大學", weight="bold", size="md"),
                    SeparatorComponent(),
                    TextComponent(text="557路線: " + bus_557_text, wrap=True),
                    SeparatorComponent(),
                    TextComponent(text="300路線: " + bus_300_text, wrap=True)
                ]
            )
        )
        return transit_bubble
    except Exception as e:
        return '無法取得最新消息，請稍後再試：{}'.format(str(e))

def get_element_text(url, href):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.select_one(f'a[href="{href}"]')
        if element:
            return element.text.strip()
    return "無法獲取資訊"

def get_elements_text(url, href):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.select_one(f'a[href="{href}"]')
        if element:
            return element.text.strip()
    return "無法獲取資訊"

if __name__ == "__main__":
    app.run()
