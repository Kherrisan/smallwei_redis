# -*- coding: utf-8 -*-
# 极其重要的核心类。定义了Message类和MessageModel类。

import json
import re
import copy
from sqlalchemy import Column, Integer, String, Text, BigInteger
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from config import MESSAGE_TABLE_NAME

Base = declarative_base()


class MessageModel(Base):
    """该类抽象了聊天的消息（即聊天记录）在数据库中的保存形式。
    每一条小微可见的消息都可以看作一条记录。
    这个类只用于数据库操作。

    Attributes:
        id:唯一标识符，自增，不需要手动设置。
        content:消息的内容。
        sendTime:消息发送的时间，以coolq得到的时间为准。
        subType:消息的类型：0为错误，1为私戳，2为群聊，3为讨论组。目前只有这三个。在cpp中这三个值是枚举值，需要保持此处和cpp端的设置一致。
        personQQ:个人qq号，包括私戳的个人qq和群聊中的发送者的qq。
        groupQQ:群qq号，只有当subType=2时才会有值，其他情况下为0。
        discussionQQ:讨论组的qq号，只有当subType=3时才会有值，其他情况下为0。
        targetQQ:接收者的qq号，即不是大微qq号就是小微2016qq号。
    """
    __tablename__ = MESSAGE_TABLE_NAME

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    content = Column(Text, nullable=True)
    sendTime = Column(BigInteger, nullable=False)
    subType = Column(Integer, nullable=False)
    personQQ = Column(BigInteger, nullable=False)
    groupQQ = Column(BigInteger, nullable=True)
    discussionQQ = Column(BigInteger, nullable=True)
    targetQQ = Column(BigInteger, nullable=True)


class Message:
    """Message类封装了消息在数据库之外，py之内的形式。虽然有的函数可能有一些累赘。。。。。。

    """

    def __init__(self, dic=None):
        self.at = False
        self.msgDict = dict()
        self.msgDict["source"] = dict()
        if dic is None:
            self.setSendTime(0).setSubType(0).setContent("").setPersonQQ(0).setDiscussionQQ(0).setGroupQQ(0)
        else:
            self.msgDict = copy.copy(dic)

    def __getitem__(self, item):
        msg = Message(self.msgDict)
        msg.at = self.at
        return msg

    def setDict(self, dic):
        self.msgDict = dic
        return self

    def getDict(self):
        return self.msgDict

    def getJsonStr(self):
        return json.dumps(self.msgDict, ensure_ascii=False)

    def getDataStream(self):
        jsonStr = self.getJsonStr()
        return jsonStr

    def getContent(self):
        return self.msgDict["msg"]

    def setContent(self, value):
        self.msgDict["msg"] = value[:]
        return self

    def getSubType(self):
        return self.msgDict["subType"]

    def setSubType(self, value):
        self.msgDict["subType"] = value
        return self

    def getPersonQQ(self):
        return self.msgDict["source"]["personQQ"]

    def setPersonQQ(self, value):
        self.msgDict["source"]["personQQ"] = value
        return self

    def getDiscussionQQ(self):
        return self["source"]["discussionQQ"]

    def setDiscussionQQ(self, value):
        self.msgDict["source"]["discussionQQ"] = value
        return self

    def getGroupQQ(self):
        return self.msgDict["source"]["groupQQ"]

    def setGroupQQ(self, value):
        self.msgDict["source"]["groupQQ"] = value
        return self

    def getSendTime(self):
        return self.msgDict["sendTime"]

    def setSendTime(self, value):
        self.msgDict["sendTime"] = value
        return self

    def getTargetQQ(self):
        return self.msgDict["targetQQ"]

    def setTargetQQ(self, target):
        self.msgDict["targetQQ"] = target

    def is_at(self):
        return self.at

    def remove_group_at(self):
        GROUP_AT_PATTERN = r"^\[CQ:at,qq=([0-9]+)\]"
        res = re.search(GROUP_AT_PATTERN, self.getContent())
        if res and res.group(1) == str(self.getTargetQQ()):
            self.setContent(self.getContent()[len(res.group(0)):])
            self.at = True
        else:
            self.at = False

    def group_at(self, atQQ=None):
        GROUP_AT_CQ = "[CQ:at,qq={0}]"
        if atQQ:
            self.setContent(GROUP_AT_CQ.format(atQQ) + self.getContent())
        else:
            self.setContent(GROUP_AT_CQ.format(self.getPersonQQ()) + self.getContent())

    def get_context_str(self):
        if self.getSubType() == 1:
            return str(self.getPersonQQ())
        elif self.getSubType() == 2:
            return str(self.getGroupQQ()) + str(self.getPersonQQ())
        else:
            return str(self.getDiscussionQQ()) + str(self.getPersonQQ())

    @staticmethod
    def produceMessege(dataStream):
        """
        将任务字符串转成一个Message对象的函数。
        :param dataStream: 从redis中取出的原始字符串。
        :return: 一个根据原始字符串生成的Message对象。
        """
        temp = dataStream[1][:-1].decode("gbk")
        jsonObj = json.loads(temp)
        return Message().setDict(jsonObj)

    @staticmethod
    def produceDBMessage(socketMessage):
        """
        根据Message对象生成MessageModel对象的函数。
        :param socketMessage: Message对象。
        :return: 相应的MessageModel对象。
        """
        jsonObj = socketMessage.getDict()
        return MessageModel(content=jsonObj["msg"],
                            sendTime=jsonObj["sendTime"],
                            subType=jsonObj["subType"],
                            personQQ=jsonObj["source"]["personQQ"],
                            groupQQ=jsonObj["source"]["groupQQ"],
                            discussionQQ=jsonObj["source"]["discussionQQ"],
                            targetQQ=jsonObj["targetQQ"])
