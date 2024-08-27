import myRobot.awesome.mycodes.main2 as test
from nonebot import on_command, CommandSession


@on_command('测试')
async def my_test_fun(session: CommandSession):
    text = test.get_baidu_api()
    print(test)
    await session.send(text)
