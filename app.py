from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = "tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "0584d0fc476d78024afcd7cbbf8096b4"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


# Flex message JSON template
flex_message_json = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "backgroundColor": "#ACD6FF",
        "cornerRadius": "md",
        "contents": [
          {
            "type": "text",
            "text": "公車到站時間",
            "weight": "bold",
            "size": "xl",
            "margin": "xs",
            "gravity": "center",
            "align": "center",
            "color": "#333333",
            "decoration": "none"
          }
        ]
      },
      {
        "type": "separator",
        "margin": "md"
      },
      {
        "type": "text",
        "text": "回學校",
        "margin": "md",
        "decoration": "none",
        "align": "center",
        "gravity": "center",
        "size": "lg",
        "color": "#333333",
        "weight": "bold"
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "士林站→東吳大學",
          "text": "捷運士林站→東吳大學"
        },
        "color": "#1E90FF",
        "margin": "xs"
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "士林站→東吳大學(錢穆故居)",
          "text": "捷運士林站→東吳大學(錢穆故居)"
        },
        "color": "#1E90FF",
        "margin": "xs"
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "劍南路→東吳大學(錢穆故居)",
          "text": "捷運劍南路→東吳大學(錢穆故居)"
        },
        "color": "#1E90FF",
        "margin": "xs"
      },
      {
        "type": "separator",
        "margin": "xxl"
      },
      {
        "type": "text",
        "text": "離開學校",
        "margin": "md",
        "align": "center",
        "gravity": "center",
        "size": "lg",
        "color": "#333333",
        "weight": "bold"
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "東吳大學→士林站",
          "text": "東吳大學→捷運士林站"
        },
        "color": "#1E90FF",
        "margin": "xs"
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "東吳大學(錢穆故居)→士林站",
          "text": "東吳大學(錢穆故居)→捷運士林站"
        },
        "color": "#1E90FF",
        "margin": "xs"
      },
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "message",
          "label": "東吳大學(錢穆故居)→劍南路",
          "text": "東吳大學(錢穆故居)→捷運劍南路"
        },
        "color": "#1E90FF",
        "margin": "xs"
      }
    ]
  },
  "styles": {
    "footer": {
      "separator": true
    }
  }
}

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=true)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "交通":
        flex_message = FlexSendMessage(alt_text="公車到站時間", contents=flex_message_json)
        line_bot_api.reply_message(event.reply_token, flex_message)

if __name__ == "__main__":
    app.run(debug=True)
