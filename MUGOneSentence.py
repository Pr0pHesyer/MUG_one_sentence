import random
import json
import os
import requests

from hoshino import Service
from hoshino.typing import MessageSegment, CQEvent

sv = Service('音游一言')

# 常量
url = 'http://pgmcloud.tk:8080/webdav/post.json'
headers = {"Content-Type": "application/json"}

@sv.on_fullmatch(("音游一言"))
async def random_post(bot, ev: CQEvent):
    # 获取json数据
    mos = requests.get(url).json().get('post')
    # 随机选取数组中的一个对象
    randomPost = random.choice(mos)
    await bot.send(ev,randomPost)

@sv.on_prefix('提交音游一言')
async def random_post(bot, ev: CQEvent):
    try:
        # 获取json数据
        nmos = requests.get(url).json().get('post')
        # 新数据
        newSentence: str = ev.message.extract_plain_text().strip()
        # 写入至数组
        nmos.append(newSentence)
        # 新对象
        nr = {'post':nmos}
        # put
        response = requests.put(url, data=json.dumps(nr,ensure_ascii=False, indent=2).encode('utf-8'), headers=headers)
        # 发送成功消息
        await bot.send(ev,'提交成功')
    except:
        await bot.send(ev,'提交失败')
