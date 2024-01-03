url = 'http://www.cgv.co.kr/theaters/?areacode=01&theaterCode=0013&date=20240103'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import telegram
import asyncio
import secret

from apscheduler.schedulers.blocking import BlockingScheduler


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
async def send(text, bot) :    
    await bot.sendMessage(chat_id=secret.chat_id, text=text)


def job_function() :
    bot = telegram.Bot(token=secret.token)

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

    is_imax_list = soup.select('span.imax')
    imax_name_lst= []
    if len(is_imax_list) > 0 :
        for i in is_imax_list :
            imax = i.find_parent('div', class_='col-times')
            imax_name_lst.append(imax.select_one('div.info-movie > a > strong').text.strip())

        asyncio.run(send(str(imax_name_lst) + " IMAX가 열렸습니다." , bot))
    else :
        asyncio.run(send("열린 IMAX가 없습니다." , bot))


sched = BlockingScheduler()
sched.add_job(job_function, 'interval', seconds=30)
sched.start()