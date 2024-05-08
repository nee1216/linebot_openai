from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage, FlexSendMessage, BubbleContainer, BoxComponent, 
    TextComponent, ButtonComponent, URIAction
)
from flask import Flask, request, abort

app = Flask(__name__)

# 請將這裡替換為你的 Channel Access Token 和 Channel Secret
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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    
    # 判斷使用者是否要求科系按鈕
    if user_message == "科系簡介":
        # 創建氣泡模板
        bubble = BubbleContainer(
            header=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(
                        text="選擇想了解的科系",
                        align="center",
                        weight="bold",
                        size="xl",
                        color="#ffffff"
                    )
                ],
                background_color="#471B00"
            ),
            body=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(
                        text="🌟先選擇想了解的科系之後，就可以查看該系的必選修課程資訊嘍!!!!",
                        size="md",
                        wrap=True,
                        weight="bold"
                    )
                ]
            ),
            footer=BoxComponent(
                layout="vertical",
                contents=[
                    ButtonComponent(
                        style="primary",
                        color="#905c44",
                        action=URIAction(
                            label="資料科學系",
                            uri="https://linecorp.com"
                        )
                    ),
                    ButtonComponent(
                        style="primary",
                        color="#905c44",
                        action=URIAction(
                            label="資料管理系",
                            uri="https://linecorp.com"
                        )
                    ),
                    ButtonComponent(
                        style="primary",
                        color="#905c44",
                        action=URIAction(
                            label="國際貿易系",
                            uri="https://linecorp.com"
                        )
                    ),
                    ButtonComponent(
                        style="primary",
                        color="#905c44",
                        action=URIAction(
                            label="化學系",
                            uri="https://linecorp.com"
                        )
                    ),
                    ButtonComponent(
                        style="primary",
                        color="#905c44",
                        action=URIAction(
                            label="物理系",
                            uri="https://linecorp.com"
                        )
                    )
                ]
            )
        )

        # 創建 FlexSendMessage，將氣泡模板作為消息內容
        flex_message = FlexSendMessage(
            alt_text="選擇想了解的科系",
            contents=bubble
        )

        # 發送 Flex Message 給用戶
        line_bot_api.reply_message(
            event.reply_token,
            flex_message
        )
    else:
        # 當使用者發送的消息不是"科系按鈕"時，發送默認回復
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入'科系按鈕'以查看可選科系。")
        )

if __name__ == "__main__":
    # 使用 Flask 啟動服務器，監聽來自 LINE 的請求
    app.run(port=5000)

