# webdriver 사용 예제
#
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'IT']

options = ChromeOptions()
options.add_argument('lang=ko_KR')
# options.add_argument('headless')    # 메모리 상에서는 브라우저가 동작 중이나 화면에는 띄워지지 않게 하는 옵션

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
my_section = 0
url = "https://news.naver.com/section/10{}".format(my_section) # 100(Politics), 101(Economic), 102(Social), 103(Culture), 104(World), 105(IT)
driver.get(url)
time.sleep(0.5) # browser 로딩 시간 확보

# //*[@id="newsct"]/div[4]/div/div[2] # X-path : 특정 id부터 hierarchy 참조 # / 표시 : 하위 tag 를 참조할 때 사용.
# /html/body/div/div[2]/div[2]/div[2]/div[4]/div/div[2] # full X-path : 전체 tag hierarchy 보기

# 버튼 클릭 driver
# for i in range(5):
#     time.sleep(0.5)
#     button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'
#     driver.find_element(By.XPATH, button_xpath).click()
# time.sleep(5)
while True:
    try:
        button_xpath = '//*[@id="newsct"]/div[4]/div/div[2]'
        driver.find_element(By.XPATH, button_xpath).click()
    except:
        break

time.sleep(0.5)
title_tags = driver.find_elements(By.CLASS_NAME, 'sa_text_strong')

titles = []
for title_tag in title_tags:
    titles.append(title_tag.text)
df_titles = pd.DataFrame(titles, columns=['title'])
df_titles['category'] = category[my_section]  # 섹션별로 카테고리 값 변경
print(df_titles.head())
df_titles.info()
df_titles.to_csv('news_titles_{}.csv'.format(category[my_section]), index=False)
