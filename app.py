from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from flask import Flask, request, abort
import time

app = Flask(__name__)

# LINE Bot 的 Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi("tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("0584d0fc476d78024afcd7cbbf8096b4")

# 設置 Selenium 的 WebDriver
options = webdriver.ChromeOptions()
service = ChromeService(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

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
    
    # 判斷使用者是否要求最新消息
    if user_message == "最新消息":
        # 使用 Selenium 抓取網頁內容
        driver.get("https://www-news.scu.edu.tw/news-7?page=1")
        time.sleep(5)
        
        # 抓取校園新聞
        tbody = driver.find_element(By.XPATH, "//tbody")
        links = tbody.find_elements(By.TAG_NAME, "a")
        
        # 組裝消息
        response_message = "校園頭條:\n"
        for link in links:
            response_message += f"{link.text}\n{link.get_attribute('href')}\n\n"
        
        # 發送消息給用戶
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response_message)
        )
    else:
        # 當使用者消息不是"最新消息"時，發送默認回復
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入'最新消息'以獲取校園頭條。")
        )

if __name__ == "__main__":
    # 使用 Flask 啟動服務器，監聽來自 LINE 的請求
    app.run(port=5000)


