from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import re
from selenium.webdriver.chrome.options import Options

#ログイン情報
uid = "***"
pw = "***"
suryo = 100
#取引パスワード
trpw = "***"

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)

url = 'https://www.sbisec.co.jp/ETGate'
driver.get(url)

driver.find_element(By.NAME, "user_id").send_keys(uid)
driver.find_element(By.NAME, "user_password").send_keys(pw)

sleep(3)

driver.find_element(By.NAME, "ACT_login").click()

sleep(3)

driver.get("https://m.sbisec.co.jp/oeliw011?type=21")
text_top = driver.page_source

#証券コードで絞る
results = re.findall("（(\d{4})）",text_top)
for r in results:
    ipo_url = "/oeapw011?type=21&amp;p_cd=%s" % r
    if (ipo_url in text_top):
        driver.get("https://m.sbisec.co.jp/oeapw011?type=21&p_cd=%s" % r)
        text_r = driver.page_source
        if ("申込受付期間外" in text_r) or ("お申し込み済み" in text_r):
            continue
        else:
        #IPO注文
        driver.find_element(By.NAME, "suryo").send_keys(100)
        driver.find_element(By.ID, "strPriceRadio").click()
        driver.find_element(By.ID, "ipoRadio1").click()

        driver.find_element(By.NAME, "tr_pass").send_keys("trpw")
        driver.find_element(By.NAME, "order_kakunin").click()
        sleep(2)
        driver.find_element(By.NAME, "order_btn").click()
        sleep(3)


driver.quit()