from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, request, abort
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "0584d0fc476d78024afcd7cbbf8096b4"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 创建字典来追踪用户的科系选择
user_choices = {}

@app.route("/callback", methods=['POST'])
def callback():
    # 解析来自 LINE 的请求
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    # 验证请求的签名
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

# 當收到 LINE 消息时的回调函数
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id  # 获取用户的 ID
    
    # 判断用户是否选择了交通路线
    if user_message == "交通":  
        # 发送快速回复，让用户选择公车路线
        quick_reply = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="士林捷運站-東吳大學", text="士林捷運站-東吳大學")),
            QuickReplyButton(action=MessageAction(label="東吳大學-士林捷運站", text="東吳大學-士林捷運站")),
            QuickReplyButton(action=MessageAction(label="士林捷運站-東吳大學(錢穆故居)", text="士林捷運站-東吳大學(錢穆故居)")),
            QuickReplyButton(action=MessageAction(label="東吳大學(錢穆故居)-士林捷運站", text="東吳大學(錢穆故居)-士林捷運站")),
            QuickReplyButton(action=MessageAction(label="捷運劍南路站-東吳大學(錢穆故居)", text="捷運劍南路站-東吳大學(錢穆故居)"))
        ])
        
        # 发送快速回复给用户
        reply_text = TextSendMessage(text="請選擇公車路線?", quick_reply=quick_reply)
        line_bot_api.reply_message(event.reply_token, reply_text)
        
    # 判断用户是否选择了公车路线
    elif user_message in ["士林捷運站-東吳大學", "東吳大學-士林捷運站", "士林捷運站-東吳大學(錢穆故居)", "東吳大學(錢穆故居)-士林捷運站", "捷運劍南路站-東吳大學(錢穆故居)"]:
        # 记录用户选择的路线
        user_choices[user_id] = user_message
        
        # 发送相应的结果给用户
        if user_message == "士林捷運站-東吳大學":
            send_transit_info(event, user_message)
        elif user_message == "東吳大學-士林捷運站":
            send_transit_info(event, user_message)
        elif user_message == "士林捷運站-東吳大學(錢穆故居)":
            send_transit_info(event, user_message)
        elif user_message == "東吳大學(錢穆故居)-士林捷運站":
            send_transit_info(event, user_message)
        elif user_message == "捷運劍南路站-東吳大學(錢穆故居)":
            send_transit_info(event, user_message)
            
    else:
        # 发送默认回复
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入正確的命令。")
        )

def send_transit
