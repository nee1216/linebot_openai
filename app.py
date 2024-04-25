from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('0584d0fc476d78024afcd7cbbf8096b4')

# 監聽所有來自 /callback 的 Post Request
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 接收到的消息文本
    msg_text = event.message.text
    
    if msg_text == '住宿':
        # 如果接收到的消息是“住宿”，則執行 new_news 函數
        result = new_news()
        # 發送結果作為回復
        message = TextSendMessage(text=result)
        line_bot_api.reply_message(event.reply_token, message)
    else:
        # 否則，回復原始消息
        message = TextSendMessage(text=msg_text)
        line_bot_api.reply_message(event.reply_token, message)

# new_news 函數
def new_news():
    url = 'https://web-ch.scu.edu.tw/index.php/housing/web_page/2540'
    
    response = requests.get(url)
    result = ""
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for i in range(1, 7):
            for tag in soup.find_all(f'h{i}'):
                result += f"Heading {i}: {tag.text.strip()}\n"
                
        result += "\nParagraphs:\n"
        for p in soup.find_all('p'):
            result += f"{p.text.strip()}\n"
    else:
        result += f"Error fetching {url}: Status code {response.status_code}"
    
    return result

import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

