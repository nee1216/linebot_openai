from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, QuickReply, QuickReplyButton, MessageAction, TextSendMessage
from flask import Flask, request, abort

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

def send_carousel_message(event):
    # 這是您提供的 JSON 格式
    bubble_message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": "110學年 資科系學分",
                    "weight": "bold",
                    "color": "#1DB446",
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": "大一",
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "sm"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xxl",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "國 文",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "4學分",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "外 文 (英、日、德、韓文)",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "4學分",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "生命關懷 & 思維方法",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "各1學分",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "體 育",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "0學分",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "通識教育",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "4學分",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "微積分",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "6學分",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "程式設計(一) & 程式設計(二)",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "各3學分",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "巨量資料概論",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "3學分",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "線性代數",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "3學分",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "計算機概論",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "3學分",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "資料庫導論",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "3學分",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        }
                    ]
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "資科系大一必修",
                            "size": "xs",
                            "color": "#aaaaaa",
                            "flex": 0
                        }
                    ]
                }
            ]
        }
    }

    # 創建 FlexSendMessage
    flex_message = FlexSendMessage(
        alt_text="110學年 資科系學分",
        contents=bubble_message
    )

    # 發送 FlexSendMessage
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
                            "label": "國際貿易系",
                            "text": "國際貿易系"
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
                            "label": "物理系",
                            "text": "物理系"
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
    elif user_message in ["資料科學系", "資料管理系", "國際貿易系", "化學系", "物理系"]:
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
        
    # 判斷用戶是否選擇了110學年
    elif user_message == "110學年":
        # 檢查用戶之前選擇的科系
        if user_id in user_choices and user_choices[user_id] == "資料科學系":
            # 調用函數發送彈性消息
            send_carousel_message(event)
        else:
            # 回覆用戶尚未選擇資料科學系
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先選擇資料科學系。"))
        
    else:
        # 當使用者消息不是您期待的內容時，發送默認回復
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入正確的命令。")
        )

if __name__ == "__main__":
    # 使用 Flask 啟動服務器，監聽來自 LINE 的請求
    app.run(port=5000)
