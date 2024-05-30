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
    # 確認 Line Webhook 的請求
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "交通":
        route15_info = get_element_text('https://yunbus.tw/lite/route.php?id=TPE15680', 'https://yunbus.tw/#!stop/TPE54724')
        route16_info = get_elements_text('https://yunbus.tw/lite/route.php?id=TPE15681', 'https://yunbus.tw/#!stop/TPE121572')

        response_message = f"內科通勤專車15: {route15_info}\n內科通勤專車16: {route16_info}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_message))

def get_element_text(url, href):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    element = soup.select_one(f'a[href="{href}"]')

    if element:
        return element.text.strip()
    else:
        return f'找不到具有 href="{href}" 的元素。'

def get_elements_text(url, href):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    element = soup.select_one(f'a[href="{href}"]')

    if element:
        return element.text.strip()
    else:
        return f'找不到具有 href="{href}" 的元素。'

if __name__ == "__main__":
    app.run(debug=True)
