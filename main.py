from selenium import webdriver
from bs4 import BeautifulSoup, PageElement

key = open("me.key", "r")
boj_id = key.readline().strip()
boj_pw = key.readline().strip()
key.close()

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
# driver.find_element_by_name("login_password").send_keys( boj_id )
# driver.find_element_by_id("submit_button").click()

input("Input anything after login success.")

user_id = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[1]/div/ul/li[1]/a").text.strip()
print(user_id)

driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[1]/div/ul/li[1]/a").click()
solved_list = getSolvedList( driver.page_source )
print( solved_list )

def getMySourceURL ( code, user_id ):
    return f"https://www.acmicpc.net/status?problem_id={code}&user_id={user_id}&language_id=-1&result_id=4&from_mine=1"

def getSourceURL ( source_id ):
    return f"https://www.acmicpc.net/source/{source_id}"

# do mining from here
driver.get( getSourceURL( 18892117 ) )
source_code = driver.execute_script( "return OnlineJudgeCodeMirror.get('source').getValue();" )
print( source_code )
