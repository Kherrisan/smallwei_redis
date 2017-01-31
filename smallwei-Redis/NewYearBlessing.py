# -*- coding:utf-8 -*-

import threading
import DatabaseSession
from Message import *
from RedisSession import *
from BaseProcessModule import BaseProcessModule

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import random
import datetime
from DatabaseSession import Session
import traceback
from GetInfoFromIni import *
import renderBlessing
from config import *

Base = declarative_base()
redisConnection = redis.Redis(connection_pool=redisPool)


class BlessingModal(Base):
    __tablename__ = BLESSING_TABLE_NAME

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    content = Column(VARCHAR(70), nullable=False)
    fromqq = Column(BigInteger, nullable=False)


class ReceiveBlessingModule(BaseProcessModule):
    name = "ReceiveBlessingModule"

    @staticmethod
    def isBless(message):
        if message.getContent()[0] == u"福":
            return True
        else:
            return False

    @staticmethod
    def process(message):
        session = Session()
        try:
            if message.getSubType() == 1 and ReceiveBlessingModule.isBless(message):
                bless = message.getContent()
                if len(bless.encode("gbk")) < 8:
                    message.setContent(u"祝福太短了哦。")
                    return message, True, True
                elif len(bless.encode("gbk")) > 68:
                    message.setContent(u"祝福太长了哦，小微记不住了呢。。。")
                    return message, True, True
                else:
                    blessModule = BlessingModal(content=message.getContent()[1:],
                                                fromqq=message.getPersonQQ())
                    session.add(blessModule)
                    session.commit()
                    temp=0
                    if message.getTargetQQ()==SMALLWEI_QQ:
                        temp=0
                    else:
                        temp=1
                    redisConnection.rpush(REDIS_BLESSING_WAITING_QUEUE,str(temp)+str(message.getPersonQQ()))
                    if getinfo(str(message.getPersonQQ()))[0]==0:
                        message.setContent(u"已收录您的祝福，系统检测到您尚未注册，请回复“绑定+一卡通号”注册后享受完整功能哦！")
                    else:
                        message.setContent(
                            u"您的祝福已经收集！请等待不久后来自陌生人的祝福哦~")
                    return message, True, True
            else:
                return 0, False, False
        except Exception as e:
            print "[" + NewyearModule.name + "][info]" + e.message
            traceback.print_exc()
            return 0, False, False
        finally:
            session.close()


class SendBlessingModule(BaseProcessModule):
    name = "SendBlessingModule"
    counter = 0
    loopFactor = 50
    BLESSING_REPLY = u"[CQ:share,url={0},title={1},content={2},image={3}]"
    BLESSING_LOGO = u"https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1485512941638&di=9825dd48f476c7001a8b540116e18bfb&imgtype=0&src=http%3A%2F%2Fimgsrc.baidu.com%2Fforum%2Fw%3D580%2Fsign%3D7adaea4da68b87d65042ab1737092860%2Ff57790cfc3fdfc035b83bbc4d33f8794a5c2265b.jpg"
    BLESSING_CONTENT = u"你收到了一条祝福哟。"
    BLESSING_TITLE = u"点击查看"

    @staticmethod
    def checkTime():
        # SendBlessingModule.counter += 1
        # if SendBlessingModule.counter %10 == 0:
        #     SendBlessingModule.counter=0
        #     return True
        # else:
        #     return False
        return True

    @staticmethod
    def process(message):
        session = Session()
        try:
            if SendBlessingModule.checkTime():
                waitqq = redisConnection.lpop(REDIS_BLESSING_WAITING_QUEUE)
                if not waitqq:
                    return 0,False,False
                blessQuery = session.query(BlessingModal).order_by(func.rand()).limit(1).first()
                if blessQuery:
                    renderblessing = renderBlessing.RenderBlessing(int(waitqq[1:]), blessQuery.fromqq, blessQuery.content)
                    url = renderblessing.render().get_url()
                    message = Message()
                    if waitqq[0]=="0":
                        message.setTargetQQ(SMALLWEI_QQ)
                    else:
                        message.setTargetQQ(SMALLWEI2016_QQ)
                    message.setSubType(1)
                    message.setPersonQQ(int(waitqq[1:]))
                    message.setContent(SendBlessingModule.BLESSING_REPLY.format(url,
                                                                                SendBlessingModule.BLESSING_TITLE,
                                                                                SendBlessingModule.BLESSING_CONTENT,
                                                                                SendBlessingModule.BLESSING_LOGO))
                    return message, True, True
                else:
                    return 0, False, False
            else:
                return 0, False, False
        except Exception as e:
            print "[" + SendBlessingModule.name + "][info]" + e.message
            traceback.print_exc()
            return 0, False, False
        finally:
            session.close()
