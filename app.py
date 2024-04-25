from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, MessageAction, URIAction, PostbackAction

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
        # 如果接收到的消息是“住宿”，則執行 new_news 函數並發送 Carousel 模板
        result = new_news()
        
        carousel_template = CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo.jpg',
                    title='校內宿舍',
                    text='松勁樓，榕華樓，柚芳樓',
                    actions=[
                        PostbackAction(
                            label='地址',
                            text='台北市士林區臨溪路70號'
                        ),
                        MessageAction(
                            label='交通資訊',
                            text='一、自行駕車
                                    1、中山重慶北路交流道（往士林方向）匝道，經百齡橋直行中正路至雙溪公園，右轉至善路。
2、北二高路線—由堤頂交流道下北二高，往左至內湖路（內湖/大直方向），過自強隧道，直行到至善路左轉。
二、捷運

1、搭乘淡水信義線至捷運士林站，1號出口出站，
     往中正路方向轉乘公車304、255、620、小18、小19、557至東吳大學站。
2、搭乘文湖線至捷運劍南路站，往劍潭寺方向出口，轉乘公車620，至東吳大學站。
三、公車

請於台北車站後站之承德路上搭乘304公車至東吳大學站。
請事先購買學生型悠遊卡（捷運公車兩用），
學生公車每段分段點扣費12元；車上投幣每車分段點每人每段15元 。
四、計程車

1、台北車站至雙溪校區約250元。
2、士林捷運站至雙溪校區約90元。
3、松山機場至雙溪校區約200元。'
                        ),
                        URIAction(
                            label='住宿費用',
                            text='    ['棟名', '宿舍别', '規格', '住宿費', '網路費', '保證金', '冷氣費用'],
    ['榕華樓', '女宿', '5人雅房', '1,200元', '窗型、分離式冷氣'],
    ['柚芳樓', '女宿', '8人雅房', '10,200元', '800元', '1,000元', '費用由寝室室友共同分'],
    ['松勁樓', '男宿', '8人雅房', '800元']'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
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
        # 處理特定訊息“學餐”
        # 根據您的需求添加處理程式碼
        # 可以添加類似 new_news() 函數
        # 然後使用 line_bot_api.reply_message(event.reply_token, message) 發送訊息
        
        # 範例：直接回復文字
        message = TextSendMessage(text='這是學餐的資訊。')
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
