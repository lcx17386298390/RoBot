import requests
from bs4 import BeautifulSoup

login_path = 'http://passport2.chaoxing.com/fanyalogin'
data = {
    'fid': -1,
    'uname': f'17757426745',
    'password': f'sc123456',
    'refer': 'https%3A%2F%2Fi.chaoxing.com',
    't': 'false',
    'forbidotherlogin': 0,
    'validate': '',
    'doubleFactorLogin': 0,
    'independentId': 0,
}
session = requests.session()
post_header = session.post(login_path, data=data)
post_hander = BeautifulSoup(session.get('http://i.chaoxing.com/base'),'lxml')
print(post_header)