import csv
import time
from openpyxl import Workbook
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def get_page():

    # 开启无头模式
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    # browser = webdriver.Chrome(chrome_options=chrome_options)
    # 非无头模式
    browser = webdriver.Chrome()
    browser.get('http://60.205.171.40/#/login')
    account = 'heyuntian'
    password = 'heyuntian'

    # 加载等待登录页面
    locatorLogin = (By.TAG_NAME, "button")
    try:
        WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locatorLogin))
        print("The login page is loaded")
        input1 = browser.find_element_by_xpath('//*[@id="app"]/section/div/div/div/form/div[1]/div/div/input').send_keys(
            '{}'.format(account))
        input2 = browser.find_element_by_xpath('//*[@id="app"]/section/div/div/div/form/div[2]/div/div/input').send_keys(
            '{}'.format(password))
    except:
        print("Login page loading error")


    browser.find_element_by_xpath('//*[@id="app"]/section/div/div/div/form/div[3]/div/button').click()
    browser.implicitly_wait(10)
    browser.find_element_by_xpath('//*[@id="app"]/section/section/aside/ul/li[1]/div').click()
    browser.implicitly_wait(2)
    browser.find_element_by_xpath('//*[@id="app"]/section/section/aside/ul/li[1]/ul/li/ul/li[3]').click()
    time.sleep(2)

    # 翻页
    # browser.find_element_by_class_name('btn-next').click()

    task_infos = browser.find_elements_by_class_name('el-table__row')
    for ti in task_infos:
        # if "已领取" in ti.text:
        button = ti.find_element_by_class_name('el-table__expand-icon ')
        button.click()

    time.sleep(2)
    pagesource = browser.page_source
    # browser.close()
    return pagesource

def get_data(pagesource):
    soup = BeautifulSoup((pagesource), "lxml")
    tasks = soup.find_all(attrs={'class': 'el-table__row'})
    groups = soup.find_all(attrs={'class': 'el-table__expanded-cell'})

    # print(tasks[1])
    # group = groups[0].find_next('span')
    # print(group.string)

    items = []
    curtime = time.strftime('%Y%m%d', time.localtime(time.time()))
    author = "hyt"

    for task in tasks:
        if task.find(class_=('el-table_2_column_13 ')) != None:
            name = str(task.find(class_=('el-table_2_column_13 ')).string)
            url = str(task.find(class_=('el-table_2_column_15 ')).string)
            msg = str(task.find(class_=('el-table_2_column_16 ')).string)
            items.append([name, msg, url, author, curtime])
    for group, item in zip(groups, items):
        gname = str(group.find_next('span').string)
        item.insert(1, gname)

    print(items)
    return items

# 存入excel
def save_as_xl(items):
    wb = Workbook()
    ws = wb.active
    for row in items:
        ws.append(row)
    wb.save("taskerror.xlsx")


# 存入csv
def save_as_csv(items):
    with open('taskerror.csv', 'w+', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(items)


def run():
    pagesource = get_page()
    items = get_data(pagesource)
    save_as_xl(items)
    # save_as_csv(items)

if __name__ == "__main__":
    run()






