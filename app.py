from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    CarouselTemplate, CarouselColumn, MessageAction, TemplateSendMessage, TextSendMessage
)
from linebot.exceptions import InvalidSignatureError
from linebot.models.events import MessageEvent, TextMessage
import random

# 用您的 Channel access token 替換
line_bot_api = LineBotApi('tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0584d0fc476d78024afcd7cbbf8096b4')

# 菜單選項
menu_options = {
    '餐廳 1': [
        '全州烤牛肉拌飯$100',
        '明洞炸豬排蓋飯$90',
        '朝鮮海苔炸雞蓋飯$90',
        '洋釀炸雞蓋飯$90',
        '豬肉嫩豆腐鍋(不辣)$110',
        '泡菜豬肉鍋(微辣)$110'
    ],
    '餐廳 2': [
        '酸辣湯餃(6顆)Dumpling in Hot&Sour Soup$90',
        '牛肉醬拌麵套餐$80',
        '高麗菜水餃套餐(10個)$80',
        '招牌鍋貼套餐(10個)$75',
        '韓式辣味鍋貼套餐(10個)$80',
        '酸辣麵套餐$85',
        '牛肉麵套餐$150'
    ],
    '餐廳 3': [
        '港式豬扒腸粉 $60',
        '港式西多士(花生、巧克力) $45',
        '港式XO醬炒蘿蔔糕 $55',
        '港式一丁麻油餐蛋麵 $80',
        '韓式辛拉麵 $90',
        '不倒翁起士濃拉麵 $95',
        '港式豬扒可頌/菠蘿包 $65'
    ],
    '餐廳 4': [
        '蒜香椒鹽雞胸餐盒$108',
        '牛雞雙重奏餐盒$175',
        '新鮮蔬食菜飯餐盒$76',
        '泰式打拋豬餐盒$105',
        '精緻滷牛腱餐盒$140',
        '油蔥雞肉飯餐盒$79',
        '泰式酸辣巴沙魚餐盒$85'
    ],
    '餐廳 5': [
        '原味咖喱飯$60',
        '日式炸豬排定食 pork chop set$85',
        '蒲燒鯛魚定食Kabayaki sea bream set$85',
        '菜飯Rice with vegetable$50',
        '親子丼$80',
        '親子丼(無菜)$70'
    ]
}

def create_carousel():
    carousel_template = CarouselTemplate(columns=[
        CarouselColumn(
            thumbnail_image_url='https://example.com/restaurant1.jpg',
            title='餐廳 1',
            text='選擇功能',
            actions=[
                MessageAction(label='菜單', text='餐廳 1 菜單'),
                MessageAction(label='小編推薦', text='餐廳 1 小編推薦'),
                MessageAction(label='隨機選擇', text='餐廳 1 隨機選擇')
            ]
        ),
        CarouselColumn(
            thumbnail_image_url='https://example.com/restaurant2.jpg',
            title='餐廳 2',
            text='選擇功能',
            actions=[
                MessageAction(label='菜單', text='餐廳 2 菜單'),
                MessageAction(label='小編推薦', text='餐廳 2 小編推薦'),
                MessageAction(label='隨機選擇', text='餐廳 2 隨機選擇')
            ]
        ),
        CarouselColumn(
            thumbnail_image_url='https://example.com/restaurant3.jpg',
            title='餐廳 3',
            text='選擇功能',
            actions=[
                MessageAction(label='菜單', text='餐廳 3 菜單'),
                MessageAction(label='小編推薦', text='餐廳 3 小編推薦'),
                MessageAction(label='隨機選擇', text='餐廳 3 隨機選擇')
            ]
        ),
        CarouselColumn(
            thumbnail_image_url='https://example.com/restaurant4.jpg',
            title='餐廳 4',
            text='選擇功能',
            actions=[
                MessageAction(label='菜單', text='餐廳 4 菜單'),
                MessageAction(label='小編推薦', text='餐廳 4 小編推薦'),
                MessageAction(label='隨機選擇', text='餐廳 4 隨機選擇')
            ]
        ),
        CarouselColumn(
            thumbnail_image_url='https://example.com/restaurant5.jpg',
            title='餐廳 5',
            text='選擇功能',
            actions=[
                MessageAction(label='菜單', text='餐廳 5 菜單'),
                MessageAction(label='小編推薦', text='餐廳 5 小編推薦'),
                MessageAction(label='隨機選擇', text='餐廳 5 隨機選擇')
            ]
        )
    ])

    template_message = TemplateSendMessage(
        alt_text='學餐選擇',
        template=carousel_template
    )

    return template_message

def handle_message(event):
    if event.message.text == '學餐':
        carousel_message = create_carousel()
        line_bot_api.reply_message(event.reply_token, carousel_message)
    elif '隨機選擇' in event.message.text:
        restaurant = event.message.text.split(' ')[0]
        if restaurant in menu_options:
            random_choice = random.choice(menu_options[restaurant])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"{restaurant} 為您隨機選擇的餐點是: {random_choice}")
            )

# 您的 webhook 處理函數（根據您的框架不同可能會有所不同）
from flask import Flask, request, abort

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == '學餐':
        carousel_message = create_carousel()
        line_bot_api.reply_message(event.reply_token, carousel_message)
    elif '隨機選擇' in event.message.text:
        restaurant = event.message.text.split(' ')[0]
        if restaurant in menu_options:
            random_choice = random.choice(menu_options[restaurant])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"{restaurant} 為您隨機選擇的餐點是: {random_choice}")
            )

if __name__ == "__main__":
    app.run()
