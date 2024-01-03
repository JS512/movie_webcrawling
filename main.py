
url = 'http://www.cgv.co.kr/theaters/?areacode=01&theaterCode=0013&date=20240103'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Selenium WebDriver를 초기화합니다. (ChromeDriver 사용 예제)
driver = webdriver.Chrome()

# 대상 웹 페이지로 이동합니다.

driver.get(url)

# iframe의 XPath를 찾아서 해당 iframe으로 전환합니다.
iframe_xpath = '//iframe[@id="ifrm_movie_time_table"]'  # 실제 웹 페이지의 iframe ID에 맞게 수정
iframe = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, iframe_xpath))
)
driver.switch_to.frame(iframe)

# iframe 내용이 로드될 때까지 대기합니다.
iframe_content_xpath = '//body'  # 실제 웹 페이지의 iframe 내용에 맞게 수정
iframe_content = WebDriverWait(driver, 1).until(
    EC.presence_of_element_located((By.XPATH, iframe_content_xpath))
).get_attribute("outerHTML")

# iframe에서 벗어나 원래의 상위 레벨로 돌아갑니다.
driver.switch_to.default_content()

# WebDriver를 종료합니다.
driver.quit()

soup = BeautifulSoup(iframe_content, 'html.parser')
# print(soup)
title_list = soup.select('div.info-movie')
for i in title_list : 
    title = i.select_one("a > strong").text.strip()
    print(title)