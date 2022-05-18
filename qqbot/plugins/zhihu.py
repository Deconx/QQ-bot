# -*- coding: utf-8 -*-
import random

from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
import time
import requests


zhihuColumn1 = "c_1480603406519238656"
zhihuColumn2 = "c_1502374640542023680"
URL1 = "https://www.zhihu.com/api/v4/columns/" + zhihuColumn1 + "/items"
URL2 = "https://www.zhihu.com/api/v4/columns/" + zhihuColumn2 + "/items"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"}


# 输入URL,得到JSON数据
def getJSON(url):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()  # 响应状态码,出错则抛出异常
        r.encoding = r.apparent_encoding
        return r.json()
    except Exception as ex:
        print(type(ex))
        time.sleep(10)
        return getJSON(url)


# 输入文章总数,输出所有文章标题和链接的CSV文件
def process(total, url):
    num = 0  # 文章编号
    posts = []
    for offset in range(0, total, 10):
        jsonData = getJSON(url.format(offset))
        items = jsonData["data"]
        for item in items:
            num = num + 1
            posts.append([num, item["title"], item["url"]])
    return posts
jsonData1 = getJSON(URL1.format(0))
posts1 = process(jsonData1["paging"]["totals"], URL1)

jsonData2 = getJSON(URL2.format(0))
posts2 = process(jsonData2["paging"]["totals"], URL2)

posts = posts1 + posts2

mes = []
index = random.randint(0, 10)
for i in range(0, len(posts)):
    mes += [f'第{str(i)}篇：{posts[i][1]}\n{posts[i][2]}']
print(mes)

zhihu = on_keyword(['知乎', 'cmu', 'csapp', 'mit', '操作系统', '考研', '博客'], priority=20)
@zhihu.handle()
async def zhihu_handle(bot: Bot, event: Event):
    jsonData1 = getJSON(URL1.format(0))
    posts1 = process(jsonData1["paging"]["totals"], URL1)

    jsonData2 = getJSON(URL2.format(0))
    posts2 = process(jsonData2["paging"]["totals"], URL2)

    posts = posts1 + posts2
    mes = []
    index = random.randint(0, len(posts))
    for i in range(0, len(posts)):
        mes += [f'第{str(i)}篇：{posts[i][1]}\n{posts[i][2]}']
    await zhihu.finish(message=Message(f'毛神知乎随机推荐\n {mes[index]}'))
