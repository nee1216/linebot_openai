from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, QuickReply, QuickReplyButton, MessageAction, TextSendMessage
from flask import Flask, request, abort
import json
import requests

app = Flask(__name__)

# LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "0584d0fc476d78024afcd7cbbf8096b4"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 創建字典來追蹤用戶的科系選擇
user_choices = {}

@app.route("/callback", methods=['POST'])
def callback():
    # 解析來自 LINE 的請求
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    # 驗證請求的簽名
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

def load_flex_message_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch JSON from URL: {response.status_code}")

# 定义发送 carousel message 的函数
def send_carousel_message(event, url, alt_text):
    # 从 URL 加载 JSON 文件内容
    carousel_message = load_flex_message_from_url(url)
    
    # 创建 FlexSendMessage
    flex_message = FlexSendMessage(
        alt_text=alt_text,
        contents=carousel_message
    )
    
    # 发送 FlexSendMessage
    line_bot_api.reply_message(event.reply_token, flex_message)

# 當收到 LINE 消息時的回調函數
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id  # 獲取用戶的 ID
    
    # 判斷是否是使用者點選科系簡介
    if user_message == "科系簡介":  
        # 構建 Flex Message
        flex_message = {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "選擇想了解的科系",
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
                        "text": "🌟先選擇想了解的科系之後，就可以查看該系的必選修課程資訊嘍!!!!",
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
                            "label": "資訊管理系",
                            "text": "資訊管理系"
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
                            "text": "法律系"
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
        
        # 發送 Flex Message 給用戶
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="選擇想了解的科系", contents=flex_message)
        )
        
    # 判斷用戶是否選擇了科系
    elif user_message in ["資料科學系", "資訊管理系", "法律系", "化學系", "日文系"]:
        # 發送快速回復，讓用戶選擇入學學年
        quick_reply = QuickReply(items=[
            QuickReplyButton(
                action=MessageAction(label="110學年", text="110學年"),
                image_url="https://thumb.silhouette-ac.com/t/8e/8e67ee69573010543bd48066cc2fb04f_t.jpeg"
            ),
            QuickReplyButton(
                action=MessageAction(label="111學年", text="111學年"),
                image_url="https://thumb.silhouette-ac.com/t/7b/7b2ef209d3fbed4189b6e8a5686df508_w.jpeg"
            ),
            QuickReplyButton(
                action=MessageAction(label="112學年", text="112學年"),
                image_url="https://thumb.silhouette-ac.com/t/8b/8be9d87e1fae34579fc57eb9abf7900c_t.jpeg"
            )
        ])
        
        # 發送快速回復給用戶
        reply_text = TextSendMessage(text="請選擇你入學學年?", quick_reply=quick_reply)
        line_bot_api.reply_message(event.reply_token, reply_text)
        
        # 記錄用戶選擇的科系
        user_choices[user_id] = user_message
        
    # 處理不同科系和學年的查詢
    else:
        if user_id in user_choices:
            department = user_choices[user_id]
            if department == "資料科學系":
                if user_message == "110學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/110%E8%B3%87%E7%A7%91%E7%B3%BB.json", "110學年 資科系學分")
                elif user_message == "111學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/111%E8%B3%87%E7%A7%91%E7%B3%BB.json", "111學年 資科系學分")
                elif user_message == "112學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/112%E8%B3%87%E7%A7%91%E7%B3%BB.json", "112學年 資科系學分")
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請選擇正確的學年。"))
            elif department == "化學系":
                if user_message == "110學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/110%E5%8C%96%E5%AD%B8%E7%B3%BB.json", "110學年 化學系學分")
                elif user_message == "111學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/111%E5%8C%96%E5%AD%B8%E7%B3%BB.json", "111學年 化學系學分")
                elif user_message == "112學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/112%E5%8C%96%E5%AD%B8%E7%B3%BB.json", "112學年 化學系學分")
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請選擇正確的學年。"))
            elif department == "資訊管理系":
                if user_message == "110學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/110%E8%B3%87%E7%AE%A1%E7%B3%BB.json", "110學年 化學系學分")
                elif user_message == "111學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/111%E8%B3%87%E7%AE%A1%E7%B3%BB.json", "111學年 化學系學分")
                elif user_message == "112學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/112%E8%B3%87%E7%AE%A1%E7%B3%BB.json", "112學年 化學系學分")
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請選擇正確的學年。"))
            elif department == "法律系":
                if user_message == "110學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/110%E6%B3%95%E5%BE%8B%E7%B3%BB.json", "110學年 化學系學分")
                elif user_message == "111學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/111%E6%B3%95%E5%BE%8B%E7%B3%BB.json", "111學年 化學系學分")
                elif user_message == "112學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/112%E6%B3%95%E5%BE%8B%E7%B3%BB.json", "112學年 化學系學分")
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請選擇正確的學年。"))
            elif department == "日文系":
                if user_message == "110學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/110%E6%97%A5%E6%96%87%E7%B3%BB.json", "110學年 化學系學分")
                elif user_message == "111學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/111%E6%97%A5%E6%96%87%E7%B3%BB.json", "111學年 化學系學分")
                elif user_message == "112學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/112%E6%97%A5%E6%96%87%E7%B3%BB.json", "112學年 化學系學分")
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請選擇正確的學年。"))
           

if __name__ == "__main__":
    app.run(port=12345)
