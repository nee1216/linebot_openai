from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, MessageEvent, TextMessage

app = Flask(__name__)

# Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('your_channel_access_token')
handler = WebhookHandler('your_channel_secret')

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 处理接收到的文本消息
    user_message = event.message.text

    if user_message == '住宿':
        # 回复与住宿相关的消息
        reply_message = TextSendMessage(text='这是关于住宿的信息。')
        line_bot_api.reply_message(event.reply_token, reply_message)
    elif user_message == '學餐':
        # 回复与学餐相关的消息
        reply_message = TextSendMessage(text='这是关于学餐的信息。')
        line_bot_api.reply_message(event.reply_token, reply_message)
    else:
        # 回复原始消息
        reply_message = TextSendMessage(text='这是回覆您的原始訊息。')
        line_bot_api.reply_message(event.reply_token, reply_message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

