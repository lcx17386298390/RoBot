# coding=utf-8
import requests


def get_baidu_api():
    session = requests.session()
    text = session.get("http://www.baidu.com")
    text.encoding = 'utf-8'
    print(text.text)
    return str(text.text)
