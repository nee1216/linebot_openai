from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
import requests
from bs4 import BeautifulSoup
import logging

app = Flask(__name__)

# LINE Bot's Channel Access Token and Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "0584d0fc476d78024afcd7cbbf8096b4"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

logging.basicConfig(level=logging.INFO)

# Store user choices
user_choices = {}


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id

    if user_message in ["最新消息"]:
        quick_reply = QuickReply(items=[
            QuickReplyButton(
                action=MessageAction(label="一般公告", text="一般公告"),
                image_url="https://thumb.silhouette-ac.com/t/8e/8e67ee69573010543bd48066cc2fb04f_t.jpeg"
            ),
            QuickReplyButton(
                action=MessageAction(label="學術活動", text="學術活動"),
                image_url="https://thumb.silhouette-ac.com/t/7b/7b2ef209d3fbed4189b6e8a5686df508_w.jpeg"
            ),
            QuickReplyButton(
                action=MessageAction(label="學生活動", text="學生活動"),
                image_url="https://thumb.silhouette-ac.com/t/8b/8be9d87e1fae34579fc57eb9abf7900c_t.jpeg"
            ),
            QuickReplyButton(
                action=MessageAction(label="校園頭條", text="校園頭條"),
                image_url="https://thumb.silhouette-ac.com/t/8b/8be9d87e1fae34579fc57eb9abf7900c_t.jpeg"
            ),
            QuickReplyButton(
                action=MessageAction(label="徵才公告", text="徵才公告"),
                image_url="https://thumb.silhouette-ac.com/t/8b/8be9d87e1fae34579fc57eb9abf7900c_t.jpeg"
            )
        ])

        reply_text = TextSendMessage(text="請選擇你想查看的最新消息類型", quick_reply=quick_reply)
        line_bot_api.reply_message(event.reply_token, reply_text)

        user_choices[user_id] = user_message
        return

    if user_message in ["一般公告", "學術活動", "學生活動", "校園頭條", "徵才公告"]:
        news_message = get_latest_news(user_message)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=news_message))


def get_latest_news(news_type):
    url_map = {
        "校園頭條": "https://news.scu.edu.tw/news-7",
        "一般公告": "https://news.scu.edu.tw/news-3",
        "學生活動": "https://news.scu.edu.tw/news-5",
        "徵才公告": "https://news.scu.edu.tw/news-6",
        "學術活動": "https://news.scu.edu.tw/news-4"
    }

    try:
        message = ""
        response = requests.get(url_map[news_type])
        response.raise_for_status()  # Raise HTTPError for bad responses
        root = BeautifulSoup(response.text, "html.parser")
        tbody = root.find("tbody")
        links = tbody.find_all("a")

        for link in links:
            message += "{}:\n{}\n".format(news_type, link.text.strip())
            message += "連結: {}\n\n".format(link["href"])

        return message.strip()

    except Exception as e:
        return '無法取得最新消息，請稍後再試：{}'.format(str(e))


if __name__ == "__main__":
    app.run(port=8000)
