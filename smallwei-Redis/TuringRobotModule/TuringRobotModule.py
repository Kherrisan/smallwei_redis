# -*- coding: utf-8 -*-
# 图灵机器人的模块。

import json
import re

import requests

import Message
from config import TURING_API_URL, TURING_KEY
from BaseProcessModule import *
from Sender import *
from Logger import log


class TuringRobotModule(BaseProcessModule):
    name = "TuringRobotModule"

    @staticmethod
    def process(message):

        try:
            if message.getSubType() == 1:
                rtn = requests.post(TURING_API_URL, data=json.dumps(
                    {"key": TURING_KEY, "info": message.getContent(),
                     "uesrid": message.getPersonQQ()}))
                message.setContent(json.loads(rtn.text)["text"])
                log(moduleName=TuringRobotModule.name,content=message.getContent()+" "+str(message.getPersonQQ()))
                send(message, True)
            elif message.getSubType() == 2 or message.getSubType() == 3:  # 如果是群或讨论组消息，则只通过图灵机器人回应at小微的消息。
                res = re.search(r"^\[CQ:at,qq=([0-9]+)\]", message.getContent())
                if res and (res.group(1) == str(SMALLWEI_QQ) or res.group(1)==str(SMALLWEI2016_QQ)):
                    rtn = requests.post(TURING_API_URL, data=json.dumps(
                        {"key": TURING_KEY, "info": message.getContent()[len(res.group(0)):],  # 实际的有意义的聊天内容需要去除at小微的部分。
                         "uesrid": str(message.getGroupQQ())+str(message.getPersonQQ())}))
                    message.setContent("[CQ:at,qq={0}]".format(message.getPersonQQ()) + json.loads(rtn.text)["text"])
                    message.setTargetQQ(int(res.group(1)))
                    log(moduleName=TuringRobotModule.name,content=message.getContent()+" "+str(message.getGroupQQ())+" "+str(message.getPersonQQ()))
                    send(message, True)
                else:
                    return
        except Exception as e:
            if isinstance(e,Block):
                raise Block()
            log(level="error",moduleName=TuringRobotModule.name,content=e.message)
            return


if __name__ == "__main__":
    msg=Message.Message()
    msg.setContent("你好")
    msg.setPersonQQ(459861669)
    msg.setSendTime(100000000)

