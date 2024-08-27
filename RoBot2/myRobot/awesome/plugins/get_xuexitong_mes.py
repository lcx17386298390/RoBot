import nonebot
from nonebot import on_command, CommandSession, get_bot
import myRobot.awesome.mycodes.main as myChaoXing
import json
import os

bot = get_bot()


@on_command('作业', aliases=('我的作业', '学习通作业'))
async def get_xuexitong_work(session: CommandSession):
    qqnum = session.ctx['user_id']
    mes = session.current_arg_text.strip()
    username = []
    work_list = await get_work(str(qqnum), username)
    print(work_list)
    send_mes = None
    if work_list is None:
        send_mes = '账号或密码错误，输入指令‘修改账号密码‘以修改'
    else:
        send_mes = '你好  ' + str(username[0]) + '  你的作业如下：\n'
        for name, works in zip(work_list.keys(), work_list.values()):
            send_mes += '       ✰' + name + '\n'
            for i in works:
                send_mes += '    ' + str(works.index(i) + 1) + '、' + i['name'] + '\n           ' + i[
                    'status'] + '\n           ' + i['time'] + '\n'
    await session.send(str(send_mes))


async def get_work(qqnum, username):
    chaoxing = myChaoXing.ChaoXing()
    todo_work = None
    try:
        await chaoxing.check_cookie_file(qqnum, username)
        todo_work = await chaoxing.get_todo_work()
    except Exception:
        todo_work = None
    return todo_work


# @on_command('任务', aliases=('我的任务', '学习通任务'))
# async def get_xuexitong_task_before(session: CommandSession):
#     qqnum = session.ctx['user_id']
#     await get_xuexitong_task(session, str(qqnum))


@on_command('任务', aliases=('我的任务', '学习通任务'))
async def get_xuexitong_task(session: CommandSession):
    qqnum = session.ctx['user_id']
    mes = session.current_arg_text.strip()
    username = []
    task_list = await get_task(str(qqnum), username)
    print(task_list)
    send_mes = ''
    if task_list is None:
        send_mes = '账号或密码错误，输入指令‘修改账号密码‘以修改'
    else:
        send_mes = '你好  ' + str(username[0]) + '  你的任务如下：\n'
        for name, tasks in zip(task_list.keys(), task_list.values()):
            send_mes += '       ✰' + name + '\n'
            for i in tasks:
                if i['time'] == '':
                    i['time'] = '无期限任务'
                send_mes += '    ' + str(tasks.index(i) + 1) + '、' + i['name'] + '\n           ' + i['time'] + '\n'
    await session.send(str(send_mes))


async def get_task(qqnum, username):
    chaoxing = myChaoXing.ChaoXing()
    await chaoxing.check_cookie_file(qqnum, username)
    now_task = await chaoxing.get_now_task()
    return now_task


@on_command('修改账号密码', aliases='创建用户')
async def modify_account(session: CommandSession):
    qqnum = session.ctx['user_id']
    phone = ''
    password = ''
    while not phone:
        phone = (await session.aget(prompt='请输入账号')).strip()
    while not password:
        password = (await session.aget(prompt='请输入密码')).strip()
    text = f'{phone}-{password}'
    with open(f'./awesome/user_account_mes/{qqnum}mes', 'w') as f:
        json.dump(text, f)
    with open(f'./awesome/user_account_mes/{qqnum}mes', 'r') as f:
        usermes = f.read().replace('"', '')
        usermes = usermes.split('-')
        if usermes[0] == phone and usermes[1] == password:
            await session.send('操作成功')
            return
        await session.send('操作不成功，请联系管理员QQ->2948065094')


@on_command('订阅超星提醒', aliases='订阅学习通提醒')
async def subscribe_chaoxing(session: CommandSession):
    qqnum = session.ctx['user_id']
    if not os.path.exists(f'./awesome/user_account_mes/{qqnum}mes'):
        await session.send(f'q{qqnum}未绑定账号，请先绑定')
        phone = ''
        password = ''
        while not phone:
            phone = (await session.aget(prompt='请输入账号')).strip()
        while not password:
            password = (await session.aget(prompt='请输入密码')).strip()
        text = f'{phone}-{password}'
        with open(f'./awesome/user_account_mes/{qqnum}mes', 'w') as f:
            json.dump(text, f)
        with open(f'./awesome/user_account_mes/{qqnum}mes', 'r') as f:
            usermes = f.read().replace('"', '')
            usermes = usermes.split('-')
            if usermes[0] == phone and usermes[1] == password:
                await session.send('绑定成功')
            else:
                await session.send('绑定不成功，请联系管理员QQ->2948065094')

    with open(f'./awesome/user_account_mes/qq_user_list', 'r') as f:
        userqq = f.read().replace('"', '')
        userqq = userqq.split('-')
        for i in userqq:
            if i == str(qqnum):
                await session.send('小主您已经订阅过啦')
                return
        text = f'{qqnum}-'
        with open(f'./awesome/user_account_mes/qq_user_list', 'a') as f:
            f.write(text)
        with open(f'./awesome/user_account_mes/qq_user_list', 'r') as f:
            userqq = f.read().replace('"', '')
            userqq = userqq.split('-')
            if str(userqq[len(userqq) - 2]) == str(qqnum):
                await session.send('订阅成功')
                return
            await session.send('订阅不成功，请联系管理员QQ->2948065094')
