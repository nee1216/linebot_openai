from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, 
    CarouselTemplate, CarouselColumn, MessageAction, FlexSendMessage
)
import requests
from bs4 import BeautifulSoup
import random
import logging

app = Flask(__name__)

# LINE Bot's Channel Access Token and Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "0584d0fc476d78024afcd7cbbf8096b4"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Define the menu options
menu_options = {
    '木槿花韓食': [
        '全州烤牛肉拌飯$100', '明洞炸豬排蓋飯$90', '朝鮮海苔炸雞蓋飯$90',
        '洋釀炸雞蓋飯$90', '豬肉嫩豆腐鍋(不辣)$110', '泡菜豬肉鍋(微辣)$110'
    ],
    '四海遊龍': [
        '酸辣湯餃(6顆)$90', '牛肉醬拌麵套餐$80', '高麗菜水餃套餐(10個)$80',
        '招牌鍋貼套餐(10個)$75', '韓式辣味鍋貼套餐(10個)$80', '酸辣麵套餐$85', '牛肉麵套餐$150'
    ],
    '媽媽樂茶餐室': [
        '港式豬扒腸粉 $60', '港式西多士(花生、巧克力) $45', '港式XO醬炒蘿蔔糕 $55',
        '港式一丁麻油餐蛋麵 $80', '韓式辛拉麵 $90', '不倒翁起士濃拉麵 $95', '港式豬扒可頌/菠蘿包 $65'
    ],
    '強尼兄弟健康廚房': [
        '蒜香椒鹽雞胸餐盒$108', '牛雞雙重奏餐盒$175', '新鮮蔬食菜飯餐盒$76',
        '泰式打拋豬餐盒$105', '精緻滷牛腱餐盒$140', '油蔥雞肉飯餐盒$79', '泰式酸辣巴沙魚餐盒$85'
    ],
    '丼步喱': [
        '原味咖喱飯$60', '日式炸豬排定食$85', '蒲燒鯛魚定食$85', '菜飯$50', '親子丼$80', '親子丼(無菜)$70'
    ]
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
    user_message = event.message.text.strip()

    if user_message == "學餐":
        carousel_template_message = create_carousel()
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
    elif user_message in [
        "木槿花韓食 小編推薦/避雷", "木槿花韓食 菜單", 
        "媽媽樂茶餐室 小編推薦/避雷", "媽媽樂茶餐室 菜單",
        "四海遊龍 小編推薦/避雷", "四海遊龍 菜單",
        "強尼兄弟健康廚房 小編推薦/避雷", "強尼兄弟健康廚房 菜單",
        "丼步喱 小編推薦/避雷", "丼步喱 菜單"
    ]:
        send_carousel_menu(event, user_message)
    elif '隨機選擇' in user_message:
        restaurant = user_message.split(' ')[0]
        if restaurant in menu_options:
            random_choice = random.choice(menu_options[restaurant])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"今天推薦你吃: {random_choice}")
            )
    elif user_message == "最新消息":
        news_message = latest_news()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=news_message))
    elif user_message == "住宿":
        show_dormitory_options(event.reply_token)
    elif user_message in [
        "校外宿舍有容學舍地址", "校外宿舍有容學舍交通方式", 
        "校外宿舍泉思學舍地址", "校外宿舍泉思學舍交通方式", 
        "校內宿舍地址", "校內宿舍交通方式", 
        "校內宿舍住宿費用", "校外宿舍有容學舍住宿費用", "校外宿舍泉思學舍住宿費用"
    ]:
        handle_dormitory_message(event, user_message)
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入正確的命令。")
        )

def create_carousel():
    carousel_template = CarouselTemplate(columns=[
        CarouselColumn(
            thumbnail_image_url='https://picdn.gomaji.com/products/o/79/244079/244079_1_5.jpg',
            title='木槿花韓食',
            text='請選擇功能',
            actions=[
                MessageAction(label='菜單', text='木槿花韓食 菜單'),
                MessageAction(label='小編推薦', text='木槿花韓食 小編推薦/避雷'),
                MessageAction(label='隨機選擇', text='木槿花韓食 隨機選擇')
            ]
        ),
        CarouselColumn(
            thumbnail_image_url='https://tb-static.uber.com/prod/image-proc/processed_images/b4bac255f2633c94d3b327df1142ace6/fb86662148be855d931b37d6c1e5fcbe.jpeg',
            title='四海遊龍',
            text='選擇功能',
            actions=[
                MessageAction(label='菜單', text='四海遊龍 菜單'),
                MessageAction(label='小編推薦', text='四海遊龍 小編推薦/避雷'),
                MessageAction(label='隨機選擇', text='四海遊龍 隨機選擇')
            ]
        ),
        CarouselColumn(
            thumbnail_image_url='https://megapx-assets.dcard.tw/images/60605333-d75f-4433-9133-5dfbd074cdce/full.jpeg',
            title='媽媽樂茶餐室',
            text='選擇功能',
            actions=[
                MessageAction(label='菜單', text='媽媽樂茶餐室 菜單'),
                MessageAction(label='小編推薦', text='媽媽樂茶餐室 小編推薦/避雷'),
                MessageAction(label='隨機選擇', text='媽媽樂茶餐室 隨機選擇')
            ]
        ),
        CarouselColumn(
            thumbnail_image_url='https://tb-static.uber.com/prod/image-proc/processed_images/5ca9bdf981c23febc06bd967c4c91df6/e00617ce8176680d1c4c1a6fb65963e2.png',
            title='強尼兄弟健康廚房',
            text='選擇功能',
            actions=[
                MessageAction(label='菜單', text='強尼兄弟健康廚房 菜單'),
                MessageAction(label='小編推薦', text='強尼兄弟健康廚房 小編推薦/避雷'),
                MessageAction(label='隨機選擇', text='強尼兄弟健康廚房 隨機選擇')
            ]
        ),
        CarouselColumn(
            thumbnail_image_url='https://ap-south-1.linodeobjects.com/nidin-production-v3/store/icons/s_3503_icon_20201030094802.jpg',
            title='丼步喱',
            text='選擇功能',
            actions=[
                MessageAction(label='菜單', text='丼步喱 菜單'),
                MessageAction(label='小編推薦', text='丼步喱 小編推薦/避雷'),
                MessageAction(label='隨機選擇', text='丼步喱 隨機選擇')
            ]
        )
    ])
    return TemplateSendMessage(alt_text='餐廳菜單', template=carousel_template)

def send_carousel_menu(event, user_message):
    restaurant, option = user_message.split(' ')[0], user_message.split(' ')[1]
    if option == '菜單':
        menu = "\n".join(menu_options[restaurant])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"{restaurant} 的菜單:\n{menu}")
        )
    elif option == '小編推薦/避雷':
        recommendation = f"{restaurant} 的推薦/避雷功能尚未實作，請期待後續更新！"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=recommendation)
        )

def latest_news():
    url = "https://udn.com/news/breaknews/1"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find_all("div", class_="story-list__text")
    news = []
    for item in items[:5]:
        title = item.find("a").get_text().strip()
        link = item.find("a")["href"]
        news.append(f"{title}\n{link}")
    return "\n\n".join(news)

def show_dormitory_options(reply_token):
    flex_message = FlexSendMessage(
        alt_text="宿舍選項",
        contents={
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "header": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "校外宿舍有容學舍"}]},
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": "地址", "text": "校外宿舍有容學舍地址"}},
                            {"type": "button", "action": {"type": "message", "label": "交通方式", "text": "校外宿舍有容學舍交通方式"}},
                            {"type": "button", "action": {"type": "message", "label": "住宿費用", "text": "校外宿舍有容學舍住宿費用"}}
                        ]
                    }
                },
                {
                    "type": "bubble",
                    "header": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "校外宿舍泉思學舍"}]},
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": "地址", "text": "校外宿舍泉思學舍地址"}},
                            {"type": "button", "action": {"type": "message", "label": "交通方式", "text": "校外宿舍泉思學舍交通方式"}},
                            {"type": "button", "action": {"type": "message", "label": "住宿費用", "text": "校外宿舍泉思學舍住宿費用"}}
                        ]
                    }
                },
                {
                    "type": "bubble",
                    "header": {"type": "box", "layout": "vertical", "contents": [{"type": "text", "text": "校內宿舍"}]},
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {"type": "button", "action": {"type": "message", "label": "地址", "text": "校內宿舍地址"}},
                            {"type": "button", "action": {"type": "message", "label": "交通方式", "text": "校內宿舍交通方式"}},
                            {"type": "button", "action": {"type": "message", "label": "住宿費用", "text": "校內宿舍住宿費用"}}
                        ]
                    }
                }
            ]
        }
    )
    line_bot_api.reply_message(reply_token, flex_message)

def handle_dormitory_message(event, user_message):
    response_text = ""
    if user_message == "校外宿舍有容學舍地址":
        response_text = "校外宿舍有容學舍地址：新北市中和區中山路二段403號9樓"
    elif user_message == "校外宿舍有容學舍交通方式":
        response_text = "搭乘捷運至南勢角站，出站後步行約10分鐘可達。"
    elif user_message == "校外宿舍泉思學舍地址":
        response_text = "校外宿舍泉思學舍地址：台北市中正區羅斯福路四段85號"
    elif user_message == "校外宿舍泉思學舍交通方式":
        response_text = "搭乘捷運至公館站，出站後步行約5分鐘可達。"
    elif user_message == "校內宿舍地址":
        response_text = "校內宿舍地址：校園內特定宿舍區域"
    elif user_message == "校內宿舍交通方式":
        response_text = "搭乘校園巴士或步行至指定宿舍區域。"
    elif user_message == "校內宿舍住宿費用":
        response_text = "校內宿舍住宿費用：每學期約10000元"
    elif user_message == "校外宿舍有容學舍住宿費用":
        response_text = "校外宿舍有容學舍住宿費用：每月約8000元"
    elif user_message == "校外宿舍泉思學舍住宿費用":
        response_text = "校外宿舍泉思學舍住宿費用：每月約8500元"
    
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_text))

if __name__ == "__main__":
    app.run(debug=True)


