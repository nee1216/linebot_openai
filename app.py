from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, CarouselTemplate, CarouselColumn, MessageAction, FlexSendMessage, QuickReply, QuickReplyButton
import requests
from bs4 import BeautifulSoup

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

def send_carousel_message(event, year):
    # 指定 JSON 文件的 URL
    json_url = f"https://raw.githubusercontent.com/nee1216/linebot_openai/master/112%E8%B3%87%E7%A7%91%E7%B3%BB.json"
    
    # 从 URL 加载 JSON 文件内容
    carousel_message = load_flex_message_from_url(json_url)
    
    # 创建 FlexSendMessage
    flex_message = FlexSendMessage(
        alt_text=f"{year}學年 資科系學分",
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
    elif user_message == "住宿":
        show_dormitory_options(event.reply_token)
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
    elif user_message in ["資料科學系", "資料管理系", "法律系", "化學系", "日文系"]:
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
    elif user_message in ["110學年", "111學年", "112學年"]:
        # 檢查用戶是否選擇了科系
        if user_id in user_choices:
            department = user_choices[user_id]
            if department == "資料科學系":
                send_carousel_message(event, user_message)
            else:
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先選擇資料科學系。"))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請先選擇科系。"))
    elif user_message in ["校外宿舍有容學舍地址", "校外宿舍有容學舍交通方式", "校外宿舍泉思學舍地址", "校外宿舍泉思學舍交通方式", "校內宿舍地址", "校內宿舍交通方式", "校內宿舍住宿費用", "校外宿舍有容學舍住宿費用", "校外宿舍泉思學舍住宿費用"]:
        handle_dormitory_message(event, user_message)
    else:
        # 當使用者消息不是您期待的內容時，發送默認回復
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請輸入正確的命令。")
        )

def load_flex_message_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch JSON from URL: {response.status_code}")

def latest_news():
    try:
        message = ""
        response = requests.get("https://www-news.scu.edu.tw/news-7?page=1")
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.select("div.views-field-title a")

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
