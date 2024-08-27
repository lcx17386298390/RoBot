import nonebot
from nonebot import on_command, CommandSession


@on_command('usage', aliases=['使用帮助', '帮助', '使用方法'])
async def _(session: CommandSession):
    # 获取设置了名称的插件列表
    # plugins = list(filter(lambda p: p.name, nonebot.get_loaded_plugins()))
    rule = {
        '创建用户': '绑定您的学习通账号密码',
        '修改账号密码': '修改您的学习通账号密码',
        '订阅超星提醒': '订阅bot的任务&作业临期截止提醒功能',
        '我的作业': '获取超星学习通您未完成的作业(已完成的不在内)',
        '我的任务': '获取超星学习通您正在进行的任务(正在进行的，完成的也算)',
        '注': '有问题请联系管理员Q=>2948065094'
    }

    arg = session.current_arg_text.strip().lower()
    if not arg:
        # 如果用户没有发送参数，则发送功能列表
        await session.send(
            '我现在支持的功能有：\n\n' + '\n'.join(f'{name}：{value}\n' for name, value in zip(rule.keys(), rule.values())))
        return

    # # 如果发了参数则发送相应命令的使用帮助
    # for p in plugins:
    #     if p.name.lower() == arg:
    #         await session.send(p.usage)
