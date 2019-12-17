# -*- coding: utf-8 -*-
# 防撤回模块

import datetime

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from BaseProcessModule import *
from DatabaseSession import Session
from Sender import *
from Logger import log

Base = declarative_base()

class MessageModal(Base):
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


class UnrecalledModule(BaseProcessModule):
    name = "UnrecalledModule"

    @staticmethod
    def isUnrecalled(msg):
        """
        判断是否为防撤回
        """
        if msg[0] == u"＋" or msg[0] == u"+":
            return True
        return False

    @staticmethod
    def isFromGroup(message):
        """
        判断消息是否来自群聊
        """
        if message.getSubType()== 2:
            return True
        return False

    @staticmethod
    def isFromDiscussion(message):
        """
        判断消息是否来自讨论组
        """
        if message.getSubType()== 3 :
            return True
        return False

    @staticmethod
    def isLastMessage(msg):
        """
        判断输入是否合法
        """
        try:
            int(msg[1:])/1           
            return True
        except Exception as e:
            return False
        
    @staticmethod
    def process(message):
        session = Session()
        try:
            message = message[:]
            msg = message.getContent()

            if UnrecalledModule.isLastMessage(msg) and UnrecalledModule.isUnrecalled(msg):
                if UnrecalledModule.isFromGroup(message):
                    """
                    群聊模块
                    """
                    getLast = session.query(MessageModal).filter_by(groupQQ=message.getGroupQQ()).all()
                    getLast_content = u"发送的：\n"+getLast[-(int(msg[1:])+1)].content
                    getLast_personQQ = getLast[-(int(msg[1:])+1)].personQQ

                    message.setContent(getLast_content)
                    message.group_at(getLast_personQQ)
                    send(message, True)


                elif UnrecalledModule.isFromDiscussion(message):
                    """
                    讨论组模块
                    """
                    getLast = session.query(MessageModal).filter_by(discussionQQ=message.getDiscussionQQ()).all()
                    getLast_content = u"发送的：\n"+getLast[-(int(msg[1:])+1)].content
                    getLast_personQQ = getLast[-(int(msg[1:])+1)].personQQ

                    message.setContent(getLast_content)
                    message.group_at(getLast_personQQ)
                    send(message, True)
            else:
                return
        except Exception as e:
            if isinstance(e, Block):
                raise Block()
            traceback.print_exc()
            return
        finally:
            session.close()
