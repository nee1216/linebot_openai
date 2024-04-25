from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextMessage, TextSendMessage, MessageEvent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import time

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('0584d0fc476d78024afcd7cbbf8096b4')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 X-Line-Signature 標頭值
    signature = request.headers['X-Line-Signature']
    # 獲取請求體為文本
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # 處理 webhook 請求體
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 定義函數來獲取最新消息
def get_latest_news():
    # 設置Selenium的Chrome瀏覽器選項
    options = webdriver.ChromeOptions()
    service = ChromeService(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    news_list = []

    try:
        # 進入網站
        driver.get("https://www-news.scu.edu.tw/news-7?page=1")
        time.sleep(5)

        # 找到最新消息列表
        tbody = driver.find_element(By.XPATH, "//tbody")
        links = tbody.find_elements(By.TAG_NAME, "a")

        # 遍歷連結並提取最新消息
        for link in links:
            news_title = link.text
            news_url = link.get_attribute("href")
            news_list.append(f"校園頭條: {news_title}\n連結: {news_url}\n")
            
    except Exception as e:
        print("發生錯誤:", str(e))
        
    finally:
        # 關閉瀏覽器
        driver.close()
        
    # 返回最新消息列表
    return "".join(news_list)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 獲取接收到的訊息
    received_message = event.message.text
    
    # 判斷訊息是否為'最新消息'
    if received_message == '最新消息':
        # 獲取最新消息
        news = get_latest_news()
        # 發送回覆
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=news))
    else:
        # 將接收到的訊息原樣發送回去
        message = TextSendMessage(text=received_message)
        line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
