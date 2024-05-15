from flask import Flask, request, abort
import random
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselTemplate,
    CarouselColumn, MessageAction
)

app = Flask(__name__)

# 用您的 Channel access token 替換
line_bot_api = LineBotApi('tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0584d0fc476d78024afcd7cbbf8096b4')

# 定義餐點列表
menus = [
    ["牛肉麵", "滷肉飯", "三杯雞", "炒麵", "燒臘飯", "義大利麵"],
    ["咖哩飯", "石鍋拌飯", "排骨飯", "炸雞排", "牛排", "乾麵"],
    ["火鍋", "涼麵", "沙拉", "壽司", "粥", "麻辣鍋"],
    ["披薩", "漢堡", "炸雞", "熱狗", "牛肉漢堡", "千層麵"],
    ["素食便當", "牛肉便當", "雞腿便當", "排骨便當", "魚排便當", "豬排便當"]
]

# Line Bot 的 Webhook 路由
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

# 處理文字訊息事件
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 接收使用者的訊息
    user_message = event.message.text.strip()

    if user_message == "學餐":
        carousel_template_message = TemplateSendMessage(
            alt_text='學餐選項',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://example.com/image1.jpg',  # 替換成你的圖片URL
                        title='餐點選項1',
                        text='請選擇以下操作',
                        actions=[
                            MessageAction(label='隨機推薦', text='隨機推薦1'),
                            MessageAction(label='菜單1', text='菜單1'),
                            MessageAction(label='私人推薦', text='私人推薦1')
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://example.com/image2.jpg',  # 替換成你的圖片URL
                        title='餐點選項2',
                        text='請選擇以下操作',
                        actions=[
                            MessageAction(label='隨機推薦', text='隨機推薦2'),
                            MessageAction(label='菜單2', text='菜單2'),
                            MessageAction(label='私人推薦', text='私人推薦2')
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://example.com/image3.jpg',  # 替換成你的圖片URL
                        title='餐點選項3',
                        text='請選擇以下操作',
                        actions=[
                            MessageAction(label='隨機推薦', text='隨機推薦3'),
                            MessageAction(label='菜單3', text='菜單3'),
                            MessageAction(label='私人推薦', text='私人推薦3')
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://example.com/image4.jpg',  # 替換成你的圖片URL
                        title='餐點選項4',
                        text='請選擇以下操作',
                        actions=[
                            MessageAction(label='隨機推薦', text='隨機推薦4'),
                            MessageAction(label='菜單4', text='菜單4'),
                            MessageAction(label='私人推薦', text='私人推薦4')
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://example.com/image5.jpg',  # 替換成你的圖片URL
                        title='餐點選項5',
                        text='請選擇以下操作',
                        actions=[
                            MessageAction(label='隨機推薦', text='隨機推薦5'),
                            MessageAction(label='菜單5', text='菜單5'),
                            MessageAction(label='私人推薦', text='私人推薦5')
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, carousel_template_message)

    elif user_message.startswith("隨機推薦"):
        menu_number = int(user_message[-1]) - 1
        recommended_food = random.choice(menus[menu_number])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"今天推薦你吃 {recommended_food}！")
        )

    elif user_message.startswith("菜單"):
        menu_number = int(user_message[-1]) - 1
        menu_text = ""
        if user_message.endswith("1"):
            menu_text = """簡易主食(單配菜：海苔)
烤牛肉飯$85
炸豬排飯$75
炸雞蓋飯$75

主食
牛肉石鍋拌飯 停售$110
全州烤牛肉拌飯$100
明洞炸豬排蓋飯$90
朝鮮海苔炸雞蓋飯$90
洋釀炸雞蓋飯$90
韓式鍋物
豬肉嫩豆腐鍋(不辣)$110
黎泰院辣豆腐湯(小辣/中辣)$110
年糕豬肉鍋(不辣)$110
泡菜豬肉鍋(微辣)$110"""
        elif user_message.endswith("2"):
            menu_text = """湯餃Dumpling in Soup
酸辣湯餃(6顆)Dumpling in Hot&Sour Soup$90
牛肉湯餃(6顆)Dumpling in Beef Soup$90
玉米湯餃(6顆)Corn Dumpling in Soup$90

飲品Drink
豆漿Soybean Milk$20
紅茶Black Tea$20
紅茶豆漿Black Tea with Soybean Milk$20
杏仁豆漿Almond Soybean Milk$25

雲吞系列
鮮肉雲吞湯(4顆)$55
菜肉雲吞湯(4顆)$55
蝦肉雲吞湯(4顆)$65
鮮肉大抄手(5顆)$70
菜肉大抄手(5顆)$70
蝦肉大抄手(5顆)$75
鮮肉雲吞麵(4顆)$75
菜肉雲吞麵(4顆)$75
蝦肉雲吞麵(4顆)$85

套餐 set menu
牛肉乾拌麵套餐$105
牛肉醬拌麵套餐$80
高麗菜水餃套餐(10個)$80
招牌鍋貼套餐(10個)$75
韓式辣味鍋貼套餐(10個)$80
酸辣麵套餐$85
牛肉麵套餐$150

麵食類Noodles
牛汁乾麵Beef Sauce on noodles$50
肉燥拌麵minced pork on noodles$50
川味椒麻拌麵Sichuan Flavor Pepper Dried Noodles$50
酸辣麵Hot and Sour Noodles$75
貢丸麵Meat ball Noodles$60
魚丸麵 Fish Ball Noodles$60
牛肉湯麵(附滷蛋)Beef Noodle Soup(No Meat)$70
牛肉醬拌麵(乾)Noodle with Ground Beef$65
牛肉乾拌麵Tossed Noodles with Beef$100
牛肉麵(6塊牛肉)Beef Noodle Soup(With meat)$150
塔香辣肉醬麵(乾)Basil meat sauce(dry)$65
塔香辣肉醬麵(湯)Basil meat sauce (soup)$70

鍋貼Potstickers
招牌鍋貼(*8個)pork potstickers$56
韓式辣味鍋貼(*8個)Kimchi potstickers$64

水餃Dumpling
高麗菜水餃(*8個)Cabbage Dumpling$56
韭菜水餃(*8個)garlic chives$56
韓式辣味水餃(*8個)Kimchi Dumpling$64
玉米水餃(*8個)Corn Dumpling$56

湯品Soup
魚丸湯Fish Ball Soup$35
貢丸湯Meat ball Soup$35
酸辣湯Hot and Sour Soup$35
玉米濃湯corn Soup$35
牛肉湯Beef Soup$80"""
        elif user_message.endswith("3"):
            menu_text = """點心小食
燒餅(青蔥) $45
燒餅(紅豆) $45
港式西多士(花生、巧克力) $45
港式XO醬炒蘿蔔糕 $55
新加坡國民厚片 $45
澳門帶骨豬扒包 $75
現烤香港菠蘿油 $50
泰式檸檬雞柳條 $35
歐姆起士薯餅塔 $45


特色腸粉
港式豬扒腸粉 $60
港式肉鬆腸粉 $55
港式混醬腸粉 $45
義式燻雞腸粉 $60
老闆鮪魚腸粉 $60
薯薯餅腸粉 $55
滑蛋起士腸粉 $45
芋頭控腸粉 $55
原味滑蛋腸粉 $35
金黃粟米腸粉 $45"""


        elif user_message.endswith("4"):
            menu_text = """飲品
無糖豆漿$27
冬瓜茶$27
薏仁漿$36
深韻紅冷萃茶$40
鐵觀音冷萃茶$40
四季春冷萃茶$40


健康廚房餐盒
黑胡椒嫩煎雞胸餐盒$99
蒜香椒鹽雞胸餐盒$108
照燒風味雞胸餐盒$108
牛雞雙重奏餐盒$175
新鮮蔬食菜飯餐盒$76
日式豬丼餐盒$97
泰式雞肉燴飯餐盒$97
義式烤雞燴飯餐盒$105
滑蛋拌飯餐盒$73
蔬菜蘑菇拌飯餐盒$73
原味滑蛋拌飯餐盒$63
紅燒雞腿肉燴飯餐盒$99
可樂餐盒$111
花雕餐盒$112
咖哩餐盒$118
椒麻餐盒$112
套餐
麻油雞排燴飯$95
醬爆豬排飯$85
蜜汁豬排飯$85
泰式椒麻雞燴飯$85
南洋咖哩雞燴飯$85
和風牛排燴飯$100
川味炒麵$85
泰式炒麵$85
滑蛋牛肉燴飯$90
滑蛋牛肉燴飯$90
滑蛋牛肉燴飯$90"""
        elif user_message.endswith("5"):
            menu_text = """熱飯
鐵板牛肉燴飯$120
鐵板豬肉燴飯$120
鐵板雞肉燴飯$120
鐵板羊肉燴飯$120
鐵板蝦仁燴飯$140
鐵板田雞燴飯$130
鐵板蔬菜燴飯$110
鐵板花枝燴飯$130
鐵板青口燴飯$130
鐵板鮮魚燴飯$130
鐵板滑蛋燴飯$100
鐵板滑蛋燴飯$100
鐵板滑蛋燴飯$100
鐵板滑蛋燴飯$100
鐵板滑蛋燴飯$100
鐵板滑蛋燴飯$100

清湯
豆腐松阪豬燴飯$130
草莓口味牛蒡燴飯$130
花椰菜培根燴飯$140
炸魚片燴飯$140
鮭魚松阪豬燴飯$150
泡菜炒飯$120
咖哩炒飯$120
鐵板炒飯$120
芋頭薯條燴飯$120
餛飩湯麵$120
花枝燴飯$140
三杯松阪豬燴飯$140
紅蘿蔔鮭魚燴飯$150
各式湯麵$120
紅蘿蔔白菜燴飯$120"""
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=menu_text)
        )

    elif user_message.startswith("私人推薦"):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="抱歉，私人推薦功能尚未開放。")
        )

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="抱歉，我不太明白你的意思。你可以輸入「學餐」來查看餐點選項。")
        )

if __name__ == "__main__":
    app.run()
