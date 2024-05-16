from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, request, abort
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "YOUR_CHANNEL_ACCESS_TOKEN"
LINE_CHANNEL_SECRET = "YOUR_CHANNEL_SECRET"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 创建字典来追踪用户的选择
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

# 当收到 LINE 消息时的回调函数
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id  # 获取用户的 ID
    
    # 判断是否是用户点击科系简介
    if user_message == "交通":  
        # 构建 Flex Message
        flex_message = {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "选择想了解的科系",
                        "align": "center",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#ffffff"
                    }
                ],
                "backgroundColor": "#471B00"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",    if user_message == "交通":  
        # 构建 Flex Message
        flex_message = {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "选择想了解的科系",
                        "align": "center",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#ffffff"
                    }
                ],
                "backgroundColor": "#471B00"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🌟先选择想了解的科系之后，就可以查看该系的必选修课程资讯咯!!!!",
                        "size": "md",
                        "wrap": True,
                        "weight": "bold"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#905c44",
                        "action": {
                            "type": "message",
                            "label": "資料科學系",
                            "text": "資料科學系"
                        }
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "sm"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#905c44",
                        "action": {
                            "type": "message",
                            "label": "資料管理系",
                            "text": "資料管理系"
                        }
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "sm"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#905c44",
                        "action": {
                            "type": "message",
                            "label": "法律系",
                            "text": "法律法律系"
                        }
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "sm"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#905c44",
                        "action": {
                            "type": "message",
                            "label": "化學系",
                            "text": "化學系"
                        }
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "sm"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#905c44",
                        "action": {
                            "type": "message",
                            "label": "日文系",
                            "text": "日文系"
                        }
                    }
                ]
            }
        }
        
        # 发送 Flex Message 给用户
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="选择想了解的科系", contents=flex_message)
        )
        
    # 判断用户是否选择了公车路线
    elif user_message in ["士林捷運站-東吳大學", "東吳大學-士林捷運站", "士林捷運站-東吳大學(錢穆故居)", "東吳大學(錢穆故居)-士林捷運站", "捷運劍南路站-東吳大學(錢穆故居)"]:
        send_transit_info(event, user_message)  # 调用

def send_transit_info(event, user_message):
    # 发送公车路线信息给用户
    if user_message == "士林捷運站-東吳大學":
        response = requests.get("https://transit.navitime.com/zh-tw/tw/transfer?start=00016389&goal=00022583")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            transit_element = soup.find(id="transit-1")
            if transit_element:
                time_element = transit_element.find(class_="time display-inline text-frame")
                if time_element:
                    time_text = time_element.get_text(strip=True)
                    transit_info = "捷運士林站(中正)-東吳大學:(557)\n" + time_text
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=transit_info))
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="未找到指定的 class 元素。"))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="未找到指定的 id 元素。"))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"无法获取页面内容。状态码: {response.status_code}"))
    elif user_message == "東吳大學-士林捷運站":
        # 处理其他路线信息的逻辑，以及其他路线的请求和回复
        pass
    # 处理其他公车路线的逻辑，以及其他路线的请求和回复

