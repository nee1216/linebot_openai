from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import time

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
    else:
        try:
            # 使用 GPT 回應
            GPT_answer = GPT_response(msg)
            print(GPT_answer)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))
        except:
            print(traceback.format_exc())
            line_bot_api.reply_message(event.reply_token, TextSendMessage('你好啊'))
