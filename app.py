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
        url = 'https://yunbus.tw/lite/route.php?id=TPE15680'
        href = 'https://yunbus.tw/#!stop/TPE54724'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 確認請求成功

        soup = BeautifulSoup(response.content, 'html.parser')

        element = soup.select_one(f'a[href="{href}"]')

        transit_1_text = ""
        if element:
            transit_1_text = element.text.strip()
        else:
            transit_1_text = f'找不到具有 href="{href}" 的元素。'

        url = 'https://yunbus.tw/lite/route.php?id=TPE15681'
        href = 'https://yunbus.tw/#!stop/TPE121572'
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 確認請求成功

        soup = BeautifulSoup(response.content, 'html.parser')

        element = soup.select_one(f'a[href="{href}"]')

        transit_2_text = ""
        if element:
            transit_2_text = element.text.strip()
        else:
            transit_2_text = f'找不到具有 href="{href}" 的元素。'

        # 建立 BubbleContainer 作為 FlexMessage
        transit_bubble = BubbleContainer(
            body=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(text="捷運劍南路站 - 東吳大學(錢穆故居)", weight="bold", size="md"),
                    SeparatorComponent(),
                    TextComponent(text="內科15往內科: " + transit_1_text, wrap=True),
                    SeparatorComponent(),
                    TextComponent(text="內科16往內科: " + transit_2_text, wrap=True)
                ]
            )
        )
        return transit_bubble
    
    except Exception as e:
        return '無法取得最新消息，請稍後再試：{}'.format(str(e))

if __name__ == "__main__":
    app.run()
