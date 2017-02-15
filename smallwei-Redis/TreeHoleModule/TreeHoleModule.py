# -*- coding: utf-8 -*-
# 树洞模块
# 使用该模块请在config.py中加入以下配置
# TREEHOLE_TABLE_NAME = 'treehole'      # 树洞功能的数据表的表名。
# YUNYINGQQ=588694674                   #运营群群号
# 同时再MySQL数据库中添加下表，当前服务器中表我已经添加好了
# +--------------+------------------+------+-----+---------+----------------+
# | Field        | Type             | Null | Key | Default | Extra          |
# +--------------+------------------+------+-----+---------+----------------+
# | id           | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
# | getContent   | text             | YES  |     | NULL    |                |
# | getPersonQQ  | bigint(20)       | YES  |     | NULL    |                |
# | getTime      | bigint(20)       | YES  |     | NULL    |                |
# | subType      | int(2)           | YES  |     | 0       |                |
# | sendPersonQQ | bigint(20)       | YES  |     | NULL    |                |
# | sendContent  | text             | YES  |     | NULL    |                |
# | sendTime     | bigint(20)       | YES  |     | NULL    |                |
# +--------------+------------------+------+-----+---------+----------------+

import datetime

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


from BaseProcessModule import *
from DatabaseSession import Session
from Sender import *
from Logger import log

Base = declarative_base()
redisConnection = redis.Redis(connection_pool=redisPool)


class TreeHoleRecordModal(Base):
    """
        id:唯一标识符，自增，不需要手动设置。
        getContent:树洞收到消息的内容。
        getPersonQQ:树洞收到消息人的qq号。
        getTime:树洞收到消息时间。
        subType:消息的类型：0为未回复，1为已回复，默认值为0。
        sendPersonQQ:树洞回复人的qq号。
        sendContent:树洞回复消息的内容。
        sendTime:树洞回复消息时间。
    """
    __tablename__ = TREEHOLE_TABLE_NAME

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    getContent = Column(Text, nullable=True)
    getPersonQQ = Column(BigInteger, nullable=True)
    getTime = Column(BigInteger, nullable=True)
    subType = Column(Integer, nullable=True)
    sendPersonQQ = Column(BigInteger, nullable=True)
    sendContent = Column(Text, nullable=True)
    sendTime = Column(BigInteger, nullable=True)


class TreeHoleModule(BaseProcessModule):
    name = "TreeHoleModule"
    CONTEXT = "TREE"
    GET_SUCCESS_REPLY = u"微微已经将你的消息加入树洞中咯√"

    @staticmethod
    def isTreeHole(msg):
        if msg == u"树洞" or msg == u"小微树洞":
            return True
        return False

    @staticmethod
    def issend(message):
        """
        是不是运营回的
        """
        if message.getContent()[0] == u"#" and message.getGroupQQ() == YUNYINGQQ:
            return True
        return False

    @staticmethod
    def ispass(message):
        """
        无效树洞信息直接pass
        """
        if message.getContent()[1:5] == u"pass":
            return True
        return False

    @staticmethod
    def process(message):
        session = Session()
        try:
            context = redisConnection.hget(
                REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str())
            message = message[:]
            message.remove_group_at()
            msg = message.getContent()
            """
            下面是接收模块
            和发送到运营群模块
            """
            if message.is_at() and TreeHoleModule.isTreeHole(msg):
                message.setContent(u"该功能涉及隐私,请私聊微微哟～")
                message.group_at(message.getPersonQQ())
                send(message, True)
            elif message.getSubType() == 1 and TreeHoleModule.isTreeHole(msg):
                redisConnection.hset(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str(),
                                     TreeHoleModule.CONTEXT)
                message.setContent(u"把你想说的发给微微哦~")
                message.group_at(message.getPersonQQ())
                send(message, True)
            elif message.getSubType() == 1 and context == TreeHoleModule.CONTEXT:
                message.setContent(TreeHoleModule.GET_SUCCESS_REPLY)
                redisConnection.hdel(
                    REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str())
                record = TreeHoleRecordModal(
                    getContent=msg,
                    getPersonQQ=message.getPersonQQ(),
                    getTime=message.getSendTime(),
                    subType=0
                )
                session.add(record)
                session.commit()
                send(message, False)
                getId = session.query(TreeHoleRecordModal).filter_by(
                    getContent=msg).all()
                message.setSubType(2)
                getId_str = str(getId[-1].id)
                message.setContent("ID:" + getId_str + "\n" + msg)
                message.setGroupQQ(YUNYINGQQ)
                message.setPersonQQ(0)
                send(message, True)
            elif message.is_at() and TreeHoleModule.issend(message):
                """
            下面是回复模块
            """
                getMessageList = message.getContent().split("#")
                ID = getMessageList[1]
                getSubType = session.query(
                    TreeHoleRecordModal).filter_by(id=ID).all()
                max = session.query(func.max(TreeHoleRecordModal.id)).first()
                try:
                    int(ID) / 1
                except Exception as e:
                    feedback = u"此次回复无效"
                    message.setContent(u"ERROR:\n" + "ID:" +
                                       str(ID) + u"输入违法\n" + feedback)
                    send(message, True)
                if int(ID) < 0 or int(ID) > int(str(max[0])):
                    feedback = u"此次回复无效"
                    message.setContent(u"ERROR:\n" + "ID:" +
                                       str(ID) + u"超出当前范围\n" + feedback)
                    send(message, True)
                elif str(getSubType[0].subType) == "1":
                    feedback = u"此次回复无效"
                    message.setContent(
                        u"WARNING:\n" + "ID:" + str(ID) + u"事件已被回复\n" + feedback)
                    send(message, True)
                elif getMessageList[2] == u"pass":
                    sendContent = "pass"
                    feedback = u"Pass成功"
                else:
                    sendContent = getMessageList[2]
                    feedback = u"回复成功~"

                """
                session.query(TreeHoleRecordModal).filter(TreeHoleRecordModal.id==2).update({TreeHoleRecordModal.subType : 1},{TreeHoleRecordModal.sendContent : sendContent},{TreeHoleRecordModal.sendPersonQQ : message.getPersonQQ()},{TreeHoleRecordModal.sendTime:message.getSendTime()})
                """
                session.query(TreeHoleRecordModal).filter(
                    TreeHoleRecordModal.id == ID).update({"subType": 1})
                session.query(TreeHoleRecordModal).filter(
                    TreeHoleRecordModal.id == ID).update({"sendContent": sendContent})
                session.query(TreeHoleRecordModal).filter(TreeHoleRecordModal.id == ID).update(
                    {"sendPersonQQ": message.getPersonQQ()})
                session.query(TreeHoleRecordModal).filter(
                    TreeHoleRecordModal.id == ID).update({"sendTime": message.getSendTime()})
                session.commit()
                message.setContent("ID:" + str(ID) + u"事件\n" + feedback)
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
