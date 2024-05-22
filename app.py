from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, BubbleContainer, BoxComponent, TextComponent, SeparatorComponent
import requests
from bs4 import BeautifulSoup

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
      "separator": True
    }
  }
}

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

@app.route("/")
def index():
    return "Hello, World!"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "交通":
        flex_message = FlexSendMessage(alt_text="公車到站時間", contents=flex_message_json)
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif event.message.text == "捷運士林站→東吳大學":
        transit_message = get_transit_info("https://transit.navitime.com/zh-tw/tw/transfer?start=00016389&goal=00022583", "捷運士林站(中正) - 東吳大學", "557路線: ", "300路線: ")
        flex_message = FlexSendMessage(alt_text="交通資訊", contents=transit_message)
        line_bot_api.reply_message(event.reply_token, flex_message)
    elif event.message.text == "捷運士林站→東吳大學(錢穆故居)":
        transit_message = get_transit_info("https://transit.navitime.com/zh-tw/tw/transfer?start=00016389&goal=00022584", "捷運士林站(中正) - 東吳大學(錢穆故居)", "內科15往內科: ", "內科16往內科: ")
        flex_message = FlexSendMessage(alt_text="交通資訊", contents=transit_message)
        line_bot_api.reply_message(event.reply_token, flex_message)

def get_transit_info(url, title, route1_label, route2_label):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 獲取 id 為 transit-1 的元素
            transit_1_element = soup.find(id="transit-1")
            transit_1_text = ""
            if transit_1_element:
                time_element_1 = transit_1_element.find(class_="time display-inline text-frame")
                if time_element_1:
                    transit_1_text = time_element_1.get_text(strip=True)
            
            # 獲取 id 為 transit-2 的元素
            transit_2_element = soup.find(id="transit-2")
            transit_2_text = ""
            if transit_2_element:
                time_element_2 = transit_2_element.find(class_="time display-inline text-frame")
                if time_element_2:
                    transit_2_text = time_element_2.get_text(strip=True)
            
            # 建立 BubbleContainer 作為 FlexMessage
            transit_bubble = BubbleContainer(
                body=BoxComponent(
                    layout="vertical",
                    contents=[
                        TextComponent(text=title, weight="bold", size="md"),
                        SeparatorComponent(),
                        TextComponent(text=route1_label + transit_1_text, wrap=True),
                        SeparatorComponent(),
                        TextComponent(text=route2_label + transit_2_text, wrap=True)
                    ]
                )
            )
            return transit_bubble
        else:
            return BubbleContainer(
                body=BoxComponent(
                    layout="vertical",
                    contents=[
                        TextComponent(text="無法獲取頁面內容。狀態碼: {}".format(response.status_code), wrap=True)
                    ]
                )
            )
    
    except Exception as e:
        return BubbleContainer(
            body=BoxComponent(
                layout="vertical",
                contents=[
                    TextComponent(text='無法取得最新消息，請稍後再試：{}'.format(str(e)), wrap=True)
                ]
            )
        )

if __name__ == "__main__":
    app.run(debug=True)


