from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import time

options = webdriver.ChromeOptions()
service = ChromeService(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

try:
    while True:
        driver.get("https://transit.navitime.com/zh-tw/tw/transfer?start=00016389&goal=00022583") 
        driver.maximize_window()
        driver.refresh()
        time.sleep(3) 

        table_element = driver.find_element(By.ID, "transit-1")
        table_text = table_element.text
        print("捷運士林站(中正)-東吳大學:")
        print(table_text)

        table_element = driver.find_element(By.ID, "transit-2")
        table_text = table_element.text
        print(" ")
        print(table_text)

        time.sleep(5)
        print("---------------------------------------------------------------------------------------")

except KeyboardInterrupt:
    print("程式被用戶中斷.")
except Exception as e:
    print("發生錯誤:", str(e))
finally:
    driver.close()
