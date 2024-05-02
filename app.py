from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, MessageAction, URIAction, PostbackAction

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0584d0fc476d78024afcd7cbbf8096b4')

# 监听来自 /callback 的 Post 请求
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

# 处理接收到的文本消息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 接收到的消息文本
    msg_text = event.message.text

    if msg_text == '住宿':
        # 回复与住宿相关的信息
        carousel_template = CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                    title='校內宿舍',
                    text='松勁樓，榕華樓，柚芳樓',
                    actions=[
                        MessageAction(
                            label='地址',
                            text='台北市士林區臨溪路70號'
                        ),
                        MessageAction(
                            label='交通資訊',
                            text='自行駕車、捷運、公車、計程車等交通方式'
                        ),
                        MessageAction(
                            label='住宿費用',
                            text='宿舍費用詳細資訊'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='S__201318420_0.jpg',
                    title='選單 2',
                    text='說明文字 2',
                    actions=[
                        PostbackAction(
                            label='postback',
                            data='data1'
                        ),
                        MessageAction(
                            label='學餐',
                            text='hi'
                        ),
                        URIAction(
                            label='STEAM 教育學習網',
                            uri='https://steam.oxxostudio.tw'
                        )
                    ]
                )
            ]
        )
        
        message = TemplateSendMessage(alt_text='CarouselTemplate', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, message)
    
    elif msg_text == '學餐':
        # 回复与学餐相关的消息
        message = TextSendMessage(text='這是學餐的資訊。')
        line_bot_api.reply_message(event.reply_token, message)
        
    else:
        # 回复原始消息
        message = TextSendMessage(text=msg_text)
        line_bot_api.reply_message(event.reply_token, message)

# new_news 函数
def new_news():
    url = 'https://web-ch.scu.edu.tw/index.php/housing/web_page/2540'
    
    response = requests.get(url)
    result = ""
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for i in range(1, 7):
            for tag in soup.find_all(f'h{i}'):
                result += f"Heading {i}: {tag.text.strip()}\n"
                
        result += "\n段落：\n"
        for p in soup.find_all('p'):
            result += f"{p.text.strip()}\n"
    else:
        result += f"Error fetching {url}: Status code {response.status_code}"
    
    return result

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
