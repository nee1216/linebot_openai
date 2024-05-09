from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TemplateSendMessage, CarouselTemplate,
    CarouselColumn, URITemplateAction, QuickReply, QuickReplyButton,
    MessageAction, TextSendMessage
)
from flask import Flask, request, abort

app = Flask(__name__)

# LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "0584d0fc476d78024afcd7cbbf8096b4"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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
    
    if user_message == "科系簡介":
        # 構建 Flex Message 讓用戶選擇科系
        flex_message = FlexSendMessage(
            alt_text="選擇想了解的科系",
            contents={
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
                            "text": "🌟先選擇想了解的科系之後，就可以查看該系的必選修課程資訊嘍!",
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
        )

        # 發送 Flex Message 給用戶
        line_bot_api.reply_message(event.reply_token, flex_message)

    elif user_message in ["資料科學系", "資料管理系", "國際貿易系", "化學系", "物理系"]:
        # 當用戶選擇了科系後，發送快速回復，讓用戶選擇入學學年
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

        reply_text = TextSendMessage(text="請選擇你入學學年？", quick_reply=quick_reply)
        line_bot_api.reply_message(event.reply_token, reply_text)

    elif user_message == "110學年":
        # 用戶選擇了110學年，發送旋轉木馬模板消息
        send_carousel_message(event)

    else:
        # 當使用者消息不是您期待的內容時，發送默認回復
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入正確的命令。")
        )

def send_carousel_message(event):
    # 建立 Carousel Template Message
    message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://thumb.silhouette-ac.com/t/8b/8be9d87e1fae34579fc57eb9abf7900c_t.jpeg',  # 請提供有效的圖片 URL
                title='YOUR_TITLE_1',  # 請提供標題
                text='YOUR_SUBTITLE_1',  # 請提供副標題
                actions=[
                    URITemplateAction(
                        label='YOUR_LABEL_1',  # 請提供行為的描述，例如「連結點這邊」
                        uri='https://ithelp.ithome.com.tw/articles/10242373'  # 請提供有效的 URL
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://thumb.silhouette-ac.com/t/8b/8be9d87e1fae34579fc57eb9abf7900c_t.jpeg',  # 請提供有效的圖片 URL
                title='YOUR_TITLE_2',  # 請提供標題
                text='YOUR_SUBTITLE_2',  # 請提供副標題
                actions=[
                    URITemplateAction(
                        label='YOUR_LABEL_2',  # 請提供行為的描述，例如「連結點這邊」
                        uri='https://ithelp.ithome.com.tw/articles/10242373'  # 請提供有效的 URL
                    )
                ]
            )
        ]
    )
)

    # 發送 Carousel Template Message 給用戶
    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    # 使用 Flask 啟動服務器，監聽來自 LINE 的請求
    app.run(port=5000)

