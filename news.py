from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
import time

options = webdriver.ChromeOptions()
service = ChromeService(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

while True:
    try:
        driver.get("https://www-news.scu.edu.tw/news-7?page=1")
        time.sleep(5)
        tbody = driver.find_element(By.XPATH, "//tbody")
        
        links = tbody.find_elements(By.TAG_NAME, "a")
        
        for link in links:
            print("校園頭條:", link.text)
            print("連結:", link.get_attribute("href"))
            
    except Exception as e:
            print("發生錯誤:", str(e))
        
    print("---------------------------------------------------------------------------------------")

driver.close()
