from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

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

def get_element_text(url, href):
    options = webdriver.ChromeOptions()
    service = ChromeService(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    driver.implicitly_wait(10)

    element = driver.find_element(By.CSS_SELECTOR, f'a[href="{href}"]')
    text = element.text.strip()

    driver.quit()

    return text

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    if user_message == "557公車":
        url = 'https://yunbus.tw/lite/route.php?id=TPE17333'
        href = 'https://yunbus.tw/#!stop/TPE171189'
        bus_info = get_element_text(url, href)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"557公車: {bus_info}"))
    elif user_message == "300公車":
        url = 'https://yunbus.tw/lite/route.php?id=TPE15532'
        href = 'https://yunbus.tw/#!stop/TPE29089'
        bus_info = get_element_text(url, href)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"300公車: {bus_info}"))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入有效指令"))

if __name__ == "__main__":
    app.run(debug=True)



