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
        driver.get(f"https://m.sbisec.co.jp/oeapw011?type=21&p_cd={r}")
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



import requests

hit_count = 0

for i in range(50):
    if i % 2 == 1:
        ipo_result = driver.find_element(By.XPATH, f"/html/body/table/tbody/tr/td/table[1]/tbody/tr/td/table[1]/tbody/tr[1]/td/div[2]/table[{i}]/tbody/tr/td/table/tbody/tr[5]/td[2]")
        ipo_result_text  = str(ipo_result.text)
        if "当選" in ipo_result_text:
            hit_count +=1

if hit_count > 0:
    def main():
        send_line_notify(f'SBI証券でIPOの当選があります。{hit_count}')

    def send_line_notify(notification_message):
        #LINEに通知する
        line_notify_token = "発行したトークンを入力"
        line_notify_api = 'https://notify-api.line.me/api/notify'
        headers = {'Authorization': f'Bearer {line_notify_token}'}
        data = {'message': f'message: {notification_message}'}
        requests.post(line_notify_api, headers = headers, data = data)

    if __name__ == "__main__":
        main()


driver.quit()