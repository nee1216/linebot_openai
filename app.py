from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from linebot import LineBotApi
from linebot.models import TextSendMessage
import os

# 使用環境變量或其他配置方式存儲敏感信息
line_bot_api = LineBotApi(os.getenv('tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU='))
user_id = os.getenv('U0a15453a9b9531b8a1517ce2863fbc84')

# 設置無頭瀏覽器
options = webdriver.ChromeOptions()
options.add_argument('--headless')

# 使用相對路徑
chromedriver_path = './chromedriver.exe'  # '.' 表示當前工作目錄
service = ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

while True:
    try:
        driver.get("https://www-news.scu.edu.tw/news-7?page=1")
        time.sleep(5)
        tbody = driver.find_element(By.XPATH, "//tbody")
        
        links = tbody.find_elements(By.TAG_NAME, "a")
        
        # 建構消息內容
        messages = []
        for link in links:
            message_text = f"校園頭條: {link.text}\n連結: {link.get_attribute('href')}\n"
            messages.append(TextSendMessage(text=message_text))
        
        # 傳送消息
        for message in messages:
            line_bot_api.push_message(user_id, message)
        
        # 控制爬蟲和發送頻率
        time.sleep(3600)  # 等待一小時再繼續執行
        
    except Exception as e:
        print("發生錯誤:", str(e))
    
    print("---------------------------------------------------------------------------------------")

driver.quit()

