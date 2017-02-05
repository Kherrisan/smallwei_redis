# -*- coding: utf-8 -*-

import base64
import cStringIO
import json
import re

import redis
import requests

import CQImgReader
from BaseProcessModule import *
from RedisSession import redisPool
from Sender import *

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import random
import datetime
from DatabaseSession import Session

from config import *

redisConnection = redis.Redis(connection_pool=redisPool)


class LostRecordModal(Base):
    __tablename__ = LOST_RECORD_TABLE_NAME

    id = Column(Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    lostPersonQQ = Column(BigInteger, nullable=True)
    pickPersonQQ = Column(BigInteger, nullable=True)
    description = Column(Text, nullable=False)
    imageFilename = Column(Text, nullable=True)
    createDate = Column(Date, nullable=True)
    visitCount = Column(Integer, nullable=False , default = 0)
    finish_Date = Column(Date, nullable=True)
    isPublished = Column(Boolean, nullable=False, default=False)
    isLost = Column(Boolean, nullable = False)#是否是寻物启事，True为寻物启事，False为失物招领
    isDelete = Column(Boolean, nullable=False ,default = False)




#存储图像路径为酷Q image目录下子目录 lost
class LostFinderModule(BaseProcessModule):
    lostFinderDirectory = u"lostfinder"

    PIC_CONTEXT_PATTERN = u"LostFinderPicContext"

    CONTEXT1 = u"LostFinderContext_1"
    PIC_CONTEXT1 = u"LostFinderPicContext_1"
    CONTEXT2 = u"LostFinderContext_2"
    PIC_CONTEXT2 = u"LostFinderPiContext_2"
    CONTEXT3 = u"LostFinderContext_3"
    CONTEXT4 = u"LostFinderContext_4"
    CONTEXT5 = u"LostFinderContext_5"

    KEY_1 = u"lf1"
    KEY_2 = u"lf2"
    KEY_3 = u"lf3"
    KEY_4 = u"lf4"
    KEY_5 = u"lf5"

    REPLY_1 = u"已经完成图片添加，寻物启事已经昭告天下咯～"
    REPLY_2 = u"已经完成图片添加，失物招领已经传遍千里啦～"
    REPLY_CANCEL = u"已经取消～"

    COOLQ_LOST_IMAGE_PATH = u"C:\\Users\Administrator\\Desktop\\{0}\\酷Q Pro\\data\\image\\"
    PICTURE_PATTERN = r"\[CQ:image,file=(.+)\]"
    PICTURE_NAME = "[CQ:image,file={0}]"

    DELETE_PATTERN = r"抹除 ([0-9]+)"
    MODIFY_PATTERN = r"修改 ([0-9]+)"
    RETURN_PATTERN = r"归还 ([0-9]+)"
    CLAIM_PATTERN = r"认领 ([0-9]+)"
    REPORT_PATTERN = r"举报 ([0-9]+)"


    name = "LostFinderModule"

    @staticmethod
    def getToday():
        today=datetime.date.today()
        return today

    @staticmethod
    def is_lost_find(message):
        if message.getContent().find(u"寻物") == 0:
            return True
        else:
            return False

    @staticmethod
    def is_lost_find1(message):
        if message.getContent() == LostFinderModule.KEY_1:
            return True
        else:
            return False

    @staticmethod
    def is_lost_find2(message):
        if message.getContent() == LostFinderModule.KEY_2:
            return True
        else:
            return False

    @staticmethod
    def is_lost_find3(message):
        if message.getContent() == LostFinderModule.KEY_3:
            return True
        else:
            return False

    @staticmethod
    def is_lost_find4(message):
        if message.getContent() == LostFinderModule.KEY_4:
            return True
        else:
            return False

    @staticmethod
    def is_lost_find5(message):
        if message.getContent() == LostFinderModule.KEY_5:
            return True
        else:
            return False

    @staticmethod
    def is_picture(message):
        if re.search(LostFinderModule.PICTURE_PATTERN, message.getContent()):
            return True
        else:
            return False

    @staticmethod
    def is_return():
        if re.search(LostFinderModule.RETURN_PATTERN, message.getContent()):
            return True
        else:
            return False

    @staticmethod
    def is_claim():
        if re.search(LostFinderModule.CLAIM_PATTERN, message.getContent()):
            return True
        else:
            return False

    @staticmethod
    def is_report():
        if re.search(LostFinderModule.REPORT_PATTERN, message.getContent()):
            return True
        else:
            return False

    @staticmethod
    def is_delete():
        if re.search(LostFinderModule.DELETE_PATTERN, message.getContent()):
            return True
        else:
            return False

    @staticmethod
    def is_modify():
        if re.search(LostFinderModule.MODIFY_PATTERN, message.getContent()):
            return True
        else:

    @staticmethod
    def process(message):
        session = Session()
        try:
            context = redisConnection.hget(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str())
            message.remove_group_at()
            if (message.is_at()):
                message.setContent(u"该功能涉及隐私,请私聊微微哟～")
                #message.group_at()
                send(message, True)
            #判断是否完成了上次的书写
            if (message.getSubType() == 1 and LostFinderModule.is_lost_find(message)):
                print "[" + LostFinderModule.name + "]"
                message.setContent(u"发送括号内命令,微微为你呈现:\
                    --["+ KEY_1 +"]--发布寻物启示\n\
                    --["+ KEY_2 +"]--发布失物招领\n\
                    --["+ KEY_3 +"]--浏览寻物启示\n\
                    --["+ KEY_4 +"]--浏览失物列表\n\
                    --["+ KEY_5 +"]--查阅我的发布\n\
                ")
                #message.group_at()
                send(message, True)
            elif (message.getSubType() == 1 and LostFinderModule.is_lost_find1(message)):
                redisConnection.hset(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str(), LostFinderModule.CONTEXT1)
                message.setContent(u"请将文字描述发给微微,回复[取消]可撤销此次发布。\n\
                    Tips:图片可在下一步添加，不要着急哦～\
                ")
                send(message, False)
            elif (message.getSubType() == 1 and LostFinderModule.is_lost_find2(message)):
                redisConnection.hset(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str(), LostFinderModule.CONTEXT2)
                message.setContent(u"请将文字描述发给微微,回复[取消]可撤销此次发布。。\n\
                    Tips:图片可在下一步添加，不要着急哦～:\
                ")
                send(message, False)
            elif (message.getSubType() == 1 and LostFinderModule.is_lost_find3(message)):
                redisConnection.hset(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str(), LostFinderModule.CONTEXT3)
                # 没被删除 是寻物启示 已经被发布 且pickPersonQQ为空--即还没有捡到的人
                result = session.query(LostRecordModal).filter(isDelete==False, isPublished == True, isLost == True, pickPersonQQ == None).all()
                for row in result:
                    recordId = row.id
                    description = row.discription
                    imageName = row.imageFilename
                    image = LostFinderModule.PICTURE_NAME.format(str(recordId) + "_.jpg")
                    content = "丢失物编号:"+ recordId +"\n丢失物描述:" +description + "\n附图:\n" + image
                    message.setContent(content)
                    send(message, True)

                content = "\n\n可用命令:\n--[归还 丢失物编号]--归还此失物\n--[举报 丢失物编号]--暂未开放的功能"
                message.setContent(content)
                send(message, True)
            elif (message.getSubType() == 1 and LostFinderModule.is_lost_find4(message)):
                redisConnection.hset(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str(), LostFinderModule.CONTEXT4)
                # 没被删除 是失物招领 已经被发布 且lostPersonQQ为空--即还没有认领的人
                result = session.query(LostRecordModal).filter(isDelete==False, isPublished == True, isLost == True, pickPersonQQ == None).all()
                for row in result:
                    recordId = row.id
                    description = row.discription
                    imageName = row.imageFilename
                    image = LostFinderModule.PICTURE_NAME.format(str(recordId) + "_.jpg")
                    content = "拾取物编号:"+ recordId +"\n拾取物描述:" +description + "\n附图:\n" + image
                    message.setContent(content)
                    send(message, True)

                content = "\n\n可用命令:\n--[认领 拾取物编号]--认领此物品\n--[举报 拾取物编号]--暂未开放的功能"
                message.setContent(content)
                send(message, True)
            elif (message.getSubType() == 1 and LostFinderModule.is_lost_find5(message)):
                redisConnection.hset(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str(), LostFinderModule.CONTEXT5)
                myqq = message.getPersonQQ()
                #发布的寻物启示
                message.setContent(u"为您展示发布的寻物启示:")
                send(message, True)
                result = session.query(LostRecordModal).filter(isDelete==False, isPublished == True, lostPersonQQ == myqq ,isLost == True)
                for row in result:
                    recordId = row.id
                    description = row.discription
                    imageName = row.imageFilename
                    image = LostFinderModule.PICTURE_NAME.format(str(recordId) + "_.jpg")
                    if (row.pickPersonQQ()!=None):
                        content = "丢失物编号:"+ recordId + "\n拾取者qq:" + str(row.pickPersonQQ) +"\n丢失物描述:" +description + "\n附图:\n" + image
                    else:
                        content = "丢失物编号:"+ recordId +"\n[还没有被拾取!]" +"\n丢失物描述:" +description + "\n附图:\n" + image
                    message.setContent(content)
                    send(message, True)

                #发布的失物招领
                message.setContent(u"为您展示发布的失物招领:")
                send(message, True)
                result = session.query(LostRecordModal).filter(isDelete==False, isPublished == True, pickPersonQQ == myqq ,isLost == False)
                for row in result:
                    recordId = row.id
                    description = row.discription
                    imageName = row.imageFilename
                    image = LostFinderModule.PICTURE_NAME.format(str(recordId + "_.jpg")
                    if (row.lostPersonQQ()!=None):
                        content = "拾取物编号:"+ recordId + "\n领取者qq:" + str(row.pickPersonQQ) +"\n拾取物描述:" +description + "\n附图:\n" + image
                    else:
                        content = "拾取物编号:"+ recordId +"\n[还没有被领取!]" +"\n拾取物描述:" +description + "\n附图:\n" + image
                    message.setContent(content)
                    send(message, True)

                message.setContent(u"\n\n回复[抹除] 拾取物/丢失物编号] 可以抹除记录\n回复[修改 编号]可以修改内容\n回复[]")
                send(message, True)

            #防止先发图片
            elif message.getSubType() == 1 and context == LostFinderModule.CONTEXT1 and LostFinderModule.is_picture(message):
                message.setContent(u"请先发送文字描述")
                send(message, True)

            elif message.getSubType() == 1 and context == LostFinderModule.CONTEXT1 and (not LostFinderModule.is_picture(message)):
                redisConnection.hset(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str(), LostFinderModule.PIC_CONTEXT1)
                lostPersonQQ = message.getPersonQQ()
                description = message.getContent()
                createDate = LostFinderModule.getToday()
                isLost = True
                record=LostRecordModal(
                    lostPersonQQ = lostPersonQQ,
                    description = description,
                    createDate = createDate,
                    isLost = isLost,
                )
                session.add(record)
                session.commit()
                message.setContent(u"已经收到文字描述，需要图片描述请继续发送图片，无图片回复[结束]直接发布。")
                send(message, False)

            elif message.getSubType() == 1 and context == LostFinderModule.PIC_CONTEXT1 and LostFinderModule.is_picture(message):
                name = re.search(LostRecordModal.PICTURE_PATTERN, msg.getContent()).group(1)
                buffer = cStringIO.StringIO()
                img = CQImgReader.CQImgReader(
                    LostFinderModule.COOLQ_IMAGE_PATH.format(
                        msg.getTargetQQ()) + name + ".cqimg").get_pil_img()

                num = int(session.query(func.count(LostRecordModal.id)))+1
                filename = str(num)
                img.save(LostFinderModule.lostFinderDirectory+"\\" + filename + ".jpg")
                img.save(buffer, format="JPEG")

                query = session.query(LostRecordModal)
                result = query.filter(LostRecordModal.lostPersonQQ == str(message.getPersonQQ()), LostRecordModal.isPublished == False)
                result.update({LostRecordModal.imageFilename: filename, LostRecordModal.isPublished: True})
                session.commit()

                msg.setContent(REPLY_1)
                send(msg, True)


            elif message.getSubType() == 1 and context == LostFinderModule.CONTEXT2:
                redisConnection.hset(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str(), LostFinderModule.PIC_CONTEXT2)
                pickPersonQQ = message.getPersonQQ()
                description = message.getContent()
                createDate = LostFinderModule.getToday()
                isLost = False
                record=LostRecordModal(
                    pickPersonQQ = pickPersonQQ,
                    description = description,
                    createDate = createDate,
                    isLost = isLost,
                )
                session.add(record)
                session.commit()
                message.setContent(u"已经收到文字描述，需要图片描述请继续发送图片，无图片回复[结束]直接发布。")
                send(message, False)

            elif message.getSubType() == 1 and context == LostFinderModule.PIC_CONTEXT2 and LostFinderModule.is_picture(message):
                name = re.search(LostRecordModal.PICTURE_PATTERN, msg.getContent()).group(1)
                buffer = cStringIO.StringIO()
                img = CQImgReader.CQImgReader(
                    LostFinderModule.COOLQ_IMAGE_PATH.format(
                        msg.getTargetQQ()) + name + ".cqimg").get_pil_img()

                num = int(session.query(func.count(LostRecordModal.id)))+1
                filename = str(num)
                img.save(LostFinderModule.lostFinderDirectory+"\\" + filename + ".jpg")
                img.save(buffer, format="JPEG")

                query = session.query(LostRecordModal)
                result = query.filter(LostRecordModal.pickPersonQQ == str(message.getPersonQQ()), LostRecordModal.isPublished == False)
                result.update({LostRecordModal.imageFilename: filename, LostRecordModal.isPublished: True})
                session.commit()

                msg.setContent(REPLY_1)
                send(msg, True)

            elif message.getSubType() == 1 and context == LostFinderModule.PIC_CONTEXT1 and (not LostFinderModule.is_picture(message)):
                redisConnection.hset(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str(), "")
                query = session.query(LostRecordModal)
                result = query.filter(LostRecordModal.lostPersonQQ == message.getPersonQQ(), LostRecordModal.isPublished == False)
                result.update({LostRecordModal.isPublished: True})
                session.commit()
                message.setContent("监测到发送的不是图片，自动发布～若为误操作，可在查看自己的发布中修改～")

            elif message.getSubType() == 1 and context == LostFinderModule.PIC_CONTEXT2 and (not LostFinderModule.is_picture(message)):
                redisConnection.hset(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str(), "")
                query = session.query(LostRecordModal)
                result = query.filter(LostRecordModal.pickPersonQQ == message.getPersonQQ(), LostRecordModal.isPublished == False)
                result.update({LostRecordModal.isPublished: True})
                session.commit()
                message.setContent("监测到发送的不是图片，自动发布～若为误操作，可在查看自己的发布中修改～")

            elif message.getSubType() == 1 and LostFinderModule.is_return(message) and context == LostFinderModule.CONTEXT3):
                recordID = LostFinderModule.RETURN_PATTERN.findall(message.getContent())
                if (not recordID)||(recordID[0]) :
                    message.setContent(u"命令似乎有些问题呢,检查命令格式哦～")
                    send(message,True)
                else:
                    recordId = recordID[0]
                    result = session.qeury(LostRecordModal).filter(id == recordId).first()
                    if not result:
                        message.setContent(u"命令似乎有些问题呢,检查命令格式哦～")
                        send(message,True)
                    else:
                        lostPersonQQ = result.lostPersonQQ
                        qqTemp = message.getPersonQQ()
                        session.update(LostRecordModal).where(id == recordId).\
                        values(
                            pickPersonQQ = int(message.getPersonQQ()),
                        )
                        session.commit()
                        message.setContent(u"归还申请已经接受，请您将物品归还给QQ:"+ str(lostPersonQQ) +"～")
                        send(message,True)
                        message.setPersonQQ(int(lostPersonQQ))
                        message.setContent(u"有人认领您发布的寻物启示，他的qq为--"+str(qqTemp)+"--")
                        send(message,True)

            elif message.getSubType() == 1 and LostFinderModule.is_claim(message) and context == LostFinderModule.CONTEXT4):
                recordID = LostFinderModule.CLAIM_PATTERN.findall(message.getContent())
                if (not recordID)||(recordID[0]) :
                    message.setContent(u"命令似乎有些问题呢,检查命令格式哦～")
                    send(message,True)
                else:
                    recordId = recordID[0]
                    result = session.qeury(LostRecordModal.pickPersonQQ).filter(id == recordId).first()
                    if not result:
                        message.setContent(u"命令似乎有些问题呢,检查命令格式哦～")
                        send(message,True)
                    else:
                        pickPersonQQ = result.pickPersonQQ
                        qqTemp = message.getPersonQQ()
                        session.update(LostRecordModal).where(id == recordId).\
                        values(
                            pickPersonQQ = int(message.getPersonQQ()),
                        )
                        session.commit()
                        message.setContent(u"认领申请已经接受，您可以联系QQ取得物品:"+ pickPersonQQ +"～")
                        send(message,True)
                        message.setPersonQQ(int(pickPersonQQ))
                        message.setContent(u"有人认领您发布的失物招领，他的qq为--"+qqTemp"--")
                        send(message,True)

            elif message.getSubType() == 1 and LostFinderModule.is_report(message) and (context == LostFinderModule.CONTEXT3||context == LostFinderModule.CONTEXT4):
                recordID = LostFinderModule.REPORT_PATTERN.findall(message.getContent())
                if (not recordID)||(recordID[0]) :
                    message.setContent(u"命令似乎有些问题呢,检查命令格式哦～")
                    send(message,True)
                else:
                    recordId = recordID[0]
                    message.setContent(u"举报功能暂未上线，可联系工作人员处理～")
                    send(message,True)

            #消除一条记录
            elif message.getSubType() == 1 and LostFinderModule.is_delete(message) and context == LostFinderModule.CONTEXT5):
                recordID = LostFinderModule.DELETE_PATTERN.findall(message.getContent())
                if (not recordID)||(recordID[0]) :
                    message.setContent(u"命令似乎有些问题呢,检查命令格式哦～")
                    send(message,True)
                else:
                    recordId = recordID[0]
                    result = session.query(LostRecordModal).filter(id == recordId).first()
                    if not result:
                        message.setContent(u"命令似乎有些问题呢,检查命令格式哦～")
                        send(message,True)
                    else:
                        if result.isLost==True:
                            result = session.query(LostRecordModal).filter(id == recordId, lostPersonQQ==message.getPersonQQ()).first()
                            if not result :
                                message.setContent(u"这条不是你发布的哦～")
                                send(message,True)
                            else:
                                session.update(LostRecordModal).where(id == recordId, lostPersonQQ==message.getPersonQQ()).\
                                values(
                                    isDelete = True,
                                )
                                session.commit()
                        else:
                            result = session.query(LostRecordModal).filter(id == recordId, pickPersonQQ==message.getPersonQQ()).first()
                            if not result :
                                message.setContent(u"这条不是你发布的哦～")
                                send(message,True)
                            else:
                                session.update(LostRecordModal).where(id == recordId, pickPersonQQ==message.getPersonQQ()).\
                                values(
                                    isDelete = True,
                                )
                                session.commit()
                    message.setContent(u"成功消除～")
                    send(message,True)

            elif message.getSubType() == 1 and LostFinderModule.is_modify(message) and context == LostFinderModule.CONTEXT5):
                recordID = LostFinderModule.MODIFY_PATTERN.findall(message.getContent())
                if (not recordID)||(recordID[0]) :
                    message.setContent(u"命令似乎有些问题呢,检查命令格式哦～")
                    send(message,True)
                else:
                    recordId = recordID[0]
                    result = session.query(LostRecordModal).filter(id == recordId).first()
                    if not result:
                        message.setContent(u"命令似乎有些问题呢,检查命令格式哦～")
                        send(message,True)
                    else:
                        #是寻物启示
                        if result.isLost==True:
                            result = session.query(LostRecordModal).filter(id == recordId, pickPersonQQ==message.getPersonQQ()).first()
                            if not result :
                                message.setContent(u"这条不是你发布的哦～")
                                send(message,True)
                            else:
                                message.setContent(u"微微突然发现之前的文字和图片都已经发给你啦，删掉重发就很方便啦，嘿嘿～")
                                send(message,True)
                        #是失物招领
                        else:
                            result = session.query(LostRecordModal).filter(id == recordId, pickPersonQQ==message.getPersonQQ()).first()
                            if not result :
                                message.setContent(u"这条不是你发布的哦～")
                                send(message,True)
                            else:
                                message.setContent(u"微微突然发现之前的文字和图片都已经发给你啦，删掉重发就很方便啦，嘿嘿～")
                                send(message,True)
                    message.setContent(u"成功消除～")
                    send(message,True)

            elif message.getSubType() == 1 and message.getContent()==u"取消" and (context == LostFinderModule.CONTEXT1||context == LostFinderModule.CONTEXT2):
                redisConnection.hset(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str(), "")
                session.query(LostRecordModal).filter(isPublished==False, lostPersonQQ==message.getPersonQQ()).delete()
                session.query(LostRecordModal).filter(isPublished==False, pickPersonQQ==message.getPersonQQ()).delete()
                session.commit()
                message.setContent(u"成功取消!")
                send(message, True)

            elif message.getSubType() == 1 and message.getContent()==u"结束" and context == LostFinderModule.PIC_CONTEXT1:
                redisConnection.hset(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str(), "")
                query = session.query(LostRecordModal)
                result = query.filter(LostRecordModal.lostPersonQQ == message.getPersonQQ(), LostRecordModal.isPublished == False)
                result.update({LostRecordModal.isPublished: True})
                session.commit()
                message.setContent(REPLY_1)
                send(message, True)

            elif message.getSubType() == 1 and message.getContent()==u"结束" and context == LostFinderModule.PIC_CONTEXT2:
                redisConnection.hset(REDIS_CONTEXT_CACHE_HASH_NAME, message.get_context_str(), "")
                query = session.query(LostRecordModal)
                result = query.filter(LostRecordModal.pickPersonQQ == message.getPersonQQ(), LostRecordModal.isPublished == False)
                result.update({LostRecordModal.isPublished: True})
                session.commit()
                message.setContent(REPLY_2)
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
