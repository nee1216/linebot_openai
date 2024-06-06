from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, MessageAction, FlexSendMessage, QuickReply, QuickReplyButton
from linebot.models.events import MessageEvent, TextMessage
import requests
from bs4 import BeautifulSoup
import random
import logging
import json


app = Flask(__name__)


# LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = "tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "0584d0fc476d78024afcd7cbbf8096b4"


line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


logging.basicConfig(level=logging.INFO)




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


# 創建字典來追蹤用戶的科系選擇
user_choices = {}


# Transport options flex message content
flex_message_json = {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
                "type": "box",
                "layout": "vertical",
                "backgroundColor": "#ACD6FF",
                "cornerRadius": "md",
                "contents": [
                    {
                        "type": "text",
                        "text": "公車到站時間",
                        "weight": "bold",
                        "size": "xl",
                        "margin": "xs",
                        "gravity": "center",
                        "align": "center",
                        "color": "#333333",
                        "decoration": "none"
                    }
                ]
            },
            {
                "type": "separator",
                "margin": "md"
            },
            {
                "type": "text",
                "text": "回學校",
                "margin": "md",
                "decoration": "none",
                "align": "center",
                "gravity": "center",
                "size": "lg",
                "color": "#333333",
                "weight": "bold"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "士林站→東吳大學",
                    "text": "捷運士林站→東吳大學"
                },
                "color": "#1E90FF",
                "margin": "xs"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "士林站→東吳大學(錢穆故居)",
                    "text": "捷運士林站→東吳大學(錢穆故居)"
                },
                "color": "#1E90FF",
                "margin": "xs"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "劍南路→東吳大學(錢穆故居)",
                    "text": "捷運劍南路→東吳大學(錢穆故居)"
                },
                "color": "#1E90FF",
                "margin": "xs"
            },
            {
                "type": "separator",
                "margin": "xxl"
            },
            {
                "type": "text",
                "text": "離開學校",
                "margin": "md",
                "align": "center",
                "gravity": "center",
                "size": "lg",
                "color": "#333333",
                "weight": "bold"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "東吳大學→士林站",
                    "text": "東吳大學→捷運士林站"
                },
                "color": "#1E90FF",
                "margin": "xs"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "東吳大學(錢穆故居)→士林站",
                    "text": "東吳大學(錢穆故居)→捷運士林站"
                },
                "color": "#1E90FF",
                "margin": "xs"
            },
            {
                "type": "button",
                "style": "link",
                "height": "sm",
                "action": {
                    "type": "message",
                    "label": "東吳大學(錢穆故居)→劍南路",
                    "text": "東吳大學(錢穆故居)→捷運劍南路"
                },
                "color": "#1E90FF",
                "margin": "xs"
            }
        ]
    },
    "styles": {
        "footer": {
            "separator": True
        }
    }
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


# 定义发送 carousel message 的函数
def send_carousel_message(event, url, alt_text):
    # 从 URL 加载 JSON 文件内容
    carousel_message = load_flex_message_from_url(url)
   
    # 创建 FlexSendMessage
    flex_message = FlexSendMessage(
        alt_text=alt_text,
        contents=carousel_message
    )
   
    # 发送 FlexSendMessage
    line_bot_api.reply_message(event.reply_token, flex_message)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id  # 獲取用戶的 ID
   
    if user_message == "最新消息":
        news_message = latest_news()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=news_message))
        return
    elif user_message == "住宿":
        show_dormitory_options(event.reply_token)
        return
    elif user_message == "學餐":
        # 建立輪播模板消息
        carousel_template_message = create_carousel()
        line_bot_api.reply_message(event.reply_token, carousel_template_message)
        return
    elif user_message == "交通":
        flex_message1 = FlexSendMessage(alt_text="公車到站時間", contents=flex_message_json)
        line_bot_api.reply_message(event.reply_token, flex_message1)
        return
    elif user_message == "東吳大學→捷運士林站":
        url1 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=557#"
        url2 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=300"
        station_info1 = scrape_station_info(url1)
        station_info2 = scrape_station_info(url2)
        reply_message = f"557公車：\n{station_info1}\n\n300公車：\n{station_info2}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        return
    elif user_message == "東吳大學(錢穆故居)→捷運士林站":
        url1 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=557#"
        url2 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=300"
        url3 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=%E5%85%A7%E7%A7%91%E9%80%9A%E5%8B%A4%E5%B0%88%E8%BB%8A15"
        url4 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=%E5%85%A7%E7%A7%91%E9%80%9A%E5%8B%A4%E5%B0%88%E8%BB%8A16"
        station_info3 = scrape_station_info1(url1)
        station_info4 = scrape_station_info1(url2)
        station_info5 = scrape_station_info1(url3)
        station_info6 = scrape_station_info1(url4)
        reply_message = f"557公車：\n{station_info3}\n\n300公車：\n{station_info4}\n\n內科15公車：\n{station_info5}\n\n內科16公車：\n{station_info6}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        return
    elif user_message == "東吳大學(錢穆故居)→捷運劍南路":
        url3 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=%E5%85%A7%E7%A7%91%E9%80%9A%E5%8B%A4%E5%B0%88%E8%BB%8A15"
        url4 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=%E5%85%A7%E7%A7%91%E9%80%9A%E5%8B%A4%E5%B0%88%E8%BB%8A16"
        url5 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=681"
        station_info7 = scrape_station_info1(url3)
        station_info8 = scrape_station_info1(url4)
        station_info15 = scrape_station_info1(url5)
        reply_message = f"內科15公車：\n{station_info7}\n\n內科16公車：\n{station_info8}\n\n681公車：\n{station_info15}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        return
    elif user_message == "捷運士林站→東吳大學":
        url1 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=557#"
        url2 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=300"
        station_info9 = scrape_station_info2(url1)
        station_info10 = scrape_station_info2_300(url2)
        reply_message = f"557公車：\n{station_info9}\n\n300公車：\n{station_info10}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        return
    elif user_message == "捷運士林站→東吳大學(錢穆故居)":
        url1 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=557#"
        url2 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=300"
        url3 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=%E5%85%A7%E7%A7%91%E9%80%9A%E5%8B%A4%E5%B0%88%E8%BB%8A15"
        url4 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=%E5%85%A7%E7%A7%91%E9%80%9A%E5%8B%A4%E5%B0%88%E8%BB%8A16"
        station_info9 = scrape_station_info2(url1)
        station_info10 = scrape_station_info2(url2)
        station_info11 = scrape_station_info2(url3)
        station_info12 = scrape_station_info2(url4)
        reply_message = f"557公車：\n{station_info9}\n\n300公車：\n{station_info10}\n\n內科15公車：\n{station_info11}\n\n內科16公車：\n{station_info12}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        return
    elif user_message == "捷運劍南路→東吳大學(錢穆故居)":
        url3 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=%E5%85%A7%E7%A7%91%E9%80%9A%E5%8B%A4%E5%B0%88%E8%BB%8A15"
        url4 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=%E5%85%A7%E7%A7%91%E9%80%9A%E5%8B%A4%E5%B0%88%E8%BB%8A16"
        url5 = "https://atis.taipei.gov.tw/aspx/businfomation/presentinfo.aspx?lang=zh-Hant-TW&ddlName=681"
        station_info13 = scrape_station_info3(url3)
        station_info14 = scrape_station_info3(url4)
        station_info16 = scrape_station_info3(url5)
        reply_message = f"內科15公車：\n{station_info13}\n\n內科16公車：\n{station_info14}\n\n681公車：\n{station_info16}"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))
        return
    elif user_message == "木槿花韓食 小編推薦/避雷":
        send_carousel_menu1(event)
        return




    elif user_message == "木槿花韓食 菜單":
        send_carousel_1menu(event)
        return




    elif user_message == "媽媽樂茶餐室 小編推薦/避雷":
        send_carousel_menu2(event)
        return




    elif user_message == "媽媽樂茶餐室 菜單":
        send_carousel_2menu(event)
        return




    elif user_message == "四海遊龍 小編推薦/避雷":
        send_carousel_menu3(event)
        return




    elif user_message == "四海遊龍 菜單":
        send_carousel_3menu(event)
        return




    elif user_message == "強尼兄弟健康廚房 小編推薦/避雷":
        send_carousel_menu4(event)
        return




    elif user_message == "強尼兄弟健康廚房 菜單":
        send_carousel_4menu(event)
        return




    elif user_message == "丼步喱 小編推薦/避雷":
        send_carousel_menu5(event)
        return




    elif user_message == "丼步喱 菜單":
        send_carousel_5menu(event)
        return




    elif '隨機選擇' in user_message:
        restaurant = user_message.split(' ')[0]
        logging.info(f"Processing random choice for: {restaurant}")
        if restaurant in menu_options:
            random_choice = random.choice(menu_options[restaurant])
            logging.info(f"Random choice result: {random_choice}")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"今天推薦你吃: {random_choice}")
            )
            return
        else:
            logging.warning(f"No matching restaurant option found: {restaurant}")


    elif user_message == "科系簡介":
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
                            "label": "資訊管理系",
                            "text": "資訊管理系"
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
                            "text": "法律系"
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
        return
    elif user_message in ["資料科學系", "資訊管理系", "法律系", "化學系", "日文系"]:
        # 發送快速回復，讓用戶選擇入學學年
        quick_reply = QuickReply(items=[
            QuickReplyButton(
                action=MessageAction(label="110學年", text="110學年"),
                image_url="https://thumb.silhouette-ac.com/t/8e/8e67ee69573010543bd48066cc2fb04f_t.jpeg"
            ),
            QuickReplyButton(
                action=MessageAction(label="111學年", text="111學年"),
                image_url="https://thumb.silhouette-ac.com/t/7b/7b2ef209d3fbed4189b6e8a5686df508_w.jpeg"
            ),
            QuickReplyButton(
                action=MessageAction(label="112學年", text="112學年"),
                image_url="https://thumb.silhouette-ac.com/t/8b/8be9d87e1fae34579fc57eb9abf7900c_t.jpeg"
            )
        ])
       
        # 發送快速回復給用戶
        reply_text = TextSendMessage(text="請選擇你入學學年?", quick_reply=quick_reply)
        line_bot_api.reply_message(event.reply_token, reply_text)
       
        # 記錄用戶選擇的科系
        user_choices[user_id] = user_message
        return
    elif user_message in ["110學年", "111學年", "112學年"]:
        # 檢查用戶是否選擇了科系
        if user_id in user_choices:
            department = user_choices[user_id]
            if department == "資料科學系":
                if user_message == "110學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/110%E8%B3%87%E7%A7%91%E7%B3%BB.json", "110學年 資科系學分")
                elif user_message == "111學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/111%E8%B3%87%E7%A7%91%E7%B3%BB.json", "111學年 資科系學分")
                elif user_message == "112學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/112%E8%B3%87%E7%A7%91%E7%B3%BB.json", "112學年 資科系學分")
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請選擇正確的學年。"))
            elif department == "化學系":
                if user_message == "110學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/110%E5%8C%96%E5%AD%B8%E7%B3%BB.json", "110學年 化學系學分")
                elif user_message == "111學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/111%E5%8C%96%E5%AD%B8%E7%B3%BB.json", "111學年 化學系學分")
                elif user_message == "112學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/112%E5%8C%96%E5%AD%B8%E7%B3%BB.json", "112學年 化學系學分")
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請選擇正確的學年。"))
            elif department == "資訊管理系":
                if user_message == "110學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/110%E8%B3%87%E7%AE%A1%E7%B3%BB.json", "110學年 化學系學分")
                elif user_message == "111學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/111%E8%B3%87%E7%AE%A1%E7%B3%BB.json", "111學年 化學系學分")
                elif user_message == "112學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/112%E8%B3%87%E7%AE%A1%E7%B3%BB.json", "112學年 化學系學分")
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請選擇正確的學年。"))
            elif department == "法律系":
                if user_message == "110學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/110%E6%B3%95%E5%BE%8B%E7%B3%BB.json", "110學年 化學系學分")
                elif user_message == "111學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/111%E6%B3%95%E5%BE%8B%E7%B3%BB.json", "111學年 化學系學分")
                elif user_message == "112學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/112%E6%B3%95%E5%BE%8B%E7%B3%BB.json", "112學年 化學系學分")
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請選擇正確的學年。"))
            elif department == "日文系":
                if user_message == "110學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/110%E6%97%A5%E6%96%87%E7%B3%BB.json", "110學年 化學系學分")
                elif user_message == "111學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/111%E6%97%A5%E6%96%87%E7%B3%BB.json", "111學年 化學系學分")
                elif user_message == "112學年":
                    send_carousel_message(event, "https://raw.githubusercontent.com/nee1216/linebot_openai/master/112%E6%97%A5%E6%96%87%E7%B3%BB.json", "112學年 化學系學分")
                else:
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請選擇正確的學年。"))
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先選擇資料科學系。"))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先選擇科系。"))
            return
    elif user_message in ["校外宿舍有容學舍地址", "校外宿舍有容學舍交通方式", "校外宿舍泉思學舍地址", "校外宿舍泉思學舍交通方式", "校內宿舍地址", "校內宿舍交通方式", "校內宿舍住宿費用", "校外宿舍有容學舍住宿費用", "校外宿舍泉思學舍住宿費用"]:
        handle_dormitory_message(event, user_message)
        return


    else:
        # 當使用者消息不是您期待的內容時，發送默認回復
        line_bot_api.reply_message(
            event.reply_token
        )


def load_flex_message_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch JSON from URL: {response.status_code}")


def scrape_station_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


    # 發送 GET 請求
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 確認請求成功


    # 解析 HTML 內容
    soup = BeautifulSoup(response.content, "html.parser")


    # 尋找捷運士林站(中正)的元素
    station_element = soup.find("a", class_="default_cursor", title="東吳大學")


    if station_element:
        # 獲取該元素對應的 tr 元素內容並返回
        return station_element.find_parent("tr").text.strip()
    else:
        return f"找不到東吳大學的內容。"


def scrape_station_info1(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


    # 發送 GET 請求
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 確認請求成功


    # 解析 HTML 內容
    soup = BeautifulSoup(response.content, "html.parser")


    # 尋找捷運士林站(中正)的元素
    station_element = soup.find("a", class_="default_cursor", title="東吳大學(錢穆故居)")


    if station_element:
        # 獲取該元素對應的 tr 元素內容並返回
        return station_element.find_parent("tr").text.strip()
    else:
        return f"找不到東吳大學(錢穆故居)的內容。"


def scrape_station_info2(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


    # 發送 GET 請求
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 確認請求成功


    # 解析 HTML 內容
    soup = BeautifulSoup(response.content, "html.parser")


    # 尋找捷運士林站(中正)的元素
    station_element = soup.find("a", class_="default_cursor", title="捷運士林站(中正)")


    if station_element:
        # 獲取該元素對應的 tr 元素內容並返回
        return station_element.find_parent("tr").text.strip()
    else:
        return f"找不到捷運士林站(中正)的內容。"
def scrape_station_info2_300(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


    # 發送 GET 請求
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 確認請求成功


    # 解析 HTML 內容
    soup = BeautifulSoup(response.content, "html.parser")

    # 尋找捷運士林站(中正)的元素
    station_element = soup.find("a", class_="default_cursor", title="捷運士林站(中正)")
    
    counter = 0

    for station_element in station_elements:
        counter += 1
        if counter == 2:
            print("300公車:", station_element.find_parent("tr").text.strip())
            break
    else:
        if counter < 2:
            print("找不到捷運士林站(中正)的內容。")

    # if station_element:
    #     # 獲取該元素對應的 tr 元素內容並返回
    #     return station_element.find_parent("tr").text.strip()
    # else:
    #     return f"找不到捷運士林站(中正)的內容。"
def scrape_station_info3(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }


    # 發送 GET 請求
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # 確認請求成功


    # 解析 HTML 內容
    soup = BeautifulSoup(response.content, "html.parser")


    # 尋找捷運士林站(中正)的元素
    station_element = soup.find("a", class_="default_cursor", title="捷運劍南路站")


    if station_element:
        # 獲取該元素對應的 tr 元素內容並返回
        return station_element.find_parent("tr").text.strip()
    else:
        return f"找不到捷運劍南路站的內容。"
   
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




def send_carousel_menu1(event):
    json_url = "https://raw.githubusercontent.com/nee1216/linebot_openai/master/menu1.json"
    carousel_message = load_flex_message_from_url(json_url)
    flex_message = FlexSendMessage(alt_text="木槿花韓食 小編推薦/避雷", contents=carousel_message)
    line_bot_api.reply_message(event.reply_token, flex_message)




def send_carousel_1menu(event):
    json_url = "https://raw.githubusercontent.com/nee1216/linebot_openai/master/1menu.json"
    carousel_message = load_flex_message_from_url(json_url)
    flex_message = FlexSendMessage(alt_text="木槿花韓食 菜單", contents=carousel_message)
    line_bot_api.reply_message(event.reply_token, flex_message)




def send_carousel_menu2(event):
    json_url = "https://raw.githubusercontent.com/nee1216/linebot_openai/master/menu2.json"
    carousel_message = load_flex_message_from_url(json_url)
    flex_message = FlexSendMessage(alt_text="媽媽樂茶餐室 小編推薦/避雷", contents=carousel_message)
    line_bot_api.reply_message(event.reply_token, flex_message)




def send_carousel_2menu(event):
    json_url = "https://raw.githubusercontent.com/nee1216/linebot_openai/master/2menu.json"
    carousel_message = load_flex_message_from_url(json_url)
    flex_message = FlexSendMessage(alt_text="媽媽樂茶餐室 菜單", contents=carousel_message)
    line_bot_api.reply_message(event.reply_token, flex_message)




def send_carousel_menu3(event):
    json_url = "https://raw.githubusercontent.com/nee1216/linebot_openai/master/menu3.json"
    carousel_message = load_flex_message_from_url(json_url)
    flex_message = FlexSendMessage(alt_text="四海遊龍 小編推薦/避雷", contents=carousel_message)
    line_bot_api.reply_message(event.reply_token, flex_message)




def send_carousel_3menu(event):
    json_url = "https://raw.githubusercontent.com/nee1216/linebot_openai/master/3menu.json"
    carousel_message = load_flex_message_from_url(json_url)
    flex_message = FlexSendMessage(alt_text="四海遊龍 菜單", contents=carousel_message)
    line_bot_api.reply_message(event.reply_token, flex_message)




def send_carousel_menu4(event):
    json_url = "https://raw.githubusercontent.com/nee1216/linebot_openai/master/menu4.json"
    carousel_message = load_flex_message_from_url(json_url)
    flex_message = FlexSendMessage(alt_text="強尼兄弟健康廚房 小編推薦/避雷", contents=carousel_message)
    line_bot_api.reply_message(event.reply_token, flex_message)




def send_carousel_4menu(event):
    json_url = "https://raw.githubusercontent.com/nee1216/linebot_openai/master/4menu.json"
    carousel_message = load_flex_message_from_url(json_url)
    flex_message = FlexSendMessage(alt_text="強尼兄弟健康廚房 菜單", contents=carousel_message)
    line_bot_api.reply_message(event.reply_token, flex_message)




def send_carousel_menu5(event):
    json_url = "https://raw.githubusercontent.com/nee1216/linebot_openai/master/menu5.json"
    carousel_message = load_flex_message_from_url(json_url)
    flex_message = FlexSendMessage(alt_text="丼步喱 小編推薦/避雷", contents=carousel_message)
    line_bot_api.reply_message(event.reply_token, flex_message)




def send_carousel_5menu(event):
    json_url = "https://raw.githubusercontent.com/nee1216/linebot_openai/master/5menu.json"
    carousel_message = load_flex_message_from_url(json_url)
    flex_message = FlexSendMessage(alt_text="丼步喱 菜單", contents=carousel_message)
    line_bot_api.reply_message(event.reply_token, flex_message)




def latest_news():
    try:
        message = ""
        response = requests.get("https://www-news.scu.edu.tw/news-7?page=1")
        root = BeautifulSoup(response.text, "html.parser")
        tbody = root.find("tbody")
        links = tbody.find_all("a")




        for link in links:
            message += "校園頭條:\n{}\n".format(link.text.strip())
            message += "連結: {}\n\n".format(link["href"])




        return message.strip()
   
    except Exception as e:
        return '無法取得最新消息，請稍後再試：{}'.format(str(e))




def show_dormitory_options(reply_token):
    carousel_columns = [
        CarouselColumn(
            thumbnail_image_url='https://pgw.udn.com.tw/gw/photo.php?u=https://uc.udn.com.tw/photo/2023/09/05/realtime/24829906.jpg&x=0&y=0&sw=0&sh=0&exp=3600',
            title='校外宿舍',
            text='有容學舍',
            actions=[
                MessageAction(label='地址', text='校外宿舍有容學舍地址'),
                MessageAction(label='交通方式', text='校外宿舍有容學舍交通方式'),
                MessageAction(label='住宿費用', text='校外宿舍有容學舍住宿費用'),
            ]
        ),
        CarouselColumn(
            thumbnail_image_url='https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhpH4M35vAgbJ4NHWeQy5JFjmhLEP182srNyTKfrad2r2oAmgIEDp8Bf2jYlmHT-aX0oFEfCbaJuX-F9QddqrZn4tkpfME-P6sWILB2ECkw9JINHkVRgpMfBcnmhAniIkCgmHZ_urVoMmw/s1667/IMG_4232.JPG',
            title='校外宿舍',
            text='泉思學舍',
            actions=[
                MessageAction(label='地址', text='校外宿舍泉思學舍地址'),
                MessageAction(label='交通方式', text='校外宿舍泉思學舍交通方式'),
                MessageAction(label='住宿費用', text='校外宿舍泉思學舍住宿費用'),
            ]
        ),
        CarouselColumn(
            thumbnail_image_url='https://233ca8414a.cbaul-cdnwnd.com/5a4223ad91b3073522caa2d53bc72ce4/200000001-9017d9113a/%E6%9F%9A%E8%8A%B3%E6%A8%93.jpg?ph=233ca8414a',
            title='校內宿舍',
            text='松勁樓，榕華樓，柚芳樓',
            actions=[
                MessageAction(label='地址', text='校內宿舍地址'),
                MessageAction(label='交通方式', text='校內宿舍交通方式'),
                MessageAction(label='住宿費用', text='校內宿舍住宿費用'),
            ]
        )
    ]




    carousel_template = TemplateSendMessage(
        alt_text='Dormitory options',
        template=CarouselTemplate(columns=carousel_columns)
    )




    line_bot_api.reply_message(reply_token, carousel_template)




# 住宿選項函數
def show_dormitory_options(reply_token):
    carousel_columns = [
        CarouselColumn(
            thumbnail_image_url='https://pgw.udn.com.tw/gw/photo.php?u=https://uc.udn.com.tw/photo/2023/09/05/realtime/24829906.jpg&x=0&y=0&sw=0&sh=0&exp=3600',
            title='校外宿舍',
            text='有容學舍',
            actions=[
                MessageAction(label='地址', text='校外宿舍有容學舍地址'),
                MessageAction(label='交通方式', text='校外宿舍有容學舍交通方式'),
                MessageAction(label='住宿費用', text='校外宿舍有容學舍住宿費用'),
            ]
        ),
        CarouselColumn(
            thumbnail_image_url='https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhpH4M35vAgbJ4NHWeQy5JFjmhLEP182srNyTKfrad2r2oAmgIEDp8Bf2jYlmHT-aX0oFEfCbaJuX-F9QddqrZn4tkpfME-P6sWILB2ECkw9JINHkVRgpMfBcnmhAniIkCgmHZ_urVoMmw/s1667/IMG_4232.JPG',
            title='校外宿舍',
            text='泉思學舍',
            actions=[
                MessageAction(label='地址', text='校外宿舍泉思學舍地址'),
                MessageAction(label='交通方式', text='校外宿舍泉思學舍交通方式'),
                MessageAction(label='住宿費用', text='校外宿舍泉思學舍住宿費用'),
            ]
        ),
        CarouselColumn(
            thumbnail_image_url='https://233ca8414a.cbaul-cdnwnd.com/5a4223ad91b3073522caa2d53bc72ce4/200000001-9017d9113a/%E6%9F%9A%E8%8A%B3%E6%A8%93.jpg?ph=233ca8414a',
            title='校內宿舍',
            text='松勁樓，榕華樓，柚芳樓',
            actions=[
                MessageAction(label='地址', text='校內宿舍地址'),
                MessageAction(label='交通方式', text='校內宿舍交通方式'),
                MessageAction(label='住宿費用', text='校內宿舍住宿費用'),
            ]
        )
    ]




    carousel_template = TemplateSendMessage(
        alt_text='Dormitory options',
        template=CarouselTemplate(columns=carousel_columns)
    )




    line_bot_api.reply_message(reply_token, carousel_template)




def handle_dormitory_message(event, user_message):
    if user_message == "校外宿舍有容學舍地址":
        response_text = "台北市萬華區大理街140號"
    elif user_message == "校外宿舍有容學舍交通方式":
        response_text = "捷運：搭乘板南線到捷運龍山寺站，步行約6分鐘即可抵達。"
    elif user_message == "校外宿舍泉思學舍地址":
        response_text = "台北市北投區北投路二段55號"
    elif user_message == "校外宿舍泉思學舍交通方式":
        response_text = "捷運：搭乘淡水信義線到捷運北投站，步行約3分鐘即可抵達。"
    elif user_message == "校內宿舍地址":
        response_text = "台北市士林區臨溪路70號"
    elif user_message == "校內宿舍交通方式":
        response_text = """一、自行駕車
1、中山重慶北路交流道（往士林方向）匝道，經百齡橋直行中正路至雙溪公園，右轉至善路。
2、北二高路線—由堤頂交流道下北二高，往左至內湖路（內湖/大直方向），過自強隧道，直行到至善路左轉。
三、捷運
1、搭乘淡水信義線至捷運士林站，1號出口出站，
往中正路方向轉乘公車304、255、620、小18、小19、557至東吳大學站。
2、搭乘文湖線至捷運劍南路站，往劍潭寺方向出口，轉乘公車620，至東吳大學站。
四、公車
請於台北車站後站之承德路上搭乘304公車至東吳大學站。
請事先購買學生型悠遊卡（捷運公車兩用），
學生公車每段分段點扣費12元；車上投幣每車分段點每人每段15元。
五、計程車
1、台北車站至雙溪校區約250元。
2、士林捷運站至雙溪校區約90元。
3、松山機場至雙溪校區約200元。"""
    elif user_message == "校內宿舍住宿費用":
        response_text = """
榕華樓(女宿)
規格：5人雅房
住宿費：10200元（每人/每學期）
網費：1200元（每人/每學期）
保證金：1,000元
冷氣費用：費用由寢室室友共同分攤




柚芳樓(女宿)
規格：8人雅房
住宿費：10,200元（每人/每學期）
網費：800元（每人/每學期）
保證金：1,000元
冷氣費用：費用由寢室室友共同分攤




松勁樓(男宿)
規格：8人雅房
住宿費：10,200元（每人/每學期）
網費：800元（每人/每學期）
保證金：1,000元
冷氣費用：費用由寢室室友共同分攤
"""
    elif user_message == "校外宿舍泉思學舍住宿費用":
        response_text = """
泉思學舍（每人/每學期）
規格: 1人套房、2人套房、4人套房
住宿費: 72,000元、36,000元、24,000元
網路費: 1,800元、900元、450元
保證金: 3,000元
寢室電費: 寢室設有獨立電表、所有用電與同寢室室友共同分攤
"""
    elif user_message == "校外宿舍有容學舍住宿費用":
        response_text = """
有容學舍（每人/每學期）
規格: 2人套房、4人套房
住宿費: 52,800元、37,200元
網路費: 有需求者付費申請
保證金: 3,000元
寢室電費: 寢室設有獨立電表、所有用電與同寢室室友共同分攤
"""
    else:
        response_text = "無法識別的命令。"




    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_text))


   
if __name__ == "__main__":
    app.run()





