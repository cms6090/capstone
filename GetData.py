from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def Crawling(username, password) -> dict:
    filter = ['이수영역', '년도학기', '교과목명', '학점', '성적', '구이수']

    # 웹 드라이버 경로 설정
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) # 크롬 버전에 따른 chromedriver.exe를 설치해야 하므로 해당 버전에 맞는 chromedriver 설치
    main_window_handle = driver.current_window_handle

    # 로그인 페이지로 이동
    login_url = 'https://www.daejin.ac.kr/subLogin/daejin/view.do?layout=unknown'
    driver.get(login_url)

    # 로그인 폼 채우기
    username_input = driver.find_element(By.ID, 'userId')
    password_input = driver.find_element(By.ID, 'userPwd')

    username_input.send_keys(username)
    password_input.send_keys(password)

    # 로그인 버튼 클릭
    login_button = driver.find_element(By.CLASS_NAME, '_loginSubmit')
    login_button.click()

    time.sleep(1)

    if 'message.do' in driver.current_url:
        driver.find_element(By.XPATH, '/html/body/div[1]/form/div/div/div[2]/div/span/input').click()

    url = 'https://dreams2.daejin.ac.kr/sugang/LinkPortal.jsp'  # 이동하려는 URL로 수정하세요
    driver.get(url)

    time.sleep(1)
    new_window_handle = None
    for handle in driver.window_handles:
        if handle != main_window_handle:
            new_window_handle = handle
            break

    if new_window_handle:
        driver.switch_to.window(new_window_handle)
        driver.close()  # 새로운 창 닫기
        driver.switch_to.window(main_window_handle)

    #테스트 시작
    driver.switch_to.frame('BBF')
    driver.switch_to.frame('LF')
    driver.find_element(By.ID, 'MFX8').click()

    element = driver.find_element(By.ID, 'MFX9')
    element.find_element(By.TAG_NAME, 'a').click()

    #이수구분별 성적조회 및 출력클릭
    driver.switch_to.parent_frame()
    driver.switch_to.frame('RF')
    driver.find_element(By.XPATH, '/html/body/table/tbody/tr/td/table[2]/tbody/tr[3]/td[1]/a').click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "crownix-absolute-100").click() # 화면 세로 맞춤
    driver.find_element(By.ID, "crownix-toolbar-height").click()

    # m2soft-crownix-text ID를 갖는 DIV 요소 찾기
    time.sleep(1)
    div_element = driver.find_element(By.ID, 'm2soft-crownix-text')

    # DIV 요소의 모든 하위 요소들 가져오기
    sub_elements = div_element.find_elements(By.XPATH, ".//*")

    Course = {}
    Course['교필'] = {'학점' : 0, '교과목명' : []}
    Course['교선1'] = {'학점' : 0, '교과목명' : []}
    Course['교선2'] = {'학점' : 0, '교과목명' : []}
    Course['교선3'] = {'학점' : 0, '교과목명' : []}
    Course['교선4'] = {'학점' : 0, '교과목명' : []}
    Course['교선5'] = {'학점' : 0, '교과목명' : []}
    Course['교선6'] = {'학점' : 0, '교과목명' : []}
    Course['교선7'] = {'학점' : 0, '교과목명' : []}
    Course['교선8'] = {'학점' : 0, '교과목명' : []}
    Course['교선8'] = {'학점' : 0, '교과목명' : []}
    Course['전필'] = {'학점' : 0, '교과목명' : []}
    Course['전선'] = {'학점' : 0, '교과목명' : []}
    Course['일선'] = {'학점' : 0, '교과목명' : []}
    Course['부전1'] = {'학점' : 0, '교과목명' : []}
    Course['복전1'] = {'학점' : 0, '교과목명' : []}

    i = 19

    while i < len(sub_elements):
        text = sub_elements[i].text
        if "일선 취득학점 계 : " in text:
            break
        elif ' 계 : ' in text:
            i += 2
        elif text not in filter:
            if text == '부전1' or text != '':
                skip = 7 if text == '부전1' else 6
                
                if len(text) > 2:
                    text = text[0:3]
                Course[text]['학점'] += int(sub_elements[i+4].text)
                Course[text]['교과목명'].append(sub_elements[i+3].text)
                i += skip
            else:
                i += 1
        else:
            i += 1
    return Course
