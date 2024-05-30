from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
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
    if event.message.text == "交通 15":
        get_element_text(event.reply_token, 'https://yunbus.tw/lite/route.php?id=TPE15680', 'https://yunbus.tw/#!stop/TPE54724')
    elif event.message.text == "交通 16":
        get_element_text(event.reply_token, 'https://yunbus.tw/lite/route.php?id=TPE15681', 'https://yunbus.tw/#!stop/TPE121572')
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入 '交通 15' 或 '交通 16' 查詢內科通勤專車資訊。"))

def get_element_text(reply_token, url, href):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 確認請求成功

        soup = BeautifulSoup(response.content, 'html.parser')
        element = soup.select_one(f'a[href="{href}"]')

        if element:
            message = f"內科通勤專車: {element.text.strip()}"
        else:
            message = f'找不到具有 href="{href}" 的元素。'
        line_bot_api.reply_message(reply_token, TextSendMessage(text=message))
    except Exception as e:
        line_bot_api.reply_message(reply_token, TextSendMessage(text='無法取得最新消息，請稍後再試：{}'.format(str(e))))

if __name__ == "__main__":
    app.run()
