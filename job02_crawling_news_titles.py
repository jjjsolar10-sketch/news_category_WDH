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
options.add_argument('headless')    # 메모리 상에서는 브라우저가 동작 중이나 화면에는 띄워지지 않게 하는 옵션

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
my_section = 2
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
# 1. 반복문 개선: 클릭 사이의 대기 시간 추가
while True:
    try:
        # 더보기 버튼의 정확한 선택자 사용 (CSS_SELECTOR가 더 안정적일 수 있음)
        # .section_more_inner 는 네이버 뉴스 더보기 버튼의 공통 클래스입니다.
        button = driver.find_element(By.CSS_SELECTOR, ".section_more_inner._CONTENT_LIST_LOAD_MORE_BUTTON")

        # 버튼이 있는 위치로 스크롤 (화면에 보여야 클릭이 잘 됨)
        driver.execute_script("arguments[0].scrollIntoView();", button)
        time.sleep(0.5)

        button.click()
        print("더보기 클릭 중...")

        # 중요: 서버에서 데이터를 받아올 시간(최소 1~1.5초)을 줍니다.
        time.sleep(1.5)
    except:
        print("더 이상 더보기 버튼이 없거나 로딩이 끝났습니다.")
        break

# 2. 제목 추출 (클래스명 확인)
# 'sa_text_strong' 대신 'sa_text_title'을 사용하는 경우가 더 정확할 수 있습니다.
title_tags = driver.find_elements(By.CLASS_NAME, 'sa_text_strong')

titles = []
for title_tag in title_tags:
    titles.append(title_tag.text)
df_titles = pd.DataFrame(titles, columns=['title'])
df_titles['category'] = category[my_section]  # 섹션별로 카테고리 값 변경
print(df_titles.head())
df_titles.info()
df_titles.to_csv('news_titles_{}.csv'.format(category[my_section]), index=False)
