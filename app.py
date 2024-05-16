import requests
from bs4 import BeautifulSoup

def fetch_transit_info():
    url = "https://transit.navitime.com/zh-tw/tw/transfer?start=00016389&goal=00022583"
    
    try:
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

    except Exception as e:
        print(f"发生错误: {str(e)}")

# 运行函数
fetch_transit_info()
