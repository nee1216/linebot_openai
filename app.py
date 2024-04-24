from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import openai
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# OPENAI API Key初始化設定
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_transit_info():
    options = webdriver.ChromeOptions()
    service = ChromeService(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://transit.navitime.com/zh-tw/tw/transfer?start=00016389&goal=00022583") 
        driver.maximize_window()
        driver.refresh()
        time.sleep(3) 

        # 獲取交通資訊
        table_element = driver.find_element(By.ID, "transit-1")
        transit_info_1 = "捷運士林站(中正)-東吳大學:\n" + table_element.text

        table_element = driver.find_element(By.ID, "transit-2")
        transit_info_2 = "\n\n" + table_element.text

        transit_info = transit_info_1 + transit_info_2
        print(transit_info)

        return transit_info

    except KeyboardInterrupt:
        print("程式被用戶中斷.")
        return None
    except Exception as e:
        print("發生錯誤:", str(e))
        return None
    finally:
        driver.close()

def GPT_response(text):
    # 接收回應
    response = openai.Completion.create(model="gpt-3.5-turbo-instruct", prompt=text, temperature=0.5, max_tokens=500)
    print(response)
    # 重組回應
    answer = response['choices'][0]['text'].replace('。','')
    return answer

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    
    if msg == '交通資訊':
        # 呼叫函數獲取交通資訊
        transit_info = get_transit_info()
        if transit_info:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(transit_info))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage('無法獲取交通資訊'))


@handler.add(PostbackEvent)
def handle_postback(event):
    print(event.postback.data)

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
