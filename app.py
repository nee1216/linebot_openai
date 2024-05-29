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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if message.startswith('Get Element Text:'):
        url, href = message.split(':', 1)[1].strip().split(',')
        get_element_text(url, href, event)
    elif message.startswith('Get Elements Text:'):
        url, href = message.split(':', 1)[1].strip().split(',')
        get_elements_text(url, href, event)

def get_element_text(url, href, event):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Confirm request success

    soup = BeautifulSoup(response.content, 'html.parser')

    element = soup.select_one(f'a[href="{href}"]')

    if element:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="內科通勤專車15:" + element.text.strip()))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'找不到具有 href="{href}" 的元素。'))

def get_elements_text(url, href, event):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Confirm request success

    soup = BeautifulSoup(response.content, 'html.parser')

    element = soup.select_one(f'a[href="{href}"]')

    if element:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="內科通勤專車16:" + element.text.strip()))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'找不到具有 href="{href}" 的元素。'))

if __name__ == "__main__":
    app.run(debug=True)
