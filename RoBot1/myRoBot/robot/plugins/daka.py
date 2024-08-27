from selenium import webdriver
import datetime
import requests
import json
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

weather = on_command("weather", rule=to_me(), aliases={"疫情打卡"}, priority=5)
date = datetime.date.today()

@weather.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    result = daka()
    mes = "              未打卡人员\n"
    num = 0
    classList = {}
    classPerson = []
    for i in result['list']:
        if i["type"] == "学生" :
            if not i["classroom"] in classList.keys():
                classList[i["classroom"]] = num
                num+=1
                classPerson.append([])
            classPerson[classList[i["classroom"]]].append(i["userRealName"])
    num = 0
    for key,value in classList.items():
        mes+="\n           "+key
        for i in range(13-len(key)):
            mes+="   "
        mes+=str(len(classPerson[value]))+"\n"
        for i in classPerson[value]:
            mes+=i+"\n"
            num+=1
    
    await matcher.send(mes+'\n'+f'共{num}人')

        #     personList.append(i["classroom"],[])
    #         # (f'姓名:{i["userRealName"]}\n年级:{i["grade"]}\n班级:{i["classroom"]}\n电话:{i["phone"]}\n')
    #         mes+=f'姓名:{i["userRealName"]}\n年级:{i["grade"]}\n班级:{i["classroom"]}\n电话:{i["phone"]}\n\n'
    # await matcher.send(mes+'\n'+f'共{result["total"]}人')
    # plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    # if plain_text:
    #     matcher.set_arg("city", args)  # 如果用户发送了参数则直接赋值

# @weather.got("city", prompt="你想查询哪个城市的天气呢？")
# async def handle_city(city: Message = Arg(), city_name: str = ArgPlainText("city")):
    # if city_name not in ["北京", "上海"]:  # 如果参数不符合要求，则提示用户重新输入
    #     # 可以使用平台的 Message 类直接构造模板消息
    #     await weather.reject(city.template("你想查询的城市 {city} 暂不支持，请重新输入！"))

    # city_weather = await get_weather(city_name)
    # await weather.finish(city_weather)


# 在这里编写获取天气信息的函数
# async def get_weather(city: str) -> str:
#     return f"{city}的天气是..."


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
                    "'classroom': '', 'searchCheckDate': '"+str(date)+"', 'checkOrNotOnThatDay': '0'}",
        'limit': '300'
    }
    session = requests.session()
    url = 'https://xf.zocedu.com/'
    driver = webdriver.PhantomJS(executable_path=r'C:/Users/lcx17/Desktop/phantomjs-2.1.1-windows/phantomjs-2.1.1-windows/bin/phantomjs.exe')
    driver.get(url + 'login')
    driver.find_element_by_name('accountId').send_keys('hgsyjsjxy')
    driver.find_element_by_name('pwd').send_keys('jsj889889')
    driver.find_element_by_id('login-btn').click()
    driver.get('https://mps.zocedu.com:683/wcs-uc/user')
    header['Cookie'] = 'JSESSIONID=' + driver.get_cookie('JSESSIONID')['value']
    res = session.post('https://mps.zocedu.com:683/wcs-uc/statHealthCheck/data', data=data, headers=header)
    if res.status_code == 200:
        result=res.json()
        return result
        # for i in result['list']:
        #     print(f'姓名:{i["userRealName"]}\n年级:{i["grade"]}\n班级:{i["classroom"]}\n电话:{i["phone"]}\n')
        # print(f'共{result["total"]}人')
    else:
        print(res.text)