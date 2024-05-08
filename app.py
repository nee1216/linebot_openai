from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    FlexSendMessage
)
from flask import Flask, request, abort

app = Flask(__name__)

# LINE Bot 的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi("tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("0584d0fc476d78024afcd7cbbf8096b4")

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

# 當收到 LINE 消息時的回調函數
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    
    # 如果使用者要求查看科系簡介
    if user_message == "科系簡介":
        # Flex Message 模板
        flex_message_data = {
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
                        "wrap": true,
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
                            "type": "uri",
                            "label": "資料科學系",
                            "uri": "https://linecorp.com"
                        },
                        "margin": "md"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#905c44",
                        "action": {
                            "type": "uri",
                            "label": "資料管理系",
                            "uri": "https://linecorp.com"
                        },
                        "margin": "md"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#905c44",
                        "action": {
                            "type": "uri",
                            "label": "國際貿易系",
                            "uri": "https://linecorp.com"
                        },
                        "margin": "md"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#905c44",
                        "action": {
                            "type": "uri",
                            "label": "化學系",
                            "uri": "https://linecorp.com"
                        },
                        "margin": "md"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#905c44",
                        "action": {
                            "type": "uri",
                            "label": "物理系",
                            "uri": "https://linecorp.com"
                        },
                        "margin": "md"
                    }
                ]
            }
        }
        
        # 創建 FlexSendMessage 並發送
        flex_message = FlexSendMessage(alt_text="科系簡介", contents=flex_message_data)
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        # 回復默認的消息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入'科系簡介'以查看相關資訊。")
        )

if __name__ == "__main__":
    # 使用 Flask 啟動服務器，監聽來自 LINE 的請求
    app.run(port=5000)
