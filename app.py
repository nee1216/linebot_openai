import requests
from bs4 import BeautifulSoup
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, FlexSendMessage

LINE_CHANNEL_ACCESS_TOKEN = "tsGykdGQN1KnwwQWwkkmq7JM0ji0RnYXFa0DBN3sfLVJ4wgcXudGmWpUZst3ZDBHXCL7xp2NhVrR1eDJKdExozjb6DInsSdHeSw1rtrjmz9Bi3Tx/YiI1g4/yGU95a0Jg15MyGM9QFCNdrM2SfU+XQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "0584d0fc476d78024afcd7cbbf8096b4"

# Initialize Line bot API with your credentials
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

def fetch_transit_info():
    url = "https://transit.navitime.com/zh-tw/tw/transfer?start=00016389&goal=00022583"
    transit_info = ""

    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            transit_element_1 = soup.find(id="transit-1")
            transit_element_2 = soup.find(id="transit-2")

            if transit_element_1:
                time_element_1 = transit_element_1.find(class_="time display-inline text-frame")
                if time_element_1:
                    time_text_1 = time_element_1.get_text(strip=True)
                    transit_info += "捷運士林站(中正)-東吳大學:(557)\n"
                    transit_info += time_text_1 + "\n"

            if transit_element_2:
                time_element_2 = transit_element_2.find(class_="time display-inline text-frame")
                if time_element_2:
                    time_text_2 = time_element_2.get_text(strip=True)
                    transit_info += "捷運士林站(中正)-東吳大學:(300)\n"
                    transit_info += time_text_2

            if not transit_info:
                transit_info = "未找到公交信息。"

        else:
            transit_info = f"无法获取页面内容。状态码: {response.status_code}"

    except Exception as e:
        transit_info = f"发生错误: {str(e)}"

    return transit_info

# Handler for Line bot messages
def handle_message(event):
    transit_info = fetch_transit_info()
    flex_message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": "Transit Information", "weight": "bold", "size": "xl"},
                {"type": "text", "text": transit_info}
            ]
        }
    }
    line_bot_api.reply_message(event.reply_token, FlexSendMessage(alt_text="Transit Info", contents=flex_message))

# Run the Line bot
if __name__ == "__main__":
    app.run(debug=True)
