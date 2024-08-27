# coding=utf-8

# import js2py
# from js2py import require
#
# with open("myTest.js", 'r', encoding='utf8') as f:
#     js = js2py.EvalJs()
#     js.execute(f.read())
#     print(js.s)
#     # varr = js.encryptByDES('123456', 'u2oh6Vu^HWe40fj')


import requests
from bs4 import BeautifulSoup

params = {
    'validate': '',
    'uname': '17757426745',
    't': 'false',
    'password': 'sc123456',
    'independentId': 0,
    'forbidotherlogin': 0,
    'fid': -1,
    'doubleFactorLogin': 0,
    'refer': 'http%3A%2F%2Fi.chaoxing.com'

}
session = requests.session()
response = session.post('http://passport2.chaoxing.com/fanyalogin', params=params)

# response.encoding = 'utf-8'
print(response.text)
print(response.headers)

classListMes = session.get(
    'http://mooc2-ans.chaoxing.com/mooc2-ans/visit/courses/list?v=1681717266508&rss=1&start=0&size=500&catalogId=0&superstarClass=0&searchname=')

print(classListMes.text)
print('-----------------------')
classListMesText = classListMes.text

# suanfaClass = session.get(
# 'http://mooc1.chaoxing.com/visit/stucoursemiddle?courseid=233033649&amp')

soup = BeautifulSoup(classListMesText, 'lxml')
div_list = soup.find_all("ul", attrs={"class": "course-list"})
div_list = soup.find_all("div", attrs={"course-info"})
print(div_list)
print('-----------')




# encTest = session.get(
#     'http://mooc1.chaoxing.com/visit/stucoursemiddle?courseid=217596161&clazzid=72067887&cpi=199759862&ismooc2=1')
# print(encTest.text)

# suanfaClass = session.get(
# 'http://mooc1.chaoxing.com/visit/stucoursemiddle?courseid=233033649&amp')
# print(suanfaClass.text)



