from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction
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
        # 點選交通按鈕時回覆按鈕模板
        buttons_template = ButtonsTemplate(
            title='請選擇交通資訊',
            text='請選擇要查詢的交通資訊',
            actions=[
                PostbackAction(label='內科通勤專車15', data = 'action=bus15'),
                PostbackAction(label='內科通勤專車16', data = 'action=bus16')
            ]
        )
        template_message = TemplateSendMessage(
            alt_text='交通資訊',
            template=buttons_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)

@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data
    if data == 'action=bus15':
        get_element_text(event.reply_token)
    elif data == 'action=bus16':
        get_elements_text(event.reply_token)

def get_element_text(reply_token):
    url = 'https://yunbus.tw/lite/route.php?id=TPE15680'
    href = 'https://yunbus.tw/#!stop/TPE54724'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 確認請求成功
        soup = BeautifulSoup(response.content, 'html.parser')
        element = soup.select_one(f'a[href="{href}"]')
        
        if element:
            line_bot_api.reply_message(reply_token, TextSendMessage(text="內科通勤專車15: " + element.text.strip()))
        else:
            line_bot_api.reply_message(reply_token, TextSendMessage(text=f'找不到具有 href="{href}" 的元素。'))
    except Exception as e:
        line_bot_api.reply_message(reply_token, TextSendMessage(text='無法取得最新消息，請稍後再試：{}'.format(str(e))))

def get_elements_text(reply_token):
    url = 'https://yunbus.tw/lite/route.php?id=TPE15681'
    href = 'https://yunbus.tw/#!stop/TPE121572'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 確認請求成功
        soup = BeautifulSoup(response.content, 'html.parser')
        element = soup.select_one(f'a[href="{href}"]')
        
        if element:
            line_bot_api.reply_message(reply_token, TextSendMessage(text="內科通勤專車16: " + element.text.strip()))
        else:
            line_bot_api.reply_message(reply_token, TextSendMessage(text=f'找不到具有 href="{href}" 的元素。'))
    except Exception as e:
        line_bot_api.reply_message(reply_token, TextSendMessage(text='無法取得最新消息，請稍後再試：{}'.format(str(e))))


if __name__ == "__main__":
    app.run()
