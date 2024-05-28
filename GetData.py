from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = DesiredCapabilities.CHROME
caps["pageLoadStrategy"] = "none"

def ChromeSetup():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-images')
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-popup-blocking")

    return options

def closepopup(driver):
    main = driver.window_handles
    for i in main:
        if i != main[0]:
            driver.switch_to.window(i)
            driver.close()

    driver.switch_to.window(main[0])

def crawl_consulting(username, password):
    driver = webdriver.Chrome(options = ChromeSetup()) # chromedriver 설치 안해도 ㄱㅊ

    # 트윈 페이지로 이동
    twin_url = 'https://together.daejin.ac.kr/clientMain/a/t/main.do'
    driver.get(twin_url)

    closepopup(driver)

    driver.find_element(By.CLASS_NAME, 'btn_log.btn_login').click()
    time.sleep(1)
    # 로그인 폼 채우기
    username_input = driver.find_element(By.ID, 'userId')
    password_input = driver.find_element(By.ID, 'userPw')

    username_input.send_keys(username)
    password_input.send_keys(password)
    driver.find_element(By.ID, 'loginBtnStd').click()
    closepopup(driver)


    driver.find_element(By.CLASS_NAME, 'my_link.status').click()
    driver.find_element(By.ID, 'cns').click()
    time.sleep(1)

    consulting_total = driver.find_element(By.ID, 'pfcCnsCnt').text

    consulting_detail = {}
    consulting_detail['1학기'] = {'1학년' : 0, '2학년' : 0, '3학년' : 0, '4학년' : 0}
    consulting_detail['2학기'] = {'1학년' : 0, '2학년' : 0, '3학년' : 0, '4학년' : 0}

    for i in range(1,3):
        for j in range(1,5):
            link = 'term'+str(i)+'_'+str(j)
            consulting_detail[str(i)+'학기'][str(j)+'학년'] = driver.find_element(By.ID, link).text
    driver.quit()
    return consulting_total, consulting_detail

def crawl_object(username, password):
    filter = ['이수영역', '년도학기', '교과목명', '학점', '성적', '구이수']

    driver = webdriver.Chrome(options = ChromeSetup()) # chromedriver 설치 안해도 ㄱㅊ
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
    closepopup(driver)

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
    Course['전필'] = {'학점' : 0, '교과목명' : []}
    Course['전선'] = {'학점' : 0, '교과목명' : []}
    Course['일선'] = {'학점' : 0, '교과목명' : []}

    i = 19

    while i < len(sub_elements):
        text = sub_elements[i].text
        if '복전1' in text and '복전1' not in Course:
            Course['복전1'] = {'학점' : 0, '교과목명' : []}
        if '부전1' in text and '부전1' not in Course:
            Course['부전1'] = {'학점' : 0, '교과목명' : []}
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
    
    require_credit_result = require_credit(Course, sub_elements)
    require_cultural_result = require_cultural(Course, sub_elements)

    driver.quit()
    return Course, require_credit_result, require_cultural_result

def crawling_main(user_id, password):
    with ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(crawl_object, user_id, password)
        future2 = executor.submit(crawl_consulting, user_id, password)

        # 결과를 변수에 저장
        Course, require_credit, require_cultural = future1.result()
        consulting_total, consulting_detail = future2.result()

    return Course, require_credit, require_cultural, consulting_total, consulting_detail

def require_credit(Course, sub_elements):
    # 초기 설정
    Require = {
        '졸업학점': {'기준': 0, '취득': 0},
        '졸업평점평균': {'기준': 0, '취득': 0},
        '교필': {'기준': 0, '취득': 0},
        '교선': {'기준': 0, '취득': 0},
        '전기': {'기준': 0, '취득': 0},
        '전필': {'기준': 0, '취득': 0},
        '전선': {'기준': 0, '취득': 0},
    }

    for key, value in Course.items():
        if '복전1' in key:
            Require['복전1'] = {'기준': 0, '취득': 0}

    # '기준'과 '취득' 값 찾기 및 업데이트
    for offset in ['기준', '취득']:
        keyword = '기 준' if offset == '기준' else '취 득'
        for i in range(len(sub_elements) - 100, len(sub_elements)):
            if keyword in sub_elements[i].text:
                start_index = i + 1
                break

        keys = ['졸업학점', '졸업평점평균', '교필', '교선', '전기', '전필', '전선']
        for idx, key in enumerate(keys):
            Require[key][offset] = sub_elements[start_index + idx].text

        basic = int(Require['전기']['기준'])
        essential = int(Require['전필']['기준'])
        Require['전선']['기준'] = str(63 - basic - essential)

        if '복전1' in Course:
            if '복전1' not in Require:
                Require['복전1'] = {'기준': 0, '취득': 0}
            Require['전선']['기준'] = str(42 - basic - essential) if offset == '기준' else Require['전선']['기준']
            Require['복전1'][offset] = sub_elements[start_index + 6 if offset == '취득' else 6].text

    return Require

def require_cultural(Course, sub_elements):
    for i in range(len(sub_elements)-50, len(sub_elements)):
        text = sub_elements[i].text
        if "기 준" in text:
            start = i+1
        if "취 득" in text:
            end = i
            break

    # 필요한 이수 영역 목록을 담을 딕셔너리 초기화
    Require_cultural = {}
    # 추출한 j 값을 사용하여 교선 영역에 대한 정보를 딕셔너리에 저장

    j = 1
    for i in range(start, end):
        Require_cultural["교선" + str(j)] = {'기준': sub_elements[i].text, '취득' : Course["교선"+str(j)]['학점']}
        j += 1
    
    return Require_cultural