import random
from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message

jrrp = on_keyword(['jrrp', '今日人品', '毛子', '群主', '啥b', '鲨', '尼玛', '你妈', '毛神', '傻', '逼'], priority=50)


@jrrp.handle()
async def jrrp_handle(bot: Bot, event: Event):
    if event.get_user_id() == '1067017428':
        await jrrp.finish(Message(f'[CQ:at,qq={event.get_user_id()}]毛神，我爱你'))
    await jrrp.finish(Message(f'[CQ:at,qq={event.get_user_id()}]鲨臂'))
