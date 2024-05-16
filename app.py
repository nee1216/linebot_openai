from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage, QuickReply, QuickReplyButton, MessageAction, TextSendMessage
from flask import Flask, request, abort
import json
import requests

app = Flask(__name__)

# LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "0584d0fc476d78024afcd7cbbf8096b4"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 創建字典來追蹤用戶的科系選擇
user_choices = {}

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

def load_flex_message_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch JSON from URL: {response.status_code}")

# 定义发送 carousel message 的函数
def send_carousel_message110(event):
    # 指定 JSON 文件的 URL
    json_url = "https://raw.githubusercontent.com/nee1216/linebot_openai/master/110%E8%B3%87%E7%A7%91%E7%B3%BB.json"
    
    # 从 URL 加载 JSON 文件内容
    carousel_message = load_flex_message_from_url(json_url)
    
    # 创建 FlexSendMessage
    flex_message = FlexSendMessage(
        alt_text="110學年 資科系學分",
        contents=carousel_message
    )
    
    # 发送 FlexSendMessage
    line_bot_api.reply_message(event.reply_token, flex_message)

# 定义发送 carousel message 的函数
def send_carousel_message111(event):
    # 指定 JSON 文件的 URL
    json_url = "https://raw.githubusercontent.com/nee1216/linebot_openai/master/111%E8%B3%87%E7%A7%91%E7%B3%BB.json"
    
    # 从 URL 加载 JSON 文件内容
    carousel_message = load_flex_message_from_url(json_url)
    
    # 创建 FlexSendMessage
    flex_message = FlexSendMessage(
        alt_text="111學年 資科系學分",
        contents=carousel_message
    )
    
    # 发送 FlexSendMessage
    line_bot_api.reply_message(event.reply_token, flex_message)
# 定义发送 carousel message 的函数
def send_carousel_message112(event):
    # 指定 JSON 文件的 URL
    json_url = "https://raw.githubusercontent.com/nee1216/linebot_openai/master/112%E8%B3%87%E7%A7%91%E7%B3%BB.json"
    
    # 从 URL 加载 JSON 文件内容
    carousel_message = load_flex_message_from_url(json_url)
    
    # 创建 FlexSendMessage
    flex_message = FlexSendMessage(
        alt_text="112學年 資科系學分",
        contents=carousel_message
    )
    
    # 发送 FlexSendMessage
    line_bot_api.reply_message(event.reply_token, flex_message)

# 當收到 LINE 消息時的回調函數
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id  # 獲取用戶的 ID
    
    # 判斷是否是使用者點選科系簡介
    if user_message == "交通":  
        # 構建 Flex Message
        flex_message = {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "選擇想了解的科系",
                        "align": "center",
                        "weight": "bold",
                        "size": "xl",
                        "color": "#ffffff"
                    }
                ],
                "backgroundColor": "#471B00"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "🌟先選擇想了解的科系之後，就可以查看該系的必選修課程資訊嘍!!!!",
                        "size": "md",
                        "wrap": True,
                        "weight": "bold"
                    }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#905c44",
                        "action": {
                            "type": "message",
                            "label": "資料科學系",
                            "text": "資料科學系"
                        }
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "sm"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#905c44",
                        "action": {
                            "type": "message",
                            "label": "資料管理系",
                            "text": "資料管理系"
                        }
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "sm"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#905c44",
                        "action": {
                            "type": "message",
                            "label": "法律系",
                            "text": "法律法律系"
                        }
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "sm"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#905c44",
                        "action": {
                            "type": "message",
                            "label": "化學系",
                            "text": "化學系"
                        }
                    },
                    {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "sm"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "color": "#905c44",
                        "action": {
                            "type": "message",
                            "label": "日文系",
                            "text": "日文系"
                        }
                    }
                ]
            }
        }
        
        # 發送 Flex Message 給用戶
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(alt_text="選擇想了解的科系", contents=flex_message)
        )
        
    # 判斷用戶是否選擇了科系
    elif user_message in ["士林捷運站-東吳大學", "東吳大學-士林捷運站", "士林捷運站-東吳大學(錢穆故居)", "東吳大學(錢穆故居)-士林捷運站", "捷運劍南路站-東吳
大學(錢穆故居)"]:
 
        # 記錄用戶選擇的科系
        user_choices[user_id] = user_message
        
    # 判斷用戶是否選擇了110學年
    elif user_message == "士林捷運站-東吳大學":
        # 檢查用戶之前選擇的科系
        if user_id in user_choices and user_choices[user_id] == "士林捷運站-東吳大學":
            # 調用函數發送彈性消息
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 获取id为'transit-1'的元素
                transit_element = soup.find(id="transit-1")
                
                if transit_element:
                    # 查找class为'time display-inline text-frame'的元素，并获取其文本内容
                    time_element = transit_element.find(class_="time display-inline text-frame")
                    if time_element:
                        time_text = time_element.get_text(strip=True)
                        print("捷運士林站(中正)-東吳大學:(557)")
                        print(time_text)
                
                transit_element = soup.find(id="transit-2")
    
                if transit_element:
                    # 查找class为'time display-inline text-frame'的元素，并获取其文本内容
                    time_element = transit_element.find(class_="time display-inline text-frame")
                    if time_element:
                        time_text = time_element.get_text(strip=True)
                        print("捷運士林站(中正)-東吳大學:(300)")
                        print(time_text)
    
                    else:
                        print("未找到指定的class元素。")
                else:
                    print("未找到指定的id元素。")
            else:
                print(f"无法获取页面内容。状态码: {response.status_code}")

        else:
            # 回覆用戶尚未選擇資料科學系
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先選擇資料科學系。"))
        
    else:
        # 當使用者消息不是您期待的內容時，發送默認回復
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入正確的命令。")
        )

if __name__ == "__main__":
    # 使用 Flask 啟動服務器，監聽來自 LINE 的請求
    app.run(port=5000)




