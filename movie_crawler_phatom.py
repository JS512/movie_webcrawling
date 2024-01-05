url = 'http://www.cgv.co.kr/theaters/?areacode=01&theaterCode=0013&date=20240104'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options

import telegram
import asyncio
import secret
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge

from apscheduler.schedulers.blocking import BlockingScheduler
from selenium.webdriver.firefox.options import Options as FirefoxOptions


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
async def send(text, bot) :    
    await bot.sendMessage(chat_id=secret.chat_id, text=text)


def job_function() :
    bot = telegram.Bot(token=secret.token)

    
   
    
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    # driver = webdriver.Firefox(options=options, executable_path=r'C:/workspace/telegram_chatbot/movie_webcrawling/geckodriver.exe')
    

    # 대상 웹 페이지로 이동합니다.

    driver.get(url)

    # iframe의 XPath를 찾아서 해당 iframe으로 전환합니다.
    iframe_xpath = '//iframe[@id="ifrm_movie_time_table"]'  # 실제 웹 페이지의 iframe ID에 맞게 수정
    iframe = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, iframe_xpath))
    )
    # print("222", iframe)
    driver.switch_to.frame(iframe)

    # iframe 내용이 로드될 때까지 대기합니다.
    iframe_content_xpath = '//body'  # 실제 웹 페이지의 iframe 내용에 맞게 수정
    iframe_content = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, iframe_content_xpath))
    ).get_attribute("outerHTML")

    # iframe에서 벗어나 원래의 상위 레벨로 돌아갑니다.
    driver.switch_to.default_content()

    # WebDriver를 종료합니다.
    driver.quit()

    soup = BeautifulSoup(iframe_content, 'html.parser')
    print(soup)
    is_imax_list = soup.select('span.imax')
    imax_name_lst= []
    if len(is_imax_list) > 0 :
        for i in is_imax_list :
            imax = i.find_parent('div', class_='col-times')
            imax_name_lst.append(imax.select_one('div.info-movie > a > strong').text.strip())

        asyncio.run(send(str(imax_name_lst) + " IMAX가 열렸습니다." , bot))
        # sched.pause()
    else :
        asyncio.run(send("열린 IMAX가 없습니다." , bot))


# sched = BlockingScheduler()
# sched.add_job(job_function, 'interval', seconds=30)
# sched.start()
        
job_function()





# url = 'http://www.cgv.co.kr/theaters/?areacode=01&theaterCode=0013&date=20240105'
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup

# # PhantomJS 실행 파일의 경로를 제공해야 합니다.
# driver = None
# try :
#     phantomjs_path = 'C:/workspace/telegram_chatbot/movie_webcrawling/phantomjs-2.1.1-windows/bin/phantomjs.exe'

#     # PhantomJS WebDriver 초기화
#     driver = webdriver.PhantomJS(executable_path=phantomjs_path)

#     # 대상 웹 페이지로 이동합니다.
#     driver.get(url)

#     # iframe의 XPath를 찾아서 해당 iframe으로 전환합니다.
#     iframe_xpath = '//iframe[@id="ifrm_movie_time_table"]'  # 실제 웹 페이지의 iframe ID에 맞게 수정
#     iframe = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, iframe_xpath))
#     )

    
#     soup2 = driver.find_elements_by_xpath('//iframe[@id="ifrm_movie_time_table"]')
#     for WebElement in soup2:
#         elementHTML = WebElement.get_attribute('outerHTML') #gives exact HTML content of the element
#         elementSoup = BeautifulSoup(elementHTML,'html.parser')
#         print(elementSoup)

#     driver.switch_to.frame(iframe)

#     # iframe 내용이 로드될 때까지 대기합니다.
#     iframe_content_xpath = '//html'  # 실제 웹 페이지의 iframe 내용에 맞게 수정
#     iframe_content = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.XPATH, iframe_content_xpath))
#     ).get_attribute("outerHTML")

#     # iframe에서 벗어나 원래의 상위 레벨로 돌아갑니다.
#     driver.switch_to.default_content()

#     # WebDriver를 종료합니다.
#     driver.quit()

#     soup = BeautifulSoup(iframe_content, 'html.parser')
#     # soup2 = BeautifulSoup(iframe, 'html.parser')
#     print(soup)
#     # print(soup2)

# except Exception as e:
#     print(e)
#     driver.save_screenshot('screenshot.png')