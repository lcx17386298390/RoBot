from csv import unregister_dialect
import datetime
import datetime
import requests
import nonebot
from email import message
from nonebot import require
from selenium import webdriver

he = require("nonebot_plugin_apscheduler").scheduler
date = datetime.date.today()


@he.scheduled_job("cron", hour="10-21/6", minute=46, id="test")
async def test():
    (bot,) = nonebot.get_bots().values()
    mes = await zhengli()
    await bot.send_msg(
        message_type="group",
        group_id=828393576,
        # int（）中填写qq号码
        message=mes

    )


async def zhengli():
    result = daka()
    mes = "                未打卡人员\n"
    num = 0
    totalNum = 0
    classList = {}
    classPerson = []
    for i in result['list']:
        if i["type"] == "学生":
            if not i["classroom"] in classList.keys():
                classList[i["classroom"]] = num
                num += 1
                classPerson.append([])
            classPerson[classList[i["classroom"]]].append(i["userRealName"])
    num = 0
    for key, value in classList.items():
        mes += "\n           " + key
        for i in range(13 - len(key)):
            mes += "   "
        mes += str(len(classPerson[value])) + "\n"
        for i in classPerson[value]:
            if num > 250:
                await longSend(mes)
                mes = ""
                num = 0
            mes += i + "\n"
            num += 1
            totalNum += 1
    mes += '\n' + f'共{totalNum}人'
    return mes
    # await matcher.send(mes+'\n'+f'共{num}人')


async def longSend(mes):
    (bot,) = nonebot.get_bots().values()
    await bot.send_msg(
        message_type="group",
        group_id=828393576,
        message=mes
    )


def daka():
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Host': 'xf.zocedu.com',
        'Referer': 'https://xf.zocedu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/95.0.4638.69 Safari/537.36',
    }
    data = {
        'offset': '1',
        'condition': "{'studentNo': '', 'college': '', 'major': '', 'type': '', 'schoolArea': '', 'grade': '',"
                     "'classroom': '', 'searchCheckDate': '" + str(date) + "', 'checkOrNotOnThatDay': '0'}",
        'limit': '700'
    }
    session = requests.session()
    url = 'https://xf.zocedu.com/'
    driver = webdriver.PhantomJS(
        executable_path=r'C:/Users/lcx17/Desktop/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs.exe')
    driver.get(url + 'login')
    driver.find_element_by_name('accountId').send_keys('hgsyjsjxy')
    driver.find_element_by_name('pwd').send_keys('jsj889889')
    driver.find_element_by_id('login-btn').click()
    driver.get('https://mps.zocedu.com:683/wcs-uc/user')
    header['Cookie'] = 'JSESSIONID=' + driver.get_cookie('JSESSIONID')['value']
    res = session.post('https://mps.zocedu.com:683/wcs-uc/statHealthCheck/data', data=data, headers=header)
    if res.status_code == 200:
        result = res.json()
        return result
        # for i in result['list']:
        #     print(f'姓名:{i["userRealName"]}\n年级:{i["grade"]}\n班级:{i["classroom"]}\n电话:{i["phone"]}\n')
        # print(f'共{result["total"]}人')
    else:
        print(res.text)
