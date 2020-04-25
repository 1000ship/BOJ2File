from selenium import webdriver
from bs4 import BeautifulSoup, PageElement

language2format = {
    'Python 3': 'py',
    'Swift': 'swift',
    'C++14': 'cpp',
    'Java': 'java',
    'PyPy3': 'pypy',
    'C': 'c',
    'C++': 'cpp'
}

def getSolvedList ( page_source ):
    bs = BeautifulSoup(page_source, "html.parser")
    success_panel, fail_panel = bs.find_all("div", {"class": "panel"})
    success_body = success_panel.find("div", {"class": "panel-body"})
    success_spans = success_body.find_all("span", {"class", "problem_number"})
    success_numbers = [int(item.text) for item in success_spans]  # 성공한 문제 코드들
    return success_numbers

driver = webdriver.Chrome('driver/chromedriver')
driver.get( "https://www.acmicpc.net/login?next=%2F" )

# I think BOJ blocked auto-login, so you should login manually
# driver.find_element_by_name("login_user_id").send_keys( boj_id )
# driver.find_element_by_name("login_password").send_keys( boj_pw )
# driver.find_element_by_id("submit_button").click()

input("Input anything after login success.")

user_id = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[1]/div/ul/li[1]/a").text.strip()
driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[1]/div/ul/li[1]/a").click()
solved_list = getSolvedList( driver.page_source )

def getSourceDict ( code ):
    driver.get(f"https://www.acmicpc.net/status?problem_id={code}&user_id={user_id}&language_id=-1&result_id=4&from_mine=1")
    boj_table = driver.find_element_by_xpath('//*[@id="status-table"]/tbody')
    boj_trs = boj_table.find_elements_by_tag_name("tr")
    sourceDict = {}
    for tr in boj_trs:
        data = [item.text for item in tr.find_elements_by_tag_name("td")]
        # ['18892117', 'cjstjdgur123', '1000', '맞았습니다!!', '29284', '56', 'Python 3 / 수정', '44', '21일 전']
        isSuccess = bool(data[3].count("맞았습니다"))
        language = data[6].split(" / ")[0]
        source_id = data[0]
        if isSuccess and language not in sourceDict:
            sourceDict[ language ] = source_id
    return sourceDict

def getSourceCode ( source_id ):
    driver.get( f"https://www.acmicpc.net/source/{source_id}" );
    return driver.execute_script( "return OnlineJudgeCodeMirror.get('source').getValue();" )

def saveSourceCode ( id, language, code ):
    format = ""
    if language in language2format:
        format = language2format[ language ]
    else:
        format = language2format[ language ] = input(f"{language}에 대한 확장자명 정의 필요: ")
        print( language2format )
    file = open(f"solved_files/{id}.{format}", "w")
    file.write( code )
    file.close()

# do mining from here
for solved_id in solved_list:
    source_dict = getSourceDict( solved_id )
    for language in source_dict:
        source_code = getSourceCode( source_dict[ language ] )
        saveSourceCode( solved_id, language, source_code )