from datetime import datetime
from nonebot import on_command, CommandSession
import myRobot.awesome.plugins.get_xuexitong_mes as chaoxing

import nonebot
import pytz
# from aiocqhttp.exceptions import Error as CQHttpError


@nonebot.scheduler.scheduled_job('cron', hour='*')
async def fun():
    bot = nonebot.get_bot()
    with open(f'./awesome/user_account_mes/qq_user_list', 'r') as f:
        userqq = f.read().replace('"', '')
        userqq = userqq.split('-')
    for i in range(0, len(userqq) - 1):
        username = []
        send_mes = ''
        qqnum = str(userqq[i])
        work_list = await chaoxing.get_work(qqnum, username)
        task_list = await chaoxing.get_task(qqnum, username)
        new_work_list = {}
        new_task_list = {}
        if work_list is None:
            send_mes = '账号或密码错误，输入指令‘修改账号密码‘以修改'
        else:
            for name, works in zip(work_list.keys(), work_list.values()):
                newlist = []
                for work in works:
                    work_time = work['time'].replace('剩余', '').replace('分钟', '')
                    work_time = work_time.split('小时')
                    if int(work_time[0]) == 23 or int(work_time[0]) == 6 or int(work_time[0]) == 3:
                        newlist.append(work)
                if newlist:
                    new_work_list[name] = newlist

            for name, tasks in zip(task_list.keys(), task_list.values()):
                newlist = []
                for task in tasks:
                    task_time = str(task['time']).replace('剩余:', '')
                    if task_time.find('小时') >= 0:
                        task_time = task_time.split('小时')
                        if int(task_time[0]) == 23 or int(task_time[0]) == 6 or int(task_time[0]) == 3:
                            newlist.append(task)
                if newlist:
                    new_task_list[name] = newlist

            send_mes = '     你好 ' + str(username[0]) + '，你有如下即将截止任务&作业：\n' + '--------------作业--------------\n'
            if not new_work_list:
                send_mes += '                      无\n'
            else:
                for name, works in zip(new_work_list.keys(), new_work_list.values()):
                    send_mes += '       ✰' + name + '\n'
                    for j in works:
                        send_mes += '    ' + str(works.index(j) + 1) + '、' + j['name'] + '\n           ' + j[
                            'status'] + '\n           ' + j['time'] + '\n'

            send_mes += '--------------任务-------------\n'
            if not new_task_list:
                send_mes += '                      无\n'
            else:
                for name, tasks in zip(new_task_list.keys(), new_task_list.values()):
                    send_mes += '       ✰' + name + '\n'
                    for j in tasks:
                        send_mes += '    ' + str(tasks.index(j) + 1) + '、' + j['name'] + '\n           ' + j[
                            'status'] + '\n           ' + j['time'] + '\n'

        if not new_work_list and not new_task_list:
            pass
        else:
            await bot.send_private_msg(user_id=str(qqnum), message=send_mes)

    # now = datetime.now(pytz.timezone('Asia/Shanghai'))
    # try:
    #     await bot.send_msg(user_id=2948065094, message=f'现在{now.hour}点整啦！')
    # except CQHttpError:
    #     pass
