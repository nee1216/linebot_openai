from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, BubbleContainer, BoxComponent, TextComponent, SeparatorComponent
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = "YOUR_CHANNEL_ACCESS_TOKEN"
LINE_CHANNEL_SECRET = "YOUR_CHANNEL_SECRET"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

def get_element_text(url, href):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Confirm successful request

    soup = BeautifulSoup(response.content, 'html.parser')
    element = soup.select_one(f'a[href="{href}"]')

    if element:
        return element.text.strip()
    else:
        return f'Element with href="{href}" not found.'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    # Example logic for responding to specific messages
    if "內科通勤專車15" in user_message:
        text_response = get_element_text('https://yunbus.tw/lite/route.php?id=TPE15680', 'https://yunbus.tw/#!stop/TPE54724')
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=f"內科通勤專車15: {text_response}")
        )
    elif "內科通勤專車16" in user_message:
        text_response = get_element_text('https://yunbus.tw/lite/route.php?id=TPE15681', 'https://yunbus.tw/#!stop/TPE121572')
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=f"內科通勤專車16: {text_response}")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="未識別的指令。請使用 '內科通勤專車15' 或 '內科通勤專車16'")
        )

if __name__ == "__main__":
    app.run(debug=True)
