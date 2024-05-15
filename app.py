from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    CarouselTemplate, CarouselColumn, MessageAction, TemplateSendMessage, TextSendMessage
)
from linebot.exceptions import InvalidSignatureError
from linebot.models.events import MessageEvent, TextMessage
import random
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)

# 用您的 Channel access token 替換
line_bot_api = LineBotApi('tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0584d0fc476d78024afcd7cbbf8096b4')

# 菜單選項
menu_options = {
    '木槿花韓食': [
        '全州烤牛肉拌飯$100',
        '明洞炸豬排蓋飯$90',
        '朝鮮海苔炸雞蓋飯$90',
        '洋釀炸雞蓋飯$90',
        '豬肉嫩豆腐鍋(不辣)$110',
        '泡菜豬肉鍋(微辣)$110'
    ],
    '四海遊龍': [
        '酸辣湯餃(6顆)Dumpling in Hot&Sour Soup$90',
        '牛肉醬拌麵套餐$80',
        '高麗菜水餃套餐(10個)$80',
        '招牌鍋貼套餐(10個)$75',
        '韓式辣味鍋貼套餐(10個)$80',
        '酸辣麵套餐$85',
        '牛肉麵套餐$150'
    ],
    '媽媽樂茶餐室': [
        '港式豬扒腸粉 $60',
        '港式西多士(花生、巧克力) $45',
        '港式XO醬炒蘿蔔糕 $55',
        '港式一丁麻油餐蛋麵 $80',
        '韓式辛拉麵 $90',
        '不倒翁起士濃拉麵 $95',
        '港式豬扒可頌/菠蘿包 $65'
    ],
    '強尼兄弟健康廚房': [
        '蒜香椒鹽雞胸餐盒$108',
        '牛雞雙重奏餐盒$175',
        '新鮮蔬食菜飯餐盒$76',
        '泰式打拋豬餐盒$105',
        '精緻滷牛腱餐盒$140',
        '油蔥雞肉飯餐盒$79',
        '泰式酸辣巴沙魚餐盒$85'
    ],
    '丼步喱': [
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
            thumbnail_image_url='https://ap-south-1.linodeobjects.com/nidin-production-v3/store/icons/s_3503_icon_20201008_151537_c1646.jpg',
            title='丼步喱',
            text='選擇功能',
            actions=[
                MessageAction(label='菜單', text='丼步喱 菜單'),
                MessageAction(label='小編推薦', text='丼步喱 小編推薦/避雷'),
                MessageAction(label='隨機選擇', text='丼步喱 隨機選擇')
            ]
        )
    ])

    template_message = TemplateSendMessage(
        alt_text='學餐選擇',
        template=carousel_template
    )

    return template_message

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    logging.info(f"收到訊息: {user_message}")
    
    if user_message == '學餐':
        carousel_message = create_carousel()
        line_bot_api.reply_message(event.reply_token, carousel_message)
    elif '隨機選擇' in user_message:
        restaurant = user_message.split(' ')[0]
        logging.info(f"處理隨機選擇功能: {restaurant}")
        if restaurant in menu_options:
            random_choice = random.choice(menu_options[restaurant])
            logging.info(f"隨機選擇結果: {random_choice}")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"今天推薦你吃: {random_choice}")
            )
        else:
            logging.warning(f"未找到對應的餐廳選項: {restaurant}")

# 您的 webhook 處理函數（根據您的框架不同可能會有所不同）
from flask import Flask, request, abort

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    logging.info(f"接收到請求: {body}")
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logging.error("Invalid signature error")
        abort(400)
    return 'OK'

if __name__ == "__main__":
    app.run()
