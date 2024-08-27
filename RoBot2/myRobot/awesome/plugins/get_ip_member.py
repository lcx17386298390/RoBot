import nonebot
import requests


@nonebot.scheduler.scheduled_job('cron', minutes='1', hour='0')
async def get_ip():
    session = requests.session()
    # 登录
    session.post('https://www.siyetian.com/login.html?username=17757426745&password=sc123456')
    # 签到领ip
    session.post('https://www.siyetian.com/member/receive.html')

