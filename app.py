from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import time
import requests

app = Flask(__name__)

# LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "0584d0fc476d78024afcd7cbbf8096b4"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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

chrome_driver_url = "https://raw.githubusercontent.com/nee1216/linebot_openai/master/chromedriver.exe"
driver_path = "chromedriver.exe"

response = requests.get(chrome_driver_url)
with open(driver_path, 'wb') as f:
    f.write(response.content)

executable_path = driver_path

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "最近消息":
        quick_reply_buttons = QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="一般公告", text="一般公告")),
                QuickReplyButton(action=MessageAction(label="學術活動", text="學術活動")),
                QuickReplyButton(action=MessageAction(label="學生活動", text="學生活動")),
                QuickReplyButton(action=MessageAction(label="徵才公告", text="徵才公告")),
            ]
        )

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請選擇你想了解的校園頭條類別：", quick_reply=quick_reply_buttons)
        )

    elif event.message.text == "一般公告":
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            service = ChromeService(executable_path=executable_path)
            driver = webdriver.Chrome(service=service, options=options)

            driver.get("https://news.scu.edu.tw/news-3")
            time.sleep(5)
            tbody = driver.find_element(By.XPATH, "//tbody")
            links = tbody.find_elements(By.TAG_NAME, "a")
            
            response = "一般公告:\n"
            for link in links:
                response += "{}\n連結: {}\n".format(link.text, link.get_attribute("href"))

            if not links:
                response += "目前沒有相關的公告。"

            driver.close()

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=response)
            )

        except Exception as e:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="發生錯誤: {}".format(str(e)))
            )

    elif event.message.text == "學術活動":
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            service = ChromeService(executable_path=executable_path)
            driver = webdriver.Chrome(service=service, options=options)

            driver.get("https://news.scu.edu.tw/news-4")
            time.sleep(5)
            tbody = driver.find_element(By.XPATH, "//tbody")
            links = tbody.find_elements(By.TAG_NAME, "a")
            
            response = "學術活動:\n"
            for link in links:
                response += "{}\n連結: {}\n".format(link.text, link.get_attribute("href"))

            if not links:
                response += "目前沒有相關的活動。"

            driver.close()

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=response)
            )

        except Exception as e:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="發生錯誤: {}".format(str(e)))
            )

    elif event.message.text == "徵才公告":
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            service = ChromeService(executable_path=executable_path)
            driver = webdriver.Chrome(service=service, options=options)

            driver.get("https://news.scu.edu.tw/news-6")
            time.sleep(5)
            tbody = driver.find_element(By.XPATH, "//tbody")
            links = tbody.find_elements(By.TAG_NAME, "a")
            
            response = "徵才公告:\n"
            for link in links:
                response += "{}\n連結: {}\n".format(link.text, link.get_attribute("href"))

            if not links:
                response += "目前沒有相關的公告。"

            driver.close()

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=response)
            )

        except Exception as e:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="發生錯誤: {}".format(str(e)))
            )
    elif event.message.text == "學生活動":
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            service = ChromeService(executable_path=executable_path)
            driver = webdriver.Chrome(service=service, options=options)

            driver.get("https://news.scu.edu.tw/news-5")
            time.sleep(5)
            tbody = driver.find_element(By.XPATH, "//tbody")
            links = tbody.find_elements(By.TAG_NAME, "a")
            
            response = "學生活動:\n"
            for link in links:
                response += "{}\n連結: {}\n".format(link.text, link.get_attribute("href"))

            if not links:
                response += "目前沒有相關的公告。"

            driver.close()

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=response)
            )

        except Exception as e:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="發生錯誤: {}".format(str(e)))
            )

if __name__ == "__main__":
    app.run()
